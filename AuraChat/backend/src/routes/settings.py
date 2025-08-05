from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config.database import get_db
from models.base_models import Setting
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger(__name__)
settings_bp = Blueprint("settings", __name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

@settings_bp.route("/", methods=["GET"])
@jwt_required()
def get_settings():
    """Get all settings."""
    db: Session = get_db_session()
    try:
        settings = db.query(Setting).all()
        settings_dict = {setting.key: setting.value for setting in settings}
        logger.info("Retrieved all settings.")
        return jsonify({"status": "success", "settings": settings_dict}), 200
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve settings"}), 500
    finally:
        db.close()

@settings_bp.route("/<key>", methods=["GET"])
@jwt_required()
def get_setting(key: str):
    """Get a specific setting by key."""
    db: Session = get_db_session()
    try:
        setting = db.query(Setting).filter(Setting.key == key).first()
        if not setting:
            logger.warning(f"Setting key 	'{key}	' not found.")
            return jsonify({"status": "error", "message": "Setting not found"}), 404
        logger.info(f"Retrieved setting: {key}")
        return jsonify({"status": "success", "setting": {"key": setting.key, "value": setting.value, "description": setting.description}}), 200
    except Exception as e:
        logger.error(f"Error getting setting 	'{key}	': {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve setting"}), 500
    finally:
        db.close()

@settings_bp.route("/", methods=["POST"])
@jwt_required()
def create_or_update_setting():
    """Create a new setting or update an existing one."""
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")
    description = data.get("description")

    if not key or value is None: # Allow empty string for value
        return jsonify({"status": "error", "message": "Missing key or value"}), 400

    db: Session = get_db_session()
    try:
        setting = db.query(Setting).filter(Setting.key == key).first()
        if setting:
            # Update existing setting
            setting.value = value
            setting.description = description
            db.commit()
            db.refresh(setting)
            logger.info(f"Updated setting: {key}")
            return jsonify({"status": "success", "message": "Setting updated successfully", "setting": {"key": setting.key, "value": setting.value}}), 200
        else:
            # Create new setting
            new_setting = Setting(key=key, value=value, description=description)
            db.add(new_setting)
            db.commit()
            db.refresh(new_setting)
            logger.info(f"Created new setting: {key}")
            return jsonify({"status": "success", "message": "Setting created successfully", "setting": {"key": new_setting.key, "value": new_setting.value}}), 210
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating/updating setting 	'{key}	': {e}")
        return jsonify({"status": "error", "message": "Failed to create or update setting"}), 500
    finally:
        db.close()

# Note: Deleting settings might be risky, consider if needed.
# @settings_bp.route("/<key>", methods=["DELETE"])
# @jwt_required()
# def delete_setting(key: str):
#     """Delete a setting by key."""
#     db: Session = get_db_session()
#     try:
#         setting = db.query(Setting).filter(Setting.key == key).first()
#         if not setting:
#             return jsonify({"status": "error", "message": "Setting not found"}), 404
#         db.delete(setting)
#         db.commit()
#         logger.info(f"Deleted setting: {key}")
#         return jsonify({"status": "success", "message": "Setting deleted successfully"}), 200
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Error deleting setting 	'{key}	': {e}")
#         return jsonify({"status": "error", "message": "Failed to delete setting"}), 500
#     finally:
#         db.close()

