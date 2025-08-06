"""
Configurações de segurança do backend do Aura.
Este módulo contém todas as configurações relacionadas à segurança.
"""
import os
import secrets
import hashlib
import string
from datetime import datetime, timedelta
from typing import Optional
import jwt
from flask import current_app
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Chaves secretas
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_hex(32))

# Configurações JWT
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24)))
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30)))
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# Configurações de senha
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_NUMBERS = True
PASSWORD_REQUIRE_SPECIAL = True
PASSWORD_HASH_ROUNDS = 12

def hash_password(password: str) -> str:
    """Hash de senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verificar senha"""
    return hash_password(password) == hashed

def generate_token(user_id: str, expires_in: int = 3600) -> str:
    """Gerar JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token: str) -> Optional[str]:
    """Verificar JWT token"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_random_string(length: int = 32) -> str:
    """Gerar string aleatória"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def sanitize_input(text: str) -> str:
    """Sanitizar entrada de texto"""
    if not text:
        return ""
    
    # Remover caracteres perigosos
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def validate_email(email: str) -> bool:
    """Validar formato de email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validar formato de telefone"""
    import re
    # Remove todos os caracteres não numéricos
    phone_clean = re.sub(r'[^\d]', '', phone)
    # Verifica se tem entre 10 e 15 dígitos
    return 10 <= len(phone_clean) <= 15

# Configurações de CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Content-Type", "Authorization", "X-Requested-With"]
CORS_EXPOSE_HEADERS = ["Content-Disposition"]
CORS_SUPPORTS_CREDENTIALS = True

# Configurações de proteção contra ataques
CSRF_ENABLED = True
CSRF_SECRET_KEY = os.getenv("CSRF_SECRET_KEY", secrets.token_hex(16))
CSRF_TIME_LIMIT = 3600  # 1 hora

# Rate limiting
RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200 per day, 50 per hour")
RATELIMIT_STORAGE_URL = os.getenv("RATELIMIT_STORAGE_URL", "memory://")
RATELIMIT_HEADERS_ENABLED = True
RATELIMIT_STRATEGY = 'fixed-window'

# Configurações de sessão
SESSION_TYPE = os.getenv("SESSION_TYPE", "filesystem")
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.getenv("SESSION_LIFETIME_DAYS", 7)))
SESSION_USE_SIGNER = True
SESSION_KEY_PREFIX = 'aura_session:'

# Configurações de cookie
REMEMBER_COOKIE_DURATION = timedelta(days=30)
REMEMBER_COOKIE_SECURE = True
REMEMBER_COOKIE_HTTPONLY = True
REMEMBER_COOKIE_SAMESITE = 'Lax'

# Configurações de cabeçalhos de segurança
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'",
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}

# Configurações de autenticação de dois fatores
MFA_ENABLED = os.getenv("MFA_ENABLED", "False").lower() in ("true", "1", "t")
MFA_ISSUER_NAME = "Aura"
MFA_DIGITS = 6
MFA_PERIOD = 30
MFA_ALGORITHM = "SHA1"

# Configurações de bloqueio de conta
ACCOUNT_LOCKOUT_THRESHOLD = 5  # tentativas
ACCOUNT_LOCKOUT_DURATION = timedelta(minutes=15)
ACCOUNT_PASSWORD_EXPIRY = timedelta(days=90)

# Configurações de auditoria
AUDIT_ENABLED = True
AUDIT_EVENTS = [
    'login', 'logout', 'register', 'password_change', 'password_reset',
    'profile_update', 'role_change', 'permission_change', 'api_key_create',
    'api_key_revoke', 'mfa_enable', 'mfa_disable', 'account_lock', 'account_unlock'
]

# Configurações de verificação de email
EMAIL_VERIFICATION_REQUIRED = True
EMAIL_VERIFICATION_EXPIRY = timedelta(days=3)
EMAIL_VERIFICATION_URL = os.getenv("EMAIL_VERIFICATION_URL", "http://localhost:3000/verify-email")

# Configurações de recuperação de senha
PASSWORD_RESET_EXPIRY = timedelta(hours=24)
PASSWORD_RESET_URL = os.getenv("PASSWORD_RESET_URL", "http://localhost:3000/reset-password")

# Configurações de API Keys
API_KEY_ENABLED = True
API_KEY_EXPIRY = timedelta(days=365)
API_KEY_PREFIX = "aura_"

# Configurações de permissões
DEFAULT_ROLE = "user"
AVAILABLE_ROLES = ["admin", "manager", "user", "guest"]
ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": ["read:*", "write:*", "delete:own_*", "manage:users"],
    "user": ["read:*", "write:own_*", "delete:own_*"],
    "guest": ["read:public_*"]
}

# Configurações de WhatsApp
WHATSAPP_WEBHOOK_VERIFY_TOKEN = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", secrets.token_hex(16))

# Configurações de AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Configurações de upload
ALLOWED_EXTENSIONS = {
    "image": ["jpg", "jpeg", "png", "gif", "webp"],
    "document": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"],
    "audio": ["mp3", "wav", "ogg"],
    "video": ["mp4", "avi", "mov", "webm"]
}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
