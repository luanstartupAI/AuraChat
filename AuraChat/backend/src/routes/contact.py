from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import or_
from config.database import get_db
from models.base_models import Contact # Use the actual model
from services.webhook_service import trigger_webhook # Import webhook trigger
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import logging

logger = logging.getLogger(__name__)
contact_bp = Blueprint("contact", __name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

@contact_bp.route("/contacts", methods=["GET"])
@jwt_required()
def get_contacts():
    """Get contacts with optional search and pagination."""
    db: Session = get_db_session()
    try:
        # --- Pagination and Search --- 
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)
        search_term = request.args.get("search", "", type=str)
        offset = (page - 1) * limit

        query = db.query(Contact)

        if search_term:
            search_filter = f"%{search_term}%"
            query = query.filter(
                or_(
                    Contact.name.ilike(search_filter),
                    Contact.email.ilike(search_filter),
                    Contact.phone_number.ilike(search_filter)
                )
            )
        
        total_contacts = query.count()
        contacts = query.order_by(Contact.name).offset(offset).limit(limit).all()

        contacts_data = [
            {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone_number": contact.phone_number,
                "avatar_url": contact.avatar_url,
                "created_at": contact.created_at.isoformat() if contact.created_at else None,
                "updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
                # Add tags or other relevant fields if needed
            }
            for contact in contacts
        ]

        pagination_data = {
            "total": total_contacts,
            "pages": (total_contacts + limit - 1) // limit,
            "currentPage": page,
            "limit": limit
        }

        logger.info(f"Retrieved {len(contacts_data)} contacts (page {page}, limit {limit}, search: 	'{search_term}'). Total: {total_contacts}")
        return jsonify({"status": "success", "contacts": contacts_data, "pagination": pagination_data}), 200
    except Exception as e:
        logger.error(f"Error getting contacts: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve contacts"}), 500
    finally:
        db.close()

@contact_bp.route("/contacts/<int:contact_id>", methods=["GET"])
@jwt_required()
def get_contact(contact_id: int):
    """Get details of a specific contact."""
    db: Session = get_db_session()
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            logger.warning(f"Contact ID {contact_id} not found.")
            return jsonify({"status": "error", "message": "Contact not found"}), 404
        
        contact_data = {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone_number": contact.phone_number,
            "avatar_url": contact.avatar_url,
            "created_at": contact.created_at.isoformat() if contact.created_at else None,
            "updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
            # Add tags, notes, group memberships etc. here
        }
        logger.info(f"Retrieved details for contact ID: {contact_id}")
        return jsonify({"status": "success", "contact": contact_data}), 200
    except Exception as e:
        logger.error(f"Error getting contact details for ID {contact_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve contact details"}), 500
    finally:
        db.close()

