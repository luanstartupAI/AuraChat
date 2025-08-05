import requests
import json
import hmac
import hashlib
import logging
from sqlalchemy.orm import Session
from src.models.automation_models import Webhook, WebhookEvent
from src.config.database import get_db

logger = logging.getLogger(__name__)

# Helper function to get DB session
def get_db_session():
    return next(get_db())

def trigger_webhook(event: WebhookEvent, payload: dict):
    """Find active webhooks for the given event and send the payload."""
    db: Session = get_db_session()
    try:
        webhooks = db.query(Webhook).filter(
            Webhook.event == event,
            Webhook.is_active == True
        ).all()

        if not webhooks:
            # logger.debug(f"No active webhooks found for event: {event.value}")
            return

        logger.info(f"Triggering {len(webhooks)} webhook(s) for event: {event.value}")

        headers = {	"Content-Type	": 	"application/json	"}
        json_payload = json.dumps(payload)

        for webhook in webhooks:
            try:
                current_headers = headers.copy()
                # Add signature if secret is configured
                if webhook.secret:
                    signature = hmac.new(
                        webhook.secret.encode(	"utf-8	"),
                        json_payload.encode(	"utf-8	"),
                        hashlib.sha256
                    ).hexdigest()
                    current_headers[	"X-Aura-Signature-256	"] = f"sha256={signature}"
                    # logger.debug(f"Generated signature for webhook {webhook.id}: {signature}")
                
                # Send the webhook request (consider making this asynchronous)
                response = requests.post(
                    webhook.url, 
                    headers=current_headers, 
                    data=json_payload, 
                    timeout=10 # Add a timeout
                )
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                logger.info(f"Webhook {webhook.id} triggered successfully for event {event.value} to {webhook.url}. Status: {response.status_code}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Error triggering webhook {webhook.id} for event {event.value} to {webhook.url}: {e}")
            except Exception as e:
                 logger.error(f"Unexpected error triggering webhook {webhook.id} for event {event.value} to {webhook.url}: {e}")

    except Exception as e:
        logger.error(f"Error querying webhooks for event {event.value}: {e}")
    finally:
        db.close()

# Example of how to call this from other services:
# from src.services.webhook_service import trigger_webhook, WebhookEvent
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

