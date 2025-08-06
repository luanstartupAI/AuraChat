from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

audience_bp = Blueprint('audience', __name__)

# Simulação de banco de dados de contatos e segmentos
contacts_db = {
    'contact1': {
        'id': 'contact1',
        'user_id': 'user1',
        'name': 'João Silva',
        'phone': '5511999999999',
        'email': 'joao@example.com',
        'avatar': 'https://i.pravatar.cc/150?img=1',
        'tags': ['cliente', 'premium'],
        'custom_fields': {
            'birthday': '1985-03-15',
            'city': 'São Paulo',
            'last_purchase': '2025-05-20'
        },
        'notes': 'Cliente desde 2023',
        'opt_in': True,
        'opt_in_date': '2023-10-15T14:30:00Z',
        'created_at': '2023-10-15T14:30:00Z',
        'updated_at': '2025-06-01T10:00:00Z'
    },
    'contact2': {
        'id': 'contact2',
        'user_id': 'user1',
        'name': 'Maria Souza',
        'phone': '5511888888888',
        'email': 'maria@example.com',
        'avatar': 'https://i.pravatar.cc/150?img=5',
        'tags': ['cliente'],
        'custom_fields': {
            'birthday': '1990-07-22',
            'city': 'Rio de Janeiro',
            'last_purchase': '2025-05-25'
        },
        'notes': 'Prefere contato por email',
        'opt_in': True,
        'opt_in_date': '2024-01-10T09:15:00Z',
        'created_at': '2024-01-10T09:15:00Z',
        'updated_at': '2025-06-01T11:00:00Z'
    },
    'contact3': {
        'id': 'contact3',
        'user_id': 'user1',
        'name': 'Carlos Oliveira',
        'phone': '5511777777777',
        'email': 'carlos@example.com',
        'avatar': 'https://i.pravatar.cc/150?img=8',
        'tags': ['lead'],
        'custom_fields': {
            'birthday': '1978-11-30',
            'city': 'Belo Horizonte',
            'interest': 'Plano Premium'
        },
        'notes': 'Interessado em nossos serviços premium',
        'opt_in': True,
        'opt_in_date': '2025-05-01T16:45:00Z',
        'created_at': '2025-05-01T16:45:00Z',
        'updated_at': '2025-05-01T16:45:00Z'
    }
}

segments_db = {
    'segment1': {
        'id': 'segment1',
        'user_id': 'user1',
        'name': 'Clientes Premium',
        'description': 'Clientes com tag premium',
        'filter': {
            'type': 'tag',
            'value': 'premium'
        },
        'estimated_reach': 1,
        'created_at': '2025-06-01T09:00:00Z',
        'updated_at': '2025-06-01T09:00:00Z'
    },
    'segment2': {
        'id': 'segment2',
        'user_id': 'user1',
        'name': 'Leads Recentes',
        'description': 'Contatos marcados como leads nos últimos 30 dias',
        'filter': {
            'type': 'tag_and_date',
            'tag': 'lead',
            'date_field': 'created_at',
            'date_comparison': 'greater_than',
            'date_value': '2025-05-01T00:00:00Z'
        },
        'estimated_reach': 1,
        'created_at': '2025-06-01T10:30:00Z',
        'updated_at': '2025-06-01T10:30:00Z'
    }
}

