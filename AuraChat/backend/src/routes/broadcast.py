from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config.database import get_db
from models.crm_models import BroadcastCampaign, CampaignStatus, Group
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
broadcast_bp = Blueprint("broadcast", __name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

# --- Broadcast Campaign CRUD --- 

@broadcast_bp.route("/campaigns", methods=["GET"])
@jwt_required()
def get_campaigns():
    """Get all broadcast campaigns."""
    db: Session = get_db_session()
    try:
        campaigns = db.query(BroadcastCampaign).order_by(BroadcastCampaign.created_at.desc()).all()
        campaigns_data = [
            {
                "id": campaign.id,
                "name": campaign.name,
                "status": campaign.status.value,
                "message_preview": (campaign.message_content[:50] + "...") if len(campaign.message_content) > 50 else campaign.message_content,
                "target_group_id": campaign.target_group_id,
                "target_group_name": campaign.target_group.name if campaign.target_group else None,
                "scheduled_at": campaign.scheduled_at.isoformat() if campaign.scheduled_at else None,
                "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
            }
            for campaign in campaigns
        ]
        logger.info(f"Retrieved {len(campaigns_data)} campaigns.")
        return jsonify({"status": "success", "campaigns": campaigns_data}), 200
    except Exception as e:
        logger.error(f"Error getting campaigns: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve campaigns"}), 500
    finally:
        db.close()

@broadcast_bp.route("/campaigns/<int:campaign_id>", methods=["GET"])
@jwt_required()
def get_campaign_details(campaign_id: int):
    """Get details of a specific campaign."""
    db: Session = get_db_session()
    try:
        campaign = db.query(BroadcastCampaign).filter(BroadcastCampaign.id == campaign_id).first()
        if not campaign:
            logger.warning(f"Campaign ID {campaign_id} not found.")
            return jsonify({"status": "error", "message": "Campaign not found"}), 404
        
        campaign_data = {
            "id": campaign.id,
            "name": campaign.name,
            "message_content": campaign.message_content,
            "status": campaign.status.value,
            "target_group_id": campaign.target_group_id,
            "target_group_name": campaign.target_group.name if campaign.target_group else None,
            "scheduled_at": campaign.scheduled_at.isoformat() if campaign.scheduled_at else None,
            "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
            "updated_at": campaign.updated_at.isoformat() if campaign.updated_at else None,
            # Add metrics here later (sent_count, failed_count, etc.)
        }
        logger.info(f"Retrieved details for campaign ID: {campaign_id}")
        return jsonify({"status": "success", "campaign": campaign_data}), 200
    except Exception as e:
        logger.error(f"Error getting campaign details for ID {campaign_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve campaign details"}), 500
    finally:
        db.close()

@broadcast_bp.route("/campaigns", methods=["POST"])
@jwt_required()
def create_campaign():
    """Create a new broadcast campaign."""
    data = request.get_json()
    name = data.get("name")
    message_content = data.get("message_content")
    target_group_id = data.get("target_group_id")
    scheduled_at_str = data.get("scheduled_at") # Expecting ISO format string e.g., "2025-06-10T10:00:00Z"

    if not name or not message_content or not target_group_id:
        return jsonify({"status": "error", "message": "Missing required fields: name, message_content, target_group_id"}), 400

    db: Session = get_db_session()
    try:
        # Validate target group exists
        target_group = db.query(Group).filter(Group.id == target_group_id).first()
        if not target_group:
             return jsonify({"status": "error", "message": f"Target group ID {target_group_id} not found"}), 404

        scheduled_at_dt = None
        status = CampaignStatus.DRAFT
        if scheduled_at_str:
            try:
                # Attempt to parse ISO format, handling potential timezone info
                if scheduled_at_str.endswith("Z"):
                     scheduled_at_dt = datetime.fromisoformat(scheduled_at_str.replace("Z", "+00:00"))
                else:
                     scheduled_at_dt = datetime.fromisoformat(scheduled_at_str)
                status = CampaignStatus.SCHEDULED
            except ValueError:
                 return jsonify({"status": "error", "message": "Invalid scheduled_at format. Use ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SSZ)."}), 400

        new_campaign = BroadcastCampaign(
            name=name,
            message_content=message_content,
            target_group_id=target_group_id,
            scheduled_at=scheduled_at_dt,
            status=status
        )
        db.add(new_campaign)
        db.commit()
        db.refresh(new_campaign)
        logger.info(f"Created new campaign: {name} (ID: {new_campaign.id}), Status: {status.value}")
        
        # TODO: If status is not SCHEDULED, trigger immediate sending via background task?
        # if status == CampaignStatus.DRAFT: # Or some other logic for immediate send
        #    trigger_background_send(new_campaign.id)

        return jsonify({
            "status": "success", 
            "message": "Campaign created successfully", 
            "campaign": {"id": new_campaign.id, "name": new_campaign.name, "status": new_campaign.status.value}
        }), 210
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating campaign 	'{name}	': {e}")
        return jsonify({"status": "error", "message": "Failed to create campaign"}), 500
    finally:
        db.close()

