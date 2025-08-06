import requests
import json
import hmac
import hashlib
import logging
from sqlalchemy.orm import Session
# Temporariamente comentado até implementarmos os modelos de automação
# from models.automation_models import Webhook, WebhookEvent
from config.database import get_db

logger = logging.getLogger(__name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

def trigger_webhook(event: str, payload: dict):
    """Simplified webhook trigger for now"""
    logger.info(f"Webhook triggered for event: {event}")
    logger.info(f"Payload: {payload}")
    # TODO: Implement full webhook functionality
    pass

# Example of how to call this from other services:
# from services.webhook_service import trigger_webhook, WebhookEvent
# 
# def some_function_that_creates_a_contact(contact_data):
#     # ... logic to create contact ...
#     created_contact_payload = {"id": contact.id, "name": contact.name, "email": contact.email, "timestamp": datetime.utcnow().isoformat()}
#     trigger_webhook(WebhookEvent.CONTACT_CREATED, created_contact_payload)
#     # ... rest of the function ...

# Example of how to trigger on message received (e.g., from whatsapp webhook handler)
# def handle_incoming_whatsapp_message(message_payload):
#     # ... process message ...
#     trigger_webhook(WebhookEvent.MESSAGE_RECEIVED, message_payload)
#     # ... rest of handling ...

