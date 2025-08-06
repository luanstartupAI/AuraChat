import React from 'react';
import { useDrag } from 'react-dnd';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  MessageSquare, 
  Send, 
  GitBranch, 
  Clock, 
  Brain, 
  Webhook, 
  Variable, 
  FileText,
  Zap,
  Filter,
  Timer,
  Bot,
  Globe,
  Database,
  Settings,
  User,
  Play,
  Heart,
  Languages
} from 'lucide-react';
import { NodeType } from '@/types/automation';

interface NodeItemProps {
  type: NodeType;
  label: string;
  description: string;
  icon: React.ReactNode;
  color: string;
}

const NodeItem: React.FC<NodeItemProps> = ({ type, label, description, icon, color }) => {
  const [{ isDragging }, drag] = useDrag({
    type: 'NODE',
    item: { type, label },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  return (
    <div
      ref={drag}
      className={`cursor-grab active:cursor-grabbing ${isDragging ? 'opacity-50' : ''}`}
    >
      <Card className="mb-3 hover:shadow-md transition-shadow">
        <CardContent className="p-3">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-lg ${color}`}>
              {icon}
            </div>
            <div className="flex-1">
              <div className="font-medium text-sm">{label}</div>
              <div className="text-xs text-gray-500">{description}</div>
            </div>
            <Badge variant="outline" className="text-xs">
              {type}
            </Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

interface NodePaletteProps {
  onAddNode: (type: NodeType, position: { x: number; y: number }) => void;
}

const NodePalette: React.FC<NodePaletteProps> = ({ onAddNode }) => {
  const nodeTypes = [
    // TRIGGER NODES
    {
      type: 'trigger' as NodeType,
      label: 'Gatilho',
      description: 'Inicia o fluxo',
      icon: <Zap className="w-4 h-4" />,
      color: 'bg-yellow-100 text-yellow-600'
    },
    {
      type: 'trigger' as NodeType,
      label: 'Mensagem',
      description: 'Detecta mensagens recebidas',
      icon: <MessageSquare className="w-4 h-4" />,
      color: 'bg-blue-100 text-blue-600'
    },
    {
      type: 'trigger' as NodeType,
      label: 'Tempo',
      description: 'Executa em horários específicos',
      icon: <Clock className="w-4 h-4" />,
      color: 'bg-green-100 text-green-600'
    },
    {
      type: 'trigger' as NodeType,
      label: 'Webhook',
      description: 'Executa via webhook externo',
      icon: <Webhook className="w-4 h-4" />,
      color: 'bg-red-100 text-red-600'
    },
    {
      type: 'trigger' as NodeType,
      label: 'Manual',
      description: 'Execução manual',
      icon: <Play className="w-4 h-4" />,
      color: 'bg-purple-100 text-purple-600'
    },
    {
      type: 'trigger' as NodeType,
      label: 'Contato',
      description: 'Detecta mudanças em contatos',
      icon: <User className="w-4 h-4" />,
      color: 'bg-indigo-100 text-indigo-600'
    },

    // ACTION NODES
    {
      type: 'action' as NodeType,
      label: 'Enviar Mensagem',
      description: 'Envia mensagem WhatsApp',
      icon: <Send className="w-4 h-4" />,
      color: 'bg-blue-100 text-blue-600'
    },
    {
      type: 'action' as NodeType,
      label: 'Enviar Template',
      description: 'Envia template aprovado',
      icon: <FileText className="w-4 h-4" />,
      color: 'bg-pink-100 text-pink-600'
    },
    {
      type: 'action' as NodeType,
      label: 'Atualizar Contato',
      description: 'Atualiza dados do contato',
      icon: <User className="w-4 h-4" />,
      color: 'bg-indigo-100 text-indigo-600'
    },
    {
      type: 'action' as NodeType,
      label: 'Criar Chat',
      description: 'Cria nova conversa',
      icon: <MessageSquare className="w-4 h-4" />,
      color: 'bg-cyan-100 text-cyan-600'
    },
    {
      type: 'action' as NodeType,
      label: 'Atribuir Agente',
      description: 'Atribui agente à conversa',
      icon: <Settings className="w-4 h-4" />,
      color: 'bg-orange-100 text-orange-600'
    },

    // AI NODES
    {
      type: 'ai' as NodeType,
      label: 'Classificar Mensagem',
      description: 'Classifica intenção da mensagem',
      icon: <Brain className="w-4 h-4" />,
      color: 'bg-green-100 text-green-600'
    },
    {
      type: 'ai' as NodeType,
      label: 'Gerar Resposta',
      description: 'Gera resposta automática',
      icon: <Bot className="w-4 h-4" />,
      color: 'bg-teal-100 text-teal-600'
    },
    {
      type: 'ai' as NodeType,
      label: 'Analisar Sentimento',
      description: 'Analisa sentimento da mensagem',
      icon: <Heart className="w-4 h-4" />,
      color: 'bg-red-100 text-red-600'
    },
    {
      type: 'ai' as NodeType,
      label: 'Traduzir',
      description: 'Traduz mensagens',
      icon: <Languages className="w-4 h-4" />,
      color: 'bg-purple-100 text-purple-600'
    },

    // LOGIC NODES
    {
      type: 'condition' as NodeType,
      label: 'Condição',
      description: 'Verifica uma condição',
      icon: <GitBranch className="w-4 h-4" />,
      color: 'bg-purple-100 text-purple-600'
    },
    {
      type: 'delay' as NodeType,
      label: 'Atraso',
      description: 'Aguarda um tempo',
      icon: <Clock className="w-4 h-4" />,
      color: 'bg-orange-100 text-orange-600'
    },
    {
      type: 'variable' as NodeType,
      label: 'Variável',
      description: 'Armazena e manipula variáveis',
      icon: <Variable className="w-4 h-4" />,
      color: 'bg-indigo-100 text-indigo-600'
    },

    // INTEGRATION NODES
    {
      type: 'webhook' as NodeType,
      label: 'HTTP Request',
      description: 'Faz requisições HTTP',
      icon: <Globe className="w-4 h-4" />,
      color: 'bg-blue-100 text-blue-600'
    },
    {
      type: 'webhook' as NodeType,
      label: 'Database',
      description: 'Operações no banco',
      icon: <Database className="w-4 h-4" />,
      color: 'bg-gray-100 text-gray-600'
    },

    // UTILITY NODES
    {
      type: 'template' as NodeType,
      label: 'Template',
      description: 'Aplica templates',
      icon: <FileText className="w-4 h-4" />,
      color: 'bg-pink-100 text-pink-600'
    }
  ];

  return (
    <div>
      <h3 className="font-semibold text-lg mb-4">Nós Disponíveis</h3>
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {nodeTypes.map((node, index) => (
          <NodeItem
            key={`${node.type}-${index}`}
            type={node.type}
            label={node.label}
            description={node.description}
            icon={node.icon}
            color={node.color}
          />
        ))}
      </div>
    </div>
  );
};

export default NodePalette;