import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import Window from '../components/layout/Window';
import { useAuth } from '../contexts/AuthContext';
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap, 
  addEdge, 
  Node, 
  Edge, 
  Connection,
  useNodesState,
  useEdgesState
} from 'reactflow';
import 'reactflow/dist/style.css';
import '../styles/theme.css';

// Tipos de nós personalizados
const nodeTypes = {
  messageNode: MessageNode,
  conditionNode: ConditionNode,
  delayNode: DelayNode,
  actionNode: ActionNode
};

// Componente de nó de mensagem
function MessageNode({ data }: any) {
  return (
    <div className="leopard-flow-node leopard-flow-message-node">
      <div className="leopard-flow-node-header">
        <i className="ph-chat-text"></i>
        <span>Mensagem</span>
      </div>
      <div className="leopard-flow-node-content">
        <p>{data.message || 'Digite sua mensagem...'}</p>
      </div>
    </div>
  );
}

// Componente de nó de condição
function ConditionNode({ data }: any) {
  return (
    <div className="leopard-flow-node leopard-flow-condition-node">
      <div className="leopard-flow-node-header">
        <i className="ph-git-branch"></i>
        <span>Condição</span>
      </div>
      <div className="leopard-flow-node-content">
        <p>{data.condition || 'Defina uma condição...'}</p>
      </div>
      <div className="leopard-flow-node-ports">
        <div className="leopard-flow-node-port">Sim</div>
        <div className="leopard-flow-node-port">Não</div>
      </div>
    </div>
  );
}

// Componente de nó de espera
function DelayNode({ data }: any) {
  return (
    <div className="leopard-flow-node leopard-flow-delay-node">
      <div className="leopard-flow-node-header">
        <i className="ph-clock"></i>
        <span>Espera</span>
      </div>
      <div className="leopard-flow-node-content">
        <p>{data.delay || 'Defina um tempo de espera...'}</p>
      </div>
    </div>
  );
}

// Componente de nó de ação
function ActionNode({ data }: any) {
  return (
    <div className="leopard-flow-node leopard-flow-action-node">
      <div className="leopard-flow-node-header">
        <i className="ph-lightning"></i>
        <span>Ação</span>
      </div>
      <div className="leopard-flow-node-content">
        <p>{data.action || 'Defina uma ação...'}</p>
      </div>
    </div>
  );
}

