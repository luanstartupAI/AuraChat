import React, { useState, useEffect } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import Window from '../components/layout/Window';
import { useAuth } from '../contexts/AuthContext';
import '../styles/theme.css';

const Chat: React.FC = () => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<any[]>([]);
  const [currentConversation, setCurrentConversation] = useState<any>(null);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulação de carregamento de dados
    const fetchChatData = async () => {
      try {
        // Em produção, isso seria uma chamada real à API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockConversations = [
          {
            id: 1,
            contact: {
              id: 101,
              name: 'João Silva',
              phone: '+5511987654321',
              avatar: null,
              status: 'online'
            },
            unread: 2,
            lastMessage: {
              id: 1001,
              content: 'Olá, preciso de ajuda com meu pedido',
              timestamp: '2025-06-02T10:45:00Z',
              sender: 'contact'
            },
            messages: [
              {
                id: 1001,
                content: 'Olá, preciso de ajuda com meu pedido',
                timestamp: '2025-06-02T10:45:00Z',
                sender: 'contact'
              },
              {
                id: 1002,
                content: 'Claro, João! Em que posso ajudar?',
                timestamp: '2025-06-02T10:47:00Z',
                sender: 'user'
              },
              {
                id: 1003,
                content: 'Meu pedido #12345 ainda não chegou',
                timestamp: '2025-06-02T10:48:00Z',
                sender: 'contact'
              },
              {
                id: 1004,
                content: 'Vou verificar o status do seu pedido agora mesmo',
                timestamp: '2025-06-02T10:50:00Z',
                sender: 'user'
              }
            ]
          },
          {
            id: 2,
            contact: {
              id: 102,
              name: 'Maria Oliveira',
              phone: '+5511976543210',
              avatar: null,
              status: 'offline'
            },
            unread: 0,
            lastMessage: {
              id: 2001,
              content: 'Obrigada pelo atendimento!',
              timestamp: '2025-06-02T09:30:00Z',
              sender: 'contact'
            },
            messages: [
              {
                id: 2001,
                content: 'Obrigada pelo atendimento!',
                timestamp: '2025-06-02T09:30:00Z',
                sender: 'contact'
              },
              {
                id: 2002,
                content: 'Por nada, Maria! Estamos sempre à disposição.',
                timestamp: '2025-06-02T09:32:00Z',
                sender: 'user'
              }
            ]
          },
          {
            id: 3,
            contact: {
              id: 103,
              name: 'Pedro Santos',
              phone: '+5511965432109',
              avatar: null,
              status: 'online'
            },
            unread: 1,
            lastMessage: {
              id: 3001,
              content: 'Quando meu produto será entregue?',
              timestamp: '2025-06-01T15:20:00Z',
              sender: 'contact'
            },
            messages: [
              {
                id: 3001,
                content: 'Quando meu produto será entregue?',
                timestamp: '2025-06-01T15:20:00Z',
                sender: 'contact'
              }
            ]
          }
        ];
        
        setConversations(mockConversations);
        setCurrentConversation(mockConversations[0]);
      } catch (error) {
        console.error('Erro ao carregar dados do chat:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchChatData();
  }, []);

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    if (date.toDateString() === today.toDateString()) {
      return 'Hoje';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Ontem';
    } else {
      return date.toLocaleDateString();
    }
  };

  const handleSendMessage = () => {
    if (!message.trim() || !currentConversation) return;
    
    const newMessage = {
      id: Date.now(),
      content: message,
      timestamp: new Date().toISOString(),
      sender: 'user'
    };
    
    // Atualiza a conversa atual com a nova mensagem
    const updatedConversation = {
      ...currentConversation,
      messages: [...currentConversation.messages, newMessage],
      lastMessage: newMessage
    };
    
    // Atualiza a lista de conversas
    const updatedConversations = conversations.map(conv => 
      conv.id === currentConversation.id ? updatedConversation : conv
    );
    
    setCurrentConversation(updatedConversation);
    setConversations(updatedConversations);
    setMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const selectConversation = (conversation: any) => {
    // Marca mensagens como lidas
    if (conversation.unread > 0) {
      const updatedConversation = {
        ...conversation,
        unread: 0
      };
      
      const updatedConversations = conversations.map(conv => 
        conv.id === conversation.id ? updatedConversation : conv
      );
      
      setConversations(updatedConversations);
      setCurrentConversation(updatedConversation);
    } else {
      setCurrentConversation(conversation);
    }
  };

  return (
    <div className="leopard-app-container">
      <Sidebar />
      
      <div className="leopard-main-content">
        <Header 
          title="Chat" 
          username={user?.name} 
          userAvatar={user?.avatar}
        />
        
        <div className="leopard-chat-container">
          {isLoading ? (
            <div className="leopard-loading">Carregando...</div>
          ) : (
            <>
              <div className="leopard-chat-sidebar">
                <div className="leopard-chat-search">
                  <input 
                    type="text" 
                    placeholder="Buscar conversas..." 
                    className="leopard-input"
                  />
                </div>
                
                <div className="leopard-chat-conversations">
                  {conversations.map(conversation => (
                    <div 
                      key={conversation.id} 
                      className={`leopard-chat-conversation-item ${currentConversation?.id === conversation.id ? 'active' : ''}`}
                      onClick={() => selectConversation(conversation)}
                    >
                      <div className="leopard-chat-avatar">
                        {conversation.contact.name.charAt(0)}
                        <span className={`leopard-chat-status ${conversation.contact.status}`}></span>
                      </div>
                      
                      <div className="leopard-chat-conversation-content">
                        <div className="leopard-chat-conversation-header">
                          <div className="leopard-chat-name">{conversation.contact.name}</div>
                          <div className="leopard-chat-time">
                            {formatDate(conversation.lastMessage.timestamp)}
                          </div>
                        </div>
                        
                        <div className="leopard-chat-last-message">
                          {conversation.lastMessage.content}
                        </div>
                      </div>
                      
                      {conversation.unread > 0 && (
                        <div className="leopard-chat-unread">{conversation.unread}</div>
                      )}
                    </div>
                  ))}
                </div>
                
                <div className="leopard-chat-sidebar-actions">
                  <button className="leopard-button">
                    <i className="ph-plus"></i> Nova Conversa
                  </button>
                </div>
              </div>
              
              <div className="leopard-chat-main">
                {currentConversation ? (
                  <>
                    <div className="leopard-chat-header">
                      <div className="leopard-chat-contact-info">
                        <div className="leopard-chat-avatar">
                          {currentConversation.contact.name.charAt(0)}
                          <span className={`leopard-chat-status ${currentConversation.contact.status}`}></span>
                        </div>
                        
                        <div className="leopard-chat-contact-details">
                          <div className="leopard-chat-contact-name">
                            {currentConversation.contact.name}
                          </div>
                          <div className="leopard-chat-contact-phone">
                            {currentConversation.contact.phone}
                          </div>
                        </div>
                      </div>
                      
                      <div className="leopard-chat-actions">
                        <button className="leopard-button-icon">
                          <i className="ph-phone"></i>
                        </button>
                        <button className="leopard-button-icon">
                          <i className="ph-video-camera"></i>
                        </button>
                        <button className="leopard-button-icon">
                          <i className="ph-info"></i>
                        </button>
                      </div>
                    </div>
                    
                    <div className="leopard-chat-messages">
                      {currentConversation.messages.map((msg: any) => (
                        <div 
                          key={msg.id} 
                          className={`leopard-chat-message ${msg.sender === 'user' ? 'sent' : 'received'}`}
                        >
                          <div className="leopard-chat-message-content">
                            {msg.content}
                          </div>
                          <div className="leopard-chat-message-time">
                            {formatTimestamp(msg.timestamp)}
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    <div className="leopard-chat-input-container">
                      <div className="leopard-chat-input-actions">
                        <button className="leopard-button-icon">
                          <i className="ph-smiley"></i>
                        </button>
                        <button className="leopard-button-icon">
                          <i className="ph-paperclip"></i>
                        </button>
                      </div>
                      
                      <textarea 
                        className="leopard-chat-input" 
                        placeholder="Digite sua mensagem..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                      ></textarea>
                      
                      <button 
                        className="leopard-button-icon leopard-send-button"
                        onClick={handleSendMessage}
                        disabled={!message.trim()}
                      >
                        <i className="ph-paper-plane-right"></i>
                      </button>
                    </div>
                  </>
                ) : (
                  <div className="leopard-chat-empty">
                    <div className="leopard-chat-empty-icon">
                      <i className="ph-chat-centered-text"></i>
                    </div>
                    <div className="leopard-chat-empty-text">
                      Selecione uma conversa para começar
                    </div>
                  </div>
                )}
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
          <div className="leopard-dock-indicator"></div>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-users ph-fill"></i>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-chart-line ph-fill"></i>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-gear ph-fill"></i>
        </div>
      </div>
    </div>
  );
};

export default Chat;
