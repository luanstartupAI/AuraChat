import React, { useState, useEffect } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import Window from '../components/layout/Window';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';
import '../styles/theme.css';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalContacts: 0,
    activeChats: 0,
    pendingTasks: 0,
    completedFlows: 0
  });
  
  const [recentChats, setRecentChats] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Buscar dados reais da API
        const [chatStats, contactsData] = await Promise.all([
          apiService.getChatStats(),
          apiService.getContacts(1, 5) // Buscar apenas 5 contatos para o dashboard
        ]);
        
        setStats({
          totalContacts: contactsData.pagination.total,
          activeChats: chatStats.active_conversations,
          pendingTasks: 0, // TODO: Implementar quando tivermos Kanban
          completedFlows: 0 // TODO: Implementar quando tivermos Fluxos
        });
        
        // Converter contatos para formato de conversas recentes
        const recentChatsData = contactsData.contacts.map(contact => ({
          id: contact.id,
          name: contact.name,
          lastMessage: 'Nova conversa iniciada',
          time: new Date(contact.created_at).toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
          }),
          unread: 0
        }));
        
        setRecentChats(recentChatsData);
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        // Fallback para dados mock em caso de erro
        setStats({
          totalContacts: 0,
          activeChats: 0,
          pendingTasks: 0,
          completedFlows: 0
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);

  return (
    <div className="leopard-app-container">
      <Sidebar />
      
      <div className="leopard-main-content">
        <Header 
          title="Dashboard" 
          username={user?.name} 
          userAvatar={user?.avatar}
          notificationsCount={5}
        />
        
        <div className="leopard-dashboard-content">
          {isLoading ? (
            <div className="leopard-loading">Carregando...</div>
          ) : (
            <>
              <div className="leopard-dashboard-stats">
                <Window title="Estatísticas" className="leopard-stats-window">
                  <div className="leopard-stats-grid">
                    <div className="leopard-stat-card">
                      <div className="leopard-stat-icon">
                        <i className="ph-users"></i>
                      </div>
                      <div className="leopard-stat-content">
                        <div className="leopard-stat-value">{stats.totalContacts}</div>
                        <div className="leopard-stat-label">Contatos</div>
                      </div>
                    </div>
                    
                    <div className="leopard-stat-card">
                      <div className="leopard-stat-icon">
                        <i className="ph-chat-circle-dots"></i>
                      </div>
                      <div className="leopard-stat-content">
                        <div className="leopard-stat-value">{stats.activeChats}</div>
                        <div className="leopard-stat-label">Conversas ativas</div>
                      </div>
                    </div>
                    
                    <div className="leopard-stat-card">
                      <div className="leopard-stat-icon">
                        <i className="ph-clipboard-text"></i>
                      </div>
                      <div className="leopard-stat-content">
                        <div className="leopard-stat-value">{stats.pendingTasks}</div>
                        <div className="leopard-stat-label">Tarefas pendentes</div>
                      </div>
                    </div>
                    
                    <div className="leopard-stat-card">
                      <div className="leopard-stat-icon">
                        <i className="ph-flow-arrow"></i>
                      </div>
                      <div className="leopard-stat-content">
                        <div className="leopard-stat-value">{stats.completedFlows}</div>
                        <div className="leopard-stat-label">Fluxos completados</div>
                      </div>
                    </div>
                  </div>
                </Window>
              </div>
              
              <div className="leopard-dashboard-recent">
                <Window title="Conversas Recentes" className="leopard-recent-window">
                  <div className="leopard-recent-chats">
                    {recentChats.map((chat: any) => (
                      <div key={chat.id} className="leopard-chat-item">
                        <div className="leopard-chat-avatar">
                          {chat.name.charAt(0)}
                        </div>
                        <div className="leopard-chat-content">
                          <div className="leopard-chat-header">
                            <div className="leopard-chat-name">{chat.name}</div>
                            <div className="leopard-chat-time">{chat.time}</div>
                          </div>
                          <div className="leopard-chat-message">{chat.lastMessage}</div>
                        </div>
                        {chat.unread > 0 && (
                          <div className="leopard-chat-unread">{chat.unread}</div>
                        )}
                      </div>
                    ))}
                  </div>
                </Window>
              </div>
              
              <div className="leopard-dashboard-activity">
                <Window title="Atividade Recente" className="leopard-activity-window">
                  <div className="leopard-activity-timeline">
                    <div className="leopard-timeline-item">
                      <div className="leopard-timeline-icon">
                        <i className="ph-user-plus"></i>
                      </div>
                      <div className="leopard-timeline-content">
                        <div className="leopard-timeline-title">Novo contato adicionado</div>
                        <div className="leopard-timeline-description">Maria Oliveira foi adicionada à sua lista de contatos</div>
                        <div className="leopard-timeline-time">Há 2 horas</div>
                      </div>
                    </div>
                    
                    <div className="leopard-timeline-item">
                      <div className="leopard-timeline-icon">
                        <i className="ph-check-circle"></i>
                      </div>
                      <div className="leopard-timeline-content">
                        <div className="leopard-timeline-title">Tarefa concluída</div>
                        <div className="leopard-timeline-description">Enviar orçamento para cliente XYZ</div>
                        <div className="leopard-timeline-time">Há 4 horas</div>
                      </div>
                    </div>
                    
                    <div className="leopard-timeline-item">
                      <div className="leopard-timeline-icon">
                        <i className="ph-broadcast"></i>
                      </div>
                      <div className="leopard-timeline-content">
                        <div className="leopard-timeline-title">Campanha enviada</div>
                        <div className="leopard-timeline-description">Promoção de Junho enviada para 250 contatos</div>
                        <div className="leopard-timeline-time">Ontem às 15:30</div>
                      </div>
                    </div>
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

export default Dashboard;