@contact_bp.route("/contacts", methods=["POST"])
@jwt_required()
def create_contact():
    """Create a new contact."""
    data = request.get_json()
    name = data.get("name")
    phone_number = data.get("phone_number")
    email = data.get("email")
    avatar_url = data.get("avatar_url")

    if not name or not phone_number:
        return jsonify({"status": "error", "message": "Name and phone number are required"}), 400

    db: Session = get_db_session()
    try:
        # Check if phone number already exists (optional, depends on requirements)
        existing_contact = db.query(Contact).filter(Contact.phone_number == phone_number).first()
        if existing_contact:
             return jsonify({"status": "error", "message": "Contact with this phone number already exists"}), 409

        new_contact = Contact(
            name=name,
            phone_number=phone_number,
            email=email,
            avatar_url=avatar_url
            # Add other fields like tags, notes if applicable
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        logger.info(f"Created new contact: {name} (ID: {new_contact.id})")

        # Trigger webhook after successful creation
        try:
            contact_payload = {
                "id": new_contact.id,
                "name": new_contact.name,
                "phone_number": new_contact.phone_number,
                "email": new_contact.email,
                "created_at": new_contact.created_at.isoformat() if new_contact.created_at else None
            }
            trigger_webhook("CONTACT_CREATED", contact_payload)
        except Exception as webhook_e:
             logger.error(f"Failed to trigger CONTACT_CREATED webhook for contact {new_contact.id}: {webhook_e}")

        return jsonify({
            "status": "success", 
            "message": "Contact created successfully", 
            "contact": {"id": new_contact.id, "name": new_contact.name, "phone_number": new_contact.phone_number}
        }), 210
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating contact 	'{name}': {e}")
        return jsonify({"status": "error", "message": "Failed to create contact"}), 500
    finally:
        db.close()

@contact_bp.route("/contacts/<int:contact_id>", methods=["PUT"])
@jwt_required()
def update_contact(contact_id: int):
    """Update an existing contact."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided for update"}), 400

    db: Session = get_db_session()
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            logger.warning(f"Attempted to update non-existent contact ID: {contact_id}")
            return jsonify({"status": "error", "message": "Contact not found"}), 404

        updated_fields = []
        if "name" in data and data["name"] != contact.name:
            contact.name = data["name"]
            updated_fields.append("name")
        if "email" in data and data["email"] != contact.email:
            contact.email = data["email"]
            updated_fields.append("email")
        if "phone_number" in data and data["phone_number"] != contact.phone_number:
            # Optional: Check if new phone number conflicts with another contact
            existing = db.query(Contact).filter(Contact.phone_number == data["phone_number"], Contact.id != contact_id).first()
            if existing:
                 return jsonify({"status": "error", "message": "Another contact already exists with this phone number"}), 409
            contact.phone_number = data["phone_number"]
            updated_fields.append("phone_number")
        if "avatar_url" in data and data["avatar_url"] != contact.avatar_url:
            contact.avatar_url = data["avatar_url"]
            updated_fields.append("avatar_url")
        # Update other fields like tags, notes here

        if not updated_fields:
             return jsonify({"status": "success", "message": "No changes detected", "contact": {"id": contact.id}}), 200

        # contact.updated_at is handled by the model/database trigger (onupdate=func.now())
        db.commit()
        db.refresh(contact)
        logger.info(f"Updated contact ID: {contact_id}. Fields changed: {', '.join(updated_fields)}")

        # Trigger webhook after successful update
        try:
            contact_payload = {
                "id": contact.id,
                "name": contact.name,
                "phone_number": contact.phone_number,
                "email": contact.email,
                "updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
                "changed_fields": updated_fields
            }
            trigger_webhook("CONTACT_UPDATED", contact_payload)
        except Exception as webhook_e:
             logger.error(f"Failed to trigger CONTACT_UPDATED webhook for contact {contact.id}: {webhook_e}")

        return jsonify({
            "status": "success", 
            "message": "Contact updated successfully",
            "contact": {"id": contact.id, "name": contact.name, "phone_number": contact.phone_number}
        }), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating contact ID {contact_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to update contact"}), 500
    finally:
        db.close()

@contact_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
@jwt_required()
def delete_contact(contact_id: int):
    """Delete a contact."""
    db: Session = get_db_session()
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            logger.warning(f"Attempted to delete non-existent contact ID: {contact_id}")
            return jsonify({"status": "error", "message": "Contact not found"}), 404

        # Consider implications: remove from groups, delete associated messages?
        # For now, just delete the contact record.
        db.delete(contact)
        db.commit()
        logger.info(f"Deleted contact ID: {contact_id}")
        # Trigger webhook? (CONTACT_DELETED event?)
        return jsonify({"status": "success", "message": "Contact deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting contact ID {contact_id}: {e}")
        # Handle potential foreign key constraints if not set up to cascade
        return jsonify({"status": "error", "message": "Failed to delete contact"}), 500
    finally:
        db.close()

# Note: The /contacts/search endpoint is effectively replaced by the GET /contacts endpoint with query parameters.
# Keeping it might be redundant unless it has significantly different logic.
# @contact_bp.route("/contacts/search", methods=["GET"])
# @jwt_required()
# def search_contacts(): ...

