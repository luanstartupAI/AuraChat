from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

flow_bp = Blueprint('flow', __name__)

# Simulação de banco de dados de fluxos de conversa para o MVP
flows_db = {
    'flow1': {
        'id': 'flow1',
        'title': 'Atendimento Inicial',
        'description': 'Fluxo de boas-vindas e triagem inicial',
        'nodes': [
            {
                'id': 'node1',
                'type': 'message',
                'content': 'Olá! Bem-vindo à Aura. Como posso ajudar você hoje?',
                'position': {'x': 100, 'y': 100}
            },
            {
                'id': 'node2',
                'type': 'condition',
                'content': 'Escolha uma opção',
                'options': [
                    {'id': 'opt1', 'text': 'Suporte', 'next_node': 'node3'},
                    {'id': 'opt2', 'text': 'Vendas', 'next_node': 'node4'},
                    {'id': 'opt3', 'text': 'Outros', 'next_node': 'node5'}
                ],
                'position': {'x': 100, 'y': 250}
            },
            {
                'id': 'node3',
                'type': 'message',
                'content': 'Entendi que você precisa de suporte. Por favor, descreva seu problema.',
                'position': {'x': 0, 'y': 400}
            },
            {
                'id': 'node4',
                'type': 'message',
                'content': 'Ótimo! Nosso time de vendas está pronto para atendê-lo. Qual produto você tem interesse?',
                'position': {'x': 200, 'y': 400}
            },
            {
                'id': 'node5',
                'type': 'message',
                'content': 'Em breve um atendente entrará em contato para ajudá-lo.',
                'position': {'x': 400, 'y': 400}
            }
        ],
        'connections': [
            {'source': 'node1', 'target': 'node2'},
            {'source': 'node2', 'target': 'node3', 'condition': 'opt1'},
            {'source': 'node2', 'target': 'node4', 'condition': 'opt2'},
            {'source': 'node2', 'target': 'node5', 'condition': 'opt3'}
        ],
        'created_at': '2025-06-01T10:00:00Z',
        'updated_at': '2025-06-01T10:00:00Z',
        'is_active': True
    }
}

@flow_bp.route('/flows', methods=['GET'])
@jwt_required()
def get_flows():
    # Em uma implementação real, filtraria por usuário
    return jsonify({
        'status': 'success',
        'flows': list(flows_db.values())
    })

@flow_bp.route('/flows/<flow_id>', methods=['GET'])
@jwt_required()
def get_flow(flow_id):
    if flow_id not in flows_db:
        return jsonify({'status': 'error', 'message': 'Fluxo não encontrado'}), 404
    
    return jsonify({
        'status': 'success',
        'flow': flows_db[flow_id]
    })

@flow_bp.route('/flows', methods=['POST'])
@jwt_required()
def create_flow():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'status': 'error', 'message': 'Título do fluxo é obrigatório'}), 400
    
    # Criar novo fluxo
    flow_id = f'flow{len(flows_db) + 1}'
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    new_flow = {
        'id': flow_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'nodes': data.get('nodes', []),
        'connections': data.get('connections', []),
        'created_at': now,
        'updated_at': now,
        'is_active': False
    }
    
    # Adicionar ao "banco de dados"
    flows_db[flow_id] = new_flow
    
    return jsonify({
        'status': 'success',
        'flow': new_flow
    }), 201

@flow_bp.route('/flows/<flow_id>', methods=['PUT'])
@jwt_required()
def update_flow(flow_id):
    if flow_id not in flows_db:
        return jsonify({'status': 'error', 'message': 'Fluxo não encontrado'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
    
    flow = flows_db[flow_id]
    
    # Atualizar campos
    if 'title' in data:
        flow['title'] = data['title']
    
    if 'description' in data:
        flow['description'] = data['description']
    
    if 'nodes' in data:
        flow['nodes'] = data['nodes']
    
    if 'connections' in data:
        flow['connections'] = data['connections']
    
    if 'is_active' in data:
        flow['is_active'] = data['is_active']
    
    # Atualizar timestamp
    flow['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    
    return jsonify({
        'status': 'success',
        'flow': flow
    })

@flow_bp.route('/flows/<flow_id>/activate', methods=['PUT'])
@jwt_required()
def activate_flow(flow_id):
    if flow_id not in flows_db:
        return jsonify({'status': 'error', 'message': 'Fluxo não encontrado'}), 404
    
    flows_db[flow_id]['is_active'] = True
    flows_db[flow_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    
    return jsonify({
        'status': 'success',
        'message': 'Fluxo ativado com sucesso',
        'flow': flows_db[flow_id]
    })

@flow_bp.route('/flows/<flow_id>/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_flow(flow_id):
    if flow_id not in flows_db:
        return jsonify({'status': 'error', 'message': 'Fluxo não encontrado'}), 404
    
    flows_db[flow_id]['is_active'] = False
    flows_db[flow_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    
    return jsonify({
        'status': 'success',
        'message': 'Fluxo desativado com sucesso',
        'flow': flows_db[flow_id]
    })
