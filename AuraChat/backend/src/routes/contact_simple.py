from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from sqlalchemy import or_
from config.database import get_db
from models.base_models import Contact
from config.security import sanitize_input, validate_phone, validate_email
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contacts", methods=["GET"])
@jwt_required()
def get_contacts():
    """Get contacts with optional search and pagination."""
    db = next(get_db())
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
                    Contact.phone.ilike(search_filter)
                )
            )
        
        total_contacts = query.count()
        contacts = query.order_by(Contact.name).offset(offset).limit(limit).all()

        contacts_data = [
            {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "avatar": contact.avatar,
                "tags": contact.tags or [],
                "status": contact.status,
                "created_at": contact.created_at.isoformat() if contact.created_at else None,
                "updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
            }
            for contact in contacts
        ]

        pagination_data = {
            "total": total_contacts,
            "pages": (total_contacts + limit - 1) // limit,
            "currentPage": page,
            "limit": limit
        }

        logger.info(f"Retrieved {len(contacts_data)} contacts (page {page}, limit {limit}, search: '{search_term}'). Total: {total_contacts}")
        return jsonify({"status": "success", "contacts": contacts_data, "pagination": pagination_data}), 200
    except Exception as e:
        logger.error(f"Error getting contacts: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve contacts"}), 500
    finally:
        db.close()

@contact_bp.route("/contacts/<contact_id>", methods=["GET"])
@jwt_required()
def get_contact(contact_id: str):
    """Get details of a specific contact."""
    db = next(get_db())
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            logger.warning(f"Contact ID {contact_id} not found.")
            return jsonify({"status": "error", "message": "Contact not found"}), 404
        
        contact_data = {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "avatar": contact.avatar,
            "tags": contact.tags or [],
            "notes": contact.notes,
            "status": contact.status,
            "created_at": contact.created_at.isoformat() if contact.created_at else None,
            "updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
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
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    name = sanitize_input(data.get("name", ""))
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip().lower() if data.get("email") else None
    tags = data.get("tags", [])
    notes = sanitize_input(data.get("notes", ""))
    
    if not name or not phone:
        return jsonify({"status": "error", "message": "Name and phone are required"}), 400
    
    if not validate_phone(phone):
        return jsonify({"status": "error", "message": "Invalid phone number format"}), 400
    
    if email and not validate_email(email):
        return jsonify({"status": "error", "message": "Invalid email format"}), 400
    
    db = next(get_db())
    try:
        # Check if phone already exists
        existing_contact = db.query(Contact).filter(Contact.phone == phone).first()
        if existing_contact:
            return jsonify({"status": "error", "message": "Contact with this phone number already exists"}), 409
        
        # Create new contact
        new_contact = Contact(
            name=name,
            phone=phone,
            email=email,
            tags=tags,
            notes=notes,
            created_by=current_user_id,
            status="active"
        )
        
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        
        logger.info(f"Created new contact: {new_contact.id}")
        
        contact_data = {
            "id": new_contact.id,
            "name": new_contact.name,
            "email": new_contact.email,
            "phone": new_contact.phone,
            "avatar": new_contact.avatar,
            "tags": new_contact.tags or [],
            "notes": new_contact.notes,
            "status": new_contact.status,
            "created_at": new_contact.created_at.isoformat() if new_contact.created_at else None
        }
        
        return jsonify({
            "status": "success", 
            "message": "Contact created successfully", 
            "contact": contact_data
        }), 201
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating contact: {e}")
        return jsonify({"status": "error", "message": "Failed to create contact"}), 500
    finally:
        db.close()

@contact_bp.route("/contacts/<contact_id>", methods=["PUT"])
@jwt_required()
def update_contact(contact_id: str):
    """Update an existing contact."""
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    db = next(get_db())
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            return jsonify({"status": "error", "message": "Contact not found"}), 404
        
        updated_fields = []
        
        # Update fields if provided
        if "name" in data:
            contact.name = sanitize_input(data["name"])
            updated_fields.append("name")
        
        if "phone" in data:
            phone = data["phone"].strip()
            if not validate_phone(phone):
                return jsonify({"status": "error", "message": "Invalid phone number format"}), 400
            
            # Check if phone is already used by another contact
            existing_contact = db.query(Contact).filter(
                Contact.phone == phone,
                Contact.id != contact_id
            ).first()
            if existing_contact:
                return jsonify({"status": "error", "message": "Phone number already in use by another contact"}), 409
            
            contact.phone = phone
            updated_fields.append("phone")
        
        if "email" in data:
            email = data["email"].strip().lower() if data["email"] else None
            if email and not validate_email(email):
                return jsonify({"status": "error", "message": "Invalid email format"}), 400
            contact.email = email
            updated_fields.append("email")
        
        if "tags" in data:
            contact.tags = data["tags"]
            updated_fields.append("tags")
        
        if "notes" in data:
            contact.notes = sanitize_input(data["notes"])
            updated_fields.append("notes")
        
        if "status" in data:
            contact.status = data["status"]
            updated_fields.append("status")
        
        if "avatar" in data:
            contact.avatar = data["avatar"]
            updated_fields.append("avatar")
        
        db.commit()
        db.refresh(contact)
        
        logger.info(f"Updated contact {contact_id}: {', '.join(updated_fields)}")
        
        contact_data = {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "avatar": contact.avatar,
            "tags": contact.tags or [],
            "notes": contact.notes,
            "status": contact.status,
            "updated_at": contact.updated_at.isoformat() if contact.updated_at else None,
            "changed_fields": updated_fields
        }
        
        return jsonify({
            "status": "success", 
            "message": "Contact updated successfully", 
            "contact": contact_data
        }), 200
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating contact {contact_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to update contact"}), 500
    finally:
        db.close()

@contact_bp.route("/contacts/<contact_id>", methods=["DELETE"])
@jwt_required()
def delete_contact(contact_id: str):
    """Delete a contact."""
    db = next(get_db())
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact:
            return jsonify({"status": "error", "message": "Contact not found"}), 404
        
        db.delete(contact)
        db.commit()
        
        logger.info(f"Deleted contact: {contact_id}")
        return jsonify({"status": "success", "message": "Contact deleted successfully"}), 200
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting contact {contact_id}: {e}")
        return jsonify({"status": "error", "message": "Failed to delete contact"}), 500
    finally:
        db.close()

@contact_bp.route("/health", methods=["GET"])
def contact_health():
    """Health check for contact module."""
    return jsonify({
        "status": "healthy",
        "module": "contact",
        "endpoints": [
            "GET /api/contact/contacts",
            "GET /api/contact/contacts/<contact_id>",
            "POST /api/contact/contacts",
            "PUT /api/contact/contacts/<contact_id>",
            "DELETE /api/contact/contacts/<contact_id>"
        ]
    }), 200