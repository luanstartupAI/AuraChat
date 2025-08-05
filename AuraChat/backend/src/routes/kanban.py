from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

kanban_bp = Blueprint('kanban', __name__)

# Simulação de banco de dados de quadros kanban para o MVP
boards_db = {
    'board1': {
        'id': 'board1',
        'title': 'Projeto X',
        'description': 'Desenvolvimento do novo site',
        'columns': [
            {
                'id': 'col1',
                'title': 'A Fazer',
                'cards': [
                    {
                        'id': 'card1',
                        'title': 'Criar layout da homepage',
                        'description': 'Desenvolver o design da página inicial seguindo o estilo macOS Leopard',
                        'labels': ['design', 'frontend'],
                        'due_date': '2025-06-15T00:00:00Z',
                        'assigned_to': 'user1'
                    },
                    {
                        'id': 'card2',
                        'title': 'Implementar autenticação',
                        'description': 'Criar sistema de login e registro',
                        'labels': ['backend', 'segurança'],
                        'due_date': '2025-06-10T00:00:00Z',
                        'assigned_to': 'user2'
                    }
                ]
            },
            {
                'id': 'col2',
                'title': 'Em Progresso',
                'cards': [
                    {
                        'id': 'card3',
                        'title': 'Integração com API do WhatsApp',
                        'description': 'Conectar com a API do WhatsApp Business',
                        'labels': ['backend', 'integração'],
                        'due_date': '2025-06-08T00:00:00Z',
                        'assigned_to': 'user1'
                    }
                ]
            },
            {
                'id': 'col3',
                'title': 'Concluído',
                'cards': [
                    {
                        'id': 'card4',
                        'title': 'Setup do ambiente de desenvolvimento',
                        'description': 'Configurar ambiente React e Flask',
                        'labels': ['devops'],
                        'due_date': '2025-06-01T00:00:00Z',
                        'assigned_to': 'user2',
                        'completed_at': '2025-06-01T18:30:00Z'
                    }
                ]
            }
        ],
        'created_at': '2025-06-01T10:00:00Z',
        'updated_at': '2025-06-01T18:30:00Z'
    }
}

@kanban_bp.route('/boards', methods=['GET'])
@jwt_required()
def get_boards():
    # Em uma implementação real, filtraria por usuário
    return jsonify({
        'status': 'success',
        'boards': list(boards_db.values())
    })

@kanban_bp.route('/boards/<board_id>', methods=['GET'])
@jwt_required()
def get_board(board_id):
    if board_id not in boards_db:
        return jsonify({'status': 'error', 'message': 'Quadro não encontrado'}), 404
    
    return jsonify({
        'status': 'success',
        'board': boards_db[board_id]
    })

@kanban_bp.route('/boards', methods=['POST'])
@jwt_required()
def create_board():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'status': 'error', 'message': 'Título do quadro é obrigatório'}), 400
    
    # Criar novo quadro
    board_id = f'board{len(boards_db) + 1}'
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    
    new_board = {
        'id': board_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'columns': [
            {
                'id': f'{board_id}_col1',
                'title': 'A Fazer',
                'cards': []
            },
            {
                'id': f'{board_id}_col2',
                'title': 'Em Progresso',
                'cards': []
            },
            {
                'id': f'{board_id}_col3',
                'title': 'Concluído',
                'cards': []
            }
        ],
        'created_at': now,
        'updated_at': now
    }
    
    # Adicionar ao "banco de dados"
    boards_db[board_id] = new_board
    
    return jsonify({
        'status': 'success',
        'board': new_board
    }), 201

@kanban_bp.route('/boards/<board_id>/cards', methods=['POST'])
@jwt_required()
def create_card(board_id):
    if board_id not in boards_db:
        return jsonify({'status': 'error', 'message': 'Quadro não encontrado'}), 404
    
    data = request.get_json()
    
    if not data or 'title' not in data or 'column_id' not in data:
        return jsonify({'status': 'error', 'message': 'Título e ID da coluna são obrigatórios'}), 400
    
    # Encontrar a coluna
    column_id = data['column_id']
    column = None
    
    for col in boards_db[board_id]['columns']:
        if col['id'] == column_id:
            column = col
            break
    
    if not column:
        return jsonify({'status': 'error', 'message': 'Coluna não encontrada'}), 404
    
    # Criar novo cartão
    card_id = f'card{len(column["cards"]) + 1}'
    
    new_card = {
        'id': card_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'labels': data.get('labels', []),
        'due_date': data.get('due_date'),
        'assigned_to': data.get('assigned_to')
    }
    
    # Adicionar à coluna
    column['cards'].append(new_card)
    
    # Atualizar timestamp do quadro
    boards_db[board_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    
    return jsonify({
        'status': 'success',
        'card': new_card
    }), 201

@kanban_bp.route('/boards/<board_id>/cards/<card_id>/move', methods=['PUT'])
@jwt_required()
def move_card(board_id, card_id):
    if board_id not in boards_db:
        return jsonify({'status': 'error', 'message': 'Quadro não encontrado'}), 404
    
    data = request.get_json()
    
    if not data or 'source_column_id' not in data or 'target_column_id' not in data:
        return jsonify({'status': 'error', 'message': 'IDs das colunas de origem e destino são obrigatórios'}), 400
    
    source_column_id = data['source_column_id']
    target_column_id = data['target_column_id']
    
    # Encontrar as colunas
    source_column = None
    target_column = None
    
    for col in boards_db[board_id]['columns']:
        if col['id'] == source_column_id:
            source_column = col
        if col['id'] == target_column_id:
            target_column = col
    
    if not source_column:
        return jsonify({'status': 'error', 'message': 'Coluna de origem não encontrada'}), 404
    
    if not target_column:
        return jsonify({'status': 'error', 'message': 'Coluna de destino não encontrada'}), 404
    
    # Encontrar o cartão
    card = None
    card_index = -1
    
    for i, c in enumerate(source_column['cards']):
        if c['id'] == card_id:
            card = c
            card_index = i
            break
    
    if card_index == -1:
        return jsonify({'status': 'error', 'message': 'Cartão não encontrado'}), 404
    
    # Remover da coluna de origem
    card = source_column['cards'].pop(card_index)
    
    # Adicionar à coluna de destino
    target_position = data.get('target_position')
    
    if target_position is not None and target_position < len(target_column['cards']):
        target_column['cards'].insert(target_position, card)
    else:
        target_column['cards'].append(card)
    
    # Se movido para "Concluído", adicionar timestamp de conclusão
    if target_column['title'] == 'Concluído' and 'completed_at' not in card:
        card['completed_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    
    # Atualizar timestamp do quadro
    boards_db[board_id]['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    
    return jsonify({
        'status': 'success',
        'card': card
    })
