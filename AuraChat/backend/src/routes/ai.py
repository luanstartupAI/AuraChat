from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import uuid
import logging
import random

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__)

# Simulação de banco de dados de modelos de IA
ai_models_db = {
    'model1': {
        'id': 'model1',
        'name': 'Atendente Virtual',
        'description': 'Modelo de IA para atendimento automatizado de clientes',
        'type': 'chat',
        'status': 'active',
        'version': '1.0.0',
        'created_at': '2025-05-01T10:00:00Z',
        'updated_at': '2025-06-01T15:00:00Z',
        'stats': {
            'total_interactions': 1250,
            'successful_interactions': 1150,
            'average_response_time': 0.8  # segundos
        },
        'settings': {
            'temperature': 0.7,
            'max_tokens': 500,
            'top_p': 0.9,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        }
    },
    'model2': {
        'id': 'model2',
        'name': 'Classificador de Intenções',
        'description': 'Modelo de IA para classificação de intenções de mensagens',
        'type': 'classification',
        'status': 'active',
        'version': '1.0.0',
        'created_at': '2025-05-10T14:00:00Z',
        'updated_at': '2025-06-01T15:00:00Z',
        'stats': {
            'total_interactions': 3500,
            'successful_interactions': 3300,
            'average_response_time': 0.3  # segundos
        },
        'settings': {
            'confidence_threshold': 0.7,
            'max_categories': 3
        }
    },
    'model3': {
        'id': 'model3',
        'name': 'Gerador de Respostas',
        'description': 'Modelo de IA para geração de respostas personalizadas',
        'type': 'generation',
        'status': 'active',
        'version': '1.0.0',
        'created_at': '2025-05-15T09:00:00Z',
        'updated_at': '2025-06-01T15:00:00Z',
        'stats': {
            'total_interactions': 2200,
            'successful_interactions': 2100,
            'average_response_time': 1.2  # segundos
        },
        'settings': {
            'temperature': 0.8,
            'max_tokens': 1000,
            'top_p': 0.9,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        }
    }
}

# Simulação de banco de dados de assistentes de IA
ai_assistants_db = {
    'assistant1': {
        'id': 'assistant1',
        'name': 'Suporte Técnico',
        'description': 'Assistente de IA para suporte técnico',
        'model_id': 'model1',
        'status': 'active',
        'created_at': '2025-05-05T10:00:00Z',
        'updated_at': '2025-06-01T15:00:00Z',
        'settings': {
            'greeting': 'Olá! Sou o assistente de suporte técnico da Aura. Como posso ajudar?',
            'fallback_message': 'Desculpe, não entendi sua pergunta. Poderia reformular?',
            'handoff_message': 'Vou transferir você para um atendente humano.',
            'working_hours': {
                'enabled': True,
                'timezone': 'America/Sao_Paulo',
                'hours': [
                    {'day': 'monday', 'start': '08:00', 'end': '18:00'},
                    {'day': 'tuesday', 'start': '08:00', 'end': '18:00'},
                    {'day': 'wednesday', 'start': '08:00', 'end': '18:00'},
                    {'day': 'thursday', 'start': '08:00', 'end': '18:00'},
                    {'day': 'friday', 'start': '08:00', 'end': '18:00'}
                ]
            },
            'handoff_threshold': 0.7,
            'max_interactions': 5
        },
        'stats': {
            'total_interactions': 850,
            'successful_interactions': 780,
            'handoffs': 70,
            'average_interaction_time': 120  # segundos
        }
    },
    'assistant2': {
        'id': 'assistant2',
        'name': 'Vendas',
        'description': 'Assistente de IA para vendas e prospecção',
        'model_id': 'model1',
        'status': 'active',
        'created_at': '2025-05-10T14:00:00Z',
        'updated_at': '2025-06-01T15:00:00Z',
        'settings': {
            'greeting': 'Olá! Sou o assistente de vendas da Aura. Como posso ajudar você hoje?',
            'fallback_message': 'Desculpe, não entendi sua pergunta. Poderia reformular?',
            'handoff_message': 'Vou transferir você para um consultor de vendas.',
            'working_hours': {
                'enabled': True,
                'timezone': 'America/Sao_Paulo',
                'hours': [
                    {'day': 'monday', 'start': '09:00', 'end': '19:00'},
                    {'day': 'tuesday', 'start': '09:00', 'end': '19:00'},
                    {'day': 'wednesday', 'start': '09:00', 'end': '19:00'},
                    {'day': 'thursday', 'start': '09:00', 'end': '19:00'},
                    {'day': 'friday', 'start': '09:00', 'end': '19:00'},
                    {'day': 'saturday', 'start': '10:00', 'end': '15:00'}
                ]
            },
            'handoff_threshold': 0.8,
            'max_interactions': 10
        },
        'stats': {
            'total_interactions': 1200,
            'successful_interactions': 1050,
            'handoffs': 150,
            'average_interaction_time': 180  # segundos
        }
    }
}

