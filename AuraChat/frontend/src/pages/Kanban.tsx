import React, { useState, useEffect } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import Window from '../components/layout/Window';
import { useAuth } from '../contexts/AuthContext';
import '../styles/theme.css';

const Kanban: React.FC = () => {
  const { user } = useAuth();
  const [boards, setBoards] = useState<any[]>([]);
  const [currentBoard, setCurrentBoard] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [draggedCard, setDraggedCard] = useState<any>(null);
  const [dragOverColumn, setDragOverColumn] = useState<string | null>(null);

  useEffect(() => {
    // Simulação de carregamento de dados
    const fetchKanbanData = async () => {
      try {
        // Em produção, isso seria uma chamada real à API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockBoards = [
          {
            id: 1,
            name: 'Atendimento ao Cliente',
            columns: [
              {
                id: 'col-1',
                title: 'Novos',
                cards: [
                  { id: 'card-1', title: 'Problema com entrega', description: 'Cliente não recebeu o produto', labels: ['urgente'], assignee: 'Maria' },
                  { id: 'card-2', title: 'Dúvida sobre produto', description: 'Cliente com dúvidas sobre funcionalidades', labels: ['suporte'], assignee: 'João' }
                ]
              },
              {
                id: 'col-2',
                title: 'Em Andamento',
                cards: [
                  { id: 'card-3', title: 'Solicitação de reembolso', description: 'Cliente deseja cancelar compra', labels: ['financeiro'], assignee: 'Ana' },
                  { id: 'card-4', title: 'Troca de produto', description: 'Produto com defeito', labels: ['logística'], assignee: 'Pedro' }
                ]
              },
              {
                id: 'col-3',
                title: 'Concluídos',
                cards: [
                  { id: 'card-5', title: 'Atualização de cadastro', description: 'Cliente atualizou informações', labels: ['admin'], assignee: 'Carlos' },
                  { id: 'card-6', title: 'Elogio ao atendimento', description: 'Cliente satisfeito com suporte', labels: ['feedback'], assignee: 'Maria' }
                ]
              }
            ]
          },
          {
            id: 2,
            name: 'Desenvolvimento de Produto',
            columns: [
              {
                id: 'col-4',
                title: 'Backlog',
                cards: [
                  { id: 'card-7', title: 'Integração com API', description: 'Conectar com serviço externo', labels: ['técnico'], assignee: 'Lucas' },
                  { id: 'card-8', title: 'Melhorar performance', description: 'Otimizar carregamento de página', labels: ['técnico'], assignee: 'Julia' }
                ]
              },
              {
                id: 'col-5',
                title: 'Em Desenvolvimento',
                cards: [
                  { id: 'card-9', title: 'Nova interface', description: 'Redesign da tela principal', labels: ['design'], assignee: 'Mariana' }
                ]
              },
              {
                id: 'col-6',
                title: 'Testes',
                cards: [
                  { id: 'card-10', title: 'Testes de integração', description: 'Verificar fluxos completos', labels: ['qa'], assignee: 'Rafael' }
                ]
              },
              {
                id: 'col-7',
                title: 'Concluído',
                cards: [
                  { id: 'card-11', title: 'Correção de bugs', description: 'Resolver problemas reportados', labels: ['bug'], assignee: 'Felipe' }
                ]
              }
            ]
          }
        ];
        
        setBoards(mockBoards);
        setCurrentBoard(mockBoards[0]);
      } catch (error) {
        console.error('Erro ao carregar dados do kanban:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchKanbanData();
  }, []);

  const handleDragStart = (card: any) => {
    setDraggedCard(card);
  };

  const handleDragOver = (e: React.DragEvent, columnId: string) => {
    e.preventDefault();
    setDragOverColumn(columnId);
  };

  const handleDrop = (e: React.DragEvent, columnId: string) => {
    e.preventDefault();
    
    if (!draggedCard) return;
    
    // Cria uma cópia do quadro atual
    const updatedBoard = { ...currentBoard };
    
    // Encontra a coluna de origem e remove o card
    let sourceColumnIndex = -1;
    let cardIndex = -1;
    
    updatedBoard.columns.forEach((column: any, colIndex: number) => {
      const index = column.cards.findIndex((c: any) => c.id === draggedCard.id);
      if (index !== -1) {
        sourceColumnIndex = colIndex;
        cardIndex = index;
      }
    });
    
    if (sourceColumnIndex === -1 || cardIndex === -1) return;
    
    // Remove o card da coluna de origem
    const card = updatedBoard.columns[sourceColumnIndex].cards.splice(cardIndex, 1)[0];
    
    // Encontra a coluna de destino e adiciona o card
    const targetColumnIndex = updatedBoard.columns.findIndex((col: any) => col.id === columnId);
    if (targetColumnIndex !== -1) {
      updatedBoard.columns[targetColumnIndex].cards.push(card);
    }
    
    // Atualiza o estado
    setCurrentBoard(updatedBoard);
    setDraggedCard(null);
    setDragOverColumn(null);
  };

  const handleDragEnd = () => {
    setDragOverColumn(null);
  };

  const switchBoard = (boardId: number) => {
    const board = boards.find(b => b.id === boardId);
    if (board) {
      setCurrentBoard(board);
    }
  };

  const getLabelColor = (label: string) => {
    const colors: {[key: string]: string} = {
      'urgente': 'leopard-label-red',
      'suporte': 'leopard-label-blue',
      'financeiro': 'leopard-label-green',
      'logística': 'leopard-label-orange',
      'admin': 'leopard-label-purple',
      'feedback': 'leopard-label-teal',
      'técnico': 'leopard-label-gray',
      'design': 'leopard-label-pink',
      'qa': 'leopard-label-indigo',
      'bug': 'leopard-label-red'
    };
    
    return colors[label] || 'leopard-label-gray';
  };

  return (
    <div className="leopard-app-container">
      <Sidebar />
      
      <div className="leopard-main-content">
        <Header 
          title="Kanban" 
          username={user?.name} 
          userAvatar={user?.avatar}
        />
        
        <div className="leopard-kanban-content">
          {isLoading ? (
            <div className="leopard-loading">Carregando...</div>
          ) : (
            <>
              <div className="leopard-kanban-header">
                <div className="leopard-kanban-board-selector">
                  <select 
                    value={currentBoard?.id} 
                    onChange={(e) => switchBoard(Number(e.target.value))}
                    className="leopard-select"
                  >
                    {boards.map(board => (
                      <option key={board.id} value={board.id}>{board.name}</option>
                    ))}
                  </select>
                </div>
                
                <div className="leopard-kanban-actions">
                  <button className="leopard-button">
                    <i className="ph-plus"></i> Novo Card
                  </button>
                  <button className="leopard-button">
                    <i className="ph-columns"></i> Nova Coluna
                  </button>
                  <button className="leopard-button">
                    <i className="ph-gear"></i> Configurações
                  </button>
                </div>
              </div>
              
              <div className="leopard-kanban-board">
                {currentBoard?.columns.map((column: any) => (
                  <div 
                    key={column.id} 
                    className={`leopard-kanban-column ${dragOverColumn === column.id ? 'leopard-kanban-column-drag-over' : ''}`}
                    onDragOver={(e) => handleDragOver(e, column.id)}
                    onDrop={(e) => handleDrop(e, column.id)}
                  >
                    <div className="leopard-kanban-column-header">
                      <h3 className="leopard-kanban-column-title">{column.title}</h3>
                      <span className="leopard-kanban-column-count">{column.cards.length}</span>
                    </div>
                    
                    <div className="leopard-kanban-cards">
                      {column.cards.map((card: any) => (
                        <div 
                          key={card.id} 
                          className="leopard-kanban-card"
                          draggable
                          onDragStart={() => handleDragStart(card)}
                          onDragEnd={handleDragEnd}
                        >
                          <div className="leopard-kanban-card-header">
                            <h4 className="leopard-kanban-card-title">{card.title}</h4>
                            <div className="leopard-kanban-card-menu">
                              <i className="ph-dots-three-vertical"></i>
                            </div>
                          </div>
                          
                          <div className="leopard-kanban-card-description">
                            {card.description}
                          </div>
                          
                          <div className="leopard-kanban-card-labels">
                            {card.labels.map((label: string, index: number) => (
                              <span 
                                key={index} 
                                className={`leopard-kanban-card-label ${getLabelColor(label)}`}
                              >
                                {label}
                              </span>
                            ))}
                          </div>
                          
                          <div className="leopard-kanban-card-footer">
                            <div className="leopard-kanban-card-assignee">
                              <div className="leopard-kanban-card-avatar">
                                {card.assignee.charAt(0)}
                              </div>
                              <span className="leopard-kanban-card-assignee-name">
                                {card.assignee}
                              </span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    <div className="leopard-kanban-column-footer">
                      <button className="leopard-kanban-add-card">
                        <i className="ph-plus"></i> Adicionar Card
                      </button>
                    </div>
                  </div>
                ))}
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

export default Kanban;
