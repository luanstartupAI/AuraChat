import React, { useState, useEffect } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import Window from '../components/layout/Window';
import { useAuth } from '../contexts/AuthContext';
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
    // Simulação de carregamento de dados
    const fetchDashboardData = async () => {
      try {
        // Em produção, isso seria uma chamada real à API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setStats({
          totalContacts: 1248,
          activeChats: 37,
          pendingTasks: 12,
          completedFlows: 89
        });
        
        setRecentChats([
          { id: 1, name: 'João Silva', lastMessage: 'Olá, preciso de ajuda com meu pedido', time: '10:45', unread: 2 },
          { id: 2, name: 'Maria Oliveira', lastMessage: 'Obrigada pelo atendimento!', time: '09:30', unread: 0 },
          { id: 3, name: 'Pedro Santos', lastMessage: 'Quando meu produto será entregue?', time: 'Ontem', unread: 1 },
          { id: 4, name: 'Ana Costa', lastMessage: 'Vou verificar e te retorno', time: 'Ontem', unread: 0 },
          { id: 5, name: 'Carlos Mendes', lastMessage: 'Preciso cancelar minha assinatura', time: 'Seg', unread: 3 }
        ]);
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
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
