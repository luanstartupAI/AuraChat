"""
Configurações globais do backend do Aura.
Este módulo contém todas as configurações centrais do sistema.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações básicas
APP_NAME = "Aura"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Plataforma de comunicação e gerenciamento inspirada no Inzali"
APP_AUTHOR = "Equipe Aura"

# Configurações de ambiente
ENV = os.getenv("FLASK_ENV", "development")
DEBUG = ENV == "development"
TESTING = ENV == "testing"

# Configurações de servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "aura-secret-key-development")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "aura-jwt-secret-key-development")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24)))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30)))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Configurações de banco de dados
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///aura.db")

# Configurações de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "uploads")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
ALLOWED_EXTENSIONS = {
    "image": ["jpg", "jpeg", "png", "gif", "webp"],
    "document": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"],
    "audio": ["mp3", "wav", "ogg"],
    "video": ["mp4", "avi", "mov", "webm"]
}

# Configurações de WhatsApp
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://graph.facebook.com/v17.0")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_WEBHOOK_VERIFY_TOKEN = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "aura-whatsapp-webhook-token")

# Configurações de IA
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", 0.7))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", 150))

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "aura.log")

# Configurações de cache
CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))

# Configurações de rate limiting
RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200 per day, 50 per hour")
RATELIMIT_STORAGE_URL = os.getenv("RATELIMIT_STORAGE_URL", "memory://")

# Configurações de email
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "t")
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", f"Aura <{MAIL_USERNAME}>")

# Configurações de AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "aura-files")

# Configurações de websocket
SOCKETIO_ASYNC_MODE = os.getenv("SOCKETIO_ASYNC_MODE", "eventlet")
SOCKETIO_CORS_ALLOWED_ORIGINS = os.getenv("SOCKETIO_CORS_ALLOWED_ORIGINS", "*").split(",")
SOCKETIO_PING_TIMEOUT = int(os.getenv("SOCKETIO_PING_TIMEOUT", 5))
SOCKETIO_PING_INTERVAL = int(os.getenv("SOCKETIO_PING_INTERVAL", 25))

# Configurações de sessão
SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.getenv("SESSION_LIFETIME_DAYS", 7)))

# Configurações de transmissão
BROADCAST_RATE_LIMIT = int(os.getenv("BROADCAST_RATE_LIMIT", 100))  # mensagens por minuto
BROADCAST_BATCH_SIZE = int(os.getenv("BROADCAST_BATCH_SIZE", 20))  # mensagens por lote
BROADCAST_COOLDOWN = int(os.getenv("BROADCAST_COOLDOWN", 3600))  # segundos entre campanhas

# Configurações de automação
AUTOMATION_MAX_NODES = int(os.getenv("AUTOMATION_MAX_NODES", 50))  # nós por fluxo
AUTOMATION_MAX_FLOWS = int(os.getenv("AUTOMATION_MAX_FLOWS", 20))  # fluxos por conta

# Configurações de métricas
METRICS_RETENTION_DAYS = int(os.getenv("METRICS_RETENTION_DAYS", 90))
