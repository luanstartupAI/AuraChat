import React, { useState, useCallback } from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  Play, 
  Pause, 
  Save, 
  Trash2, 
  Plus,
  Settings,
  Eye,
  EyeOff,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Download,
  Upload
} from 'lucide-react';
import FlowCanvas from './FlowCanvas';
import NodePalette from './NodePalette';
import { FlowNode, Connection, NodeType } from '@/types/automation';

const FlowEditor: React.FC = () => {
  const [nodes, setNodes] = useState<FlowNode[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [showGrid, setShowGrid] = useState(true);
  const [zoom, setZoom] = useState(1);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const addNode = useCallback((nodeType: NodeType, position: { x: number; y: number }) => {
    const newNode: FlowNode = {
      id: `node_${Date.now()}`,
      type: nodeType,
      position,
      data: {
        label: getNodeLabel(nodeType),
        description: getNodeDescription(nodeType),
        icon: getNodeIcon(nodeType),
        color: getNodeColor(nodeType),
        config: getDefaultConfig(nodeType)
      }
    };
    setNodes(prev => [...prev, newNode]);
  }, []);

  const updateNode = useCallback((nodeId: string, data: any) => {
    setNodes(prev => prev.map(node => 
      node.id === nodeId ? { ...node, ...data } : node
    ));
  }, []);

  const deleteNode = useCallback((nodeId: string) => {
    setNodes(prev => prev.filter(node => node.id !== nodeId));
    setConnections(prev => prev.filter(conn => 
      conn.source !== nodeId && conn.target !== nodeId
    ));
  }, []);

  const getNodeLabel = (type: NodeType): string => {
    const labels = {
      trigger: 'Gatilho',
      action: 'Ação',
      condition: 'Condição',
      delay: 'Atraso',
      ai: 'IA',
      webhook: 'Webhook',
      variable: 'Variável',
      template: 'Template'
    };
    return labels[type] || type;
  };

  const getNodeDescription = (type: NodeType): string => {
    const descriptions = {
      trigger: 'Inicia o fluxo de automação',
      action: 'Executa uma ação específica',
      condition: 'Verifica uma condição',
      delay: 'Aguarda um tempo específico',
      ai: 'Processamento de inteligência artificial',
      webhook: 'Chama API externa',
      variable: 'Armazena e manipula variáveis',
      template: 'Aplica templates de mensagem'
    };
    return descriptions[type] || '';
  };

  const getNodeIcon = (type: NodeType): string => {
    const icons = {
      trigger: '⚡',
      action: '▶️',
      condition: '❓',
      delay: '⏰',
      ai: '🤖',
      webhook: '🌐',
      variable: '📦',
      template: '📄'
    };
    return icons[type] || '🔧';
  };

  const getNodeColor = (type: NodeType): string => {
    const colors = {
      trigger: 'bg-yellow-100 text-yellow-600',
      action: 'bg-blue-100 text-blue-600',
      condition: 'bg-purple-100 text-purple-600',
      delay: 'bg-orange-100 text-orange-600',
      ai: 'bg-green-100 text-green-600',
      webhook: 'bg-red-100 text-red-600',
      variable: 'bg-indigo-100 text-indigo-600',
      template: 'bg-pink-100 text-pink-600'
    };
    return colors[type] || 'bg-gray-100 text-gray-600';
  };

  const getDefaultConfig = (type: NodeType): any => {
    const configs = {
      trigger: { event: 'message_received', filters: [] },
      action: { action: 'send_message', params: {} },
      condition: { operator: 'equals', value: '' },
      delay: { duration: 5000 },
      ai: { model: 'gemini', prompt: '' },
      webhook: { url: '', method: 'POST' },
      variable: { name: '', value: '' },
      template: { template_name: '', params: {} }
    };
    return configs[type] || {};
  };

  const handleRun = () => {
    setIsRunning(true);
    // Implementar execução do fluxo
    setTimeout(() => setIsRunning(false), 2000);
  };

  const handleSave = () => {
    const flow = { nodes, connections };
    localStorage.setItem('current_flow', JSON.stringify(flow));
    // Implementar salvamento no backend
  };

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.1, 2));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.1, 0.5));
  const handleResetZoom = () => setZoom(1);

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="h-screen flex flex-col bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Editor de Fluxos</h1>
              <p className="text-gray-600">Crie automações inteligentes para WhatsApp</p>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowGrid(!showGrid)}
              >
                {showGrid ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                Grid
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleZoomOut}
              >
                <ZoomOut className="w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleResetZoom}
              >
                <RotateCcw className="w-4 h-4" />
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleZoomIn}
              >
                <ZoomIn className="w-4 h-4" />
              </Button>
              <Separator orientation="vertical" className="h-6" />
              <Button
                variant="outline"
                size="sm"
                onClick={handleSave}
              >
                <Save className="w-4 h-4 mr-2" />
                Salvar
              </Button>
              <Button
                onClick={handleRun}
                disabled={isRunning}
                className="bg-green-600 hover:bg-green-700"
              >
                {isRunning ? (
                  <Pause className="w-4 h-4 mr-2" />
                ) : (
                  <Play className="w-4 h-4 mr-2" />
                )}
                {isRunning ? 'Executando...' : 'Executar'}
              </Button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex">
          {/* Node Palette */}
          <div className="w-80 bg-white border-r p-4">
            <NodePalette onAddNode={addNode} />
          </div>

          {/* Flow Canvas */}
          <div className="flex-1 relative">
            <FlowCanvas
              nodes={nodes}
              connections={connections}
              onUpdateNode={updateNode}
              onDeleteNode={deleteNode}
              onAddConnection={(source, target) => {
                setConnections(prev => [...prev, { 
                  id: `conn_${Date.now()}`, 
                  source, 
                  target 
                }]);
              }}
              showGrid={showGrid}
              zoom={zoom}
            />
          </div>

          {/* Properties Panel */}
          <div className="w-80 bg-white border-l p-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Propriedades</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium">Zoom</label>
                    <div className="flex items-center space-x-2 mt-1">
                      <Button size="sm" variant="outline" onClick={handleZoomOut}>
                        <ZoomOut className="w-3 h-3" />
                      </Button>
                      <span className="text-sm">{Math.round(zoom * 100)}%</span>
                      <Button size="sm" variant="outline" onClick={handleZoomIn}>
                        <ZoomIn className="w-3 h-3" />
                      </Button>
                    </div>
                  </div>
                  <Separator />
                  <div>
                    <h3 className="font-medium mb-2">Estatísticas</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Nós:</span>
                        <Badge variant="outline">{nodes.length}</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Conexões:</span>
                        <Badge variant="outline">{connections.length}</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Status:</span>
                        <Badge variant={isRunning ? "default" : "secondary"}>
                          {isRunning ? 'Executando' : 'Parado'}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </DndProvider>
  );
};

export default FlowEditor;