const FlowEditor: React.FC = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [flowName, setFlowName] = useState('Novo Fluxo');
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [nodeProperties, setNodeProperties] = useState<any>({});
  const [flows, setFlows] = useState<any[]>([]);
  const [currentFlowId, setCurrentFlowId] = useState<number | null>(null);
  
  // Estados para o ReactFlow
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Carregar dados iniciais
  useEffect(() => {
    const fetchFlowData = async () => {
      try {
        // Em produção, isso seria uma chamada real à API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockFlows = [
          {
            id: 1,
            name: 'Boas-vindas',
            active: true,
            nodes: [
              {
                id: '1',
                type: 'messageNode',
                position: { x: 250, y: 100 },
                data: { message: 'Olá! Bem-vindo à nossa empresa. Como posso ajudar?' }
              },
              {
                id: '2',
                type: 'conditionNode',
                position: { x: 250, y: 250 },
                data: { condition: 'Contém "produto"' }
              },
              {
                id: '3',
                type: 'messageNode',
                position: { x: 100, y: 400 },
                data: { message: 'Temos diversos produtos disponíveis. Qual você procura?' }
              },
              {
                id: '4',
                type: 'messageNode',
                position: { x: 400, y: 400 },
                data: { message: 'Como posso ajudar com outras informações?' }
              }
            ],
            edges: [
              { id: 'e1-2', source: '1', target: '2' },
              { id: 'e2-3', source: '2', target: '3', sourceHandle: 'yes' },
              { id: 'e2-4', source: '2', target: '4', sourceHandle: 'no' }
            ]
          },
          {
            id: 2,
            name: 'Suporte Técnico',
            active: false,
            nodes: [
              {
                id: '1',
                type: 'messageNode',
                position: { x: 250, y: 100 },
                data: { message: 'Olá! Você está no suporte técnico. Qual o problema?' }
              },
              {
                id: '2',
                type: 'delayNode',
                position: { x: 250, y: 250 },
                data: { delay: '5 segundos' }
              },
              {
                id: '3',
                type: 'actionNode',
                position: { x: 250, y: 400 },
                data: { action: 'Transferir para atendente' }
              }
            ],
            edges: [
              { id: 'e1-2', source: '1', target: '2' },
              { id: 'e2-3', source: '2', target: '3' }
            ]
          }
        ];
        
        setFlows(mockFlows);
        
        // Carregar o primeiro fluxo por padrão
        if (mockFlows.length > 0) {
          loadFlow(mockFlows[0]);
        }
      } catch (error) {
        console.error('Erro ao carregar dados do editor de fluxos:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchFlowData();
  }, []);

  // Carregar um fluxo específico
  const loadFlow = (flow: any) => {
    setFlowName(flow.name);
    setCurrentFlowId(flow.id);
    setNodes(flow.nodes);
    setEdges(flow.edges);
  };

  // Adicionar uma conexão entre nós
  const onConnect = useCallback((params: Connection) => {
    setEdges((eds) => addEdge(params, eds));
  }, [setEdges]);

  // Selecionar um nó para edição
  const onNodeClick = (_: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
    setNodeProperties(node.data);
  };

  // Atualizar propriedades do nó selecionado
  const updateNodeProperties = (properties: any) => {
    if (!selectedNode) return;
    
    setNodeProperties(properties);
    
    // Atualizar o nó com as novas propriedades
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === selectedNode.id) {
          return {
            ...node,
            data: {
              ...node.data,
              ...properties
            }
          };
        }
        return node;
      })
    );
  };

  // Adicionar um novo nó
  const addNode = (type: string) => {
    const newNode = {
      id: `${Date.now()}`,
      type: `${type}Node`,
      position: { x: 250, y: 250 },
      data: {}
    };
    
    setNodes((nds) => [...nds, newNode]);
  };

  // Salvar o fluxo atual
  const saveFlow = () => {
    const updatedFlow = {
      id: currentFlowId,
      name: flowName,
      nodes,
      edges
    };
    
    // Atualizar o fluxo na lista
    setFlows((flows) =>
      flows.map((flow) => (flow.id === currentFlowId ? updatedFlow : flow))
    );
    
    // Em produção, aqui seria feita uma chamada à API para salvar o fluxo
    alert('Fluxo salvo com sucesso!');
  };

  // Alternar o estado ativo do fluxo
  const toggleFlowActive = (flowId: number) => {
    setFlows((flows) =>
      flows.map((flow) => {
        if (flow.id === flowId) {
          return {
            ...flow,
            active: !flow.active
          };
        }
        return flow;
      })
    );
  };

  return (
    <div className="leopard-app-container">
      <Sidebar />
      
      <div className="leopard-main-content">
        <Header 
          title="Editor de Fluxos" 
          username={user?.name} 
          userAvatar={user?.avatar}
        />
        
        <div className="leopard-flow-editor-container">
          {isLoading ? (
            <div className="leopard-loading">Carregando...</div>
          ) : (
            <>
              <div className="leopard-flow-sidebar">
                <Window title="Fluxos" className="leopard-flow-list-window">
                  <div className="leopard-flow-list">
                    {flows.map((flow) => (
                      <div 
                        key={flow.id} 
                        className={`leopard-flow-item ${currentFlowId === flow.id ? 'active' : ''}`}
                        onClick={() => loadFlow(flow)}
                      >
                        <div className="leopard-flow-item-name">{flow.name}</div>
                        <div 
                          className={`leopard-flow-item-status ${flow.active ? 'active' : 'inactive'}`}
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleFlowActive(flow.id);
                          }}
                        >
                          {flow.active ? 'Ativo' : 'Inativo'}
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="leopard-flow-list-actions">
                    <button className="leopard-button">
                      <i className="ph-plus"></i> Novo Fluxo
                    </button>
                  </div>
                </Window>
                
                <Window title="Nós" className="leopard-flow-nodes-window">
                  <div className="leopard-flow-nodes-palette">
                    <div 
                      className="leopard-flow-node-item"
                      onClick={() => addNode('message')}
                    >
                      <i className="ph-chat-text"></i>
                      <span>Mensagem</span>
                    </div>
                    
                    <div 
                      className="leopard-flow-node-item"
                      onClick={() => addNode('condition')}
                    >
                      <i className="ph-git-branch"></i>
                      <span>Condição</span>
                    </div>
                    
                    <div 
                      className="leopard-flow-node-item"
                      onClick={() => addNode('delay')}
                    >
                      <i className="ph-clock"></i>
                      <span>Espera</span>
                    </div>
                    
                    <div 
                      className="leopard-flow-node-item"
                      onClick={() => addNode('action')}
                    >
                      <i className="ph-lightning"></i>
                      <span>Ação</span>
                    </div>
                  </div>
                </Window>
                
                {selectedNode && (
                  <Window title="Propriedades" className="leopard-flow-properties-window">
                    <div className="leopard-flow-properties">
                      {selectedNode.type === 'messageNode' && (
                        <div className="leopard-flow-property">
                          <label>Mensagem:</label>
                          <textarea
                            value={nodeProperties.message || ''}
                            onChange={(e) => updateNodeProperties({ message: e.target.value })}
                            className="leopard-input"
                            rows={4}
                          />
                        </div>
                      )}
                      
                      {selectedNode.type === 'conditionNode' && (
                        <div className="leopard-flow-property">
                          <label>Condição:</label>
                          <input
                            type="text"
                            value={nodeProperties.condition || ''}
                            onChange={(e) => updateNodeProperties({ condition: e.target.value })}
                            className="leopard-input"
                          />
                        </div>
                      )}
                      
                      {selectedNode.type === 'delayNode' && (
                        <div className="leopard-flow-property">
                          <label>Tempo de espera:</label>
                          <input
                            type="text"
                            value={nodeProperties.delay || ''}
                            onChange={(e) => updateNodeProperties({ delay: e.target.value })}
                            className="leopard-input"
                          />
                        </div>
                      )}
                      
                      {selectedNode.type === 'actionNode' && (
                        <div className="leopard-flow-property">
                          <label>Ação:</label>
                          <input
                            type="text"
                            value={nodeProperties.action || ''}
                            onChange={(e) => updateNodeProperties({ action: e.target.value })}
                            className="leopard-input"
                          />
                        </div>
                      )}
                    </div>
                  </Window>
                )}
              </div>
              
              <div className="leopard-flow-canvas">
                <div className="leopard-flow-header">
                  <input
                    type="text"
                    value={flowName}
                    onChange={(e) => setFlowName(e.target.value)}
                    className="leopard-flow-name-input"
                  />
                  
                  <div className="leopard-flow-actions">
                    <button 
                      className="leopard-button leopard-button-primary"
                      onClick={saveFlow}
                    >
                      <i className="ph-floppy-disk"></i> Salvar
                    </button>
                    
                    <button className="leopard-button">
                      <i className="ph-play"></i> Testar
                    </button>
                  </div>
                </div>
                
                <div className="leopard-flow-editor">
                  <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onNodeClick={onNodeClick}
                    nodeTypes={nodeTypes}
                    fitView
                  >
                    <Background />
                    <Controls />
                    <MiniMap />
                  </ReactFlow>
                </div>
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
          <i className="ph-flow-arrow ph-fill"></i>
          <div className="leopard-dock-indicator"></div>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-users ph-fill"></i>
        </div>
        <div className="leopard-dock-item">
          <i className="ph-gear ph-fill"></i>
        </div>
      </div>
    </div>
  );
};

export default FlowEditor;
