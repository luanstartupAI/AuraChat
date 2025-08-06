import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Play, 
  Pause, 
  Plus, 
  Settings, 
  Bot, 
  Zap, 
  GitBranch, 
  Clock,
  Brain,
  Webhook,
  Variable,
  FileText,
  MessageSquare,
  Send,
  Filter,
  Timer,
  Eye,
  Edit,
  Trash2
} from 'lucide-react';
import FlowEditor from '@/components/automation/FlowEditor';

const Automation: React.FC = () => {
  const [activeTab, setActiveTab] = useState('flows');
  const [showEditor, setShowEditor] = useState(false);

  const activeFlows = 3;
  const totalFlows = 8;
  const executionsToday = 1247;

  const nodeTypes = [
    { type: 'trigger', label: 'Gatilhos', icon: Zap, color: 'bg-yellow-100 text-yellow-600', count: 4 },
    { type: 'action', label: 'Ações', icon: Send, color: 'bg-blue-100 text-blue-600', count: 12 },
    { type: 'condition', label: 'Condições', icon: GitBranch, color: 'bg-purple-100 text-purple-600', count: 6 },
    { type: 'delay', label: 'Atrasos', icon: Clock, color: 'bg-orange-100 text-orange-600', count: 3 },
    { type: 'ai', label: 'IA', icon: Brain, color: 'bg-green-100 text-green-600', count: 8 },
    { type: 'webhook', label: 'Webhooks', icon: Webhook, color: 'bg-red-100 text-red-600', count: 5 },
    { type: 'variable', label: 'Variáveis', icon: Variable, color: 'bg-indigo-100 text-indigo-600', count: 7 },
    { type: 'template', label: 'Templates', icon: FileText, color: 'bg-pink-100 text-pink-600', count: 9 }
  ];

  const recentFlows = [
    {
      id: '1',
      name: 'Boas-vindas Automática',
      description: 'Envia mensagem de boas-vindas para novos contatos',
      status: 'active',
      executions: 156,
      lastExecuted: '2 min atrás'
    },
    {
      id: '2',
      name: 'Suporte Inteligente',
      description: 'Classifica e direciona solicitações de suporte',
      status: 'active',
      executions: 89,
      lastExecuted: '5 min atrás'
    },
    {
      id: '3',
      name: 'Follow-up de Vendas',
      description: 'Acompanha leads após demonstração',
      status: 'paused',
      executions: 23,
      lastExecuted: '1 hora atrás'
    }
  ];

  if (showEditor) {
    return <FlowEditor />;
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Automações</h1>
          <p className="text-gray-600">Crie fluxos inteligentes para automatizar seu WhatsApp</p>
        </div>
        <Button 
          className="bg-blue-600 hover:bg-blue-700"
          onClick={() => setShowEditor(true)}
        >
          <Plus className="w-4 h-4 mr-2" />
          Novo Fluxo
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="flows">Fluxos</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="flows" className="space-y-6">
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Bot className="w-8 h-8 text-blue-600" />
                  <div>
                    <p className="text-sm text-gray-600">Fluxos Ativos</p>
                    <p className="text-2xl font-bold">{activeFlows}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Zap className="w-8 h-8 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-600">Total de Fluxos</p>
                    <p className="text-2xl font-bold">{totalFlows}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Play className="w-8 h-8 text-purple-600" />
                  <div>
                    <p className="text-sm text-gray-600">Execuções Hoje</p>
                    <p className="text-2xl font-bold">{executionsToday}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Settings className="w-8 h-8 text-orange-600" />
                  <div>
                    <p className="text-sm text-gray-600">Taxa de Sucesso</p>
                    <p className="text-2xl font-bold">98.5%</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Node Types */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Bot className="w-5 h-5 mr-2" />
                  Tipos de Nós
                </CardTitle>
                <CardDescription>
                  Blocos disponíveis para criar automações
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {nodeTypes.map((node) => (
                    <div key={node.type} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded-lg ${node.color}`}>
                          <node.icon className="w-4 h-4" />
                        </div>
                        <div>
                          <div className="font-medium">{node.label}</div>
                          <div className="text-sm text-gray-500">{node.count} nós criados</div>
                        </div>
                      </div>
                      <Badge variant="outline">{node.type}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recent Flows */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="w-5 h-5 mr-2" />
                  Fluxos Recentes
                </CardTitle>
                <CardDescription>
                  Seus fluxos de automação mais ativos
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentFlows.map((flow) => (
                    <div key={flow.id} className="p-4 border rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-medium">{flow.name}</h4>
                          <p className="text-sm text-gray-600 mt-1">{flow.description}</p>
                          <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                            <span>{flow.executions} execuções</span>
                            <span>{flow.lastExecuted}</span>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge 
                            variant={flow.status === 'active' ? 'default' : 'secondary'}
                            className={flow.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}
                          >
                            {flow.status === 'active' ? 'Ativo' : 'Pausado'}
                          </Badge>
                          <Button size="sm" variant="ghost">
                            <Eye className="w-3 h-3" />
                          </Button>
                          <Button size="sm" variant="ghost">
                            <Edit className="w-3 h-3" />
                          </Button>
                          <Button size="sm" variant="ghost">
                            <Trash2 className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Play className="w-5 h-5 mr-2" />
                  Ações Rápidas
                </CardTitle>
                <CardDescription>
                  Crie automações comuns rapidamente
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Button className="w-full justify-start" variant="outline">
                    <MessageSquare className="w-4 h-4 mr-2" />
                    Boas-vindas Automática
                  </Button>
                  <Button className="w-full justify-start" variant="outline">
                    <Filter className="w-4 h-4 mr-2" />
                    Classificação de Mensagens
                  </Button>
                  <Button className="w-full justify-start" variant="outline">
                    <Timer className="w-4 h-4 mr-2" />
                    Follow-up de Vendas
                  </Button>
                  <Button className="w-full justify-start" variant="outline">
                    <Brain className="w-4 h-4 mr-2" />
                    Suporte com IA
                  </Button>
                  <Button className="w-full justify-start" variant="outline">
                    <Webhook className="w-4 h-4 mr-2" />
                    Integração Externa
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* AI Integration Info */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Brain className="w-5 h-5 mr-2" />
                Integração com IA (Gemini)
              </CardTitle>
              <CardDescription>
                Recursos de inteligência artificial disponíveis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium mb-2">Classificação de Mensagens</h4>
                  <p className="text-sm text-gray-600">
                    Classifica automaticamente as mensagens recebidas por intenção
                  </p>
                </div>
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium mb-2">Respostas Inteligentes</h4>
                  <p className="text-sm text-gray-600">
                    Gera respostas contextualizadas baseadas no histórico
                  </p>
                </div>
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium mb-2">Análise de Sentimento</h4>
                  <p className="text-sm text-gray-600">
                    Analisa o sentimento das mensagens para melhor atendimento
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="templates">
          <Card>
            <CardHeader>
              <CardTitle>Templates de Automação</CardTitle>
              <CardDescription>
                Templates pré-configurados para criar fluxos rapidamente
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Em desenvolvimento...</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          <Card>
            <CardHeader>
              <CardTitle>Analytics de Automação</CardTitle>
              <CardDescription>
                Métricas e insights sobre seus fluxos de automação
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

export default Automation;

