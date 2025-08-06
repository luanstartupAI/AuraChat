import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  MessageSquare, 
  Send, 
  Phone, 
  Wifi, 
  WifiOff, 
  QrCode,
  Settings,
  Users,
  FileText,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react';
import apiService from '@/services/api';

interface WhatsAppStatus {
  connected: boolean;
  provider?: string;
  rate_limits?: {
    messages_per_minute: number;
    messages_per_hour: number;
    messages_sent: number;
  };
  error?: string;
}

interface WhatsAppTemplate {
  name: string;
  language: string;
  category: string;
  components: Array<{
    type: string;
    text: string;
  }>;
}

interface WhatsAppMessage {
  id: string;
  content: string;
  message_type: string;
  sender_type: string;
  delivery_status: string;
  created_at: string;
  sent_at?: string;
  media_url?: string;
  metadata?: any;
}

const WhatsApp: React.FC = () => {
  const [status, setStatus] = useState<WhatsAppStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [phone, setPhone] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [templateParams, setTemplateParams] = useState<string[]>(['']);
  const [templates, setTemplates] = useState<WhatsAppTemplate[]>([]);
  const [recentMessages, setRecentMessages] = useState<WhatsAppMessage[]>([]);
  const [showQR, setShowQR] = useState(false);
  const [qrCodeUrl, setQrCodeUrl] = useState('');

  // Carregar status inicial
  useEffect(() => {
    loadWhatsAppStatus();
    loadTemplates();
  }, []);

  const loadWhatsAppStatus = async () => {
    try {
      setLoading(true);
      const response = await apiService.request('/whatsapp/status');
      setStatus(response);
    } catch (error) {
      console.error('Erro ao carregar status WhatsApp:', error);
      setStatus({
        connected: false,
        error: 'Erro ao conectar com WhatsApp'
      });
    } finally {
      setLoading(false);
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await apiService.request('/whatsapp/templates');
      setTemplates(response.templates || []);
    } catch (error) {
      console.error('Erro ao carregar templates:', error);
    }
  };

  const connectWhatsApp = async (provider: string = 'hybrid') => {
    try {
      setLoading(true);
      const response = await apiService.request('/whatsapp/connect', {
        method: 'POST',
        body: JSON.stringify({ provider })
      });
      
      if (response.success) {
        await loadWhatsAppStatus();
        if (provider === 'web_whatsapp') {
          setShowQR(true);
          setQrCodeUrl('/whatsapp_qr.png');
        }
      }
    } catch (error) {
      console.error('Erro ao conectar WhatsApp:', error);
    } finally {
      setLoading(false);
    }
  };

  const disconnectWhatsApp = async () => {
    try {
      setLoading(true);
      await apiService.request('/whatsapp/disconnect', {
        method: 'POST'
      });
      await loadWhatsAppStatus();
      setShowQR(false);
    } catch (error) {
      console.error('Erro ao desconectar WhatsApp:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!message.trim() && !selectedTemplate) return;

    try {
      setLoading(true);
      
      const payload: any = {
        to: phone,
        content: message,
        message_type: 'text'
      };

      if (selectedTemplate) {
        payload.template_name = selectedTemplate;
        payload.template_params = templateParams.reduce((acc, param, index) => {
          acc[`${index + 1}`] = param;
          return acc;
        }, {} as Record<string, string>);
      }

      const response = await apiService.request('/whatsapp/send', {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      if (response.success) {
        setMessage('');
        setPhone('');
        setSelectedTemplate('');
        setTemplateParams(['']);
        // Recarregar mensagens recentes
        loadRecentMessages();
      }
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRecentMessages = async () => {
    try {
      // Em um sistema real, buscaríamos mensagens de um chat específico
      // Por enquanto, vamos simular algumas mensagens
      setRecentMessages([
        {
          id: '1',
          content: 'Olá! Como posso ajudar?',
          message_type: 'text',
          sender_type: 'user',
          delivery_status: 'sent',
          created_at: new Date().toISOString(),
          sent_at: new Date().toISOString()
        }
      ]);
    } catch (error) {
      console.error('Erro ao carregar mensagens:', error);
    }
  };

  const handleTemplateChange = (templateName: string) => {
    setSelectedTemplate(templateName);
    const template = templates.find(t => t.name === templateName);
    if (template) {
      // Contar variáveis no template
      const bodyComponent = template.components.find(c => c.type === 'BODY');
      if (bodyComponent) {
        const variableCount = (bodyComponent.text.match(/\{\{(\d+)\}\}/g) || []).length;
        setTemplateParams(Array(variableCount).fill(''));
      }
    }
  };

  const updateTemplateParam = (index: number, value: string) => {
    const newParams = [...templateParams];
    newParams[index] = value;
    setTemplateParams(newParams);
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">WhatsApp</h1>
          <p className="text-gray-600">Gerencie suas conexões e envie mensagens</p>
        </div>
        <div className="flex items-center space-x-2">
          {status?.connected ? (
            <Badge variant="default" className="bg-green-100 text-green-800">
              <Wifi className="w-4 h-4 mr-1" />
              Conectado
            </Badge>
          ) : (
            <Badge variant="secondary" className="bg-red-100 text-red-800">
              <WifiOff className="w-4 h-4 mr-1" />
              Desconectado
            </Badge>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Status e Conexão */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Phone className="w-5 h-5 mr-2" />
              Status da Conexão
            </CardTitle>
            <CardDescription>
              Gerencie sua conexão com o WhatsApp
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {status?.error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{status.error}</AlertDescription>
              </Alert>
            )}

            {status?.rate_limits && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Mensagens/min:</span>
                  <span>{status.rate_limits.messages_sent}/{status.rate_limits.messages_per_minute}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Mensagens/hora:</span>
                  <span>{status.rate_limits.messages_sent}/{status.rate_limits.messages_per_hour}</span>
                </div>
              </div>
            )}

            <div className="flex space-x-2">
              {!status?.connected ? (
                <>
                  <Button 
                    onClick={() => connectWhatsApp('official_api')}
                    disabled={loading}
                    className="flex-1"
                  >
                    API Oficial
                  </Button>
                  <Button 
                    onClick={() => connectWhatsApp('web_whatsapp')}
                    disabled={loading}
                    variant="outline"
                    className="flex-1"
                  >
                    Web WhatsApp
                  </Button>
                </>
              ) : (
                <Button 
                  onClick={disconnectWhatsApp}
                  disabled={loading}
                  variant="destructive"
                  className="w-full"
                >
                  Desconectar
                </Button>
              )}
            </div>

            {showQR && (
              <div className="text-center">
                <p className="text-sm text-gray-600 mb-2">
                  Escaneie o QR Code para conectar
                </p>
                <img 
                  src={qrCodeUrl} 
                  alt="QR Code WhatsApp" 
                  className="mx-auto border rounded-lg"
                  style={{ maxWidth: '200px' }}
                />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Envio de Mensagens */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Send className="w-5 h-5 mr-2" />
              Enviar Mensagem
            </CardTitle>
            <CardDescription>
              Envie mensagens para seus contatos
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Número de Telefone</label>
              <Input
                placeholder="+55 11 99999-9999"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="mt-1"
              />
            </div>

            <div>
              <label className="text-sm font-medium">Tipo de Mensagem</label>
              <div className="flex space-x-2 mt-1">
                <Button
                  variant={!selectedTemplate ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedTemplate('')}
                >
                  Texto Livre
                </Button>
                <Button
                  variant={selectedTemplate ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedTemplate('welcome_message')}
                >
                  Template
                </Button>
              </div>
            </div>

            {!selectedTemplate ? (
              <div>
                <label className="text-sm font-medium">Mensagem</label>
                <Textarea
                  placeholder="Digite sua mensagem..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  className="mt-1"
                  rows={4}
                />
              </div>
            ) : (
              <div className="space-y-2">
                <label className="text-sm font-medium">Template: {selectedTemplate}</label>
                {templateParams.map((param, index) => (
                  <Input
                    key={index}
                    placeholder={`Parâmetro ${index + 1}`}
                    value={param}
                    onChange={(e) => updateTemplateParam(index, e.target.value)}
                    className="mt-1"
                  />
                ))}
              </div>
            )}

            <Button 
              onClick={sendMessage}
              disabled={loading || (!message.trim() && !selectedTemplate)}
              className="w-full"
            >
              {loading ? 'Enviando...' : 'Enviar Mensagem'}
            </Button>
          </CardContent>
        </Card>

        {/* Templates */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="w-5 h-5 mr-2" />
              Templates
            </CardTitle>
            <CardDescription>
              Templates aprovados do WhatsApp Business
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {templates.map((template) => (
                <div
                  key={template.name}
                  className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50"
                  onClick={() => handleTemplateChange(template.name)}
                >
                  <div className="font-medium">{template.name}</div>
                  <div className="text-sm text-gray-600">{template.category}</div>
                  <div className="text-xs text-gray-500">{template.language}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Mensagens Recentes */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <MessageSquare className="w-5 h-5 mr-2" />
            Mensagens Recentes
          </CardTitle>
          <CardDescription>
            Histórico das últimas mensagens enviadas
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recentMessages.map((msg) => (
              <div key={msg.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                <div className="flex-shrink-0">
                  {msg.delivery_status === 'sent' ? (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  ) : msg.delivery_status === 'failed' ? (
                    <AlertCircle className="w-5 h-5 text-red-500" />
                  ) : (
                    <Clock className="w-5 h-5 text-yellow-500" />
                  )}
                </div>
                <div className="flex-1">
                  <div className="font-medium">{msg.content}</div>
                  <div className="text-sm text-gray-500">
                    {new Date(msg.created_at).toLocaleString()}
                  </div>
                </div>
                <Badge variant="outline">
                  {msg.delivery_status}
                </Badge>
              </div>
            ))}
            {recentMessages.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                Nenhuma mensagem enviada ainda
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default WhatsApp;