@audience_bp.route('/contacts', methods=['GET'])
@jwt_required()
def get_contacts():
    try:
        current_user = get_jwt_identity()
        
        # Parâmetros de paginação e filtros
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search', '')
        tag = request.args.get('tag', '')
        
        # Filtrar contatos
        filtered_contacts = []
        for contact_id, contact in contacts_db.items():
            # Filtrar por pesquisa
            if search and not (
                search.lower() in contact['name'].lower() or
                search in contact['phone'] or
                search.lower() in contact['email'].lower()
            ):
                continue
            
            # Filtrar por tag
            if tag and tag not in contact['tags']:
                continue
            
            filtered_contacts.append(contact)
        
        # Ordenar por nome
        filtered_contacts.sort(key=lambda x: x['name'])
        
        # Aplicar paginação
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_contacts = filtered_contacts[start_idx:end_idx]
        
        total_contacts = len(filtered_contacts)
        total_pages = (total_contacts + per_page - 1) // per_page
        
        logger.info(f"Contatos listados para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'contacts': paginated_contacts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_items': total_contacts,
                'total_pages': total_pages
            }
        })
    except Exception as e:
        logger.error(f"Erro ao listar contatos: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/contacts/<contact_id>', methods=['GET'])
@jwt_required()
def get_contact(contact_id):
    try:
        current_user = get_jwt_identity()
        
        if contact_id not in contacts_db:
            logger.warning(f"Tentativa de acesso a contato inexistente: {contact_id}")
            return jsonify({'status': 'error', 'message': 'Contato não encontrado'}), 404
        
        contact = contacts_db[contact_id]
        
        logger.info(f"Contato {contact_id} acessado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'contact': contact
        })
    except Exception as e:
        logger.error(f"Erro ao acessar contato: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/contacts', methods=['POST'])
@jwt_required()
def create_contact():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'name' not in data or 'phone' not in data:
            return jsonify({'status': 'error', 'message': 'Nome e telefone são obrigatórios'}), 400
        
        # Validar dados
        name = data.get('name')
        phone = data.get('phone')
        
        if not name or not phone:
            return jsonify({'status': 'error', 'message': 'Nome e telefone são obrigatórios'}), 400
        
        # Verificar se o telefone já existe
        for contact in contacts_db.values():
            if contact['phone'] == phone:
                logger.warning(f"Tentativa de criar contato com telefone duplicado: {phone}")
                return jsonify({'status': 'error', 'message': 'Telefone já cadastrado'}), 409
        
        # Criar novo contato
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        contact_id = str(uuid.uuid4())
        
        new_contact = {
            'id': contact_id,
            'user_id': 'user1',  # Em um sistema real, seria o ID do usuário atual
            'name': name,
            'phone': phone,
            'email': data.get('email', ''),
            'avatar': data.get('avatar', f'https://i.pravatar.cc/150?img={len(contacts_db) + 1}'),
            'tags': data.get('tags', []),
            'custom_fields': data.get('custom_fields', {}),
            'notes': data.get('notes', ''),
            'opt_in': data.get('opt_in', True),
            'opt_in_date': now if data.get('opt_in', True) else None,
            'created_at': now,
            'updated_at': now
        }
        
        # Adicionar ao "banco de dados"
        contacts_db[contact_id] = new_contact
        
        logger.info(f"Novo contato criado por {current_user}: {contact_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Contato criado com sucesso',
            'contact': new_contact
        }), 201
    except Exception as e:
        logger.error(f"Erro ao criar contato: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/contacts/<contact_id>', methods=['PUT'])
@jwt_required()
def update_contact(contact_id):
    try:
        current_user = get_jwt_identity()
        
        if contact_id not in contacts_db:
            logger.warning(f"Tentativa de atualização de contato inexistente: {contact_id}")
            return jsonify({'status': 'error', 'message': 'Contato não encontrado'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
        
        contact = contacts_db[contact_id]
        
        # Atualizar campos permitidos
        if 'name' in data:
            contact['name'] = data['name']
        
        if 'phone' in data:
            # Verificar se o novo telefone já existe em outro contato
            for c_id, c in contacts_db.items():
                if c_id != contact_id and c['phone'] == data['phone']:
                    logger.warning(f"Tentativa de atualizar contato com telefone duplicado: {data['phone']}")
                    return jsonify({'status': 'error', 'message': 'Telefone já cadastrado em outro contato'}), 409
            
            contact['phone'] = data['phone']
        
        if 'email' in data:
            contact['email'] = data['email']
        
        if 'avatar' in data:
            contact['avatar'] = data['avatar']
        
        if 'tags' in data:
            contact['tags'] = data['tags']
        
        if 'custom_fields' in data:
            # Mesclar campos personalizados existentes com novos
            for key, value in data['custom_fields'].items():
                contact['custom_fields'][key] = value
        
        if 'notes' in data:
            contact['notes'] = data['notes']
        
        if 'opt_in' in data:
            old_opt_in = contact['opt_in']
            new_opt_in = data['opt_in']
            
            contact['opt_in'] = new_opt_in
            
            # Se mudou de opt-out para opt-in, atualizar a data
            if not old_opt_in and new_opt_in:
                contact['opt_in_date'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        # Atualizar timestamp
        contact['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Contato {contact_id} atualizado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Contato atualizado com sucesso',
            'contact': contact
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar contato: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/contacts/<contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    try:
        current_user = get_jwt_identity()
        
        if contact_id not in contacts_db:
            logger.warning(f"Tentativa de exclusão de contato inexistente: {contact_id}")
            return jsonify({'status': 'error', 'message': 'Contato não encontrado'}), 404
        
        # Remover do "banco de dados"
        deleted_contact = contacts_db.pop(contact_id)
        
        logger.info(f"Contato {contact_id} excluído por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Contato excluído com sucesso',
            'contact': deleted_contact
        })
    except Exception as e:
        logger.error(f"Erro ao excluir contato: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/contacts/import', methods=['POST'])
@jwt_required()
def import_contacts():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'contacts' not in data or not isinstance(data['contacts'], list):
            return jsonify({'status': 'error', 'message': 'Formato de dados inválido'}), 400
        
        contacts_to_import = data['contacts']
        imported_count = 0
        skipped_count = 0
        errors = []
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        for contact_data in contacts_to_import:
            # Validar dados mínimos
            if 'name' not in contact_data or 'phone' not in contact_data:
                errors.append({
                    'data': contact_data,
                    'reason': 'Nome e telefone são obrigatórios'
                })
                continue
            
            # Verificar se o telefone já existe
            phone_exists = False
            for contact in contacts_db.values():
                if contact['phone'] == contact_data['phone']:
                    skipped_count += 1
                    phone_exists = True
                    break
            
            if phone_exists:
                continue
            
            # Criar novo contato
            contact_id = str(uuid.uuid4())
            
            new_contact = {
                'id': contact_id,
                'user_id': 'user1',  # Em um sistema real, seria o ID do usuário atual
                'name': contact_data['name'],
                'phone': contact_data['phone'],
                'email': contact_data.get('email', ''),
                'avatar': contact_data.get('avatar', f'https://i.pravatar.cc/150?img={len(contacts_db) + 1}'),
                'tags': contact_data.get('tags', []),
                'custom_fields': contact_data.get('custom_fields', {}),
                'notes': contact_data.get('notes', ''),
                'opt_in': contact_data.get('opt_in', True),
                'opt_in_date': now if contact_data.get('opt_in', True) else None,
                'created_at': now,
                'updated_at': now
            }
            
            # Adicionar ao "banco de dados"
            contacts_db[contact_id] = new_contact
            imported_count += 1
        
        logger.info(f"Importação de contatos por {current_user}: {imported_count} importados, {skipped_count} ignorados")
        
        return jsonify({
            'status': 'success',
            'message': f'Importação concluída: {imported_count} contatos importados, {skipped_count} ignorados',
            'summary': {
                'imported': imported_count,
                'skipped': skipped_count,
                'errors': errors
            }
        })
    except Exception as e:
        logger.error(f"Erro na importação de contatos: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/segments', methods=['GET'])
@jwt_required()
def get_segments():
    try:
        current_user = get_jwt_identity()
        
        # Listar todos os segmentos
        segments_list = list(segments_db.values())
        
        # Ordenar por nome
        segments_list.sort(key=lambda x: x['name'])
        
        logger.info(f"Segmentos listados para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'segments': segments_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar segmentos: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/segments/<segment_id>', methods=['GET'])
@jwt_required()
def get_segment(segment_id):
    try:
        current_user = get_jwt_identity()
        
        if segment_id not in segments_db:
            logger.warning(f"Tentativa de acesso a segmento inexistente: {segment_id}")
            return jsonify({'status': 'error', 'message': 'Segmento não encontrado'}), 404
        
        segment = segments_db[segment_id]
        
        # Calcular contatos no segmento
        segment_contacts = []
        
        # Aplicar filtro do segmento
        filter_type = segment['filter']['type']
        
        if filter_type == 'tag':
            tag_value = segment['filter']['value']
            for contact in contacts_db.values():
                if tag_value in contact['tags']:
                    segment_contacts.append(contact)
        
        elif filter_type == 'tag_and_date':
            tag = segment['filter']['tag']
            date_field = segment['filter']['date_field']
            date_comparison = segment['filter']['date_comparison']
            date_value = segment['filter']['date_value']
            
            for contact in contacts_db.values():
                # Verificar tag
                if tag not in contact['tags']:
                    continue
                
                # Verificar data
                if date_field not in contact:
                    continue
                
                contact_date = contact[date_field]
                
                if date_comparison == 'greater_than' and contact_date > date_value:
                    segment_contacts.append(contact)
                elif date_comparison == 'less_than' and contact_date < date_value:
                    segment_contacts.append(contact)
                elif date_comparison == 'equal' and contact_date == date_value:
                    segment_contacts.append(contact)
        
        logger.info(f"Segmento {segment_id} acessado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'segment': segment,
            'contacts': segment_contacts,
            'total_contacts': len(segment_contacts)
        })
    except Exception as e:
        logger.error(f"Erro ao acessar segmento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/segments', methods=['POST'])
@jwt_required()
def create_segment():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'name' not in data or 'filter' not in data:
            return jsonify({'status': 'error', 'message': 'Nome e filtro são obrigatórios'}), 400
        
        # Validar dados
        name = data.get('name')
        filter_data = data.get('filter')
        
        if not name or not filter_data:
            return jsonify({'status': 'error', 'message': 'Nome e filtro são obrigatórios'}), 400
        
        # Validar filtro
        if 'type' not in filter_data:
            return jsonify({'status': 'error', 'message': 'Tipo de filtro é obrigatório'}), 400
        
        filter_type = filter_data['type']
        
        if filter_type == 'tag' and 'value' not in filter_data:
            return jsonify({'status': 'error', 'message': 'Valor da tag é obrigatório para filtro por tag'}), 400
        
        elif filter_type == 'tag_and_date' and (
            'tag' not in filter_data or
            'date_field' not in filter_data or
            'date_comparison' not in filter_data or
            'date_value' not in filter_data
        ):
            return jsonify({'status': 'error', 'message': 'Dados incompletos para filtro por tag e data'}), 400
        
        # Criar novo segmento
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        segment_id = str(uuid.uuid4())
        
        new_segment = {
            'id': segment_id,
            'user_id': 'user1',  # Em um sistema real, seria o ID do usuário atual
            'name': name,
            'description': data.get('description', ''),
            'filter': filter_data,
            'estimated_reach': 0,  # Será calculado abaixo
            'created_at': now,
            'updated_at': now
        }
        
        # Calcular alcance estimado
        count = 0
        
        if filter_type == 'tag':
            tag_value = filter_data['value']
            for contact in contacts_db.values():
                if tag_value in contact['tags']:
                    count += 1
        
        elif filter_type == 'tag_and_date':
            tag = filter_data['tag']
            date_field = filter_data['date_field']
            date_comparison = filter_data['date_comparison']
            date_value = filter_data['date_value']
            
            for contact in contacts_db.values():
                # Verificar tag
                if tag not in contact['tags']:
                    continue
                
                # Verificar data
                if date_field not in contact:
                    continue
                
                contact_date = contact[date_field]
                
                if date_comparison == 'greater_than' and contact_date > date_value:
                    count += 1
                elif date_comparison == 'less_than' and contact_date < date_value:
                    count += 1
                elif date_comparison == 'equal' and contact_date == date_value:
                    count += 1
        
        new_segment['estimated_reach'] = count
        
        # Adicionar ao "banco de dados"
        segments_db[segment_id] = new_segment
        
        logger.info(f"Novo segmento criado por {current_user}: {segment_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'Segmento criado com sucesso',
            'segment': new_segment
        }), 201
    except Exception as e:
        logger.error(f"Erro ao criar segmento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/segments/<segment_id>', methods=['PUT'])
@jwt_required()
def update_segment(segment_id):
    try:
        current_user = get_jwt_identity()
        
        if segment_id not in segments_db:
            logger.warning(f"Tentativa de atualização de segmento inexistente: {segment_id}")
            return jsonify({'status': 'error', 'message': 'Segmento não encontrado'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados inválidos'}), 400
        
        segment = segments_db[segment_id]
        
        # Atualizar campos permitidos
        if 'name' in data:
            segment['name'] = data['name']
        
        if 'description' in data:
            segment['description'] = data['description']
        
        if 'filter' in data:
            filter_data = data['filter']
            
            # Validar filtro
            if 'type' not in filter_data:
                return jsonify({'status': 'error', 'message': 'Tipo de filtro é obrigatório'}), 400
            
            filter_type = filter_data['type']
            
            if filter_type == 'tag' and 'value' not in filter_data:
                return jsonify({'status': 'error', 'message': 'Valor da tag é obrigatório para filtro por tag'}), 400
            
            elif filter_type == 'tag_and_date' and (
                'tag' not in filter_data or
                'date_field' not in filter_data or
                'date_comparison' not in filter_data or
                'date_value' not in filter_data
            ):
                return jsonify({'status': 'error', 'message': 'Dados incompletos para filtro por tag e data'}), 400
            
            segment['filter'] = filter_data
            
            # Recalcular alcance estimado
            count = 0
            
            if filter_type == 'tag':
                tag_value = filter_data['value']
                for contact in contacts_db.values():
                    if tag_value in contact['tags']:
                        count += 1
            
            elif filter_type == 'tag_and_date':
                tag = filter_data['tag']
                date_field = filter_data['date_field']
                date_comparison = filter_data['date_comparison']
                date_value = filter_data['date_value']
                
                for contact in contacts_db.values():
                    # Verificar tag
                    if tag not in contact['tags']:
                        continue
                    
                    # Verificar data
                    if date_field not in contact:
                        continue
                    
                    contact_date = contact[date_field]
                    
                    if date_comparison == 'greater_than' and contact_date > date_value:
                        count += 1
                    elif date_comparison == 'less_than' and contact_date < date_value:
                        count += 1
                    elif date_comparison == 'equal' and contact_date == date_value:
                        count += 1
            
            segment['estimated_reach'] = count
        
        # Atualizar timestamp
        segment['updated_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
        
        logger.info(f"Segmento {segment_id} atualizado por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Segmento atualizado com sucesso',
            'segment': segment
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar segmento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/segments/<segment_id>', methods=['DELETE'])
@jwt_required()
def delete_segment(segment_id):
    try:
        current_user = get_jwt_identity()
        
        if segment_id not in segments_db:
            logger.warning(f"Tentativa de exclusão de segmento inexistente: {segment_id}")
            return jsonify({'status': 'error', 'message': 'Segmento não encontrado'}), 404
        
        # Remover do "banco de dados"
        deleted_segment = segments_db.pop(segment_id)
        
        logger.info(f"Segmento {segment_id} excluído por: {current_user}")
        
        return jsonify({
            'status': 'success',
            'message': 'Segmento excluído com sucesso',
            'segment': deleted_segment
        })
    except Exception as e:
        logger.error(f"Erro ao excluir segmento: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/tags', methods=['GET'])
@jwt_required()
def get_tags():
    try:
        current_user = get_jwt_identity()
        
        # Coletar todas as tags únicas
        all_tags = set()
        for contact in contacts_db.values():
            all_tags.update(contact['tags'])
        
        # Contar uso de cada tag
        tag_counts = {}
        for tag in all_tags:
            count = sum(1 for contact in contacts_db.values() if tag in contact['tags'])
            tag_counts[tag] = count
        
        # Formatar resultado
        tags_list = [{'name': tag, 'count': count} for tag, count in tag_counts.items()]
        
        # Ordenar por nome
        tags_list.sort(key=lambda x: x['name'])
        
        logger.info(f"Tags listadas para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'tags': tags_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar tags: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500

@audience_bp.route('/custom-fields', methods=['GET'])
@jwt_required()
def get_custom_fields():
    try:
        current_user = get_jwt_identity()
        
        # Coletar todos os campos personalizados únicos
        all_fields = set()
        for contact in contacts_db.values():
            all_fields.update(contact['custom_fields'].keys())
        
        # Contar uso de cada campo
        field_counts = {}
        for field in all_fields:
            count = sum(1 for contact in contacts_db.values() if field in contact['custom_fields'])
            field_counts[field] = count
        
        # Formatar resultado
        fields_list = [{'name': field, 'count': count} for field, count in field_counts.items()]
        
        # Ordenar por nome
        fields_list.sort(key=lambda x: x['name'])
        
        logger.info(f"Campos personalizados listados para usuário: {current_user}")
        
        return jsonify({
            'status': 'success',
            'custom_fields': fields_list
        })
    except Exception as e:
        logger.error(f"Erro ao listar campos personalizados: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro interno do servidor'}), 500
