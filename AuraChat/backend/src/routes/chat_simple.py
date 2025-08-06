from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from config.database import get_db
from models.base_models import Chat, Message, Contact, User
from config.security import sanitize_input
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Obter lista de conversas do usuário"""
    try:
        current_user_id = get_jwt_identity()
        db = next(get_db())
        
        # Buscar conversas do usuário
        conversations = db.query(Chat).filter(
            Chat.user_id == current_user_id
        ).order_by(Chat.last_message_at.desc()).all()
        
        conversations_data = []
        for chat in conversations:
            # Buscar última mensagem
            last_message = db.query(Message).filter(
                Message.chat_id == chat.id
            ).order_by(Message.created_at.desc()).first()
            
            conversations_data.append({
                "id": chat.id,
                "contact": {
                    "id": chat.contact.id,
                    "name": chat.contact.name,
                    "phone": chat.contact.phone,
                    "avatar": chat.contact.avatar
                },
                "status": chat.status,
                "last_message": {
                    "content": last_message.content if last_message else "",
                    "created_at": last_message.created_at.isoformat() if last_message else None
                },
                "unread_count": db.query(Message).filter(
                    Message.chat_id == chat.id,
                    Message.direction == "inbound",
                    Message.status == "sent"
                ).count()
            })
        
        return jsonify({
            "conversations": conversations_data
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar conversas: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/conversations/<chat_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(chat_id):
    """Obter mensagens de uma conversa específica"""
    try:
        current_user_id = get_jwt_identity()
        db = next(get_db())
        
        # Verificar se o chat pertence ao usuário
        chat = db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.user_id == current_user_id
        ).first()
        
        if not chat:
            return jsonify({"error": "Conversa não encontrada"}), 404
        
        # Buscar mensagens
        messages = db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.created_at.asc()).all()
        
        messages_data = []
        for message in messages:
            messages_data.append({
                "id": message.id,
                "content": message.content,
                "message_type": message.message_type,
                "media_url": message.media_url,
                "direction": message.direction,
                "status": message.status,
                "created_at": message.created_at.isoformat()
            })
        
        return jsonify({
            "chat_id": chat_id,
            "contact": {
                "id": chat.contact.id,
                "name": chat.contact.name,
                "phone": chat.contact.phone,
                "avatar": chat.contact.avatar
            },
            "messages": messages_data
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar mensagens: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/conversations/<chat_id>/messages', methods=['POST'])
@jwt_required()
def send_message(chat_id):
    """Enviar mensagem em uma conversa"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({"error": "Conteúdo da mensagem é obrigatório"}), 400
        
        content = sanitize_input(data.get('content', ''))
        message_type = data.get('message_type', 'text')
        media_url = data.get('media_url')
        
        if not content and not media_url:
            return jsonify({"error": "Mensagem deve ter conteúdo ou mídia"}), 400
        
        db = next(get_db())
        
        # Verificar se o chat pertence ao usuário
        chat = db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.user_id == current_user_id
        ).first()
        
        if not chat:
            return jsonify({"error": "Conversa não encontrada"}), 404
        
        # Criar nova mensagem
        new_message = Message(
            chat_id=chat_id,
            content=content,
            message_type=message_type,
            media_url=media_url,
            direction="outbound",
            status="sent"
        )
        
        db.add(new_message)
        
        # Atualizar última mensagem do chat
        chat.last_message_at = datetime.utcnow()
        
        db.commit()
        db.refresh(new_message)
        
        return jsonify({
            "message": "Mensagem enviada com sucesso",
            "message_id": new_message.id
        }), 201
        
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/conversations/<chat_id>/read', methods=['POST'])
@jwt_required()
def mark_as_read(chat_id):
    """Marcar mensagens como lidas"""
    try:
        current_user_id = get_jwt_identity()
        db = next(get_db())
        
        # Verificar se o chat pertence ao usuário
        chat = db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.user_id == current_user_id
        ).first()
        
        if not chat:
            return jsonify({"error": "Conversa não encontrada"}), 404
        
        # Marcar mensagens como lidas
        db.query(Message).filter(
            Message.chat_id == chat_id,
            Message.direction == "inbound",
            Message.status == "sent"
        ).update({"status": "read"})
        
        db.commit()
        
        return jsonify({"message": "Mensagens marcadas como lidas"}), 200
        
    except Exception as e:
        logger.error(f"Erro ao marcar mensagens como lidas: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_chat_stats():
    """Obter estatísticas de chat"""
    try:
        current_user_id = get_jwt_identity()
        db = next(get_db())
        
        # Estatísticas básicas
        total_conversations = db.query(Chat).filter(
            Chat.user_id == current_user_id
        ).count()
        
        active_conversations = db.query(Chat).filter(
            Chat.user_id == current_user_id,
            Chat.status == "active"
        ).count()
        
        unread_messages = db.query(Message).join(Chat).filter(
            Chat.user_id == current_user_id,
            Message.direction == "inbound",
            Message.status == "sent"
        ).count()
        
        today_messages = db.query(Message).join(Chat).filter(
            Chat.user_id == current_user_id,
            Message.created_at >= datetime.utcnow().date()
        ).count()
        
        return jsonify({
            "total_conversations": total_conversations,
            "active_conversations": active_conversations,
            "unread_messages": unread_messages,
            "today_messages": today_messages
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@chat_bp.route('/health', methods=['GET'])
def chat_health():
    """Verificação de saúde do módulo de chat"""
    return jsonify({
        "status": "healthy",
        "module": "chat",
        "endpoints": [
            "GET /api/chat/conversations",
            "GET /api/chat/conversations/<chat_id>/messages",
            "POST /api/chat/conversations/<chat_id>/messages",
            "POST /api/chat/conversations/<chat_id>/read",
            "GET /api/chat/stats"
        ]
    }), 200