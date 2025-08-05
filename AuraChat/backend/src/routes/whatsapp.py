from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import uuid
import logging
import random

logger = logging.getLogger(__name__)

whatsapp_bp = Blueprint('whatsapp', __name__)

# Simulação de banco de dados de conexões WhatsApp
whatsapp_connections_db = {
    'connection1': {
        'id': 'connection1',
        'user_id': 'user1',
        'phone_number': '5511999999999',
        'name': 'Atendimento Principal',
        'status': 'connected',  # connected, disconnected, pending
        'qr_code': None,
        'business_profile': {
            'name': 'Aura Solutions',
            'description': 'Soluções de comunicação inteligente',
            'address': 'Av. Paulista, 1000, São Paulo - SP',
            'email': 'contato@aura.com',
            'website': 'https://aura.com',
            'category': 'Software & IT'
        },
        'stats': {
            'messages_sent': 1250,
            'messages_received': 980,
            'active_chats': 45
        },
        'created_at': '2025-05-01T10:00:00Z',
        'updated_at': '2025-06-02T09:00:00Z',
        'last_connected': '2025-06-02T09:00:00Z'
    },
    'connection2': {
        'id': 'connection2',
        'user_id': 'user1',
        'phone_number': '5511888888888',
        'name': 'Suporte Técnico',
        'status': 'connected',
        'qr_code': None,
        'business_profile': {
            'name': 'Aura Suporte',
            'description': 'Suporte técnico para produtos Aura',
            'address': 'Av. Paulista, 1000, São Paulo - SP',
            'email': 'suporte@aura.com',
            'website': 'https://suporte.aura.com',
            'category': 'Customer Service'
        },
        'stats': {
            'messages_sent': 850,
            'messages_received': 720,
            'active_chats': 30
        },
        'created_at': '2025-05-15T14:00:00Z',
        'updated_at': '2025-06-02T09:15:00Z',
        'last_connected': '2025-06-02T09:15:00Z'
    }
}

# Simulação de banco de dados de mensagens
whatsapp_messages_db = {
    'msg1': {
        'id': 'msg1',
        'connection_id': 'connection1',
        'chat_id': 'chat1',
        'contact_id': 'contact1',
        'direction': 'inbound',
        'type': 'text',
        'content': 'Olá, gostaria de saber mais sobre os serviços de vocês.',
        'media_url': None,
        'status': 'read',  # sent, delivered, read, failed
        'timestamp': '2025-06-01T14:30:00Z',
        'metadata': {}
    },
    'msg2': {
        'id': 'msg2',
        'connection_id': 'connection1',
        'chat_id': 'chat1',
        'contact_id': 'contact1',
        'direction': 'outbound',
        'type': 'text',
        'content': 'Olá! Obrigado pelo seu interesse. Oferecemos soluções de comunicação inteligente para empresas de todos os tamanhos. Como posso ajudar?',
        'media_url': None,
        'status': 'read',
        'timestamp': '2025-06-01T14:32:00Z',
        'metadata': {
            'agent_id': 'user1',
            'automation_id': None
        }
    },
    'msg3': {
        'id': 'msg3',
        'connection_id': 'connection1',
        'chat_id': 'chat1',
        'contact_id': 'contact1',
        'direction': 'inbound',
        'type': 'text',
        'content': 'Gostaria de saber os preços dos planos.',
        'media_url': None,
        'status': 'read',
        'timestamp': '2025-06-01T14:35:00Z',
        'metadata': {}
    },
    'msg4': {
        'id': 'msg4',
        'connection_id': 'connection1',
        'chat_id': 'chat1',
        'contact_id': 'contact1',
        'direction': 'outbound',
        'type': 'text',
        'content': 'Claro! Temos três planos: Básico (R$49,90/mês), Premium (R$99,90/mês) e Enterprise (R$249,90/mês). Cada um oferece diferentes recursos e limites. Posso enviar mais detalhes sobre cada plano?',
        'media_url': None,
        'status': 'read',
        'timestamp': '2025-06-01T14:37:00Z',
        'metadata': {
            'agent_id': 'user1',
            'automation_id': None
        }
    },
    'msg5': {
        'id': 'msg5',
        'connection_id': 'connection1',
        'chat_id': 'chat2',
        'contact_id': 'contact2',
        'direction': 'inbound',
        'type': 'text',
        'content': 'Estou com problemas para acessar minha conta.',
        'media_url': None,
        'status': 'read',
        'timestamp': '2025-06-02T10:15:00Z',
        'metadata': {}
    },
    'msg6': {
        'id': 'msg6',
        'connection_id': 'connection1',
        'chat_id': 'chat2',
        'contact_id': 'contact2',
        'direction': 'outbound',
        'type': 'text',
        'content': 'Lamento pelo inconveniente. Pode me informar qual erro está recebendo? Também pode me dizer seu email para que eu possa verificar sua conta?',
        'media_url': None,
        'status': 'delivered',
        'timestamp': '2025-06-02T10:17:00Z',
        'metadata': {
            'agent_id': 'user2',
            'automation_id': None
        }
    }
}