@broadcast_bp.route("/campaigns/<int:campaign_id>", methods=["PUT"])
@jwt_required()
def update_campaign(campaign_id: int):
    """Update an existing campaign (e.g., message, schedule). Only possible for DRAFT or SCHEDULED campaigns."""
    data = request.get_json()
    db: Session = get_db_session()
    try:
        campaign = db.query(BroadcastCampaign).filter(BroadcastCampaign.id == campaign_id).first()
        if not campaign:
            return jsonify({"status": "error", "message": "Campaign not found"}), 404

        # Prevent updates to campaigns that are already sending or completed
        if campaign.status not in [CampaignStatus.DRAFT, CampaignStatus.SCHEDULED]:
            return jsonify({"status": "error", "message": f"Cannot update campaign in 	'{campaign.status.value}	' status"}), 409

        # Update fields if provided
        if "name" in data: campaign.name = data["name"]
        if "message_content" in data: campaign.message_content = data["message_content"]
        if "target_group_id" in data:
            target_group = db.query(Group).filter(Group.id == data["target_group_id"]).first()
            if not target_group:
                 return jsonify({"status": "error", "message": f"Target group ID {data['target_group_id']} not found"}), 404
            campaign.target_group_id = data["target_group_id"]
        
        new_status = campaign.status
        if "scheduled_at" in data:
            scheduled_at_str = data["scheduled_at"]
            if scheduled_at_str:
                try:
                    if scheduled_at_str.endswith("Z"):
                        campaign.scheduled_at = datetime.fromisoformat(scheduled_at_str.replace("Z", "+00:00"))
                    else:
                        campaign.scheduled_at = datetime.fromisoformat(scheduled_at_str)
                    new_status = CampaignStatus.SCHEDULED
                except ValueError:
                    return jsonify({"status": "error", "message": "Invalid scheduled_at format. Use ISO 8601 format."}), 400
            else:
                campaign.scheduled_at = None
                new_status = CampaignStatus.DRAFT # If schedule removed, becomes draft
        
        # Update status only if changed by scheduling logic
        if new_status != campaign.status:
             campaign.status = new_status

        db.commit()
        db.refresh(campaign)
        logger.info(f"Updated campaign ID: {campaign_id}")
        return jsonify({"status": "success", "message": "Campaign updated successfully", "campaign": {"id": campaign.id, "name": campaign.name, "status": campaign.status.value}}), 200

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating campaign ID {campaign_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to update campaign"}), 500
    finally:
        db.close()

@broadcast_bp.route("/campaigns/<int:campaign_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_campaign(campaign_id: int):
    """Cancel a scheduled campaign."""
    db: Session = get_db_session()
    try:
        campaign = db.query(BroadcastCampaign).filter(BroadcastCampaign.id == campaign_id).first()
        if not campaign:
            return jsonify({"status": "error", "message": "Campaign not found"}), 404

        if campaign.status != CampaignStatus.SCHEDULED:
            return jsonify({"status": "error", "message": f"Cannot cancel campaign in 	'{campaign.status.value}	' status. Only scheduled campaigns can be cancelled."}), 409

        campaign.status = CampaignStatus.CANCELLED
        # TODO: Add logic here to interact with the background task scheduler (e.g., Celery, RQ) 
        # to actually remove the scheduled job.
        # Example: cancel_scheduled_task(campaign.id)
        
        db.commit()
        db.refresh(campaign)
        logger.info(f"Cancelled campaign ID: {campaign_id}")
        return jsonify({"status": "success", "message": "Campaign cancelled successfully", "campaign": {"id": campaign.id, "status": campaign.status.value}}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error cancelling campaign ID {campaign_id}: {e}")
        # If cancelling the background task fails, should we rollback the status change?
        return jsonify({"status": "error", "message": "Failed to cancel campaign"}), 500
    finally:
        db.close()

# Note: Deleting campaigns might be complex due to history/metrics.
# Consider soft delete (e.g., adding an is_deleted flag) or archiving instead of hard delete.
# @broadcast_bp.route("/campaigns/<int:campaign_id>", methods=["DELETE"])
# @jwt_required()
# def delete_campaign(campaign_id: int): ...

# TODO: Implement background task logic (e.g., using Celery or RQ)
# - A task to periodically check for scheduled campaigns and trigger sending.
# - A task to handle the actual sending process for a given campaign ID (iterate contacts, call WhatsApp API, update status).
# - Need to add a task queue setup (Redis/RabbitMQ) and worker process.

