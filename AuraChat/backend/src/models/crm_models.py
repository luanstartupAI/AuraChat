from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
from models.base_models import Contact # Import Contact model
import enum

# Association table for Many-to-Many relationship between Group and Contact
group_contacts_association = Table(
    "group_contacts",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column("contact_id", Integer, ForeignKey("contacts.id"), primary_key=True),
)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-Many relationship with Contact
    contacts = relationship(
        "Contact",
        secondary=group_contacts_association,
        backref="groups" # Allows accessing group from contact object
    )

class CampaignStatus(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class BroadcastCampaign(Base):
    __tablename__ = "broadcast_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    message_content = Column(Text, nullable=False)
    status = Column(SQLAlchemyEnum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True, index=True) # Nullable if it's a draft or sent immediately
    # target_group_id = Column(Integer, ForeignKey("groups.id"), nullable=False) # Assuming targeting one group per campaign for now
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to Group (Many-to-One)
    # target_group = relationship("Group")

    # --- Alternative: Many-to-Many relationship with Group for targeting multiple groups --- 
    # target_groups = relationship("Group", secondary=campaign_groups_association, backref="campaigns")
    # Need to define campaign_groups_association table if using Many-to-Many

    # --- Let's stick to a simpler approach first: Store target group IDs as a list or link to a separate target table? --- 
    # For simplicity now, let's assume a campaign targets ONE group. If multiple needed, refactor later.
    target_group_id = Column(Integer, ForeignKey("groups.id"), nullable=True) # Allow null if targeting individual contacts or other criteria later?
    target_group = relationship("Group")

    # Add fields for basic metrics if needed directly on the campaign
    # sent_count = Column(Integer, default=0)
    # failed_count = Column(Integer, default=0)

# --- Optional: Association table for Campaign to Group (if Many-to-Many targeting) ---
# campaign_groups_association = Table(
#     "campaign_groups",
#     Base.metadata,
#     Column("campaign_id", Integer, ForeignKey("broadcast_campaigns.id"), primary_key=True),
#     Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
# )

