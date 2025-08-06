import React, { useState, useCallback } from 'react';
import { useDrag } from 'react-dnd';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  MoreVertical, 
  Edit, 
  Trash2, 
  Calendar,
  User,
  Tag,
  AlertCircle,
  Clock,
  Star,
  GripVertical
} from 'lucide-react';
import { KanbanCard as KanbanCardType } from '@/types/kanban';

interface KanbanCardProps {
  card: KanbanCardType;
  onUpdateCard: (updates: Partial<KanbanCardType>) => void;
  onDeleteCard: () => void;
  onMoveCard: (newPosition: number) => void;
  position: number;
  totalCards: number;
  boardSettings: any;
}

const KanbanCard: React.FC<KanbanCardProps> = ({
  card,
  onUpdateCard,
  onDeleteCard,
  onMoveCard,
  position,
  totalCards,
  boardSettings
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

  const [{ isDragging }, drag] = useDrag({
    type: 'CARD',
    item: { 
      id: card.id, 
      sourceColumnId: card.status // Usando status como columnId temporário
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  const getPriorityColor = (priority: string) => {
    const colors = {
      low: 'bg-green-100 text-green-800',
      medium: 'bg-yellow-100 text-yellow-800',
      high: 'bg-orange-100 text-orange-800',
      urgent: 'bg-red-100 text-red-800'
    };
    return colors[priority as keyof typeof colors] || colors.medium;
  };

  const getPriorityIcon = (priority: string) => {
    const icons = {
      low: <Star className="w-3 h-3" />,
      medium: <Star className="w-3 h-3" />,
      high: <AlertCircle className="w-3 h-3" />,
      urgent: <AlertCircle className="w-3 h-3" />
    };
    return icons[priority as keyof typeof icons] || icons.medium;
  };

  const isOverdue = card.dueDate && new Date() > card.dueDate;
  const isDueSoon = card.dueDate && 
    new Date() <= card.dueDate && 
    new Date(card.dueDate) - new Date() < 24 * 60 * 60 * 1000; // 24 horas

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).format(new Date(date));
  };

  return (
    <div
      ref={drag}
      className={`cursor-move ${isDragging ? 'opacity-50' : ''}`}
    >
      <Card className={`mb-2 hover:shadow-md transition-shadow ${
        isOverdue ? 'border-red-300 bg-red-50' : 
        isDueSoon ? 'border-yellow-300 bg-yellow-50' : ''
      }`}>
        <CardContent className="p-3">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-medium text-sm leading-tight">{card.title}</h4>
                <div className="flex items-center space-x-1">
                  {boardSettings?.showPriority && (
                    <Badge 
                      variant="outline" 
                      className={`text-xs ${getPriorityColor(card.priority)}`}
                    >
                      {getPriorityIcon(card.priority)}
                    </Badge>
                  )}
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowMenu(!showMenu)}
                  >
                    <MoreVertical className="w-3 h-3" />
                  </Button>
                </div>
              </div>

              {card.description && (
                <p className="text-xs text-gray-600 mb-2 line-clamp-2">
                  {card.description}
                </p>
              )}

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {card.assignee && (
                    <div className="flex items-center space-x-1">
                      <User className="w-3 h-3 text-gray-500" />
                      <span className="text-xs text-gray-600">{card.assignee}</span>
                    </div>
                  )}
                  
                  {card.dueDate && boardSettings?.showDueDates && (
                    <div className="flex items-center space-x-1">
                      <Calendar className={`w-3 h-3 ${
                        isOverdue ? 'text-red-500' : 
                        isDueSoon ? 'text-yellow-500' : 'text-gray-500'
                      }`} />
                      <span className={`text-xs ${
                        isOverdue ? 'text-red-600' : 
                        isDueSoon ? 'text-yellow-600' : 'text-gray-600'
                      }`}>
                        {formatDate(card.dueDate)}
                      </span>
                    </div>
                  )}
                </div>

                {card.tags.length > 0 && boardSettings?.showTags && (
                  <div className="flex items-center space-x-1">
                    <Tag className="w-3 h-3 text-gray-500" />
                    <div className="flex space-x-1">
                      {card.tags.slice(0, 2).map((tag, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {card.tags.length > 2 && (
                        <Badge variant="outline" className="text-xs">
                          +{card.tags.length - 2}
                        </Badge>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Menu dropdown */}
          {showMenu && (
            <div className="absolute right-0 top-8 mt-1 w-48 bg-white border rounded-lg shadow-lg z-10">
              <div className="py-1">
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => {
                    setIsEditing(true);
                    setShowMenu(false);
                  }}
                >
                  <Edit className="w-3 h-3 mr-2" />
                  Editar
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start text-red-600 hover:text-red-700"
                  onClick={() => {
                    onDeleteCard();
                    setShowMenu(false);
                  }}
                >
                  <Trash2 className="w-3 h-3 mr-2" />
                  Excluir
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default KanbanCard;