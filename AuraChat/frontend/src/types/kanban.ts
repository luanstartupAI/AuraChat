// Tipos para Sistema Kanban

export interface KanbanCard {
  id: string;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'todo' | 'in_progress' | 'review' | 'done';
  assignee?: string;
  dueDate?: Date;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  position: number; // Para ordenação
}

export interface KanbanColumn {
  id: string;
  title: string;
  description?: string;
  color: string;
  cards: KanbanCard[];
  position: number; // Para ordenação
  maxCards?: number; // Limite opcional de cards
}

export interface KanbanBoard {
  id: string;
  name: string;
  description?: string;
  columns: KanbanColumn[];
  createdAt: Date;
  updatedAt: Date;
  isActive: boolean;
  settings: {
    allowCardCreation: boolean;
    allowCardEditing: boolean;
    allowCardDeletion: boolean;
    allowColumnEditing: boolean;
    showDueDates: boolean;
    showPriority: boolean;
    showTags: boolean;
  };
}

export interface KanbanStats {
  totalCards: number;
  completedCards: number;
  overdueCards: number;
  averageCompletionTime: number;
  cardsByPriority: {
    low: number;
    medium: number;
    high: number;
    urgent: number;
  };
  cardsByStatus: {
    todo: number;
    in_progress: number;
    review: number;
    done: number;
  };
}

export interface KanbanFilter {
  assignee?: string;
  priority?: string[];
  tags?: string[];
  dueDate?: {
    start?: Date;
    end?: Date;
  };
  status?: string[];
}

export interface KanbanSearch {
  query: string;
  searchIn: 'title' | 'description' | 'all';
  caseSensitive: boolean;
}