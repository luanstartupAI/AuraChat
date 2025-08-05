from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config.database import get_db
# Temporariamente comentado até implementarmos o modelo Setting
# from models.base_models import Setting
from flask_jwt_extended import jwt_required
import logging

logger = logging.getLogger(__name__)
settings_bp = Blueprint("settings", __name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

# Configurações padrão do sistema
DEFAULT_SETTINGS = {
    "theme": "light",
    "language": "pt-BR",
    "notifications_enabled": "true",
    "auto_reply_enabled": "false",
    "whatsapp_webhook_url": "",
    "ai_assistant_enabled": "true",
    "max_contacts_per_page": "50",
    "chat_refresh_interval": "5000"
}

@settings_bp.route("/", methods=["GET"])
@jwt_required()
def get_settings():
    """Get all settings."""
    try:
        # TODO: Implement when Setting model is ready
        logger.info("Settings endpoint called - returning default settings")
        return jsonify({
            "status": "success", 
            "settings": DEFAULT_SETTINGS
        }), 200
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve settings"}), 500

@settings_bp.route("/<key>", methods=["GET"])
@jwt_required()
def get_setting(key: str):
    """Get a specific setting by key."""
    try:
        # TODO: Implement when Setting model is ready
        if key in DEFAULT_SETTINGS:
            logger.info(f"Retrieved setting: {key}")
            return jsonify({
                "status": "success", 
                "setting": {
                    "key": key, 
                    "value": DEFAULT_SETTINGS[key], 
                    "description": f"Setting for {key}"
                }
            }), 200
        else:
            logger.warning(f"Setting key '{key}' not found.")
            return jsonify({"status": "error", "message": "Setting not found"}), 404
    except Exception as e:
        logger.error(f"Error getting setting '{key}': {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve setting"}), 500

@settings_bp.route("/", methods=["POST"])
@jwt_required()
def create_or_update_setting():
    """Create a new setting or update an existing one."""
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")
    description = data.get("description")

    if not key or value is None:
        return jsonify({"status": "error", "message": "Missing key or value"}), 400

    try:
        # TODO: Implement when Setting model is ready
        logger.info(f"Setting update requested: {key} = {value}")
        return jsonify({
            "status": "success", 
            "message": "Setting functionality coming soon",
            "setting": {"key": key, "value": value}
        }), 200
    except Exception as e:
        logger.error(f"Error creating/updating setting '{key}': {e}")
        return jsonify({"status": "error", "message": "Failed to create or update setting"}), 500

@settings_bp.route("/health", methods=["GET"])
def settings_health():
    """Health check for settings module."""
    return jsonify({
        "status": "healthy",
        "module": "settings",
        "message": "Settings module is running (basic functionality)"
    }), 200

