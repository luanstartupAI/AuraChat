from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

chat_bp = Blueprint('chat', __name__)

# Simulação de banco de dados de conversas para o MVP
conversations_db = {
    'conv1': {
        'id': 'conv1',
        'contact': {
            'id': 'contact1',
            'name': 'João Silva',
            'phone': '5511999999999',
            'avatar': 'https://i.pravatar.cc/150?img=1'
        },
        'messages': [
            {
                'id': 'msg1',
                'sender': 'contact',
                'content': 'Olá, preciso de ajuda com meu pedido',
                'timestamp': '2025-06-01T10:30:00Z',
                'status': 'read'
            },
            {
                'id': 'msg2',
                'sender': 'user',
                'content': 'Olá João! Como posso ajudar?',
                'timestamp': '2025-06-01T10:32:00Z',
                'status': 'delivered'
            }
        ],
        'status': 'active',
        'last_activity': '2025-06-01T10:32:00Z'
    },
    'conv2': {
        'id': 'conv2',
        'contact': {
            'id': 'contact2',
            'name': 'Maria Souza',
            'phone': '5511888888888',
            'avatar': 'https://i.pravatar.cc/150?img=5'
        },
        'messages': [
            {
                'id': 'msg3',
                'sender': 'contact',
                'content': 'Quando meu produto será entregue?',
                'timestamp': '2025-06-01T09:15:00Z',
                'status': 'read'
            }
        ],
        'status': 'active',
        'last_activity': '2025-06-01T09:15:00Z'
    }
}

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    # Em uma implementação real, filtraria por usuário
    return jsonify({
        'status': 'success',
        'conversations': list(conversations_db.values())
    })

@chat_bp.route('/conversations/<conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    if conversation_id not in conversations_db:
        return jsonify({'status': 'error', 'message': 'Conversa não encontrada'}), 404
    
    return jsonify({
        'status': 'success',
        'conversation': conversations_db[conversation_id]
    })

@chat_bp.route('/conversations/<conversation_id>/messages', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    if conversation_id not in conversations_db:
        return jsonify({'status': 'error', 'message': 'Conversa não encontrada'}), 404
    
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'status': 'error', 'message': 'Conteúdo da mensagem é obrigatório'}), 400
    
    # Criar nova mensagem
    new_message = {
        'id': f'msg{len(conversations_db[conversation_id]["messages"]) + 1}',
        'sender': 'user',
        'content': data['content'],
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'status': 'sent'
    }
    
    # Adicionar à conversa
    conversations_db[conversation_id]['messages'].append(new_message)
    conversations_db[conversation_id]['last_activity'] = new_message['timestamp']
    
    return jsonify({
        'status': 'success',
        'message': new_message
    }), 201

@chat_bp.route('/conversations', methods=['POST'])
@jwt_required()
def create_conversation():
    data = request.get_json()
    
    if not data or 'contact_id' not in data:
        return jsonify({'status': 'error', 'message': 'ID do contato é obrigatório'}), 400
    
    # Em uma implementação real, buscaria o contato no banco de dados
    contact_id = data['contact_id']
    contact = {
        'id': contact_id,
        'name': data.get('contact_name', 'Novo Contato'),
        'phone': data.get('contact_phone', ''),
        'avatar': f'https://i.pravatar.cc/150?img={len(conversations_db) + 1}'
    }
    
    # Criar nova conversa
    conversation_id = f'conv{len(conversations_db) + 1}'
    new_conversation = {
        'id': conversation_id,
        'contact': contact,
        'messages': [],
        'status': 'active',
        'last_activity': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    
    # Adicionar ao "banco de dados"
    conversations_db[conversation_id] = new_conversation
    
    return jsonify({
        'status': 'success',
        'conversation': new_conversation
    }), 201
