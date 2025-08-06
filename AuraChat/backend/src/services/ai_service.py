#!/usr/bin/env python3
"""
Serviço de Inteligência Artificial - AuraChat
Integração com Google Gemini AI
"""
import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import google.generativeai as genai
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AITaskType(Enum):
    """Tipos de tarefas de IA disponíveis"""
    CLASSIFY_MESSAGE = "classify_message"
    GENERATE_RESPONSE = "generate_response"
    ANALYZE_SENTIMENT = "analyze_sentiment"
    TRANSLATE = "translate"
    EXTRACT_INFO = "extract_info"
    SUMMARIZE = "summarize"
    GENERATE_TEMPLATE = "generate_template"

@dataclass
class AIRequest:
    """Estrutura de requisição para IA"""
    task_type: AITaskType
    content: str
    context: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None

@dataclass
class AIResponse:
    """Estrutura de resposta da IA"""
    success: bool
    result: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class AIService:
    """Serviço principal de Inteligência Artificial"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = None
        self.is_initialized = False
        self.prompt_templates = self._load_prompt_templates()
        
    def initialize(self) -> bool:
        """Inicializa o serviço de IA"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_initialized = True
            logger.info("✅ Serviço de IA (Gemini) inicializado")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar IA: {e}")
            return False
    
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Carrega templates de prompts"""
        return {
            "classify_message": """
            Você é um assistente especializado em classificar mensagens de WhatsApp.
            
            Classifique a seguinte mensagem em uma das categorias:
            - VENDA: Interesse em comprar produtos/serviços
            - SUPORTE: Problemas técnicos ou dúvidas
            - INFORMAÇÃO: Solicitações de informações gerais
            - RECLAMAÇÃO: Problemas ou insatisfações
            - ELOGIO: Feedback positivo
            - OUTROS: Não se encaixa nas categorias acima
            
            Mensagem: {content}
            
            Responda apenas com a categoria e uma breve explicação.
            """,
            
            "generate_response": """
            Você é um assistente de atendimento ao cliente.
            
            Contexto: {context}
            Mensagem do cliente: {content}
            
            Gere uma resposta profissional, amigável e útil.
            A resposta deve ser em português brasileiro.
            """,
            
            "analyze_sentiment": """
            Analise o sentimento da seguinte mensagem:
            
            Mensagem: {content}
            
            Classifique como:
            - POSITIVO: Sentimento positivo
            - NEUTRO: Sentimento neutro
            - NEGATIVO: Sentimento negativo
            
            Forneça também uma pontuação de 0 a 10.
            """,
            
            "translate": """
            Traduza a seguinte mensagem para {target_language}:
            
            Mensagem: {content}
            
            Mantenha o tom e contexto original.
            """,
            
            "extract_info": """
            Extraia informações importantes da seguinte mensagem:
            
            Mensagem: {content}
            
            Extraia:
            - Nome (se mencionado)
            - Telefone (se mencionado)
            - Email (se mencionado)
            - Produto/serviço de interesse
            - Urgência (alta/média/baixa)
            
            Responda em formato JSON.
            """,
            
            "summarize": """
            Faça um resumo da seguinte conversa:
            
            Conversa: {content}
            
            Destaque os pontos principais e ações necessárias.
            """,
            
            "generate_template": """
            Gere um template de mensagem para WhatsApp com base no contexto:
            
            Contexto: {context}
            Tipo: {template_type}
            
            O template deve ser profissional e persuasivo.
            """
        }
    
    async def process_request(self, request: AIRequest) -> AIResponse:
        """Processa uma requisição de IA"""
        try:
            if not self.is_initialized:
                return AIResponse(
                    success=False,
                    error="Serviço de IA não inicializado"
                )
            
            # Seleciona o template apropriado
            template = self.prompt_templates.get(request.task_type.value, "")
            if not template:
                return AIResponse(
                    success=False,
                    error=f"Tipo de tarefa não suportado: {request.task_type}"
                )
            
            # Prepara o prompt
            prompt = template.format(
                content=request.content,
                context=request.context or {},
                **request.parameters or {}
            )
            
            # Gera resposta
            response = self.model.generate_content(prompt)
            
            if response.text:
                return AIResponse(
                    success=True,
                    result=response.text,
                    confidence=0.9,  # Gemini não fornece confidence score
                    metadata={
                        "model": "gemini-pro",
                        "timestamp": datetime.now().isoformat(),
                        "task_type": request.task_type.value
                    }
                )
            else:
                return AIResponse(
                    success=False,
                    error="Resposta vazia da IA"
                )
                
        except Exception as e:
            logger.error(f"Erro ao processar requisição de IA: {e}")
            return AIResponse(
                success=False,
                error=str(e)
            )
    
    async def classify_message(self, message: str, context: Optional[Dict] = None) -> AIResponse:
        """Classifica uma mensagem"""
        request = AIRequest(
            task_type=AITaskType.CLASSIFY_MESSAGE,
            content=message,
            context=context
        )
        return await self.process_request(request)
    
    async def generate_response(self, message: str, context: Optional[Dict] = None) -> AIResponse:
        """Gera uma resposta para uma mensagem"""
        request = AIRequest(
            task_type=AITaskType.GENERATE_RESPONSE,
            content=message,
            context=context
        )
        return await self.process_request(request)
    
    async def analyze_sentiment(self, message: str) -> AIResponse:
        """Analisa o sentimento de uma mensagem"""
        request = AIRequest(
            task_type=AITaskType.ANALYZE_SENTIMENT,
            content=message
        )
        return await self.process_request(request)
    
    async def translate_message(self, message: str, target_language: str) -> AIResponse:
        """Traduz uma mensagem"""
        request = AIRequest(
            task_type=AITaskType.TRANSLATE,
            content=message,
            parameters={"target_language": target_language}
        )
        return await self.process_request(request)
    
    async def extract_info(self, message: str) -> AIResponse:
        """Extrai informações de uma mensagem"""
        request = AIRequest(
            task_type=AITaskType.EXTRACT_INFO,
            content=message
        )
        return await self.process_request(request)
    
    async def summarize_conversation(self, conversation: str) -> AIResponse:
        """Resume uma conversa"""
        request = AIRequest(
            task_type=AITaskType.SUMMARIZE,
            content=conversation
        )
        return await self.process_request(request)
    
    async def generate_template(self, context: Dict, template_type: str) -> AIResponse:
        """Gera um template de mensagem"""
        request = AIRequest(
            task_type=AITaskType.GENERATE_TEMPLATE,
            content="",
            context=context,
            parameters={"template_type": template_type}
        )
        return await self.process_request(request)
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Retorna status do serviço de IA"""
        return {
            "initialized": self.is_initialized,
            "model": "gemini-pro" if self.is_initialized else None,
            "available_tasks": [task.value for task in AITaskType],
            "api_key_configured": bool(self.api_key)
        }

# Instância global do serviço de IA
ai_service = None

async def init_ai_service(api_key: str) -> AIService:
    """Inicializa serviço de IA global"""
    global ai_service
    if ai_service is None:
        ai_service = AIService(api_key)
        await ai_service.initialize()
    return ai_service

async def get_ai_service() -> AIService:
    """Retorna instância do serviço de IA"""
    if ai_service is None:
        raise RuntimeError("Serviço de IA não inicializado")
    return ai_service