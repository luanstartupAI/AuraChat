from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config.database import get_db
from models.automation_models import Webhook, WebhookEvent, AutomationRule # Import Rule models if needed later
from flask_jwt_extended import jwt_required
import logging
import secrets # For generating secrets

logger = logging.getLogger(__name__)
automation_bp = Blueprint("automation", __name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

# --- Webhook Management --- 

@automation_bp.route("/webhooks", methods=["GET"])
@jwt_required()
def get_webhooks():
    """Get all configured webhooks."""
    db: Session = get_db_session()
    try:
        webhooks = db.query(Webhook).order_by(Webhook.created_at.desc()).all()
        webhooks_data = [
            {
                "id": wh.id,
                "url": wh.url,
                "event": wh.event.value,
                "is_active": wh.is_active,
                "has_secret": bool(wh.secret), # Don't expose the secret itself
                "created_at": wh.created_at.isoformat() if wh.created_at else None,
            }
            for wh in webhooks
        ]
        logger.info(f"Retrieved {len(webhooks_data)} webhooks.")
        return jsonify({"status": "success", "webhooks": webhooks_data}), 200
    except Exception as e:
        logger.error(f"Error getting webhooks: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve webhooks"}), 500
    finally:
        db.close()

@automation_bp.route("/webhooks", methods=["POST"])
@jwt_required()
def create_webhook():
    """Create a new webhook subscription."""
    data = request.get_json()
    url = data.get("url")
    event_str = data.get("event")
    generate_secret = data.get("generate_secret", False) # Option to auto-generate a secret

    if not url or not event_str:
        return jsonify({"status": "error", "message": "Missing required fields: url, event"}), 400

    try:
        event_enum = WebhookEvent(event_str)
    except ValueError:
        valid_events = [e.value for e in WebhookEvent]
        return jsonify({"status": "error", "message": f"Invalid event type. Valid events are: {', '.join(valid_events)}"}), 400

    db: Session = get_db_session()
    try:
        secret_value = secrets.token_hex(16) if generate_secret else None

        new_webhook = Webhook(
            url=url,
            event=event_enum,
            secret=secret_value,
            is_active=True # Active by default
        )
        db.add(new_webhook)
        db.commit()
        db.refresh(new_webhook)
        logger.info(f"Created new webhook ID: {new_webhook.id} for event {event_enum.value} at {url}")
        
        response_data = {
            "id": new_webhook.id,
            "url": new_webhook.url,
            "event": new_webhook.event.value,
            "is_active": new_webhook.is_active,
            "secret": secret_value # Return the secret ONLY on creation if generated
        }

        return jsonify({
            "status": "success", 
            "message": "Webhook created successfully", 
            "webhook": response_data
        }), 210
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating webhook for event {event_str} at {url}: {e}")
        return jsonify({"status": "error", "message": "Failed to create webhook"}), 500
    finally:
        db.close()

@automation_bp.route("/webhooks/<int:webhook_id>", methods=["PUT"])
@jwt_required()
def update_webhook(webhook_id: int):
    """Update an existing webhook (URL, active status). Secret cannot be updated here."""
    data = request.get_json()
    db: Session = get_db_session()
    try:
        webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not webhook:
            return jsonify({"status": "error", "message": "Webhook not found"}), 404

        if "url" in data: webhook.url = data["url"]
        if "is_active" in data: webhook.is_active = bool(data["is_active"])
        # Event type is generally not updatable, delete and recreate if needed.
        # Secret is not updatable via this endpoint for security.

        db.commit()
        db.refresh(webhook)
        logger.info(f"Updated webhook ID: {webhook_id}")
        return jsonify({
            "status": "success", 
            "message": "Webhook updated successfully",
            "webhook": {
                "id": webhook.id, 
                "url": webhook.url, 
                "event": webhook.event.value,
                "is_active": webhook.is_active
            }
        }), 200

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating webhook ID {webhook_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to update webhook"}), 500
    finally:
        db.close()

@automation_bp.route("/webhooks/<int:webhook_id>", methods=["DELETE"])
@jwt_required()
def delete_webhook(webhook_id: int):
    """Delete a webhook subscription."""
    db: Session = get_db_session()
    try:
        webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not webhook:
            return jsonify({"status": "error", "message": "Webhook not found"}), 404

        db.delete(webhook)
        db.commit()
        logger.info(f"Deleted webhook ID: {webhook_id}")
        return jsonify({"status": "success", "message": "Webhook deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting webhook ID {webhook_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to delete webhook"}), 500
    finally:
        db.close()

# --- Automation Rules (Optional - Basic Structure) ---
# Add endpoints for CRUD operations on AutomationRule if implementing this feature.
# Example:
# @automation_bp.route("/rules", methods=["GET"])
# @jwt_required()
# def get_rules(): ...

# @automation_bp.route("/rules", methods=["POST"])
# @jwt_required()
# def create_rule(): ...

# @automation_bp.route("/rules/<int:rule_id>", methods=["PUT"])
# @jwt_required()
# def update_rule(rule_id: int): ...

# @automation_bp.route("/rules/<int:rule_id>", methods=["DELETE"])
# @jwt_required()
# def delete_rule(rule_id: int): ...

