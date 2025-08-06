import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Plus, 
  Settings, 
  BarChart3, 
  Users, 
  Calendar,
  CheckCircle,
  Clock,
  AlertCircle,
  Star,
  Filter,
  Search,
  Download,
  Upload
} from 'lucide-react';
import KanbanBoard from '@/components/kanban/KanbanBoard';
import { KanbanBoard as KanbanBoardType, KanbanCard, KanbanColumn } from '@/types/kanban';

const Kanban: React.FC = () => {
  const [activeTab, setActiveTab] = useState('boards');
  const [showBoard, setShowBoard] = useState(false);
  const [selectedBoard, setSelectedBoard] = useState<KanbanBoardType | null>(null);

  // Dados mockados para demonstração
  const mockBoard: KanbanBoardType = {
    id: 'board_1',
    name: 'Projeto AuraChat',
    description: 'Desenvolvimento do sistema de automação WhatsApp',
    columns: [
      {
        id: 'col_1',
        title: 'A Fazer',
        description: 'Tarefas pendentes',
        color: '#ef4444',
        cards: [
          {
            id: 'card_1',
            title: 'Implementar Gemini AI',
            description: 'Integrar IA do Google para automações',
            priority: 'high',
            status: 'todo',
            assignee: 'João Silva',
            dueDate: new Date('2024-01-15'),
            tags: ['AI', 'Backend'],
            createdAt: new Date('2024-01-10'),
            updatedAt: new Date('2024-01-10'),
            position: 0
          },
          {
            id: 'card_2',
            title: 'Criar Sistema Kanban',
            description: 'Desenvolver interface drag & drop',
            priority: 'urgent',
            status: 'todo',
            assignee: 'Maria Santos',
            dueDate: new Date('2024-01-12'),
            tags: ['Frontend', 'UI/UX'],
            createdAt: new Date('2024-01-09'),
            updatedAt: new Date('2024-01-09'),
            position: 1
          }
        ],
        position: 0
      },
      {
        id: 'col_2',
        title: 'Em Progresso',
        description: 'Tarefas em desenvolvimento',
        color: '#f59e0b',
        cards: [
          {
            id: 'card_3',
            title: 'WhatsApp Integration',
            description: 'Conectar com API do WhatsApp',
            priority: 'high',
            status: 'in_progress',
            assignee: 'Pedro Costa',
            dueDate: new Date('2024-01-20'),
            tags: ['WhatsApp', 'API'],
            createdAt: new Date('2024-01-08'),
            updatedAt: new Date('2024-01-11'),
            position: 0
          }
        ],
        position: 1
      },
      {
        id: 'col_3',
        title: 'Em Revisão',
        description: 'Tarefas aguardando revisão',
        color: '#3b82f6',
        cards: [
          {
            id: 'card_4',
            title: 'Design System',
            description: 'Criar biblioteca de componentes',
            priority: 'medium',
            status: 'review',
            assignee: 'Ana Oliveira',
            dueDate: new Date('2024-01-18'),
            tags: ['Design', 'Frontend'],
            createdAt: new Date('2024-01-07'),
            updatedAt: new Date('2024-01-10'),
            position: 0
          }
        ],
        position: 2
      },
      {
        id: 'col_4',
        title: 'Concluído',
        description: 'Tarefas finalizadas',
        color: '#10b981',
        cards: [
          {
            id: 'card_5',
            title: 'Setup do Projeto',
            description: 'Configurar ambiente de desenvolvimento',
            priority: 'low',
            status: 'done',
            assignee: 'Carlos Lima',
            dueDate: new Date('2024-01-05'),
            tags: ['Setup', 'DevOps'],
            createdAt: new Date('2024-01-01'),
            updatedAt: new Date('2024-01-05'),
            position: 0
          }
        ],
        position: 3
      }
    ],
    createdAt: new Date('2024-01-01'),
    updatedAt: new Date('2024-01-11'),
    isActive: true,
    settings: {
      allowCardCreation: true,
      allowCardEditing: true,
      allowCardDeletion: true,
      allowColumnEditing: true,
      showDueDates: true,
      showPriority: true,
      showTags: true
    }
  };

  const boards = [
    {
      id: 'board_1',
      name: 'Projeto AuraChat',
      description: 'Desenvolvimento do sistema de automação WhatsApp',
      totalCards: 5,
      completedCards: 1,
      progress: 20,
      lastUpdated: '2 horas atrás'
    },
    {
      id: 'board_2',
      name: 'Marketing Digital',
      description: 'Campanhas e estratégias de marketing',
      totalCards: 12,
      completedCards: 8,
      progress: 67,
      lastUpdated: '1 dia atrás'
    },
    {
      id: 'board_3',
      name: 'Suporte ao Cliente',
      description: 'Tickets e atendimento ao cliente',
      totalCards: 8,
      completedCards: 6,
      progress: 75,
      lastUpdated: '3 horas atrás'
    }
  ];

  const stats = {
    totalBoards: 3,
    totalCards: 25,
    completedCards: 15,
    overdueCards: 2,
    averageCompletionTime: 3.2 // dias
  };

  const handleOpenBoard = (board: KanbanBoardType) => {
    setSelectedBoard(board);
    setShowBoard(true);
  };

  const handleUpdateBoard = useCallback((updatedBoard: KanbanBoardType) => {
    setSelectedBoard(updatedBoard);
    // Aqui você salvaria no backend
    console.log('Board atualizado:', updatedBoard);
  }, []);

  const handleAddCard = useCallback((columnId: string, card: KanbanCard) => {
    if (selectedBoard) {
      const updatedBoard = {
        ...selectedBoard,
        columns: selectedBoard.columns.map(col =>
          col.id === columnId 
            ? { ...col, cards: [...col.cards, card] }
            : col
        )
      };
      setSelectedBoard(updatedBoard);
    }
  }, [selectedBoard]);

  const handleUpdateCard = useCallback((cardId: string, updates: Partial<KanbanCard>) => {
    if (selectedBoard) {
      const updatedBoard = {
        ...selectedBoard,
        columns: selectedBoard.columns.map(col => ({
          ...col,
          cards: col.cards.map(card =>
            card.id === cardId ? { ...card, ...updates, updatedAt: new Date() } : card
          )
        }))
      };
      setSelectedBoard(updatedBoard);
    }
  }, [selectedBoard]);

  const handleDeleteCard = useCallback((cardId: string) => {
    if (selectedBoard) {
      const updatedBoard = {
        ...selectedBoard,
        columns: selectedBoard.columns.map(col => ({
          ...col,
          cards: col.cards.filter(card => card.id !== cardId)
        }))
      };
      setSelectedBoard(updatedBoard);
    }
  }, [selectedBoard]);

  const handleMoveCard = useCallback((
    cardId: string, 
    sourceColumnId: string, 
    targetColumnId: string, 
    position: number
  ) => {
    if (selectedBoard) {
      const sourceColumn = selectedBoard.columns.find(col => col.id === sourceColumnId);
      const targetColumn = selectedBoard.columns.find(col => col.id === targetColumnId);
      
      if (sourceColumn && targetColumn) {
        const card = sourceColumn.cards.find(c => c.id === cardId);
        if (card) {
          const updatedBoard = {
            ...selectedBoard,
            columns: selectedBoard.columns.map(col => {
              if (col.id === sourceColumnId) {
                return { ...col, cards: col.cards.filter(c => c.id !== cardId) };
              }
              if (col.id === targetColumnId) {
                const newCards = [...col.cards];
                newCards.splice(position, 0, { ...card, position });
                return { ...col, cards: newCards };
              }
              return col;
            })
          };
          setSelectedBoard(updatedBoard);
        }
      }
    }
  }, [selectedBoard]);

  if (showBoard && selectedBoard) {
    return (
      <div className="h-screen">
        <div className="bg-white border-b p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                onClick={() => setShowBoard(false)}
              >
                ← Voltar
              </Button>
              <div>
                <h1 className="text-xl font-bold">{selectedBoard.name}</h1>
                <p className="text-sm text-gray-600">{selectedBoard.description}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Exportar
              </Button>
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4 mr-2" />
                Configurações
              </Button>
            </div>
          </div>
        </div>
        <KanbanBoard
          board={selectedBoard}
          onUpdateBoard={handleUpdateBoard}
          onAddCard={handleAddCard}
          onUpdateCard={handleUpdateCard}
          onDeleteCard={handleDeleteCard}
          onMoveCard={handleMoveCard}
        />
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Kanban</h1>
          <p className="text-gray-600">Gerencie projetos e tarefas com quadros visuais</p>
        </div>
        <Button 
          className="bg-blue-600 hover:bg-blue-700"
          onClick={() => handleOpenBoard(mockBoard)}
        >
          <Plus className="w-4 h-4 mr-2" />
          Novo Quadro
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="boards">Quadros</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="boards" className="space-y-6">
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <BarChart3 className="w-8 h-8 text-blue-600" />
                  <div>
                    <p className="text-sm text-gray-600">Total de Quadros</p>
                    <p className="text-2xl font-bold">{stats.totalBoards}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Calendar className="w-8 h-8 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-600">Total de Cards</p>
                    <p className="text-2xl font-bold">{stats.totalCards}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-8 h-8 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-600">Concluídos</p>
                    <p className="text-2xl font-bold">{stats.completedCards}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-8 h-8 text-red-600" />
                  <div>
                    <p className="text-sm text-gray-600">Atrasados</p>
                    <p className="text-2xl font-bold">{stats.overdueCards}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Clock className="w-8 h-8 text-orange-600" />
                  <div>
                    <p className="text-sm text-gray-600">Tempo Médio</p>
                    <p className="text-2xl font-bold">{stats.averageCompletionTime}d</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Boards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {boards.map((board) => (
              <Card 
                key={board.id} 
                className="cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => handleOpenBoard(mockBoard)}
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg">{board.name}</CardTitle>
                      <CardDescription className="mt-1">
                        {board.description}
                      </CardDescription>
                    </div>
                    <Button variant="ghost" size="sm">
                      <Settings className="w-4 h-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Progresso</span>
                      <span className="font-medium">{board.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${board.progress}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{board.totalCards} cards</span>
                      <span>{board.completedCards} concluídos</span>
                    </div>
                    <div className="text-xs text-gray-500">
                      Atualizado {board.lastUpdated}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="templates">
          <Card>
            <CardHeader>
              <CardTitle>Templates de Quadros</CardTitle>
              <CardDescription>
                Templates pré-configurados para criar quadros rapidamente
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="cursor-pointer hover:shadow-md">
                  <CardContent className="p-4">
                    <h4 className="font-medium mb-2">Desenvolvimento de Software</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Quadro para projetos de desenvolvimento com colunas: Backlog, Em Desenvolvimento, Teste, Produção
                    </p>
                    <Button size="sm" className="w-full">
                      Usar Template
                    </Button>
                  </CardContent>
                </Card>
                <Card className="cursor-pointer hover:shadow-md">
                  <CardContent className="p-4">
                    <h4 className="font-medium mb-2">Marketing Digital</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Quadro para campanhas de marketing com colunas: Ideação, Em Criação, Em Revisão, Publicado
                    </p>
                    <Button size="sm" className="w-full">
                      Usar Template
                    </Button>
                  </CardContent>
                </Card>
                <Card className="cursor-pointer hover:shadow-md">
                  <CardContent className="p-4">
                    <h4 className="font-medium mb-2">Suporte ao Cliente</h4>
                    <p className="text-sm text-gray-600 mb-3">
                      Quadro para tickets de suporte com colunas: Novo, Em Análise, Em Andamento, Resolvido
                    </p>
                    <Button size="sm" className="w-full">
                      Usar Template
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          <Card>
            <CardHeader>
              <CardTitle>Analytics de Produtividade</CardTitle>
              <CardDescription>
                Métricas e insights sobre seus quadros Kanban
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Em desenvolvimento...</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Kanban;
