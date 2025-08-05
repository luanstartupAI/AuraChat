from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from config.database import get_db
from models.base_models import Contact
from models.crm_models import Group
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)
group_bp = Blueprint("group", __name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

# --- Group CRUD --- 

@group_bp.route("/", methods=["GET"])
@jwt_required()
def get_groups():
    """Get all groups."""
    db: Session = get_db_session()
    try:
        groups = db.query(Group).order_by(Group.name).all()
        groups_data = [
            {
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "contacts_count": len(group.contacts), # Calculate count
                "created_at": group.created_at.isoformat() if group.created_at else None,
            }
            for group in groups
        ]
        logger.info(f"Retrieved {len(groups_data)} groups.")
        return jsonify({"status": "success", "groups": groups_data}), 200
    except Exception as e:
        logger.error(f"Error getting groups: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve groups"}), 500
    finally:
        db.close()

@group_bp.route("/<int:group_id>", methods=["GET"])
@jwt_required()
def get_group_details(group_id: int):
    """Get details of a specific group, including its contacts."""
    db: Session = get_db_session()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            logger.warning(f"Group ID {group_id} not found.")
            return jsonify({"status": "error", "message": "Group not found"}), 404
        
        contacts_data = [
            {"id": contact.id, "name": contact.name, "phone_number": contact.phone_number}
            for contact in group.contacts
        ]
        
        group_data = {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "created_at": group.created_at.isoformat() if group.created_at else None,
            "contacts": contacts_data
        }
        logger.info(f"Retrieved details for group ID: {group_id}")
        return jsonify({"status": "success", "group": group_data}), 200
    except Exception as e:
        logger.error(f"Error getting group details for ID {group_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve group details"}), 500
    finally:
        db.close()

@group_bp.route("/", methods=["POST"])
@jwt_required()
def create_group():
    """Create a new group."""
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"status": "error", "message": "Group name is required"}), 400

    db: Session = get_db_session()
    try:
        new_group = Group(name=name, description=description)
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        logger.info(f"Created new group: {name} (ID: {new_group.id})")
        return jsonify({
            "status": "success", 
            "message": "Group created successfully", 
            "group": {"id": new_group.id, "name": new_group.name, "description": new_group.description}
        }), 210
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating group 	'{name}	': {e}")
        return jsonify({"status": "error", "message": "Failed to create group"}), 500
    finally:
        db.close()

@group_bp.route("/<int:group_id>", methods=["PUT"])
@jwt_required()
def update_group(group_id: int):
    """Update an existing group's name or description."""
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name:
         return jsonify({"status": "error", "message": "Group name cannot be empty"}), 400

    db: Session = get_db_session()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            logger.warning(f"Attempted to update non-existent group ID: {group_id}")
            return jsonify({"status": "error", "message": "Group not found"}), 404

        group.name = name
        group.description = description
        db.commit()
        db.refresh(group)
        logger.info(f"Updated group ID: {group_id}")
        return jsonify({
            "status": "success", 
            "message": "Group updated successfully",
            "group": {"id": group.id, "name": group.name, "description": group.description}
        }), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating group ID {group_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to update group"}), 500
    finally:
        db.close()

@group_bp.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_group(group_id: int):
    """Delete a group."""
    db: Session = get_db_session()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            logger.warning(f"Attempted to delete non-existent group ID: {group_id}")
            return jsonify({"status": "error", "message": "Group not found"}), 404

        # Note: Deleting the group might cascade or affect relationships.
        # Consider implications or handle manually (e.g., remove associations first).
        db.delete(group)
        db.commit()
        logger.info(f"Deleted group ID: {group_id}")
        return jsonify({"status": "success", "message": "Group deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting group ID {group_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to delete group"}), 500
    finally:
        db.close()

# --- Group Contact Management --- 

@group_bp.route("/<int:group_id>/contacts", methods=["POST"])
@jwt_required()
def add_contact_to_group(group_id: int):
    """Add a contact to a specific group."""
    data = request.get_json()
    contact_id = data.get("contact_id")

    if not contact_id:
        return jsonify({"status": "error", "message": "Contact ID is required"}), 400

    db: Session = get_db_session()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            return jsonify({"status": "error", "message": "Group not found"}), 404

        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
             return jsonify({"status": "error", "message": "Contact not found"}), 404

        if contact in group.contacts:
            return jsonify({"status": "error", "message": "Contact already in group"}), 409 # Conflict

        group.contacts.append(contact)
        db.commit()
        logger.info(f"Added contact ID {contact_id} to group ID {group_id}")
        return jsonify({"status": "success", "message": "Contact added to group"}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding contact {contact_id} to group {group_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to add contact to group"}), 500
    finally:
        db.close()

@group_bp.route("/<int:group_id>/contacts/<int:contact_id>", methods=["DELETE"])
@jwt_required()
def remove_contact_from_group(group_id: int, contact_id: int):
    """Remove a contact from a specific group."""
    db: Session = get_db_session()
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if not group:
            return jsonify({"status": "error", "message": "Group not found"}), 404

        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
             return jsonify({"status": "error", "message": "Contact not found"}), 404

        if contact not in group.contacts:
            return jsonify({"status": "error", "message": "Contact not found in this group"}), 404

        group.contacts.remove(contact)
        db.commit()
        logger.info(f"Removed contact ID {contact_id} from group ID {group_id}")
        return jsonify({"status": "success", "message": "Contact removed from group"}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing contact {contact_id} from group {group_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to remove contact from group"}), 500
    finally:
        db.close()

