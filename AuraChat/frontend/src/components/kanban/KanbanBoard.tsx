import React, { useState, useCallback } from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  Plus, 
  Search, 
  Filter, 
  Settings, 
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  Calendar,
  User,
  Tag,
  AlertCircle,
  CheckCircle,
  Clock,
  Star
} from 'lucide-react';
import KanbanColumn from './KanbanColumn';
import { KanbanBoard as KanbanBoardType, KanbanCard, KanbanColumn as KanbanColumnType } from '@/types/kanban';

interface KanbanBoardProps {
  board: KanbanBoardType;
  onUpdateBoard: (board: KanbanBoardType) => void;
  onAddCard: (columnId: string, card: KanbanCard) => void;
  onUpdateCard: (cardId: string, updates: Partial<KanbanCard>) => void;
  onDeleteCard: (cardId: string) => void;
  onMoveCard: (cardId: string, sourceColumnId: string, targetColumnId: string, position: number) => void;
}

const KanbanBoard: React.FC<KanbanBoardProps> = ({
  board,
  onUpdateBoard,
  onAddCard,
  onUpdateCard,
  onDeleteCard,
  onMoveCard
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);

  const handleAddColumn = useCallback(() => {
    const newColumn: KanbanColumnType = {
      id: `column_${Date.now()}`,
      title: 'Nova Coluna',
      description: '',
      color: '#3b82f6',
      cards: [],
      position: board.columns.length
    };

    const updatedBoard = {
      ...board,
      columns: [...board.columns, newColumn]
    };

    onUpdateBoard(updatedBoard);
  }, [board, onUpdateBoard]);

  const handleUpdateColumn = useCallback((columnId: string, updates: Partial<KanbanColumnType>) => {
    const updatedColumns = board.columns.map(column =>
      column.id === columnId ? { ...column, ...updates } : column
    );

    const updatedBoard = {
      ...board,
      columns: updatedColumns
    };

    onUpdateBoard(updatedBoard);
  }, [board, onUpdateBoard]);

  const handleDeleteColumn = useCallback((columnId: string) => {
    const updatedColumns = board.columns.filter(column => column.id !== columnId);
    
    const updatedBoard = {
      ...board,
      columns: updatedColumns
    };

    onUpdateBoard(updatedBoard);
  }, [board, onUpdateBoard]);

  const handleMoveColumn = useCallback((columnId: string, newPosition: number) => {
    const columns = [...board.columns];
    const columnIndex = columns.findIndex(col => col.id === columnId);
    
    if (columnIndex !== -1) {
      const [movedColumn] = columns.splice(columnIndex, 1);
      columns.splice(newPosition, 0, movedColumn);
      
      // Atualizar posições
      const updatedColumns = columns.map((col, index) => ({
        ...col,
        position: index
      }));

      const updatedBoard = {
        ...board,
        columns: updatedColumns
      };

      onUpdateBoard(updatedBoard);
    }
  }, [board, onUpdateBoard]);

  const filteredColumns = board.columns.map(column => ({
    ...column,
    cards: column.cards.filter(card =>
      searchQuery === '' ||
      card.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      card.description?.toLowerCase().includes(searchQuery.toLowerCase())
    )
  }));

  const getBoardStats = () => {
    const totalCards = board.columns.reduce((sum, col) => sum + col.cards.length, 0);
    const completedCards = board.columns
      .filter(col => col.title.toLowerCase().includes('done') || col.title.toLowerCase().includes('concluído'))
      .reduce((sum, col) => sum + col.cards.length, 0);
    
    return {
      totalCards,
      completedCards,
      completionRate: totalCards > 0 ? Math.round((completedCards / totalCards) * 100) : 0
    };
  };

  const stats = getBoardStats();

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="h-screen flex flex-col bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{board.name}</h1>
              <p className="text-gray-600">{board.description}</p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-2">
                <Input
                  placeholder="Buscar cards..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-64"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowFilters(!showFilters)}
                >
                  <Filter className="w-4 h-4 mr-2" />
                  Filtros
                </Button>
              </div>
              <Button
                variant="outline"
                size="sm"
              >
                <Settings className="w-4 h-4 mr-2" />
                Configurações
              </Button>
              <Button
                onClick={handleAddColumn}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <Plus className="w-4 h-4 mr-2" />
                Nova Coluna
              </Button>
            </div>
          </div>

          {/* Stats */}
          <div className="flex items-center space-x-6 mt-4">
            <div className="flex items-center space-x-2">
              <Badge variant="outline">{stats.totalCards} cards</Badge>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <span className="text-sm text-gray-600">{stats.completedCards} concluídos</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${stats.completionRate}%` }}
                />
              </div>
              <span className="text-sm text-gray-600">{stats.completionRate}%</span>
            </div>
          </div>
        </div>

        {/* Board Content */}
        <div className="flex-1 overflow-x-auto p-4">
          <div className="flex space-x-4 min-w-max">
            {filteredColumns.map((column, index) => (
              <KanbanColumn
                key={column.id}
                column={column}
                onUpdateColumn={(updates) => handleUpdateColumn(column.id, updates)}
                onDeleteColumn={() => handleDeleteColumn(column.id)}
                onMoveColumn={(newPosition) => handleMoveColumn(column.id, newPosition)}
                onAddCard={(card) => onAddCard(column.id, card)}
                onUpdateCard={onUpdateCard}
                onDeleteCard={onDeleteCard}
                onMoveCard={onMoveCard}
                position={index}
                totalColumns={filteredColumns.length}
                boardSettings={board.settings}
              />
            ))}
          </div>
        </div>
      </div>
    </DndProvider>
  );
};

export default KanbanBoard;