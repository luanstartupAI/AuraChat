#!/usr/bin/env python3
"""
Rotas de Inteligência Artificial - AuraChat
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import asyncio
import json
import logging
import os

from config.database import get_db
from models.base_models import User
from services.ai_service import (
    AIService, AIRequest, AIResponse, AITaskType,
    init_ai_service, get_ai_service
)
from config.security import sanitize_input

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')
logger = logging.getLogger(__name__)

# Configuração da API Key do Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')

@ai_bp.route('/status', methods=['GET'])
@jwt_required()
def get_ai_status():
    """Retorna status do serviço de IA"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        status = loop.run_until_complete(ai_service.get_service_status())
        loop.close()
        
        return jsonify({
            "success": True,
            "data": status
        }), 200
    except Exception as e:
        logger.error(f"Erro ao obter status da IA: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao obter status do serviço de IA"
        }), 500

@ai_bp.route('/classify', methods=['POST'])
@jwt_required()
def classify_message():
    """Classifica uma mensagem usando IA"""
    try:
        data = request.get_json()
        message = sanitize_input(data.get('message', ''))
        context = data.get('context', {})
        
        if not message:
            return jsonify({
                "success": False,
                "error": "Mensagem é obrigatória"
            }), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        response = loop.run_until_complete(ai_service.classify_message(message, context))
        loop.close()
        
        if response.success:
            return jsonify({
                "success": True,
                "data": {
                    "classification": response.result,
                    "confidence": response.confidence,
                    "metadata": response.metadata
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.error
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao classificar mensagem: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao processar classificação"
        }), 500

@ai_bp.route('/generate-response', methods=['POST'])
@jwt_required()
def generate_response():
    """Gera uma resposta usando IA"""
    try:
        data = request.get_json()
        message = sanitize_input(data.get('message', ''))
        context = data.get('context', {})
        
        if not message:
            return jsonify({
                "success": False,
                "error": "Mensagem é obrigatória"
            }), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        response = loop.run_until_complete(ai_service.generate_response(message, context))
        loop.close()
        
        if response.success:
            return jsonify({
                "success": True,
                "data": {
                    "response": response.result,
                    "confidence": response.confidence,
                    "metadata": response.metadata
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.error
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao gerar resposta: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao gerar resposta"
        }), 500

@ai_bp.route('/analyze-sentiment', methods=['POST'])
@jwt_required()
def analyze_sentiment():
    """Analisa o sentimento de uma mensagem"""
    try:
        data = request.get_json()
        message = sanitize_input(data.get('message', ''))
        
        if not message:
            return jsonify({
                "success": False,
                "error": "Mensagem é obrigatória"
            }), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        response = loop.run_until_complete(ai_service.analyze_sentiment(message))
        loop.close()
        
        if response.success:
            return jsonify({
                "success": True,
                "data": {
                    "sentiment": response.result,
                    "confidence": response.confidence,
                    "metadata": response.metadata
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.error
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao analisar sentimento: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao analisar sentimento"
        }), 500

@ai_bp.route('/translate', methods=['POST'])
@jwt_required()
def translate_message():
    """Traduz uma mensagem"""
    try:
        data = request.get_json()
        message = sanitize_input(data.get('message', ''))
        target_language = data.get('target_language', 'inglês')
        
        if not message:
            return jsonify({
                "success": False,
                "error": "Mensagem é obrigatória"
            }), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        response = loop.run_until_complete(ai_service.translate_message(message, target_language))
        loop.close()
        
        if response.success:
            return jsonify({
                "success": True,
                "data": {
                    "translation": response.result,
                    "original": message,
                    "target_language": target_language,
                    "metadata": response.metadata
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.error
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao traduzir mensagem: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao traduzir mensagem"
        }), 500

@ai_bp.route('/extract-info', methods=['POST'])
@jwt_required()
def extract_info():
    """Extrai informações de uma mensagem"""
    try:
        data = request.get_json()
        message = sanitize_input(data.get('message', ''))
        
        if not message:
            return jsonify({
                "success": False,
                "error": "Mensagem é obrigatória"
            }), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        response = loop.run_until_complete(ai_service.extract_info(message))
        loop.close()
        
        if response.success:
            try:
                # Tenta fazer parse do JSON retornado
                extracted_info = json.loads(response.result)
            except:
                # Se não for JSON válido, retorna como texto
                extracted_info = response.result
            
            return jsonify({
                "success": True,
                "data": {
                    "extracted_info": extracted_info,
                    "confidence": response.confidence,
                    "metadata": response.metadata
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.error
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao extrair informações: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao extrair informações"
        }), 500

@ai_bp.route('/summarize', methods=['POST'])
@jwt_required()
def summarize_conversation():
    """Resume uma conversa"""
    try:
        data = request.get_json()
        conversation = sanitize_input(data.get('conversation', ''))
        
        if not conversation:
            return jsonify({
                "success": False,
                "error": "Conversa é obrigatória"
            }), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        response = loop.run_until_complete(ai_service.summarize_conversation(conversation))
        loop.close()
        
        if response.success:
            return jsonify({
                "success": True,
                "data": {
                    "summary": response.result,
                    "metadata": response.metadata
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.error
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao resumir conversa: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao resumir conversa"
        }), 500

@ai_bp.route('/generate-template', methods=['POST'])
@jwt_required()
def generate_template():
    """Gera um template de mensagem"""
    try:
        data = request.get_json()
        context = data.get('context', {})
        template_type = data.get('template_type', 'vendas')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        response = loop.run_until_complete(ai_service.generate_template(context, template_type))
        loop.close()
        
        if response.success:
            return jsonify({
                "success": True,
                "data": {
                    "template": response.result,
                    "template_type": template_type,
                    "metadata": response.metadata
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": response.error
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao gerar template: {e}")
        return jsonify({
            "success": False,
            "error": "Erro ao gerar template"
        }), 500

@ai_bp.route('/health', methods=['GET'])
def ai_health():
    """Health check do serviço de IA"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_service = loop.run_until_complete(get_ai_service())
        status = loop.run_until_complete(ai_service.get_service_status())
        loop.close()
        
        return jsonify({
            "status": "healthy" if status["initialized"] else "unhealthy",
            "service": "ai",
            "model": status.get("model"),
            "available_tasks": status.get("available_tasks", []),
            "api_key_configured": status.get("api_key_configured", False)
        }), 200
    except Exception as e:
        logger.error(f"Erro no health check da IA: {e}")
        return jsonify({
            "status": "unhealthy",
            "service": "ai",
            "error": str(e)
        }), 500
