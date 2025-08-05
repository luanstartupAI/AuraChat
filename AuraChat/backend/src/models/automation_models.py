from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum

class WebhookEvent(enum.Enum):
    MESSAGE_RECEIVED = "message.received"
    MESSAGE_SENT = "message.sent"
    CONTACT_CREATED = "contact.created"
    CONTACT_UPDATED = "contact.updated"
    GROUP_UPDATED = "group.updated"
    # Add more events as needed

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False, index=True)
    event = Column(SQLAlchemyEnum(WebhookEvent), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    secret = Column(String, nullable=True) # Optional secret for signature verification
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# --- Optional: Basic Automation Rule Model (Example) ---
# This is a simplified example. Real-world rules engines can be much more complex.

class RuleTriggerEvent(enum.Enum):
    MESSAGE_RECEIVED_MATCHING = "message.received.matching"
    TAG_ADDED = "tag.added"
    # Add more triggers

class RuleActionType(enum.Enum):
    SEND_MESSAGE = "send.message"
    ADD_TAG = "add.tag"
    ASSIGN_TO_AGENT = "assign.to.agent"
    # Add more actions

class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    trigger_event = Column(SQLAlchemyEnum(RuleTriggerEvent), nullable=False, index=True)
    trigger_config = Column(Text, nullable=True) # JSON string for trigger details (e.g., keywords, tag name)
    action_type = Column(SQLAlchemyEnum(RuleActionType), nullable=False, index=True)
    action_config = Column(Text, nullable=True) # JSON string for action details (e.g., message template, tag name, agent ID)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

