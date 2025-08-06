#!/usr/bin/env python3
"""
Rotas do WhatsApp - AuraChat
Integração completa com WhatsApp Business API e Web WhatsApp
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import asyncio
import json
import logging

from config.database import get_db
from models.base_models import User, Contact, Chat, Message, WhatsAppConnection
from services.whatsapp_service import (
    WhatsAppService, WhatsAppMessage, WhatsAppResponse,
    init_whatsapp_service, get_whatsapp_service
)
from config.security import validate_phone, sanitize_input

# Configuração
whatsapp_bp = Blueprint('whatsapp', __name__, url_prefix='/api/whatsapp')
logger = logging.getLogger(__name__)

# Configuração do WhatsApp
WHATSAPP_CONFIG = {
    "provider": "hybrid",  # hybrid, official_api, web_whatsapp
    "official_api_token": None,  # Configurar via env
    "official_api_url": "https://graph.facebook.com/v18.0",
    "rate_limits": {
        "messages_per_minute": 30,
        "messages_per_hour": 1000
    }
}

@whatsapp_bp.route('/status', methods=['GET'])
@jwt_required()
def get_whatsapp_status():
    """Retorna status da conexão WhatsApp"""
    try:
        db: Session = get_db()
        current_user_id = get_jwt_identity()
        
        # Busca conexão do usuário
        connection = db.query(WhatsAppConnection).filter(
            WhatsAppConnection.user_id == current_user_id
        ).first()
        
        if not connection:
            return jsonify({
                "connected": False,
                "provider": None,
                "message": "Conexão não configurada"
            }), 404
        
        # Verifica status do serviço
        try:
            service = asyncio.run(get_whatsapp_service())
            status = asyncio.run(service.get_connection_status())
            return jsonify(status), 200
        except Exception as e:
            return jsonify({
                "connected": False,
                "provider": connection.provider,
                "error": str(e)
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao verificar status WhatsApp: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@whatsapp_bp.route('/connect', methods=['POST'])
@jwt_required()
def connect_whatsapp():
    """Conecta ao WhatsApp"""
    try:
        db: Session = get_db()
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        provider = data.get('provider', 'hybrid')
        api_token = data.get('api_token')
        
        # Valida provedor
        valid_providers = ['official_api', 'web_whatsapp', 'hybrid']
        if provider not in valid_providers:
            return jsonify({"error": "Provedor inválido"}), 400
        
        # Atualiza configuração
        WHATSAPP_CONFIG['provider'] = provider
        if api_token:
            WHATSAPP_CONFIG['official_api_token'] = api_token
        
        # Salva conexão no banco
        connection = db.query(WhatsAppConnection).filter(
            WhatsAppConnection.user_id == current_user_id
        ).first()
        
        if not connection:
            connection = WhatsAppConnection(
                user_id=current_user_id,
                provider=provider,
                api_token=api_token,
                is_active=True
            )
            db.add(connection)
        else:
            connection.provider = provider
            connection.api_token = api_token
            connection.is_active = True
        
        db.commit()
        
        # Inicializa serviço
        try:
            service = asyncio.run(init_whatsapp_service(WHATSAPP_CONFIG))
            status = asyncio.run(service.get_connection_status())
            
            return jsonify({
                "success": True,
                "message": "WhatsApp conectado com sucesso",
                "status": status
            }), 200
            
        except Exception as e:
            connection.is_active = False
            db.commit()
            
            return jsonify({
                "success": False,
                "error": f"Erro ao conectar: {str(e)}"
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao conectar WhatsApp: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@whatsapp_bp.route('/disconnect', methods=['POST'])
@jwt_required()
def disconnect_whatsapp():
    """Desconecta do WhatsApp"""
    try:
        db: Session = get_db()
        current_user_id = get_jwt_identity()
        
        # Busca conexão
        connection = db.query(WhatsAppConnection).filter(
            WhatsAppConnection.user_id == current_user_id
        ).first()
        
        if not connection:
            return jsonify({"error": "Conexão não encontrada"}), 404
        
        # Desconecta serviço
        try:
            service = asyncio.run(get_whatsapp_service())
            asyncio.run(service.disconnect())
        except Exception as e:
            logger.warning(f"Erro ao desconectar serviço: {e}")
        
        # Atualiza banco
        connection.is_active = False
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "WhatsApp desconectado"
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao desconectar WhatsApp: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@whatsapp_bp.route('/send', methods=['POST'])
@jwt_required()
def send_whatsapp_message():
    """Envia mensagem WhatsApp"""
    try:
        db: Session = get_db()
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Valida dados
        required_fields = ['to', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400
        
        to_phone = data['to']
        content = data['content']
        message_type = data.get('message_type', 'text')
        media_url = data.get('media_url')
        template_name = data.get('template_name')
        template_params = data.get('template_params')
        reply_to = data.get('reply_to')
        
        # Valida telefone
        if not validate_phone(to_phone):
            return jsonify({"error": "Número de telefone inválido"}), 400
        
        # Sanitiza conteúdo
        content = sanitize_input(content)
        
        # Busca ou cria contato
        contact = db.query(Contact).filter(
            Contact.phone == to_phone,
            Contact.created_by == current_user_id
        ).first()
        
        if not contact:
            contact = Contact(
                name=f"Contato {to_phone}",
                phone=to_phone,
                created_by=current_user_id
            )
            db.add(contact)
            db.commit()
        
        # Busca ou cria chat
        chat = db.query(Chat).filter(
            Chat.contact_id == contact.id,
            Chat.created_by == current_user_id
        ).first()
        
        if not chat:
            chat = Chat(
                contact_id=contact.id,
                created_by=current_user_id,
                chat_type="whatsapp"
            )
            db.add(chat)
            db.commit()
        
        # Cria mensagem no banco
        message = Message(
            chat_id=chat.id,
            content=content,
            message_type=message_type,
            sender_type="user",
            sender_id=current_user_id,
            media_url=media_url,
            metadata={
                "template_name": template_name,
                "template_params": template_params,
                "reply_to": reply_to
            }
        )
        db.add(message)
        db.commit()
        
        # Envia via WhatsApp
        try:
            service = asyncio.run(get_whatsapp_service())
            
            whatsapp_message = WhatsAppMessage(
                to=to_phone,
                content=content,
                message_type=message_type,
                media_url=media_url,
                template_name=template_name,
                template_params=template_params,
                reply_to=reply_to
            )
            
            response = asyncio.run(service.send_message(whatsapp_message))
            
            # Atualiza mensagem com resultado
            if response.success:
                message.external_id = response.message_id
                message.delivery_status = response.delivery_status
                message.sent_at = response.timestamp
            else:
                message.delivery_status = "failed"
                message.metadata["error"] = response.error
            
            db.commit()
            
            return jsonify({
                "success": response.success,
                "message_id": message.id,
                "external_id": response.message_id,
                "delivery_status": response.delivery_status,
                "error": response.error
            }), 200 if response.success else 400
            
        except Exception as e:
            message.delivery_status = "failed"
            message.metadata["error"] = str(e)
            db.commit()
            
            return jsonify({
                "success": False,
                "error": f"Erro ao enviar mensagem: {str(e)}"
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem WhatsApp: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@whatsapp_bp.route('/messages/<chat_id>', methods=['GET'])
@jwt_required()
def get_whatsapp_messages(chat_id: str):
    """Busca mensagens de um chat WhatsApp"""
    try:
        db: Session = get_db()
        current_user_id = get_jwt_identity()
        
        # Busca chat
        chat = db.query(Chat).filter(
            Chat.id == chat_id,
            Chat.created_by == current_user_id,
            Chat.chat_type == "whatsapp"
        ).first()
        
        if not chat:
            return jsonify({"error": "Chat não encontrado"}), 404
        
        # Busca mensagens
        messages = db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.created_at.desc()).limit(50).all()
        
        return jsonify({
            "chat_id": chat_id,
            "messages": [
                {
                    "id": msg.id,
                    "content": msg.content,
                    "message_type": msg.message_type,
                    "sender_type": msg.sender_type,
                    "delivery_status": msg.delivery_status,
                    "created_at": msg.created_at.isoformat(),
                    "sent_at": msg.sent_at.isoformat() if msg.sent_at else None,
                    "media_url": msg.media_url,
                    "metadata": msg.metadata
                }
                for msg in messages
            ]
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar mensagens WhatsApp: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@whatsapp_bp.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Webhook para receber mensagens do WhatsApp"""
    try:
        data = request.get_json()
        
        # Verifica se é verificação do webhook
        if 'hub.mode' in data and data['hub.mode'] == 'subscribe':
            if data['hub.verify_token'] == 'aura_chat_webhook':
                return data['hub.challenge'], 200
            else:
                return jsonify({"error": "Token inválido"}), 403
        
        # Processa mensagem recebida
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change['value'].get('messages'):
                            for message in change['value']['messages']:
                                # Processa mensagem recebida
                                asyncio.run(_process_incoming_message(message))
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        logger.error(f"Erro no webhook WhatsApp: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

async def _process_incoming_message(message_data: Dict[str, Any]):
    """Processa mensagem recebida do WhatsApp"""
    try:
        db: Session = get_db()
        
        # Extrai dados da mensagem
        phone = message_data['from']
        content = message_data['text']['body'] if 'text' in message_data else ""
        message_type = message_data.get('type', 'text')
        timestamp = message_data.get('timestamp')
        
        # Busca contato
        contact = db.query(Contact).filter(Contact.phone == phone).first()
        if not contact:
            # Cria contato se não existir
            contact = Contact(
                name=f"Contato {phone}",
                phone=phone,
                created_by=1  # Admin user
            )
            db.add(contact)
            db.commit()
        
        # Busca ou cria chat
        chat = db.query(Chat).filter(
            Chat.contact_id == contact.id,
            Chat.chat_type == "whatsapp"
        ).first()
        
        if not chat:
            chat = Chat(
                contact_id=contact.id,
                created_by=1,  # Admin user
                chat_type="whatsapp"
            )
            db.add(chat)
            db.commit()
        
        # Cria mensagem
        message = Message(
            chat_id=chat.id,
            content=content,
            message_type=message_type,
            sender_type="contact",
            sender_id=contact.id,
            external_id=message_data.get('id'),
            delivery_status="received",
            metadata={
                "whatsapp_message": message_data
            }
        )
        db.add(message)
        db.commit()
        
        logger.info(f"Mensagem recebida: {content} de {phone}")
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem recebida: {e}")

@whatsapp_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_whatsapp_templates():
    """Lista templates do WhatsApp Business"""
    try:
        # Templates padrão
        templates = [
            {
                "name": "welcome_message",
                "language": "pt_BR",
                "category": "UTILITY",
                "components": [
                    {
                        "type": "HEADER",
                        "text": "Bem-vindo ao AuraChat!"
                    },
                    {
                        "type": "BODY",
                        "text": "Olá {{1}}, seja bem-vindo! Como posso ajudá-lo hoje?"
                    }
                ]
            },
            {
                "name": "order_confirmation",
                "language": "pt_BR",
                "category": "MARKETING",
                "components": [
                    {
                        "type": "HEADER",
                        "text": "Pedido Confirmado"
                    },
                    {
                        "type": "BODY",
                        "text": "Olá {{1}}, seu pedido #{{2}} foi confirmado e será enviado em {{3}}."
                    }
                ]
            },
            {
                "name": "support_request",
                "language": "pt_BR",
                "category": "UTILITY",
                "components": [
                    {
                        "type": "HEADER",
                        "text": "Suporte Técnico"
                    },
                    {
                        "type": "BODY",
                        "text": "Olá {{1}}, recebemos sua solicitação de suporte. Nossa equipe entrará em contato em breve."
                    }
                ]
            }
        ]
        
        return jsonify({"templates": templates}), 200
        
    except Exception as e:
        logger.error(f"Erro ao buscar templates: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@whatsapp_bp.route('/health', methods=['GET'])
def whatsapp_health():
    """Health check do WhatsApp"""
    try:
        return jsonify({
            "service": "WhatsApp Integration",
            "status": "healthy",
            "version": "1.0.0",
            "features": [
                "Official API Integration",
                "Web WhatsApp Wrapper",
                "Hybrid Strategy",
                "Rate Limiting",
                "Template Support",
                "Webhook Processing"
            ]
        }), 200
    except Exception as e:
        return jsonify({
            "service": "WhatsApp Integration",
            "status": "unhealthy",
            "error": str(e)
        }), 500
