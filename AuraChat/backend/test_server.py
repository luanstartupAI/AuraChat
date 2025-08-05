#!/usr/bin/env python3
"""
Script de teste simples para o servidor AuraChat
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from flask import Flask, jsonify
    from flask_cors import CORS
    print("✅ Flask e CORS importados com sucesso")
    
    from config.database import get_db, init_db
    print("✅ Configuração do banco de dados importada com sucesso")
    
    from models.base_models import User, Contact, Chat, Message
    print("✅ Modelos importados com sucesso")
    
    from routes.auth import auth_bp
    print("✅ Rotas de autenticação importadas com sucesso")
    
    # Criar app Flask simples
    app = Flask(__name__)
    CORS(app)
    
    @app.route("/test", methods=["GET"])
    def test():
        return jsonify({"message": "AuraChat Backend funcionando!"})
    
    print("✅ Servidor Flask criado com sucesso")
    print("🎉 Todos os imports funcionaram! O servidor está pronto para ser executado.")
    
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1)