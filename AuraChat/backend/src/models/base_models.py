from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    avatar = Column(String(500))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    chats = relationship("Chat", back_populates="user")
    contacts = relationship("Contact", back_populates="created_by_rel")
    kanban_cards = relationship("KanbanCard", back_populates="assigned_to_rel")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(255))
    avatar = Column(String(500))
    tags = Column(JSON, default=list)
    notes = Column(Text)
    status = Column(String(50), default="active")
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    created_by_rel = relationship("User", back_populates="contacts")
    chats = relationship("Chat", back_populates="contact")

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    contact_id = Column(String, ForeignKey("contacts.id"))
    user_id = Column(String, ForeignKey("users.id"))
    status = Column(String(50), default="active")
    last_message_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    contact = relationship("Contact", back_populates="chats")
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    chat_id = Column(String, ForeignKey("chats.id"))
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")  # text, image, audio, video, document
    media_url = Column(String(500))
    direction = Column(String(20), default="inbound")  # inbound, outbound
    status = Column(String(50), default="sent")  # sent, delivered, read
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    chat = relationship("Chat", back_populates="messages")

class KanbanBoard(Base):
    __tablename__ = "kanban_boards"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    columns = relationship("KanbanColumn", back_populates="board")

class KanbanColumn(Base):
    __tablename__ = "kanban_columns"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    board_id = Column(String, ForeignKey("kanban_boards.id"))
    name = Column(String(255), nullable=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    board = relationship("KanbanBoard", back_populates="columns")
    cards = relationship("KanbanCard", back_populates="column")

class KanbanCard(Base):
    __tablename__ = "kanban_cards"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    column_id = Column(String, ForeignKey("kanban_columns.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    assigned_to = Column(String, ForeignKey("users.id"))
    priority = Column(String(20), default="medium")  # low, medium, high
    due_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    column = relationship("KanbanColumn", back_populates="cards")
    assigned_to_rel = relationship("User", back_populates="kanban_cards")

class Flow(Base):
    __tablename__ = "flows"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    flow_data = Column(JSON)  # Dados do fluxo em formato JSON
    is_active = Column(Boolean, default=True)
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Broadcast(Base):
    __tablename__ = "broadcasts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    target_audience = Column(JSON)  # Critérios de segmentação
    scheduled_at = Column(DateTime(timezone=True))
    status = Column(String(50), default="draft")  # draft, scheduled, sent, cancelled
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WhatsAppConnection(Base):
    __tablename__ = "whatsapp_connections"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    connection_type = Column(String(50), default="api")  # api, qr_code
    api_credentials = Column(JSON)  # Credenciais da API Meta
    status = Column(String(50), default="disconnected")  # connected, disconnected, connecting
    last_connected = Column(DateTime(timezone=True))
    created_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

