from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from config.database import get_db, init_db
from models.base_models import User
from config.security import hash_password, verify_password, validate_email, sanitize_input
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        name = sanitize_input(data.get('name', ''))
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        # Validações
        if not name or not email or not password:
            return jsonify({"error": "Nome, email e senha são obrigatórios"}), 400
        
        if not validate_email(email):
            return jsonify({"error": "Email inválido"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Senha deve ter pelo menos 6 caracteres"}), 400
        
        db = next(get_db())
        
        # Verificar se email já existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return jsonify({"error": "Email já cadastrado"}), 409
        
        # Criar novo usuário
        hashed_password = hash_password(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password,
            role="user"
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Gerar token
        access_token = create_access_token(identity=new_user.id)
        
        return jsonify({
            "message": "Usuário registrado com sucesso",
            "token": access_token,
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role,
                "avatar": new_user.avatar
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Erro no registro: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login de usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        db = next(get_db())
        
        # Buscar usuário
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password_hash):
            return jsonify({"error": "Credenciais inválidas"}), 401
        
        if not user.is_active:
            return jsonify({"error": "Conta desativada"}), 401
        
        # Gerar token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            "message": "Login realizado com sucesso",
            "token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "avatar": user.avatar
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    """Obter perfil do usuário atual"""
    try:
        current_user_id = get_jwt_identity()
        db = next(get_db())
        
        user = db.query(User).filter(User.id == current_user_id).first()
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "avatar": user.avatar,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter perfil: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """Atualizar perfil do usuário"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        db = next(get_db())
        user = db.query(User).filter(User.id == current_user_id).first()
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        # Atualizar campos permitidos
        if 'name' in data:
            user.name = sanitize_input(data['name'])
        
        if 'avatar' in data:
            user.avatar = data['avatar']
        
        db.commit()
        
        return jsonify({
            "message": "Perfil atualizado com sucesso",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "avatar": user.avatar
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao atualizar perfil: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Alterar senha do usuário"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({"error": "Senha atual e nova senha são obrigatórias"}), 400
        
        if len(new_password) < 6:
            return jsonify({"error": "Nova senha deve ter pelo menos 6 caracteres"}), 400
        
        db = next(get_db())
        user = db.query(User).filter(User.id == current_user_id).first()
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        # Verificar senha atual
        if not verify_password(current_password, user.password_hash):
            return jsonify({"error": "Senha atual incorreta"}), 401
        
        # Atualizar senha
        user.password_hash = hash_password(new_password)
        db.commit()
        
        return jsonify({"message": "Senha alterada com sucesso"}), 200
        
    except Exception as e:
        logger.error(f"Erro ao alterar senha: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout do usuário"""
    # Em uma implementação mais robusta, você pode adicionar o token a uma blacklist
    return jsonify({"message": "Logout realizado com sucesso"}), 200

@auth_bp.route('/health', methods=['GET'])
def auth_health():
    """Verificação de saúde do módulo de autenticação"""
    return jsonify({
        "status": "healthy",
        "module": "auth",
        "endpoints": [
            "POST /api/auth/register",
            "POST /api/auth/login",
            "GET /api/auth/me",
            "PUT /api/auth/me",
            "POST /api/auth/change-password",
            "POST /api/auth/logout"
        ]
    }), 200