# Simulação de banco de dados de chats
whatsapp_chats_db = {
    'chat1': {
        'id': 'chat1',
        'connection_id': 'connection1',
        'contact_id': 'contact1',
        'contact_name': 'João Silva',
        'contact_phone': '5511999999991',
        'unread_count': 0,
        'last_message': {
            'content': 'Claro! Temos três planos: Básico (R$49,90/mês), Premium (R$99,90/mês) e Enterprise (R$249,90/mês). Cada um oferece diferentes recursos e limites. Posso enviar mais detalhes sobre cada plano?',
            'timestamp': '2025-06-01T14:37:00Z',
            'direction': 'outbound'
        },
        'status': 'active',  # active, archived, pending
        'assigned_to': 'user1',
        'tags': ['lead', 'interested'],
        'created_at': '2025-06-01T14:30:00Z',
        'updated_at': '2025-06-01T14:37:00Z'
    },
    'chat2': {
        'id': 'chat2',
        'connection_id': 'connection1',
        'contact_id': 'contact2',
        'contact_name': 'Maria Souza',
        'contact_phone': '5511999999992',
        'unread_count': 0,
        'last_message': {
            'content': 'Lamento pelo inconveniente. Pode me informar qual erro está recebendo? Também pode me dizer seu email para que eu possa verificar sua conta?',
            'timestamp': '2025-06-02T10:17:00Z',
            'direction': 'outbound'
        },
        'status': 'active',
        'assigned_to': 'user2',
        'tags': ['support'],
        'created_at': '2025-06-02T10:15:00Z',
        'updated_at': '2025-06-02T10:17:00Z'
    },
    'chat3': {
        'id': 'chat3',
        'connection_id': 'connection2',
        'contact_id': 'contact3',
        'contact_name': 'Carlos Oliveira',
        'contact_phone': '5511999999993',
        'unread_count': 2,
        'last_message': {
            'content': 'Preciso de ajuda com a configuração do sistema.',
            'timestamp': '2025-06-02T11:05:00Z',
            'direction': 'inbound'
        },
        'status': 'pending',
        'assigned_to': None,
        'tags': ['support', 'technical'],
        'created_at': '2025-06-02T11:05:00Z',
        'updated_at': '2025-06-02T11:05:00Z'
    }
}

# Simulação de banco de dados de templates de mensagens
whatsapp_templates_db = {
    'template1': {
        'id': 'template1',
        'user_id': 'user1',
        'name': 'welcome',
        'status': 'approved',  # pending, approved, rejected
        'category': 'MARKETING',
        'language': 'pt_BR',
        'components': [
            {
                'type': 'HEADER',
                'format': 'TEXT',
                'text': 'Bem-vindo à Aura Solutions!'
            },
            {
                'type': 'BODY',
                'text': 'Olá {{1}}, obrigado por entrar em contato conosco. Como podemos ajudar você hoje?',
                'variables': [
                    {
                        'name': 'customer_name',
                        'example': 'João'
                    }
                ]
            },
            {
                'type': 'FOOTER',
                'text': 'Responda a esta mensagem para iniciar o atendimento.'
            }
        ],
        'created_at': '2025-05-10T09:00:00Z',
        'updated_at': '2025-05-10T09:00:00Z'
    },
    'template2': {
        'id': 'template2',
        'user_id': 'user1',
        'name': 'order_confirmation',
        'status': 'approved',
        'category': 'UTILITY',
        'language': 'pt_BR',
        'components': [
            {
                'type': 'HEADER',
                'format': 'TEXT',
                'text': 'Confirmação de Pedido #{{1}}'
            },
            {
                'type': 'BODY',
                'text': 'Olá {{2}}, seu pedido #{{1}} foi confirmado e está sendo processado. O valor total é de R$ {{3}}.\n\nEstimativa de entrega: {{4}}.\n\nObrigado pela preferência!',
                'variables': [
                    {
                        'name': 'order_number',
                        'example': '12345'
                    },
                    {
                        'name': 'customer_name',
                        'example': 'João'
                    },
                    {
                        'name': 'order_total',
                        'example': '150,00'
                    },
                    {
                        'name': 'delivery_date',
                        'example': '15/06/2025'
                    }
                ]
            },
            {
                'type': 'FOOTER',
                'text': 'Para mais informações, acesse nosso site.'
            }
        ],
        'created_at': '2025-05-15T11:30:00Z',
        'updated_at': '2025-05-15T11:30:00Z'
    }
}