# Simulação de banco de dados de conhecimento para IA
ai_knowledge_db = {
    'knowledge1': {
        'id': 'knowledge1',
        'name': 'FAQ Produtos',
        'description': 'Perguntas frequentes sobre produtos',
        'type': 'faq',
        'status': 'active',
        'created_at': '2025-05-01T10:00:00Z',
        'updated_at': '2025-06-01T15:00:00Z',
        'items': [
            {
                'question': 'Quais são os planos disponíveis?',
                'answer': 'Oferecemos três planos: Básico (R$49,90/mês), Premium (R$99,90/mês) e Enterprise (R$249,90/mês). Cada um com diferentes recursos e limites.'
            },
            {
                'question': 'Como funciona o período de teste?',
                'answer': 'Oferecemos um período de teste gratuito de 14 dias para todos os planos. Não é necessário cartão de crédito para iniciar o teste.'
            },
            {
                'question': 'Posso mudar de plano depois?',
                'answer': 'Sim, você pode fazer upgrade ou downgrade do seu plano a qualquer momento. As mudanças entram em vigor imediatamente, com ajuste proporcional na cobrança.'
            }
        ]
    },
    'knowledge2': {
        'id': 'knowledge2',
        'name': 'Suporte Técnico',
        'description': 'Base de conhecimento para suporte técnico',
        'type': 'technical',
        'status': 'active',
        'created_at': '2025-05-10T14:00:00Z',
        'updated_at': '2025-06-01T15:00:00Z',
        'items': [
            {
                'question': 'Como conectar meu WhatsApp?',
                'answer': 'Para conectar seu WhatsApp, acesse a seção "WhatsApp" no painel, clique em "Adicionar Conexão", informe o número e escaneie o QR code com seu celular.'
            },
            {
                'question': 'O que fazer se a conexão cair?',
                'answer': 'Se a conexão do WhatsApp cair, acesse a seção "WhatsApp", encontre a conexão com problema e clique em "Reconectar". Um novo QR code será gerado para escaneamento.'
            },
            {
                'question': 'Como criar um fluxo de automação?',
                'answer': 'Para criar um fluxo de automação, acesse a seção "Automação", clique em "Novo Fluxo", defina um nome e comece a adicionar os blocos de ação arrastando-os para o editor.'
            }
        ]
    }
}

# Simulação de banco de dados de interações de IA
ai_interactions_db = {
    'interaction1': {
        'id': 'interaction1',
        'assistant_id': 'assistant1',
        'chat_id': 'chat1',
        'contact_id': 'contact1',
        'status': 'completed',
        'started_at': '2025-06-01T14:30:00Z',
        'ended_at': '2025-06-01T14:35:00Z',
        'messages': [
            {
                'role': 'user',
                'content': 'Olá, estou com problemas para conectar meu WhatsApp',
                'timestamp': '2025-06-01T14:30:00Z'
            },
            {
                'role': 'assistant',
                'content': 'Olá! Sou o assistente de suporte técnico da Aura. Lamento pelo inconveniente com a conexão do WhatsApp. Para conectar, você precisa acessar a seção "WhatsApp" no painel, clicar em "Adicionar Conexão", informar o número e escanear o QR code com seu celular. Você já tentou esse processo?',
                'timestamp': '2025-06-01T14:30:05Z'
            },
            {
                'role': 'user',
                'content': 'Sim, mas o QR code não aparece',
                'timestamp': '2025-06-01T14:31:00Z'
            },
            {
                'role': 'assistant',
                'content': 'Entendo. Esse problema pode ocorrer por algumas razões. Vamos tentar algumas soluções:\n\n1. Atualize a página do navegador\n2. Verifique se você está usando um navegador compatível (Chrome, Firefox, Edge)\n3. Limpe o cache do navegador\n\nSe o problema persistir, pode ser uma questão temporária com nossos servidores. Você gostaria de tentar essas soluções ou prefere que eu transfira para um atendente humano?',
                'timestamp': '2025-06-01T14:31:10Z'
            },
            {
                'role': 'user',
                'content': 'Vou tentar atualizar a página',
                'timestamp': '2025-06-01T14:32:00Z'
            },
            {
                'role': 'assistant',
                'content': 'Ótimo! Por favor, me informe se a atualização da página resolver o problema do QR code. Estou aqui para ajudar caso precise de mais assistência.',
                'timestamp': '2025-06-01T14:32:05Z'
            },
            {
                'role': 'user',
                'content': 'Funcionou! Obrigado pela ajuda',
                'timestamp': '2025-06-01T14:34:00Z'
            },
            {
                'role': 'assistant',
                'content': 'Excelente! Fico feliz em saber que a atualização da página resolveu o problema. Se precisar de mais ajuda com o WhatsApp ou qualquer outro recurso da Aura, é só me perguntar. Tenha um ótimo dia!',
                'timestamp': '2025-06-01T14:34:05Z'
            }
        ],
        'metrics': {
            'total_messages': 8,
            'average_response_time': 0.9,  # segundos
            'sentiment': 'positive',
            'resolution': 'solved'
        }
    },
    'interaction2': {
        'id': 'interaction2',
        'assistant_id': 'assistant2',
        'chat_id': 'chat2',
        'contact_id': 'contact2',
        'status': 'handoff',
        'started_at': '2025-06-02T10:15:00Z',
        'ended_at': '2025-06-02T10:20:00Z',
        'messages': [
            {
                'role': 'user',
                'content': 'Quero saber mais sobre os planos de assinatura',
                'timestamp': '2025-06-02T10:15:00Z'
            },
            {
                'role': 'assistant',
                'content': 'Olá! Sou o assistente de vendas da Aura. Ficarei feliz em fornecer informações sobre nossos planos de assinatura. Oferecemos três planos:\n\n1. Básico (R$49,90/mês): Ideal para pequenas empresas e profissionais autônomos. Inclui 1 número de WhatsApp, até 500 contatos e 3 usuários.\n\n2. Premium (R$99,90/mês): Para empresas em crescimento. Inclui 3 números de WhatsApp, até 2.000 contatos e 10 usuários.\n\n3. Enterprise (R$249,90/mês): Para grandes empresas. Inclui números de WhatsApp, contatos e usuários ilimitados.\n\nTodos os planos incluem suporte e atualizações. Qual deles mais se adequa às suas necessidades?',
                'timestamp': '2025-06-02T10:15:10Z'
            },
            {
                'role': 'user',
                'content': 'O Premium parece interessante. Vocês oferecem desconto para pagamento anual?',
                'timestamp': '2025-06-02T10:16:00Z'
            },
            {
                'role': 'assistant',
                'content': 'Sim, oferecemos desconto para pagamento anual! No plano Premium, o valor mensal seria R$99,90, totalizando R$1.198,80 por ano. Com o pagamento anual, oferecemos o valor de R$1.079,00, o que representa aproximadamente 10% de desconto. Além da economia, o pagamento anual também traz a vantagem de manter o preço fixo durante todo o período, mesmo que ocorram reajustes. Gostaria de saber mais detalhes sobre o plano Premium ou sobre as formas de pagamento?',
                'timestamp': '2025-06-02T10:16:15Z'
            },
            {
                'role': 'user',
                'content': 'Quero falar com um consultor para negociar um desconto maior para minha empresa',
                'timestamp': '2025-06-02T10:17:00Z'
            },
            {
                'role': 'assistant',
                'content': 'Entendo perfeitamente! Para negociações personalizadas, é melhor falar diretamente com um de nossos consultores de vendas. Vou transferir você agora mesmo. Um consultor especializado entrará em contato em breve para discutir condições especiais para sua empresa. Obrigado pelo interesse na Aura!',
                'timestamp': '2025-06-02T10:17:10Z',
                'metadata': {
                    'handoff_reason': 'customer_request',
                    'assigned_to': 'user2'
                }
            }
        ],
        'metrics': {
            'total_messages': 6,
            'average_response_time': 1.1,  # segundos
            'sentiment': 'positive',
            'resolution': 'handoff'
        }
    }
}

