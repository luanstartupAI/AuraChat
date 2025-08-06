import React, { useState, useCallback } from 'react';
import { useDrop } from 'react-dnd';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  Plus, 
  MoreVertical, 
  Edit, 
  Trash2,
  GripVertical
} from 'lucide-react';
import KanbanCard from './KanbanCard';
import { KanbanColumn as KanbanColumnType, KanbanCard as KanbanCardType } from '@/types/kanban';

interface KanbanColumnProps {
  column: KanbanColumnType;
  onUpdateColumn: (updates: Partial<KanbanColumnType>) => void;
  onDeleteColumn: () => void;
  onMoveColumn: (newPosition: number) => void;
  onAddCard: (card: KanbanCardType) => void;
  onUpdateCard: (cardId: string, updates: Partial<KanbanCardType>) => void;
  onDeleteCard: (cardId: string) => void;
  onMoveCard: (cardId: string, sourceColumnId: string, targetColumnId: string, position: number) => void;
  position: number;
  totalColumns: number;
  boardSettings: any;
}

const KanbanColumn: React.FC<KanbanColumnProps> = ({
  column,
  onUpdateColumn,
  onDeleteColumn,
  onMoveColumn,
  onAddCard,
  onUpdateCard,
  onDeleteCard,
  onMoveCard,
  position,
  totalColumns,
  boardSettings
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(column.title);
  const [showAddCard, setShowAddCard] = useState(false);
  const [newCardTitle, setNewCardTitle] = useState('');

  const [{ isOver }, drop] = useDrop({
    accept: 'CARD',
    drop: (item: { id: string; sourceColumnId: string }) => {
      if (item.sourceColumnId !== column.id) {
        onMoveCard(item.id, item.sourceColumnId, column.id, column.cards.length);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  });

  const handleSaveTitle = useCallback(() => {
    onUpdateColumn({ title: editTitle });
    setIsEditing(false);
  }, [editTitle, onUpdateColumn]);

  const handleCancelEdit = useCallback(() => {
    setEditTitle(column.title);
    setIsEditing(false);
  }, [column.title]);

  const handleAddCard = useCallback(() => {
    if (newCardTitle.trim()) {
      const newCard: KanbanCardType = {
        id: `card_${Date.now()}`,
        title: newCardTitle,
        description: '',
        priority: 'medium',
        status: 'todo',
        tags: [],
        createdAt: new Date(),
        updatedAt: new Date(),
        position: column.cards.length
      };

      onAddCard(newCard);
      setNewCardTitle('');
      setShowAddCard(false);
    }
  }, [newCardTitle, column.cards.length, onAddCard]);

  const handleMoveCard = useCallback((cardId: string, newPosition: number) => {
    const cards = [...column.cards];
    const cardIndex = cards.findIndex(card => card.id === cardId);
    
    if (cardIndex !== -1) {
      const [movedCard] = cards.splice(cardIndex, 1);
      cards.splice(newPosition, 0, movedCard);
      
      // Atualizar posições
      const updatedCards = cards.map((card, index) => ({
        ...card,
        position: index
      }));

      onUpdateColumn({ cards: updatedCards });
    }
  }, [column.cards, onUpdateColumn]);

  const getPriorityColor = (priority: string) => {
    const colors = {
      low: 'bg-green-100 text-green-800',
      medium: 'bg-yellow-100 text-yellow-800',
      high: 'bg-orange-100 text-orange-800',
      urgent: 'bg-red-100 text-red-800'
    };
    return colors[priority as keyof typeof colors] || colors.medium;
  };

  return (
    <div
      ref={drop}
      className={`w-80 flex-shrink-0 ${isOver ? 'bg-blue-50' : ''}`}
    >
      <Card className="h-full">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: column.color }}
              />
              {isEditing ? (
                <div className="flex items-center space-x-2">
                  <Input
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    className="h-6 text-sm"
                    autoFocus
                  />
                  <Button size="sm" onClick={handleSaveTitle}>
                    ✓
                  </Button>
                  <Button size="sm" variant="outline" onClick={handleCancelEdit}>
                    ✕
                  </Button>
                </div>
              ) : (
                <CardTitle className="text-sm font-medium">{column.title}</CardTitle>
              )}
            </div>
            <div className="flex items-center space-x-1">
              <Badge variant="outline" className="text-xs">
                {column.cards.length}
              </Badge>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setIsEditing(true)}
              >
                <Edit className="w-3 h-3" />
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={onDeleteColumn}
              >
                <Trash2 className="w-3 h-3" />
              </Button>
            </div>
          </div>
          {column.description && (
            <p className="text-xs text-gray-500">{column.description}</p>
          )}
        </CardHeader>

        <CardContent className="pt-0">
          <div className="space-y-2">
            {column.cards.map((card, index) => (
              <KanbanCard
                key={card.id}
                card={card}
                onUpdateCard={(updates) => onUpdateCard(card.id, updates)}
                onDeleteCard={() => onDeleteCard(card.id)}
                onMoveCard={(newPosition) => handleMoveCard(card.id, newPosition)}
                position={index}
                totalCards={column.cards.length}
                boardSettings={boardSettings}
              />
            ))}

            {showAddCard ? (
              <div className="p-3 border-2 border-dashed border-gray-300 rounded-lg">
                <Input
                  placeholder="Título do card..."
                  value={newCardTitle}
                  onChange={(e) => setNewCardTitle(e.target.value)}
                  className="mb-2"
                  autoFocus
                />
                <div className="flex items-center space-x-2">
                  <Button size="sm" onClick={handleAddCard}>
                    Adicionar
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => {
                      setShowAddCard(false);
                      setNewCardTitle('');
                    }}
                  >
                    Cancelar
                  </Button>
                </div>
              </div>
            ) : (
              <Button
                variant="outline"
                size="sm"
                className="w-full justify-start text-gray-500 hover:text-gray-700"
                onClick={() => setShowAddCard(true)}
              >
                <Plus className="w-4 h-4 mr-2" />
                Adicionar Card
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default KanbanColumn;