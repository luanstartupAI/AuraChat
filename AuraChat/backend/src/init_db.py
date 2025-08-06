#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do AuraChat
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import init_db, engine
from models.base_models import Base
from config.security import hash_password
from models.base_models import User
from sqlalchemy.orm import Session
from config.database import SessionLocal

def create_tables():
    """Criar todas as tabelas"""
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

def create_admin_user():
    """Criar usuário administrador padrão"""
    print("Criando usuário administrador...")
    
    db = SessionLocal()
    try:
        # Verificar se já existe um admin
        admin = db.query(User).filter(User.email == "admin@aura.com").first()
        if admin:
            print("Usuário administrador já existe!")
            return
        
        # Criar usuário admin
        admin_user = User(
            name="Administrador",
            email="admin@aura.com",
            password_hash=hash_password("admin123"),
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Usuário administrador criado com sucesso!")
        print("Email: admin@aura.com")
        print("Senha: admin123")
        
    except Exception as e:
        print(f"Erro ao criar usuário administrador: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal"""
    print("=== Inicialização do Banco de Dados AuraChat ===")
    
    try:
        # Criar tabelas
        create_tables()
        
        # Criar usuário admin
        create_admin_user()
        
        print("\n=== Inicialização concluída com sucesso! ===")
        print("Você pode agora executar o servidor com: python src/main.py")
        
    except Exception as e:
        print(f"Erro durante a inicialização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()