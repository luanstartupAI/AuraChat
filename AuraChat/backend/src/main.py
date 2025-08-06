# src/main.py (Minimal Health Check Only)
import os
import sys
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Importar rotas
from routes.auth import auth_bp
from routes.chat_simple import chat_bp
from routes.contact_simple import contact_bp
from routes.whatsapp import whatsapp_bp
from routes.ai import ai_bp

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("aura_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar aplicação Flask
app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aura-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'aura-jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens não expiram para desenvolvimento

# Configurar CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Inicializar JWT
jwt = JWTManager(app)

# Inicializar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(whatsapp_bp, url_prefix='/api/whatsapp')
app.register_blueprint(ai_bp, url_prefix='/api/ai')

# Rota de verificação de saúde
@app.route("/api/health", methods=["GET"])
def health_check():
    logger.info("Health check endpoint called.")
    return jsonify({
        "status": "success",
        "message": "Aura API is running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "modules": {
            "auth": "active",
            "chat": "active",
            "contact": "active",
            "whatsapp": "active",
            "ai": "active"
        }
    })

# Rota raiz
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "AuraChat API v1.0",
        "documentation": "/api/docs",
        "health": "/api/health"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# WebSocket events
@socketio.on('connect')
def handle_connect():
    logger.info(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('join_chat')
def handle_join_chat(data):
    chat_id = data.get('chat_id')
    if chat_id:
        socketio.join_room(f"chat_{chat_id}")
        logger.info(f"Client {request.sid} joined chat {chat_id}")

@socketio.on('leave_chat')
def handle_leave_chat(data):
    chat_id = data.get('chat_id')
    if chat_id:
        socketio.leave_room(f"chat_{chat_id}")
        logger.info(f"Client {request.sid} left chat {chat_id}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    
    logger.info(f"Iniciando Aura API na porta {port}, modo {'desenvolvimento' if debug else 'produção'}")
    
    try:
        socketio.run(app, host="0.0.0.0", port=port, debug=debug)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}", exc_info=True)

