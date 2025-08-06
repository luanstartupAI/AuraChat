import React, { useState, useRef, useCallback } from 'react';
import { useDrop } from 'react-dnd';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Settings, 
  Trash2, 
  Copy, 
  Eye,
  Play,
  Pause
} from 'lucide-react';
import { FlowNode, Connection, NodeType } from '@/types/automation';

interface FlowCanvasProps {
  nodes: FlowNode[];
  connections: Connection[];
  onUpdateNode: (nodeId: string, data: any) => void;
  onDeleteNode: (nodeId: string) => void;
  onAddConnection: (source: string, target: string) => void;
  showGrid?: boolean;
  zoom?: number;
}

const FlowCanvas: React.FC<FlowCanvasProps> = ({
  nodes,
  connections,
  onUpdateNode,
  onDeleteNode,
  onAddConnection,
  showGrid = true,
  zoom = 1
}) => {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const canvasRef = useRef<HTMLDivElement>(null);

  const [{ isOver }, drop] = useDrop({
    accept: 'NODE',
    drop: (item: { type: NodeType; label: string }, monitor) => {
      const offset = monitor.getClientOffset();
      if (offset && canvasRef.current) {
        const rect = canvasRef.current.getBoundingClientRect();
        const position = {
          x: (offset.x - rect.left) / zoom,
          y: (offset.y - rect.top) / zoom
        };
        
        // Aqui você chamaria a função para adicionar o nó
        console.log('Dropped node:', item, 'at position:', position);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  });

  const handleNodeClick = (nodeId: string) => {
    setSelectedNode(nodeId);
  };

  const handleNodeDrag = useCallback((nodeId: string, position: { x: number; y: number }) => {
    onUpdateNode(nodeId, { position });
  }, [onUpdateNode]);

  const getNodeColor = (type: NodeType): string => {
    const colors = {
      trigger: 'border-yellow-300 bg-yellow-50',
      action: 'border-blue-300 bg-blue-50',
      condition: 'border-purple-300 bg-purple-50',
      delay: 'border-orange-300 bg-orange-50',
      ai: 'border-green-300 bg-green-50',
      webhook: 'border-red-300 bg-red-50',
      variable: 'border-indigo-300 bg-indigo-50',
      template: 'border-pink-300 bg-pink-50'
    };
    return colors[type] || 'border-gray-300 bg-gray-50';
  };

  const getNodeIcon = (type: NodeType) => {
    // Aqui você retornaria o ícone baseado no tipo
    return '⚡';
  };

  return (
    <div 
      ref={drop}
      className={`relative w-full h-full overflow-auto bg-gray-50 ${
        showGrid ? 'bg-grid-pattern' : ''
      } ${isOver ? 'bg-blue-50' : ''}`}
      style={{ 
        transform: `scale(${zoom})`,
        transformOrigin: 'top left'
      }}
    >
      <div ref={canvasRef} className="relative min-w-full min-h-full">
        {/* Grid Pattern */}
        {showGrid && (
          <div 
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage: `
                linear-gradient(to right, #e5e7eb 1px, transparent 1px),
                linear-gradient(to bottom, #e5e7eb 1px, transparent 1px)
              `,
              backgroundSize: '20px 20px'
            }}
          />
        )}

        {/* Nodes */}
        {nodes.map((node) => (
          <div
            key={node.id}
            className={`absolute cursor-move ${getNodeColor(node.type)} ${
              selectedNode === node.id ? 'ring-2 ring-blue-500' : ''
            }`}
            style={{
              left: node.position.x,
              top: node.position.y,
              transform: 'translate(-50%, -50%)'
            }}
            onClick={() => handleNodeClick(node.id)}
          >
            <Card className="w-64 shadow-lg">
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{getNodeIcon(node.type)}</span>
                    <span className="font-medium text-sm">{node.data.label}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={(e) => {
                        e.stopPropagation();
                        // Abrir configurações do nó
                      }}
                    >
                      <Settings className="w-3 h-3" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteNode(node.id);
                      }}
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
                
                <div className="text-xs text-gray-600 mb-2">
                  {node.data.description}
                </div>
                
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="text-xs">
                    {node.type}
                  </Badge>
                  <div className="flex items-center space-x-1">
                    <Button size="sm" variant="ghost">
                      <Play className="w-3 h-3" />
                    </Button>
                    <Button size="sm" variant="ghost">
                      <Eye className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        ))}

        {/* Connections */}
        {connections.map((connection) => {
          const sourceNode = nodes.find(n => n.id === connection.source);
          const targetNode = nodes.find(n => n.id === connection.target);
          
          if (!sourceNode || !targetNode) return null;

          const startX = sourceNode.position.x;
          const startY = sourceNode.position.y;
          const endX = targetNode.position.x;
          const endY = targetNode.position.y;

          return (
            <svg
              key={connection.id}
              className="absolute top-0 left-0 w-full h-full pointer-events-none"
              style={{ zIndex: 1 }}
            >
              <line
                x1={startX}
                y1={startY}
                x2={endX}
                y2={endY}
                stroke="#6b7280"
                strokeWidth="2"
                markerEnd="url(#arrowhead)"
              />
              <defs>
                <marker
                  id="arrowhead"
                  markerWidth="10"
                  markerHeight="7"
                  refX="9"
                  refY="3.5"
                  orient="auto"
                >
                  <polygon
                    points="0 0, 10 3.5, 0 7"
                    fill="#6b7280"
                  />
                </marker>
              </defs>
            </svg>
          );
        })}

        {/* Drop Zone Indicator */}
        {isOver && (
          <div className="absolute inset-0 border-2 border-dashed border-blue-400 bg-blue-50 bg-opacity-50 flex items-center justify-center">
            <div className="text-blue-600 font-medium">
              Solte o nó aqui para adicionar ao fluxo
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FlowCanvas;