@whatsapp_bp.route('/whatsapp/connections', methods=['GET'])
@jwt_required()
def get_connections():
    try:
        current_user = get_jwt_identity()
        
        # Listar todas as conexões
        connections_list = list(whatsapp_connections_db.values())
        
        # Ordenar por data de atualização (mais recente primeiro)
        connections_list.sort(key=lambda x: x['updated_at'], reverse=True)
        
        logger.info(f"Conexões WhatsApp listadas para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'connections': connections_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar conexões WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/connections/<connection_id>', methods=['GET'])
@jwt_required()
def get_connection(connection_id):
    try:
        current_user = get_jwt_identity()
        
        if connection_id not in whatsapp_connections_db:
            logger.warning(f"Tentativa de acesso a conexão WhatsApp inexistente: {connection_id}")
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        connection = whatsapp_connections_db[connection_id]
        
        logger.info(f"Conexão WhatsApp {connection_id} acessada por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'connection': connection
        })
    except Exception as e:
        logger.error(f"Erro ao acessar conexão WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/connections', methods=['POST'])
@jwt_required()
def create_connection():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'phone_number' not in data or 'name' not in data:
            return jsonify({'status': 'error', 'message': 'Número de telefone e nome são obrigatórios'}), 400
        
        # Validar dados
        phone_number = data.get('phone_number')
        name = data.get('name')
        
        if not phone_number or not name:
            return jsonify({'status': 'error', 'message': 'Número de telefone e nome são obrigatórios'}), 400
        
        # Verificar se o número já existe
        for connection in whatsapp_connections_db.values():
            if connection['phone_number'] == phone_number:
                logger.warning(f"Tentativa de criar conexão com número duplicado: {phone_number}")
                return jsonify({'status': 'error', 'message': 'Número de telefone já cadastrado'}), 409
        
        # Criar nova conexão
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        connection_id = str(uuid.uuid4())
        
        # Gerar QR code (simulação)
        qr_code = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=whatsapp-connection-{connection_id}"
        
        new_connection = {
            'id': connection_id,
            'user_id': 'user1',  # Em um sistema real, seria o ID do usuário atual
            'phone_number': phone_number,
            'name': name,
            'status': 'pending',
            'qr_code': qr_code,
            'business_profile': {
                'name': data.get('business_name', name),
                'description': data.get('business_description', ''),
                'address': data.get('business_address', ''),
                'email': data.get('business_email', ''),
                'website': data.get('business_website', ''),
                'category': data.get('business_category', 'Other')
            },
            'stats': {
                'messages_sent': 0,
                'messages_received': 0,
                'active_chats': 0
            },
            'created_at': now,
            'updated_at': now,
            'last_connected': None
        }
        
        # Adicionar ao "banco de dados"
        whatsapp_connections_db[connection_id] = new_connection
        
        logger.info(f"Nova conexão WhatsApp criada por {current_user}: {connection_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Conexão WhatsApp criada com sucesso',
            'connection': new_connection
        }), 201
    except Exception as e:
        logger.error(f"Erro ao criar conexão WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/connections/<connection_id>', methods=['PUT'])
@jwt_required()
def update_connection(connection_id):
    try:
        current_user = get_jwt_identity()
        
        if connection_id not in whatsapp_connections_db:
            logger.warning(f"Tentativa de atualização de conexão WhatsApp inexistente: {connection_id}")
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
        
        connection = whatsapp_connections_db[connection_id]
        
        # Atualizar campos permitidos
        if 'name' in data:
            connection['name'] = data['name']
        
        if 'business_profile' in data:
            business_profile = data['business_profile']
            
            if 'name' in business_profile:
                connection['business_profile']['name'] = business_profile['name']
            
            if 'description' in business_profile:
                connection['business_profile']['description'] = business_profile['description']
            
            if 'address' in business_profile:
                connection['business_profile']['address'] = business_profile['address']
            
            if 'email' in business_profile:
                connection['business_profile']['email'] = business_profile['email']
            
            if 'website' in business_profile:
                connection['business_profile']['website'] = business_profile['website']
            
            if 'category' in business_profile:
                connection['business_profile']['category'] = business_profile['category']
        
        # Atualizar timestamp
        connection['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Conexão WhatsApp {connection_id} atualizada por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Conexão WhatsApp atualizada com sucesso',
            'connection': connection
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar conexão WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/connections/<connection_id>', methods=['DELETE'])
@jwt_required()
def delete_connection(connection_id):
    try:
        current_user = get_jwt_identity()
        
        if connection_id not in whatsapp_connections_db:
            logger.warning(f"Tentativa de exclusão de conexão WhatsApp inexistente: {connection_id}")
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        # Remover do "banco de dados"
        deleted_connection = whatsapp_connections_db.pop(connection_id)
        
        logger.info(f"Conexão WhatsApp {connection_id} excluída por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Conexão WhatsApp excluída com sucesso',
            'connection': deleted_connection
        })
    except Exception as e:
        logger.error(f"Erro ao excluir conexão WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/connections/<connection_id>/reconnect', methods=['POST'])
@jwt_required()
def reconnect_connection(connection_id):
    try:
        current_user = get_jwt_identity()
        
        if connection_id not in whatsapp_connections_db:
            logger.warning(f"Tentativa de reconexão de conexão WhatsApp inexistente: {connection_id}")
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        connection = whatsapp_connections_db[connection_id]
        
        # Verificar se a conexão está desconectada
        if connection['status'] == 'connected':
            return jsonify({'status': 'error', 'message': 'Conexão já está ativa'}), 400
        
        # Gerar novo QR code (simulação)
        qr_code = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=whatsapp-reconnection-{connection_id}-{uuid.uuid4().hex}"
        
        # Atualizar status e QR code
        connection['status'] = 'pending'
        connection['qr_code'] = qr_code
        connection['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Reconexão de WhatsApp {connection_id} iniciada por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Reconexão iniciada. Escaneie o QR code para conectar.',
            'connection': connection
        })
    except Exception as e:
        logger.error(f"Erro ao iniciar reconexão de WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/connections/<connection_id>/disconnect', methods=['POST'])
@jwt_required()
def disconnect_connection(connection_id):
    try:
        current_user = get_jwt_identity()
        
        if connection_id not in whatsapp_connections_db:
            logger.warning(f"Tentativa de desconexão de conexão WhatsApp inexistente: {connection_id}")
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        connection = whatsapp_connections_db[connection_id]
        
        # Verificar se a conexão está conectada
        if connection['status'] != 'connected':
            return jsonify({'status': 'error', 'message': 'Conexão não está ativa'}), 400
        
        # Atualizar status
        connection['status'] = 'disconnected'
        connection['qr_code'] = None
        connection['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Conexão WhatsApp {connection_id} desconectada por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Conexão WhatsApp desconectada com sucesso',
            'connection': connection
        })
    except Exception as e:
        logger.error(f"Erro ao desconectar WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/connections/<connection_id>/verify', methods=['POST'])
@jwt_required()
def verify_connection(connection_id):
    try:
        current_user = get_jwt_identity()
        
        if connection_id not in whatsapp_connections_db:
            logger.warning(f"Tentativa de verificação de conexão WhatsApp inexistente: {connection_id}")
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        connection = whatsapp_connections_db[connection_id]
        
        # Simulação de verificação
        # Em um sistema real, verificaríamos o status da conexão com a API do WhatsApp
        
        # Atualizar status (simulação)
        if connection['status'] == 'pending':
            # Simular 80% de chance de sucesso
            if random.random() < 0.8:
                connection['status'] = 'connected'
                connection['qr_code'] = None
                connection['last_connected'] = datetime.datetime.utcnow().isoformat() + 'Z'
                message = 'Conexão WhatsApp verificada e ativa'
            else:
                message = 'Conexão ainda pendente. Escaneie o QR code para conectar.'
        elif connection['status'] == 'connected':
            message = 'Conexão WhatsApp já está ativa'
        else:
            message = 'Conexão WhatsApp está desconectada. Inicie uma reconexão.'
        
        connection['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Verificação de conexão WhatsApp {connection_id} por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': message,
            'connection': connection
        })
    except Exception as e:
        logger.error(f"Erro ao verificar conexão WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/chats', methods=['GET'])
@jwt_required()
def get_chats():
    try:
        current_user = get_jwt_identity()
        
        # Parâmetros de filtro
        connection_id = request.args.get('connection_id')
        status = request.args.get('status')
        assigned_to = request.args.get('assigned_to')
        tag = request.args.get('tag')
        
        # Filtrar chats
        filtered_chats = []
        for chat_id, chat in whatsapp_chats_db.items():
            # Filtrar por conexão
            if connection_id and chat['connection_id'] != connection_id:
                continue
            
            # Filtrar por status
            if status and chat['status'] != status:
                continue
            
            # Filtrar por atribuição
            if assigned_to:
                if assigned_to == 'unassigned' and chat['assigned_to'] is not None:
                    continue
                elif assigned_to != 'unassigned' and chat['assigned_to'] != assigned_to:
                    continue
            
            # Filtrar por tag
            if tag and tag not in chat['tags']:
                continue
            
            filtered_chats.append(chat)
        
        # Ordenar por data de atualização (mais recente primeiro)
        filtered_chats.sort(key=lambda x: x['updated_at'], reverse=True)
        
        logger.info(f"Chats WhatsApp listados para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'chats': filtered_chats
        })
    except Exception as e:
        logger.error(f"Erro ao listar chats WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/chats/<chat_id>', methods=['GET'])
@jwt_required()
def get_chat(chat_id):
    try:
        current_user = get_jwt_identity()
        
        if chat_id not in whatsapp_chats_db:
            logger.warning(f"Tentativa de acesso a chat WhatsApp inexistente: {chat_id}")
            return jsonify({'status': 'error', 'message': 'Chat WhatsApp não encontrado'}), 404
        
        chat = whatsapp_chats_db[chat_id]
        
        # Buscar mensagens do chat
        chat_messages = []
        for message_id, message in whatsapp_messages_db.items():
            if message['chat_id'] == chat_id:
                chat_messages.append(message)
        
        # Ordenar mensagens por timestamp
        chat_messages.sort(key=lambda x: x['timestamp'])
        
        logger.info(f"Chat WhatsApp {chat_id} acessado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'chat': chat,
            'messages': chat_messages
        })
    except Exception as e:
        logger.error(f"Erro ao acessar chat WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/chats/<chat_id>/assign', methods=['POST'])
@jwt_required()
def assign_chat(chat_id):
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if chat_id not in whatsapp_chats_db:
            logger.warning(f"Tentativa de atribuição de chat WhatsApp inexistente: {chat_id}")
            return jsonify({'status': 'error', 'message': 'Chat WhatsApp não encontrado'}), 404
        
        if not data or 'user_id' not in data:
            return jsonify({'status': 'error', 'message': 'ID do usuário é obrigatório'}), 400
        
        user_id = data.get('user_id')
        
        # Em um sistema real, verificaríamos se o usuário existe
        
        chat = whatsapp_chats_db[chat_id]
        
        # Atualizar atribuição
        chat['assigned_to'] = user_id
        chat['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        # Se o chat estava pendente, atualizar para ativo
        if chat['status'] == 'pending':
            chat['status'] = 'active'
        
        logger.info(f"Chat WhatsApp {chat_id} atribuído a {user_id} por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Chat atribuído com sucesso',
            'chat': chat
        })
    except Exception as e:
        logger.error(f"Erro ao atribuir chat WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/chats/<chat_id>/status', methods=['PUT'])
@jwt_required()
def update_chat_status(chat_id):
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if chat_id not in whatsapp_chats_db:
            logger.warning(f"Tentativa de atualização de status de chat WhatsApp inexistente: {chat_id}")
            return jsonify({'status': 'error', 'message': 'Chat WhatsApp não encontrado'}), 404
        
        if not data or 'status' not in data:
            return jsonify({'status': 'error', 'message': 'Status é obrigatório'}), 400
        
        status = data.get('status')
        
        # Validar status
        valid_statuses = ['active', 'archived', 'pending']
        if status not in valid_statuses:
            return jsonify({'status': 'error', 'message': 'Status inválido'}), 400
        
        chat = whatsapp_chats_db[chat_id]
        
        # Atualizar status
        chat['status'] = status
        chat['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Status do chat WhatsApp {chat_id} atualizado para {status} por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': f'Status do chat atualizado para {status}',
            'chat': chat
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar status do chat WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/chats/<chat_id>/tags', methods=['PUT'])
@jwt_required()
def update_chat_tags(chat_id):
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if chat_id not in whatsapp_chats_db:
            logger.warning(f"Tentativa de atualização de tags de chat WhatsApp inexistente: {chat_id}")
            return jsonify({'status': 'error', 'message': 'Chat WhatsApp não encontrado'}), 404
        
        if not data or 'tags' not in data:
            return jsonify({'status': 'error', 'message': 'Tags são obrigatórias'}), 400
        
        tags = data.get('tags')
        
        if not isinstance(tags, list):
            return jsonify({'status': 'error', 'message': 'Tags devem ser uma lista'}), 400
        
        chat = whatsapp_chats_db[chat_id]
        
        # Atualizar tags
        chat['tags'] = tags
        chat['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Tags do chat WhatsApp {chat_id} atualizadas por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Tags do chat atualizadas com sucesso',
            'chat': chat
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar tags do chat WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/messages', methods=['POST'])
@jwt_required()
def send_message():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'chat_id' not in data or 'content' not in data:
            return jsonify({'status': 'error', 'message': 'ID do chat e conteúdo são obrigatórios'}), 400
        
        chat_id = data.get('chat_id')
        content = data.get('content')
        message_type = data.get('type', 'text')
        media_url = data.get('media_url')
        
        if not content and not media_url:
            return jsonify({'status': 'error', 'message': 'Conteúdo ou mídia é obrigatório'}), 400
        
        if chat_id not in whatsapp_chats_db:
            logger.warning(f"Tentativa de envio de mensagem para chat WhatsApp inexistente: {chat_id}")
            return jsonify({'status': 'error', 'message': 'Chat WhatsApp não encontrado'}), 404
        
        chat = whatsapp_chats_db[chat_id]
        
        # Verificar se a conexão está ativa
        connection_id = chat['connection_id']
        if connection_id not in whatsapp_connections_db:
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        connection = whatsapp_connections_db[connection_id]
        
        if connection['status'] != 'connected':
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não está ativa'}), 400
        
        # Criar nova mensagem
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        message_id = str(uuid.uuid4())
        
        new_message = {
            'id': message_id,
            'connection_id': connection_id,
            'chat_id': chat_id,
            'contact_id': chat['contact_id'],
            'direction': 'outbound',
            'type': message_type,
            'content': content,
            'media_url': media_url,
            'status': 'sent',  # Em um sistema real, seria inicialmente 'sending'
            'timestamp': now,
            'metadata': {
                'agent_id': 'user1',  # Em um sistema real, seria o ID do usuário atual
                'automation_id': data.get('automation_id')
            }
        }
        
        # Adicionar ao "banco de dados"
        whatsapp_messages_db[message_id] = new_message
        
        # Atualizar chat
        chat['last_message'] = {
            'content': content[:100] + ('...' if len(content) > 100 else ''),
            'timestamp': now,
            'direction': 'outbound'
        }
        chat['updated_at'] = now
        
        # Atualizar estatísticas da conexão
        connection['stats']['messages_sent'] += 1
        
        logger.info(f"Mensagem WhatsApp enviada para chat {chat_id} por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Mensagem enviada com sucesso',
            'whatsapp_message': new_message
        }), 201
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/templates', methods=['GET'])
@jwt_required()
def get_templates():
    try:
        current_user = get_jwt_identity()
        
        # Listar todos os templates
        templates_list = list(whatsapp_templates_db.values())
        
        # Ordenar por nome
        templates_list.sort(key=lambda x: x['name'])
        
        logger.info(f"Templates WhatsApp listados para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'templates': templates_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar templates WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/templates/<template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    try:
        current_user = get_jwt_identity()
        
        if template_id not in whatsapp_templates_db:
            logger.warning(f"Tentativa de acesso a template WhatsApp inexistente: {template_id}")
            return jsonify({'status': 'error', 'message': 'Template WhatsApp não encontrado'}), 404
        
        template = whatsapp_templates_db[template_id]
        
        logger.info(f"Template WhatsApp {template_id} acessado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'template': template
        })
    except Exception as e:
        logger.error(f"Erro ao acessar template WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/templates', methods=['POST'])
@jwt_required()
def create_template():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'name' not in data or 'components' not in data or 'language' not in data or 'category' not in data:
            return jsonify({'status': 'error', 'message': 'Nome, componentes, idioma e categoria são obrigatórios'}), 400
        
        name = data.get('name')
        components = data.get('components')
        language = data.get('language')
        category = data.get('category')
        
        # Validar dados
        if not name or not components or not language or not category:
            return jsonify({'status': 'error', 'message': 'Nome, componentes, idioma e categoria são obrigatórios'}), 400
        
        if not isinstance(components, list) or len(components) == 0:
            return jsonify({'status': 'error', 'message': 'Componentes devem ser uma lista não vazia'}), 400
        
        # Validar categoria
        valid_categories = ['MARKETING', 'UTILITY', 'AUTHENTICATION']
        if category not in valid_categories:
            return jsonify({'status': 'error', 'message': f'Categoria inválida. Deve ser uma das seguintes: {", ".join(valid_categories)}'}), 400
        
        # Validar idioma
        valid_languages = ['pt_BR', 'en_US', 'es_ES']
        if language not in valid_languages:
            return jsonify({'status': 'error', 'message': f'Idioma inválido. Deve ser um dos seguintes: {", ".join(valid_languages)}'}), 400
        
        # Criar novo template
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        template_id = str(uuid.uuid4())
        
        new_template = {
            'id': template_id,
            'user_id': 'user1',  # Em um sistema real, seria o ID do usuário atual
            'name': name,
            'status': 'pending',
            'category': category,
            'language': language,
            'components': components,
            'created_at': now,
            'updated_at': now
        }
        
        # Adicionar ao "banco de dados"
        whatsapp_templates_db[template_id] = new_template
        
        logger.info(f"Novo template WhatsApp criado por {current_user}: {template_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Template WhatsApp criado com sucesso e enviado para aprovação',
            'template': new_template
        }), 201
    except Exception as e:
        logger.error(f"Erro ao criar template WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/templates/<template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    try:
        current_user = get_jwt_identity()
        
        if template_id not in whatsapp_templates_db:
            logger.warning(f"Tentativa de exclusão de template WhatsApp inexistente: {template_id}")
            return jsonify({'status': 'error', 'message': 'Template WhatsApp não encontrado'}), 404
        
        # Remover do "banco de dados"
        deleted_template = whatsapp_templates_db.pop(template_id)
        
        logger.info(f"Template WhatsApp {template_id} excluído por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Template WhatsApp excluído com sucesso',
            'template': deleted_template
        })
    except Exception as e:
        logger.error(f"Erro ao excluir template WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/templates/<template_id>/send', methods=['POST'])
@jwt_required()
def send_template_message(template_id):
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if template_id not in whatsapp_templates_db:
            logger.warning(f"Tentativa de envio de template WhatsApp inexistente: {template_id}")
            return jsonify({'status': 'error', 'message': 'Template WhatsApp não encontrado'}), 404
        
        if not data or 'connection_id' not in data or 'to' not in data:
            return jsonify({'status': 'error', 'message': 'ID da conexão e destinatário são obrigatórios'}), 400
        
        connection_id = data.get('connection_id')
        to = data.get('to')
        variables = data.get('variables', [])
        
        if connection_id not in whatsapp_connections_db:
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        
        connection = whatsapp_connections_db[connection_id]
        
        if connection['status'] != 'connected':
            return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não está ativa'}), 400
        
        template = whatsapp_templates_db[template_id]
        
        if template['status'] != 'approved':
            return jsonify({'status': 'error', 'message': 'Template não está aprovado para uso'}), 400
        
        # Em um sistema real, enviaríamos o template via API do WhatsApp
        # Para simulação, criamos uma mensagem fictícia
        
        # Verificar se o chat existe ou criar um novo
        chat_id = None
        for cid, chat in whatsapp_chats_db.items():
            if chat['connection_id'] == connection_id and chat['contact_phone'] == to:
                chat_id = cid
                break
        
        if not chat_id:
            # Criar novo chat
            chat_id = str(uuid.uuid4())
            contact_id = str(uuid.uuid4())
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            new_chat = {
                'id': chat_id,
                'connection_id': connection_id,
                'contact_id': contact_id,
                'contact_name': 'Novo Contato',  # Em um sistema real, buscaríamos o nome do contato
                'contact_phone': to,
                'unread_count': 0,
                'last_message': None,
                'status': 'active',
                'assigned_to': 'user1',  # Em um sistema real, seria o ID do usuário atual
                'tags': [],
                'created_at': now,
                'updated_at': now
            }
            
            whatsapp_chats_db[chat_id] = new_chat
        
        # Criar mensagem de template
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        message_id = str(uuid.uuid4())
        
        # Simular conteúdo do template com variáveis
        template_content = f"[Template: {template['name']}]"
        if len(template['components']) > 0:
            for component in template['components']:
                if component['type'] == 'BODY' and 'text' in component:
                    template_content = component['text']
                    break
        
        # Substituir variáveis
        for i, variable in enumerate(variables):
            placeholder = f"{{{{1}}}}" if i == 0 else f"{{{{i+1}}}}"
            template_content = template_content.replace(placeholder, variable)
        
        new_message = {
            'id': message_id,
            'connection_id': connection_id,
            'chat_id': chat_id,
            'contact_id': whatsapp_chats_db[chat_id]['contact_id'],
            'direction': 'outbound',
            'type': 'template',
            'content': template_content,
            'media_url': None,
            'status': 'sent',
            'timestamp': now,
            'metadata': {
                'agent_id': 'user1',  # Em um sistema real, seria o ID do usuário atual
                'template_id': template_id,
                'template_name': template['name'],
                'variables': variables
            }
        }
        
        # Adicionar ao "banco de dados"
        whatsapp_messages_db[message_id] = new_message
        
        # Atualizar chat
        chat = whatsapp_chats_db[chat_id]
        chat['last_message'] = {
            'content': template_content[:100] + ('...' if len(template_content) > 100 else ''),
            'timestamp': now,
            'direction': 'outbound'
        }
        chat['updated_at'] = now
        
        # Atualizar estatísticas da conexão
        connection['stats']['messages_sent'] += 1
        
        logger.info(f"Template WhatsApp {template_id} enviado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Template enviado com sucesso',
            'whatsapp_message': new_message
        }), 201
    except Exception as e:
        logger.error(f"Erro ao enviar template WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@whatsapp_bp.route('/whatsapp/stats', methods=['GET'])
@jwt_required()
def get_whatsapp_stats():
    try:
        current_user = get_jwt_identity()
        
        # Parâmetros de filtro
        connection_id = request.args.get('connection_id')
        period = request.args.get('period', 'today')  # today, week, month, year
        
        # Em um sistema real, buscaríamos estatísticas do banco de dados
        # Para simulação, calculamos com base nos dados existentes
        
        # Filtrar por conexão
        connections = []
        if connection_id:
            if connection_id in whatsapp_connections_db:
                connections = [whatsapp_connections_db[connection_id]]
            else:
                return jsonify({'status': 'error', 'message': 'Conexão WhatsApp não encontrada'}), 404
        else:
            connections = list(whatsapp_connections_db.values())
        
        # Calcular estatísticas
        total_messages_sent = sum(conn['stats']['messages_sent'] for conn in connections)
        total_messages_received = sum(conn['stats']['messages_received'] for conn in connections)
        total_active_chats = sum(conn['stats']['active_chats'] for conn in connections)
        
        # Calcular estatísticas por período (simulação)
        now = datetime.datetime.utcnow()
        
        if period == 'today':
            period_label = 'Hoje'
            period_factor = 0.1  # 10% das mensagens totais
        elif period == 'week':
            period_label = 'Esta semana'
            period_factor = 0.3  # 30% das mensagens totais
        elif period == 'month':
            period_label = 'Este mês'
            period_factor = 0.7  # 70% das mensagens totais
        else:  # year
            period_label = 'Este ano'
            period_factor = 1.0  # 100% das mensagens totais
        
        period_messages_sent = int(total_messages_sent * period_factor)
        period_messages_received = int(total_messages_received * period_factor)
        
        # Estatísticas de chats
        total_chats = len(whatsapp_chats_db)
        active_chats = sum(1 for chat in whatsapp_chats_db.values() if chat['status'] == 'active')
        archived_chats = sum(1 for chat in whatsapp_chats_db.values() if chat['status'] == 'archived')
        pending_chats = sum(1 for chat in whatsapp_chats_db.values() if chat['status'] == 'pending')
        
        # Estatísticas de templates
        total_templates = len(whatsapp_templates_db)
        approved_templates = sum(1 for template in whatsapp_templates_db.values() if template['status'] == 'approved')
        pending_templates = sum(1 for template in whatsapp_templates_db.values() if template['status'] == 'pending')
        rejected_templates = sum(1 for template in whatsapp_templates_db.values() if template['status'] == 'rejected')
        
        logger.info(f"Estatísticas WhatsApp acessadas por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'stats': {
                'connections': {
                    'total': len(connections),
                    'connected': sum(1 for conn in connections if conn['status'] == 'connected'),
                    'disconnected': sum(1 for conn in connections if conn['status'] == 'disconnected'),
                    'pending': sum(1 for conn in connections if conn['status'] == 'pending')
                },
                'messages': {
                    'total': total_messages_sent + total_messages_received,
                    'sent': total_messages_sent,
                    'received': total_messages_received,
                    'period': {
                        'label': period_label,
                        'sent': period_messages_sent,
                        'received': period_messages_received,
                        'total': period_messages_sent + period_messages_received
                    }
                },
                'chats': {
                    'total': total_chats,
                    'active': active_chats,
                    'archived': archived_chats,
                    'pending': pending_chats
                },
                'templates': {
                    'total': total_templates,
                    'approved': approved_templates,
                    'pending': pending_templates,
                    'rejected': rejected_templates
                }
            }
        })
    except Exception as e:
        logger.error(f"Erro ao acessar estatísticas WhatsApp: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500