@ai_bp.route('/ai/models', methods=['GET'])
@jwt_required()
def get_models():
    try:
        current_user = get_jwt_identity()
        
        # Listar todos os modelos
        models_list = list(ai_models_db.values())
        
        # Ordenar por nome
        models_list.sort(key=lambda x: x['name'])
        
        logger.info(f"Modelos de IA listados para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'models': models_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar modelos de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/models/<model_id>', methods=['GET'])
@jwt_required()
def get_model(model_id):
    try:
        current_user = get_jwt_identity()
        
        if model_id not in ai_models_db:
            logger.warning(f"Tentativa de acesso a modelo de IA inexistente: {model_id}")
            return jsonify({'status': 'error', 'message': 'Modelo de IA não encontrado'}), 404
        
        model = ai_models_db[model_id]
        
        logger.info(f"Modelo de IA {model_id} acessado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'model': model
        })
    except Exception as e:
        logger.error(f"Erro ao acessar modelo de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/assistants', methods=['GET'])
@jwt_required()
def get_assistants():
    try:
        current_user = get_jwt_identity()
        
        # Listar todos os assistentes
        assistants_list = list(ai_assistants_db.values())
        
        # Ordenar por nome
        assistants_list.sort(key=lambda x: x['name'])
        
        logger.info(f"Assistentes de IA listados para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'assistants': assistants_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar assistentes de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/assistants/<assistant_id>', methods=['GET'])
@jwt_required()
def get_assistant(assistant_id):
    try:
        current_user = get_jwt_identity()
        
        if assistant_id not in ai_assistants_db:
            logger.warning(f"Tentativa de acesso a assistente de IA inexistente: {assistant_id}")
            return jsonify({'status': 'error', 'message': 'Assistente de IA não encontrado'}), 404
        
        assistant = ai_assistants_db[assistant_id]
        
        logger.info(f"Assistente de IA {assistant_id} acessado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'assistant': assistant
        })
    except Exception as e:
        logger.error(f"Erro ao acessar assistente de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/assistants', methods=['POST'])
@jwt_required()
def create_assistant():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'name' not in data or 'model_id' not in data:
            return jsonify({'status': 'error', 'message': 'Nome e ID do modelo são obrigatórios'}), 400
        
        name = data.get('name')
        model_id = data.get('model_id')
        description = data.get('description', '')
        
        # Validar modelo
        if model_id not in ai_models_db:
            return jsonify({'status': 'error', 'message': 'Modelo de IA não encontrado'}), 404
        
        # Criar novo assistente
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        assistant_id = str(uuid.uuid4())
        
        new_assistant = {
            'id': assistant_id,
            'name': name,
            'description': description,
            'model_id': model_id,
            'status': 'active',
            'created_at': now,
            'updated_at': now,
            'settings': {
                'greeting': data.get('greeting', 'Olá! Como posso ajudar?'),
                'fallback_message': data.get('fallback_message', 'Desculpe, não entendi sua pergunta. Poderia reformular?'),
                'handoff_message': data.get('handoff_message', 'Vou transferir você para um atendente humano.'),
                'working_hours': data.get('working_hours', {
                    'enabled': False,
                    'timezone': 'America/Sao_Paulo',
                    'hours': []
                }),
                'handoff_threshold': data.get('handoff_threshold', 0.7),
                'max_interactions': data.get('max_interactions', 5)
            },
            'stats': {
                'total_interactions': 0,
                'successful_interactions': 0,
                'handoffs': 0,
                'average_interaction_time': 0
            }
        }
        
        # Adicionar ao "banco de dados"
        ai_assistants_db[assistant_id] = new_assistant
        
        logger.info(f"Novo assistente de IA criado por {current_user}: {assistant_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Assistente de IA criado com sucesso',
            'assistant': new_assistant
        }), 201
    except Exception as e:
        logger.error(f"Erro ao criar assistente de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/assistants/<assistant_id>', methods=['PUT'])
@jwt_required()
def update_assistant(assistant_id):
    try:
        current_user = get_jwt_identity()
        
        if assistant_id not in ai_assistants_db:
            logger.warning(f"Tentativa de atualização de assistente de IA inexistente: {assistant_id}")
            return jsonify({'status': 'error', 'message': 'Assistente de IA não encontrado'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
        
        assistant = ai_assistants_db[assistant_id]
        
        # Atualizar campos permitidos
        if 'name' in data:
            assistant['name'] = data['name']
        
        if 'description' in data:
            assistant['description'] = data['description']
        
        if 'model_id' in data:
            model_id = data['model_id']
            if model_id not in ai_models_db:
                return jsonify({'status': 'error', 'message': 'Modelo de IA não encontrado'}), 404
            assistant['model_id'] = model_id
        
        if 'status' in data:
            status = data['status']
            if status not in ['active', 'inactive']:
                return jsonify({'status': 'error', 'message': 'Status inválido'}), 400
            assistant['status'] = status
        
        if 'settings' in data:
            settings = data['settings']
            
            if 'greeting' in settings:
                assistant['settings']['greeting'] = settings['greeting']
            
            if 'fallback_message' in settings:
                assistant['settings']['fallback_message'] = settings['fallback_message']
            
            if 'handoff_message' in settings:
                assistant['settings']['handoff_message'] = settings['handoff_message']
            
            if 'working_hours' in settings:
                assistant['settings']['working_hours'] = settings['working_hours']
            
            if 'handoff_threshold' in settings:
                assistant['settings']['handoff_threshold'] = settings['handoff_threshold']
            
            if 'max_interactions' in settings:
                assistant['settings']['max_interactions'] = settings['max_interactions']
        
        # Atualizar timestamp
        assistant['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Assistente de IA {assistant_id} atualizado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Assistente de IA atualizado com sucesso',
            'assistant': assistant
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar assistente de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/assistants/<assistant_id>', methods=['DELETE'])
@jwt_required()
def delete_assistant(assistant_id):
    try:
        current_user = get_jwt_identity()
        
        if assistant_id not in ai_assistants_db:
            logger.warning(f"Tentativa de exclusão de assistente de IA inexistente: {assistant_id}")
            return jsonify({'status': 'error', 'message': 'Assistente de IA não encontrado'}), 404
        
        # Remover do "banco de dados"
        deleted_assistant = ai_assistants_db.pop(assistant_id)
        
        logger.info(f"Assistente de IA {assistant_id} excluído por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Assistente de IA excluído com sucesso',
            'assistant': deleted_assistant
        })
    except Exception as e:
        logger.error(f"Erro ao excluir assistente de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/knowledge', methods=['GET'])
@jwt_required()
def get_knowledge_bases():
    try:
        current_user = get_jwt_identity()
        
        # Listar todas as bases de conhecimento
        knowledge_list = list(ai_knowledge_db.values())
        
        # Ordenar por nome
        knowledge_list.sort(key=lambda x: x['name'])
        
        logger.info(f"Bases de conhecimento listadas para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'knowledge_bases': knowledge_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar bases de conhecimento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/knowledge/<knowledge_id>', methods=['GET'])
@jwt_required()
def get_knowledge_base(knowledge_id):
    try:
        current_user = get_jwt_identity()
        
        if knowledge_id not in ai_knowledge_db:
            logger.warning(f"Tentativa de acesso a base de conhecimento inexistente: {knowledge_id}")
            return jsonify({'status': 'error', 'message': 'Base de conhecimento não encontrada'}), 404
        
        knowledge = ai_knowledge_db[knowledge_id]
        
        logger.info(f"Base de conhecimento {knowledge_id} acessada por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'knowledge_base': knowledge
        })
    except Exception as e:
        logger.error(f"Erro ao acessar base de conhecimento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/knowledge', methods=['POST'])
@jwt_required()
def create_knowledge_base():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'name' not in data or 'type' not in data:
            return jsonify({'status': 'error', 'message': 'Nome e tipo são obrigatórios'}), 400
        
        name = data.get('name')
        knowledge_type = data.get('type')
        description = data.get('description', '')
        items = data.get('items', [])
        
        # Validar tipo
        valid_types = ['faq', 'technical', 'product', 'policy']
        if knowledge_type not in valid_types:
            return jsonify({'status': 'error', 'message': f'Tipo inválido. Deve ser um dos seguintes: {", ".join(valid_types)}'}), 400
        
        # Criar nova base de conhecimento
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        knowledge_id = str(uuid.uuid4())
        
        new_knowledge = {
            'id': knowledge_id,
            'name': name,
            'description': description,
            'type': knowledge_type,
            'status': 'active',
            'created_at': now,
            'updated_at': now,
            'items': items
        }
        
        # Adicionar ao "banco de dados"
        ai_knowledge_db[knowledge_id] = new_knowledge
        
        logger.info(f"Nova base de conhecimento criada por {current_user}: {knowledge_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Base de conhecimento criada com sucesso',
            'knowledge_base': new_knowledge
        }), 201
    except Exception as e:
        logger.error(f"Erro ao criar base de conhecimento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/knowledge/<knowledge_id>', methods=['PUT'])
@jwt_required()
def update_knowledge_base(knowledge_id):
    try:
        current_user = get_jwt_identity()
        
        if knowledge_id not in ai_knowledge_db:
            logger.warning(f"Tentativa de atualização de base de conhecimento inexistente: {knowledge_id}")
            return jsonify({'status': 'error', 'message': 'Base de conhecimento não encontrada'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
        
        knowledge = ai_knowledge_db[knowledge_id]
        
        # Atualizar campos permitidos
        if 'name' in data:
            knowledge['name'] = data['name']
        
        if 'description' in data:
            knowledge['description'] = data['description']
        
        if 'type' in data:
            knowledge_type = data['type']
            valid_types = ['faq', 'technical', 'product', 'policy']
            if knowledge_type not in valid_types:
                return jsonify({'status': 'error', 'message': f'Tipo inválido. Deve ser um dos seguintes: {", ".join(valid_types)}'}), 400
            knowledge['type'] = knowledge_type
        
        if 'status' in data:
            status = data['status']
            if status not in ['active', 'inactive']:
                return jsonify({'status': 'error', 'message': 'Status inválido'}), 400
            knowledge['status'] = status
        
        if 'items' in data:
            knowledge['items'] = data['items']
        
        # Atualizar timestamp
        knowledge['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Base de conhecimento {knowledge_id} atualizada por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Base de conhecimento atualizada com sucesso',
            'knowledge_base': knowledge
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar base de conhecimento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/knowledge/<knowledge_id>', methods=['DELETE'])
@jwt_required()
def delete_knowledge_base(knowledge_id):
    try:
        current_user = get_jwt_identity()
        
        if knowledge_id not in ai_knowledge_db:
            logger.warning(f"Tentativa de exclusão de base de conhecimento inexistente: {knowledge_id}")
            return jsonify({'status': 'error', 'message': 'Base de conhecimento não encontrada'}), 404
        
        # Remover do "banco de dados"
        deleted_knowledge = ai_knowledge_db.pop(knowledge_id)
        
        logger.info(f"Base de conhecimento {knowledge_id} excluída por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Base de conhecimento excluída com sucesso',
            'knowledge_base': deleted_knowledge
        })
    except Exception as e:
        logger.error(f"Erro ao excluir base de conhecimento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/knowledge/<knowledge_id>/items', methods=['POST'])
@jwt_required()
def add_knowledge_item(knowledge_id):
    try:
        current_user = get_jwt_identity()
        
        if knowledge_id not in ai_knowledge_db:
            logger.warning(f"Tentativa de adição de item a base de conhecimento inexistente: {knowledge_id}")
            return jsonify({'status': 'error', 'message': 'Base de conhecimento não encontrada'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
        
        knowledge = ai_knowledge_db[knowledge_id]
        
        # Validar dados conforme o tipo da base de conhecimento
        if knowledge['type'] == 'faq':
            if 'question' not in data or 'answer' not in data:
                return jsonify({'status': 'error', 'message': 'Pergunta e resposta são obrigatórias para o tipo FAQ'}), 400
        else:
            if 'question' not in data or 'answer' not in data:
                return jsonify({'status': 'error', 'message': 'Pergunta e resposta são obrigatórias'}), 400
        
        # Adicionar item
        knowledge['items'].append(data)
        
        # Atualizar timestamp
        knowledge['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Item adicionado à base de conhecimento {knowledge_id} por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Item adicionado com sucesso',
            'knowledge_base': knowledge
        })
    except Exception as e:
        logger.error(f"Erro ao adicionar item à base de conhecimento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/interactions', methods=['GET'])
@jwt_required()
def get_interactions():
    try:
        current_user = get_jwt_identity()
        
        # Parâmetros de filtro
        assistant_id = request.args.get('assistant_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Filtrar interações
        filtered_interactions = []
        for interaction_id, interaction in ai_interactions_db.items():
            # Filtrar por assistente
            if assistant_id and interaction['assistant_id'] != assistant_id:
                continue
            
            # Filtrar por status
            if status and interaction['status'] != status:
                continue
            
            # Filtrar por data de início
            if start_date:
                interaction_date = datetime.datetime.fromisoformat(interaction['started_at'].replace('Z', '+00:00'))
                filter_date = datetime.datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                if interaction_date < filter_date:
                    continue
            
            # Filtrar por data de fim
            if end_date:
                interaction_date = datetime.datetime.fromisoformat(interaction['started_at'].replace('Z', '+00:00'))
                filter_date = datetime.datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                if interaction_date > filter_date:
                    continue
            
            filtered_interactions.append(interaction)
        
        # Ordenar por data de início (mais recente primeiro)
        filtered_interactions.sort(key=lambda x: x['started_at'], reverse=True)
        
        logger.info(f"Interações de IA listadas para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'interactions': filtered_interactions
        })
    except Exception as e:
        logger.error(f"Erro ao listar interações de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/interactions/<interaction_id>', methods=['GET'])
@jwt_required()
def get_interaction(interaction_id):
    try:
        current_user = get_jwt_identity()
        
        if interaction_id not in ai_interactions_db:
            logger.warning(f"Tentativa de acesso a interação de IA inexistente: {interaction_id}")
            return jsonify({'status': 'error', 'message': 'Interação de IA não encontrada'}), 404
        
        interaction = ai_interactions_db[interaction_id]
        
        logger.info(f"Interação de IA {interaction_id} acessada por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'interaction': interaction
        })
    except Exception as e:
        logger.error(f"Erro ao acessar interação de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/chat', methods=['POST'])
@jwt_required()
def chat_with_ai():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'assistant_id' not in data or 'message' not in data:
            return jsonify({'status': 'error', 'message': 'ID do assistente e mensagem são obrigatórios'}), 400
        
        assistant_id = data.get('assistant_id')
        message = data.get('message')
        chat_id = data.get('chat_id')
        interaction_id = data.get('interaction_id')
        
        if assistant_id not in ai_assistants_db:
            return jsonify({'status': 'error', 'message': 'Assistente de IA não encontrado'}), 404
        
        assistant = ai_assistants_db[assistant_id]
        
        if assistant['status'] != 'active':
            return jsonify({'status': 'error', 'message': 'Assistente de IA não está ativo'}), 400
        
        # Verificar se é uma nova interação ou continuação
        if not interaction_id:
            # Nova interação
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            interaction_id = str(uuid.uuid4())
            
            new_interaction = {
                'id': interaction_id,
                'assistant_id': assistant_id,
                'chat_id': chat_id,
                'contact_id': data.get('contact_id'),
                'status': 'in_progress',
                'started_at': now,
                'ended_at': None,
                'messages': [
                    {
                        'role': 'user',
                        'content': message,
                        'timestamp': now
                    }
                ],
                'metrics': {
                    'total_messages': 1,
                    'average_response_time': 0,
                    'sentiment': 'neutral',
                    'resolution': 'pending'
                }
            }
            
            ai_interactions_db[interaction_id] = new_interaction
            
            # Simular resposta do assistente
            response_time = random.uniform(0.5, 1.5)  # segundos
            response_timestamp = (datetime.datetime.fromisoformat(now.replace('Z', '+00:00')) + 
                                 datetime.timedelta(seconds=response_time)).isoformat() + 'Z'
            
            # Gerar resposta com base no tipo de assistente
            if assistant['name'] == 'Suporte Técnico':
                # Buscar na base de conhecimento de suporte técnico
                knowledge = ai_knowledge_db.get('knowledge2', {'items': []})
                
                # Simular busca de resposta
                response_content = assistant['settings']['greeting']
                
                for item in knowledge['items']:
                    if any(keyword in message.lower() for keyword in item['question'].lower().split()):
                        response_content = item['answer']
                        break
            else:
                # Assistente de vendas ou outro tipo
                response_content = assistant['settings']['greeting']
                
                # Buscar na base de conhecimento de FAQ
                knowledge = ai_knowledge_db.get('knowledge1', {'items': []})
                
                for item in knowledge['items']:
                    if any(keyword in message.lower() for keyword in item['question'].lower().split()):
                        response_content = item['answer']
                        break
            
            # Adicionar resposta do assistente
            new_interaction['messages'].append({
                'role': 'assistant',
                'content': response_content,
                'timestamp': response_timestamp
            })
            
            # Atualizar métricas
            new_interaction['metrics']['total_messages'] = 2
            new_interaction['metrics']['average_response_time'] = response_time
            
            logger.info(f"Nova interação de IA iniciada por {current_user}: {interaction_id}")
            
            return jsonify({
                'status': 'success',
                'message': 'Mensagem enviada com sucesso',
                'interaction': new_interaction
            })
        else:
            # Continuação de interação existente
            if interaction_id not in ai_interactions_db:
                return jsonify({'status': 'error', 'message': 'Interação de IA não encontrada'}), 404
            
            interaction = ai_interactions_db[interaction_id]
            
            if interaction['status'] != 'in_progress':
                return jsonify({'status': 'error', 'message': 'Interação de IA já foi finalizada'}), 400
            
            # Adicionar mensagem do usuário
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            interaction['messages'].append({
                'role': 'user',
                'content': message,
                'timestamp': now
            })
            
            # Verificar se deve fazer handoff
            handoff_threshold = assistant['settings']['handoff_threshold']
            max_interactions = assistant['settings']['max_interactions']
            
            user_messages_count = sum(1 for msg in interaction['messages'] if msg['role'] == 'user')
            
            if user_messages_count >= max_interactions or 'handoff' in message.lower():
                # Fazer handoff
                handoff_message = assistant['settings']['handoff_message']
                
                # Adicionar mensagem de handoff
                response_time = random.uniform(0.5, 1.5)  # segundos
                response_timestamp = (datetime.datetime.fromisoformat(now.replace('Z', '+00:00')) + 
                                     datetime.timedelta(seconds=response_time)).isoformat() + 'Z'
                
                interaction['messages'].append({
                    'role': 'assistant',
                    'content': handoff_message,
                    'timestamp': response_timestamp,
                    'metadata': {
                        'handoff_reason': 'max_interactions' if user_messages_count >= max_interactions else 'customer_request',
                        'assigned_to': None
                    }
                })
                
                # Atualizar status e métricas
                interaction['status'] = 'handoff'
                interaction['ended_at'] = response_timestamp
                interaction['metrics']['total_messages'] = len(interaction['messages'])
                interaction['metrics']['average_response_time'] = response_time
                interaction['metrics']['resolution'] = 'handoff'
                
                # Atualizar estatísticas do assistente
                assistant['stats']['total_interactions'] += 1
                assistant['stats']['handoffs'] += 1
                
                logger.info(f"Handoff de interação de IA {interaction_id} por: {current_user}")
                
                return jsonify({
                    'status': 'success',
                    'message': 'Handoff realizado com sucesso',
                    'interaction': interaction
                })
            else:
                # Continuar interação
                # Simular resposta do assistente
                response_time = random.uniform(0.5, 1.5)  # segundos
                response_timestamp = (datetime.datetime.fromisoformat(now.replace('Z', '+00:00')) + 
                                     datetime.timedelta(seconds=response_time)).isoformat() + 'Z'
                
                # Gerar resposta com base no tipo de assistente e mensagem
                if 'obrigado' in message.lower() or 'valeu' in message.lower() or 'agradeço' in message.lower():
                    response_content = "De nada! Fico feliz em poder ajudar. Há mais alguma coisa em que eu possa auxiliar?"
                elif 'não' in message.lower() and len(message) < 10:
                    response_content = "Tudo bem! Se precisar de mais alguma coisa, é só me chamar. Tenha um ótimo dia!"
                    
                    # Finalizar interação
                    interaction['status'] = 'completed'
                    interaction['ended_at'] = response_timestamp
                    interaction['metrics']['resolution'] = 'solved'
                    
                    # Atualizar estatísticas do assistente
                    assistant['stats']['total_interactions'] += 1
                    assistant['stats']['successful_interactions'] += 1
                else:
                    # Buscar resposta nas bases de conhecimento
                    found_answer = False
                    
                    for knowledge_id, knowledge in ai_knowledge_db.items():
                        for item in knowledge['items']:
                            if any(keyword in message.lower() for keyword in item['question'].lower().split()):
                                response_content = item['answer']
                                found_answer = True
                                break
                        
                        if found_answer:
                            break
                    
                    if not found_answer:
                        # Resposta genérica
                        response_content = assistant['settings']['fallback_message']
                
                # Adicionar resposta do assistente
                interaction['messages'].append({
                    'role': 'assistant',
                    'content': response_content,
                    'timestamp': response_timestamp
                })
                
                # Atualizar métricas
                interaction['metrics']['total_messages'] = len(interaction['messages'])
                
                # Calcular tempo médio de resposta
                response_times = []
                for i in range(1, len(interaction['messages']), 2):
                    if i < len(interaction['messages']):
                        user_time = datetime.datetime.fromisoformat(interaction['messages'][i-1]['timestamp'].replace('Z', '+00:00'))
                        assistant_time = datetime.datetime.fromisoformat(interaction['messages'][i]['timestamp'].replace('Z', '+00:00'))
                        response_times.append((assistant_time - user_time).total_seconds())
                
                if response_times:
                    interaction['metrics']['average_response_time'] = sum(response_times) / len(response_times)
                
                logger.info(f"Mensagem enviada para interação de IA {interaction_id} por: {current_user}")
                
                return jsonify({
                    'status': 'success',
                    'message': 'Mensagem enviada com sucesso',
                    'interaction': interaction
                })
    except Exception as e:
        logger.error(f"Erro ao interagir com IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/interactions/<interaction_id>/handoff', methods=['POST'])
@jwt_required()
def handoff_interaction(interaction_id):
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if interaction_id not in ai_interactions_db:
            logger.warning(f"Tentativa de handoff de interação de IA inexistente: {interaction_id}")
            return jsonify({'status': 'error', 'message': 'Interação de IA não encontrada'}), 404
        
        interaction = ai_interactions_db[interaction_id]
        
        if interaction['status'] != 'in_progress':
            return jsonify({'status': 'error', 'message': 'Interação de IA já foi finalizada'}), 400
        
        # Obter assistente
        assistant_id = interaction['assistant_id']
        if assistant_id not in ai_assistants_db:
            return jsonify({'status': 'error', 'message': 'Assistente de IA não encontrado'}), 404
        
        assistant = ai_assistants_db[assistant_id]
        
        # Adicionar mensagem de handoff
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        handoff_message = assistant['settings']['handoff_message']
        
        interaction['messages'].append({
            'role': 'assistant',
            'content': handoff_message,
            'timestamp': now,
            'metadata': {
                'handoff_reason': data.get('reason', 'manual_handoff'),
                'assigned_to': data.get('assigned_to')
            }
        })
        
        # Atualizar status e métricas
        interaction['status'] = 'handoff'
        interaction['ended_at'] = now
        interaction['metrics']['total_messages'] = len(interaction['messages'])
        interaction['metrics']['resolution'] = 'handoff'
        
        # Atualizar estatísticas do assistente
        assistant['stats']['total_interactions'] += 1
        assistant['stats']['handoffs'] += 1
        
        logger.info(f"Handoff manual de interação de IA {interaction_id} por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Handoff realizado com sucesso',
            'interaction': interaction
        })
    except Exception as e:
        logger.error(f"Erro ao realizar handoff de interação de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@ai_bp.route('/ai/stats', methods=['GET'])
@jwt_required()
def get_ai_stats():
    try:
        current_user = get_jwt_identity()
        
        # Parâmetros de filtro
        period = request.args.get('period', 'month')  # day, week, month, year
        
        # Em um sistema real, buscaríamos estatísticas do banco de dados
        # Para simulação, calculamos com base nos dados existentes
        
        # Estatísticas de assistentes
        total_assistants = len(ai_assistants_db)
        active_assistants = sum(1 for assistant in ai_assistants_db.values() if assistant['status'] == 'active')
        
        # Estatísticas de interações
        total_interactions = sum(assistant['stats']['total_interactions'] for assistant in ai_assistants_db.values())
        successful_interactions = sum(assistant['stats']['successful_interactions'] for assistant in ai_assistants_db.values())
        handoffs = sum(assistant['stats']['handoffs'] for assistant in ai_assistants_db.values())
        
        # Calcular taxa de sucesso
        success_rate = (successful_interactions / total_interactions) * 100 if total_interactions > 0 else 0
        
        # Estatísticas de bases de conhecimento
        total_knowledge_bases = len(ai_knowledge_db)
        total_knowledge_items = sum(len(knowledge['items']) for knowledge in ai_knowledge_db.values())
        
        # Estatísticas por período (simulação)
        if period == 'day':
            period_label = 'Hoje'
            period_factor = 0.1  # 10% das interações totais
        elif period == 'week':
            period_label = 'Esta semana'
            period_factor = 0.3  # 30% das interações totais
        elif period == 'month':
            period_label = 'Este mês'
            period_factor = 0.7  # 70% das interações totais
        else:  # year
            period_label = 'Este ano'
            period_factor = 1.0  # 100% das interações totais
        
        period_interactions = int(total_interactions * period_factor)
        period_successful = int(successful_interactions * period_factor)
        period_handoffs = int(handoffs * period_factor)
        
        logger.info(f"Estatísticas de IA acessadas por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'stats': {
                'assistants': {
                    'total': total_assistants,
                    'active': active_assistants,
                    'inactive': total_assistants - active_assistants
                },
                'interactions': {
                    'total': total_interactions,
                    'successful': successful_interactions,
                    'handoffs': handoffs,
                    'success_rate': round(success_rate, 2),
                    'period': {
                        'label': period_label,
                        'total': period_interactions,
                        'successful': period_successful,
                        'handoffs': period_handoffs,
                        'success_rate': round((period_successful / period_interactions) * 100 if period_interactions > 0 else 0, 2)
                    }
                },
                'knowledge': {
                    'total_bases': total_knowledge_bases,
                    'total_items': total_knowledge_items,
                    'average_items_per_base': round(total_knowledge_items / total_knowledge_bases, 2) if total_knowledge_bases > 0 else 0
                },
                'models': {
                    'total': len(ai_models_db),
                    'by_type': {
                        'chat': sum(1 for model in ai_models_db.values() if model['type'] == 'chat'),
                        'classification': sum(1 for model in ai_models_db.values() if model['type'] == 'classification'),
                        'generation': sum(1 for model in ai_models_db.values() if model['type'] == 'generation')
                    }
                }
            }
        })
    except Exception as e:
        logger.error(f"Erro ao acessar estatísticas de IA: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500
