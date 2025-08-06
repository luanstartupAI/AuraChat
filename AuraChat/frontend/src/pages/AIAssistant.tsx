import React, { useState, useEffect } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import Window from '../components/layout/Window';
import { useAuth } from '../contexts/AuthContext';
import '../styles/theme.css';

const AIAssistant: React.FC = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState<any[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [assistantSettings, setAssistantSettings] = useState({
    name: 'Aura AI',
    personality: 'Amigável e prestativa',
    knowledgeBase: 'Geral',
    model: 'GPT-4'
  });

  useEffect(() => {
    // Simulação de carregamento de dados
    const fetchAIData = async () => {
      try {
        // Em produção, isso seria uma chamada real à API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mensagem inicial do assistente
        setConversation([
          {
            id: 1,
            role: 'assistant',
            content: 'Olá! Sou a Aura AI, sua assistente virtual. Como posso ajudar você hoje?',
            timestamp: new Date().toISOString()
          }
        ]);
      } catch (error) {
        console.error('Erro ao carregar dados do assistente de IA:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchAIData();
  }, []);

  const handleSendMessage = async () => {
    if (!message.trim() || isProcessing) return;
    
    // Adicionar mensagem do usuário à conversa
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };
    
    setConversation(prev => [...prev, userMessage]);
    setMessage('');
    setIsProcessing(true);
    
    try {
      // Simular processamento da IA
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Gerar resposta simulada da IA
      let aiResponse = '';
      
      if (message.toLowerCase().includes('olá') || message.toLowerCase().includes('oi')) {
        aiResponse = 'Olá! Como posso ajudar você hoje?';
      } else if (message.toLowerCase().includes('ajuda')) {
        aiResponse = 'Estou aqui para ajudar! Posso responder perguntas, fornecer informações sobre produtos, ajudar com problemas técnicos ou encaminhar você para um atendente humano se necessário.';
      } else if (message.toLowerCase().includes('produto')) {
        aiResponse = 'Temos diversos produtos disponíveis. Para informações específicas sobre um produto, por favor forneça o nome ou código do produto que você está interessado.';
      } else if (message.toLowerCase().includes('preço')) {
        aiResponse = 'Para informações de preço, preciso saber qual produto específico você está interessado. Poderia me informar o nome ou código do produto?';
      } else if (message.toLowerCase().includes('entrega')) {
        aiResponse = 'Nosso prazo de entrega padrão é de 3 a 5 dias úteis, dependendo da sua localização. Para um prazo mais preciso, precisarei do seu CEP.';
      } else if (message.toLowerCase().includes('problema') || message.toLowerCase().includes('erro')) {
        aiResponse = 'Sinto muito pelo inconveniente. Poderia descrever o problema com mais detalhes para que eu possa ajudar melhor? Ou prefere ser transferido para um atendente humano?';
      } else if (message.toLowerCase().includes('humano') || message.toLowerCase().includes('atendente')) {
        aiResponse = 'Entendo que você prefira falar com um humano. Vou transferir você para um de nossos atendentes. Por favor, aguarde um momento.';
      } else {
        aiResponse = 'Obrigado por sua mensagem. Estou processando sua solicitação e farei o possível para ajudar. Há algo específico que você gostaria de saber?';
      }
      
      // Adicionar resposta da IA à conversa
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: aiResponse,
        timestamp: new Date().toISOString()
      };
      
      setConversation(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Erro ao processar mensagem:', error);
      
      // Mensagem de erro
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.',
        timestamp: new Date().toISOString(),
        error: true
      };
      
      setConversation(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const updateAssistantSetting = (key: string, value: string) => {
    setAssistantSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="leopard-app-container">
      <Sidebar />
      
      <div className="leopard-main-content">
        <Header 
          title="Assistente de IA" 
          username={user?.name} 
          userAvatar={user?.avatar}
        />
        
        <div className="leopard-ai-container">
          {isLoading ? (
            <div className="leopard-loading">Carregando...</div>
          ) : (
            <>
              <div className="leopard-ai-sidebar">
                <Window title="Configurações" className="leopard-ai-settings-window">
                  <div className="leopard-ai-settings">
                    <div className="leopard-ai-setting">
                      <label>Nome do Assistente:</label>
                      <input
                        type="text"
                        value={assistantSettings.name}
                        onChange={(e) => updateAssistantSetting('name', e.target.value)}
                        className="leopard-input"
                      />
                    </div>
                    
                    <div className="leopard-ai-setting">
                      <label>Personalidade:</label>
                      <select
                        value={assistantSettings.personality}
                        onChange={(e) => updateAssistantSetting('personality', e.target.value)}
                        className="leopard-select"
                      >
                        <option value="Amigável e prestativa">Amigável e prestativa</option>
                        <option value="Profissional e direta">Profissional e direta</option>
                        <option value="Entusiasta e energética">Entusiasta e energética</option>
                        <option value="Calma e paciente">Calma e paciente</option>
                      </select>
                    </div>
                    
                    <div className="leopard-ai-setting">
                      <label>Base de Conhecimento:</label>
                      <select
                        value={assistantSettings.knowledgeBase}
                        onChange={(e) => updateAssistantSetting('knowledgeBase', e.target.value)}
                        className="leopard-select"
                      >
                        <option value="Geral">Geral</option>
                        <option value="Suporte Técnico">Suporte Técnico</option>
                        <option value="Vendas">Vendas</option>
                        <option value="FAQ">FAQ</option>
                      </select>
                    </div>
                    
                    <div className="leopard-ai-setting">
                      <label>Modelo:</label>
                      <select
                        value={assistantSettings.model}
                        onChange={(e) => updateAssistantSetting('model', e.target.value)}
                        className="leopard-select"
                      >
                        <option value="GPT-4">GPT-4</option>
                        <option value="GPT-3.5">GPT-3.5</option>
                        <option value="Claude">Claude</option>
                        <option value="Personalizado">Personalizado</option>
                      </select>
                    </div>
                  </div>
                  
                  <div className="leopard-ai-settings-actions">
                    <button className="leopard-button leopard-button-primary">
                      Salvar Configurações
                    </button>
                  </div>
                </Window>
                
                <Window title="Treinamento" className="leopard-ai-training-window">
                  <div className="leopard-ai-training">
                    <div className="leopard-ai-training-status">
                      <div className="leopard-ai-training-status-icon">
                        <i className="ph-check-circle"></i>
                      </div>
                      <div className="leopard-ai-training-status-text">
                        <div className="leopard-ai-training-status-title">Modelo Treinado</div>
                        <div className="leopard-ai-training-status-info">Última atualização: 01/06/2025</div>
                      </div>
                    </div>
                    
                    <div className="leopard-ai-training-metrics">
                      <div className="leopard-ai-training-metric">
                        <div className="leopard-ai-training-metric-value">98%</div>
                        <div className="leopard-ai-training-metric-label">Precisão</div>
                      </div>
                      
                      <div className="leopard-ai-training-metric">
                        <div className="leopard-ai-training-metric-value">1.2s</div>
                        <div className="leopard-ai-training-metric-label">Tempo de Resposta</div>
                      </div>
                      
                      <div className="leopard-ai-training-metric">
                        <div className="leopard-ai-training-metric-value">5,432</div>
                        <div className="leopard-ai-training-metric-label">Exemplos</div>
                      </div>
                    </div>
                    
                    <div className="leopard-ai-training-actions">
                      <button className="leopard-button">
                        <i className="ph-arrows-clockwise"></i> Treinar Modelo
                      </button>
                      <button className="leopard-button">
                        <i className="ph-upload"></i> Importar Dados
                      </button>
                    </div>
                  </div>
                </Window>
              </div>
              
              <div className="leopard-ai-chat">
                <Window title={assistantSettings.name} className="leopard-ai-chat-window">
                  <div className="leopard-ai-chat-messages">
                    {conversation.map((msg) => (
                      <div 
                        key={msg.id} 
                        className={`leopard-ai-message ${msg.role === 'user' ? 'user' : 'assistant'} ${msg.error ? 'error' : ''}`}
                      >
                        <div className="leopard-ai-message-avatar">
                          {msg.role === 'user' ? (
                            user?.name?.charAt(0) || 'U'
                          ) : (
                            <i className="ph-robot"></i>
                          )}
                        </div>
                        
                        <div className="leopard-ai-message-content">
                          <div className="leopard-ai-message-text">
                            {msg.content}
                          </div>
                          <div className="leopard-ai-message-time">
                            {formatTimestamp(msg.timestamp)}
                          </div>
                        </div>
                      </div>
                    ))}
                    
                    {isProcessing && (
                      <div className="leopard-ai-message assistant">
                        <div className="leopard-ai-message-avatar">
                          <i className="ph-robot"></i>
                        </div>
                        
                        <div className="leopard-ai-message-content">
                          <div className="leopard-ai-message-text">
                            <div className="leopard-ai-typing-indicator">
                              <span></span>
                              <span></span>
                              <span></span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="leopard-ai-chat-input-container">
                    <textarea 
                      className="leopard-ai-chat-input" 
                      placeholder="Digite sua mensagem..."
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      disabled={isProcessing}
                    ></textarea>
                    
                    <button 
                      className="leopard-button leopard-button-primary leopard-ai-send-button"
                      onClick={handleSendMessage}
                      disabled={!message.trim() || isProcessing}
                    >
                      <i className="ph-paper-plane-right"></i>
                    </button>
                  </div>
                </Window>
              </div>
            </>
          )}
        </div>
      </div>
      
      <div className="leopard-dock">
        <div className="leopard-dock-item">
          <img src="/logo.png" alt="Aura" />
        </div>
        <div className="leopard-dock-item">
          <i className="ph-chat-centered-text ph-fill"></i>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-robot ph-fill"></i>
          <div className="leopard-dock-indicator"></div>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-users ph-fill"></i>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-gear ph-fill"></i>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
