#!/usr/bin/env python3
"""
Serviço de Integração WhatsApp - AuraChat
Estratégia Híbrida: API Oficial + Web WhatsApp Wrapper
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import qrcode
from PIL import Image
import io

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppProvider(Enum):
    """Provedores de WhatsApp disponíveis"""
    OFFICIAL_API = "official_api"
    WEB_WHATSAPP = "web_whatsapp"
    HYBRID = "hybrid"

@dataclass
class WhatsAppMessage:
    """Estrutura de mensagem WhatsApp"""
    to: str
    content: str
    message_type: str = "text"
    media_url: Optional[str] = None
    template_name: Optional[str] = None
    template_params: Optional[Dict] = None
    reply_to: Optional[str] = None

@dataclass
class WhatsAppResponse:
    """Resposta do WhatsApp"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    delivery_status: Optional[str] = None
    timestamp: Optional[str] = None

class WhatsAppService:
    """Serviço principal de integração WhatsApp"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = WhatsAppProvider(config.get("provider", "hybrid"))
        self.official_api_token = config.get("official_api_token")
        self.official_api_url = config.get("official_api_url")
        self.web_driver = None
        self.is_connected = False
        self.message_queue = []
        self.rate_limits = {
            "messages_per_minute": 30,
            "messages_per_hour": 1000,
            "last_message_time": 0
        }
        
    async def initialize(self) -> bool:
        """Inicializa o serviço WhatsApp"""
        try:
            if self.provider == WhatsAppProvider.OFFICIAL_API:
                return await self._init_official_api()
            elif self.provider == WhatsAppProvider.WEB_WHATSAPP:
                return await self._init_web_whatsapp()
            elif self.provider == WhatsAppProvider.HYBRID:
                return await self._init_hybrid()
            else:
                raise ValueError(f"Provedor não suportado: {self.provider}")
        except Exception as e:
            logger.error(f"Erro ao inicializar WhatsApp: {e}")
            return False
    
    async def _init_official_api(self) -> bool:
        """Inicializa API oficial do WhatsApp Business"""
        try:
            if not self.official_api_token:
                logger.error("Token da API oficial não configurado")
                return False
                
            # Testa conexão com API oficial
            headers = {
                "Authorization": f"Bearer {self.official_api_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.official_api_url}/v1/phone_numbers",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ API oficial WhatsApp conectada")
                self.is_connected = True
                return True
            else:
                logger.error(f"Erro ao conectar API oficial: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao inicializar API oficial: {e}")
            return False
    
    async def _init_web_whatsapp(self) -> bool:
        """Inicializa Web WhatsApp Wrapper"""
        try:
            # Configuração do Chrome
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Inicializa driver
            self.web_driver = webdriver.Chrome(options=chrome_options)
            self.web_driver.get("https://web.whatsapp.com")
            
            # Aguarda QR Code aparecer
            wait = WebDriverWait(self.web_driver, 60)
            qr_code_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "canvas"))
            )
            
            # Gera QR Code para exibição
            qr_code_data = qr_code_element.get_attribute("data-ref")
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_code_data)
            qr.make(fit=True)
            
            # Salva QR Code
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("whatsapp_qr.png")
            logger.info("📱 QR Code gerado: whatsapp_qr.png")
            
            # Aguarda conexão
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']"))
            )
            
            logger.info("✅ Web WhatsApp conectado")
            self.is_connected = True
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar Web WhatsApp: {e}")
            if self.web_driver:
                self.web_driver.quit()
            return False
    
    async def _init_hybrid(self) -> bool:
        """Inicializa estratégia híbrida"""
        try:
            # Tenta API oficial primeiro
            official_ok = await self._init_official_api()
            
            if not official_ok:
                logger.info("🔄 Fallback para Web WhatsApp")
                web_ok = await self._init_web_whatsapp()
                if web_ok:
                    self.provider = WhatsAppProvider.WEB_WHATSAPP
                    return True
                else:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar estratégia híbrida: {e}")
            return False
    
    async def send_message(self, message: WhatsAppMessage) -> WhatsAppResponse:
        """Envia mensagem WhatsApp"""
        try:
            # Verifica rate limits
            if not self._check_rate_limit():
                return WhatsAppResponse(
                    success=False,
                    error="Rate limit excedido"
                )
            
            # Escolhe provedor baseado no tipo de mensagem
            if message.template_name and self.provider == WhatsAppProvider.HYBRID:
                # Templates só funcionam com API oficial
                return await self._send_official_message(message)
            else:
                # Mensagem normal - usa provedor atual
                if self.provider == WhatsAppProvider.OFFICIAL_API:
                    return await self._send_official_message(message)
                elif self.provider == WhatsAppProvider.WEB_WHATSAPP:
                    return await self._send_web_message(message)
                else:
                    # Híbrido - tenta oficial primeiro
                    response = await self._send_official_message(message)
                    if not response.success:
                        logger.info("🔄 Fallback para Web WhatsApp")
                        return await self._send_web_message(message)
                    return response
                    
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            return WhatsAppResponse(
                success=False,
                error=str(e)
            )
    
    async def _send_official_message(self, message: WhatsAppMessage) -> WhatsAppResponse:
        """Envia mensagem via API oficial"""
        try:
            headers = {
                "Authorization": f"Bearer {self.official_api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": message.to,
                "type": message.message_type
            }
            
            if message.template_name:
                payload["template"] = {
                    "name": message.template_name,
                    "language": {"code": "pt_BR"}
                }
                if message.template_params:
                    payload["template"]["components"] = [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": value}
                                for value in message.template_params.values()
                            ]
                        }
                    ]
            else:
                payload["text"] = {"body": message.content}
            
            response = requests.post(
                f"{self.official_api_url}/v1/messages",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return WhatsAppResponse(
                    success=True,
                    message_id=data.get("messages", [{}])[0].get("id"),
                    delivery_status="sent"
                )
            else:
                return WhatsAppResponse(
                    success=False,
                    error=f"API Error: {response.status_code}"
                )
                
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem oficial: {e}")
            return WhatsAppResponse(
                success=False,
                error=str(e)
            )
    
    async def _send_web_message(self, message: WhatsAppMessage) -> WhatsAppResponse:
        """Envia mensagem via Web WhatsApp"""
        try:
            if not self.web_driver:
                return WhatsAppResponse(
                    success=False,
                    error="Web driver não inicializado"
                )
            
            # Formata número de telefone
            phone = self._format_phone_number(message.to)
            
            # Abre conversa
            chat_url = f"https://web.whatsapp.com/send?phone={phone}&text={message.content}"
            self.web_driver.get(chat_url)
            
            # Aguarda carregamento
            wait = WebDriverWait(self.web_driver, 30)
            send_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='send']"))
            )
            
            # Envia mensagem
            send_button.click()
            
            # Aguarda confirmação
            time.sleep(2)
            
            return WhatsAppResponse(
                success=True,
                message_id=f"web_{int(time.time())}",
                delivery_status="sent"
            )
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem web: {e}")
            return WhatsAppResponse(
                success=False,
                error=str(e)
            )
    
    def _format_phone_number(self, phone: str) -> str:
        """Formata número de telefone para WhatsApp"""
        # Remove caracteres especiais
        phone = ''.join(filter(str.isdigit, phone))
        
        # Adiciona código do país se necessário
        if not phone.startswith('55'):
            phone = '55' + phone
        
        return phone
    
    def _check_rate_limit(self) -> bool:
        """Verifica rate limits"""
        current_time = time.time()
        
        # Verifica limite por minuto
        if current_time - self.rate_limits["last_message_time"] < 60:
            if len(self.message_queue) >= self.rate_limits["messages_per_minute"]:
                return False
        
        # Verifica limite por hora
        hour_ago = current_time - 3600
        recent_messages = [msg for msg in self.message_queue if msg > hour_ago]
        
        if len(recent_messages) >= self.rate_limits["messages_per_hour"]:
            return False
        
        self.rate_limits["last_message_time"] = current_time
        self.message_queue.append(current_time)
        
        # Mantém apenas mensagens da última hora
        self.message_queue = [msg for msg in self.message_queue if msg > hour_ago]
        
        return True
    
    async def get_connection_status(self) -> Dict[str, Any]:
        """Retorna status da conexão"""
        return {
            "connected": self.is_connected,
            "provider": self.provider.value,
            "rate_limits": {
                "messages_per_minute": self.rate_limits["messages_per_minute"],
                "messages_per_hour": self.rate_limits["messages_per_hour"],
                "messages_sent": len(self.message_queue)
            }
        }
    
    async def disconnect(self):
        """Desconecta do WhatsApp"""
        if self.web_driver:
            self.web_driver.quit()
        self.is_connected = False
        logger.info("🔌 WhatsApp desconectado")

# Instância global do serviço
whatsapp_service = None

async def init_whatsapp_service(config: Dict[str, Any]) -> WhatsAppService:
    """Inicializa serviço WhatsApp global"""
    global whatsapp_service
    
    if whatsapp_service is None:
        whatsapp_service = WhatsAppService(config)
        await whatsapp_service.initialize()
    
    return whatsapp_service

async def get_whatsapp_service() -> WhatsAppService:
    """Retorna instância do serviço WhatsApp"""
    if whatsapp_service is None:
        raise RuntimeError("Serviço WhatsApp não inicializado")
    return whatsapp_service