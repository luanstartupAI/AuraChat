# Planejamento Detalhado de Módulos - Projeto Aura

## Visão Geral
Este documento detalha o planejamento modular completo para o Projeto Aura, seguindo o design inspirado no macOS Leopard e replicando as funcionalidades do Inzali de forma robusta e escalável.

## Estrutura de Diretórios

```
aura-project/
├── backend/
│   ├── venv/                      # Ambiente virtual Python
│   └── src/
│       ├── config/                # Configurações
│       │   ├── database.py        # Configuração de banco de dados
│       │   ├── security.py        # Configurações de segurança
│       │   └── settings.py        # Configurações gerais
│       ├── models/                # Modelos de dados
│       │   ├── user.py            # Modelo de usuário
│       │   ├── chat.py            # Modelos de chat
│       │   ├── kanban.py          # Modelos de kanban
│       │   ├── flow.py            # Modelos de fluxos
│       │   ├── contact.py         # Modelos de contatos
│       │   ├── broadcast.py       # Modelos de transmissão
│       │   ├── group.py           # Modelos de grupos
│       │   └── automation.py      # Modelos de automação
│       ├── routes/                # Rotas da API
│       │   ├── auth.py            # Autenticação
│       │   ├── chat.py            # Chat ao vivo
│       │   ├── kanban.py          # Kanban
│       │   ├── flow.py            # Fluxos de conversa
│       │   ├── contact.py         # Contatos
│       │   ├── broadcast.py       # Transmissão
│       │   ├── audience.py        # Audiência
│       │   ├── group.py           # Grupos
│       │   ├── automation.py      # Automação
│       │   ├── settings.py        # Configurações
│       │   ├── whatsapp.py        # Integração WhatsApp
│       │   └── ai.py              # IA e automação
│       ├── services/              # Serviços
│       │   ├── auth_service.py    # Serviço de autenticação
│       │   ├── chat_service.py    # Serviço de chat
│       │   ├── kanban_service.py  # Serviço de kanban
│       │   ├── flow_service.py    # Serviço de fluxos
│       │   ├── contact_service.py # Serviço de contatos
│       │   ├── broadcast_service.py # Serviço de transmissão
│       │   ├── whatsapp_service.py # Serviço de WhatsApp
│       │   └── ai_service.py      # Serviço de IA
│       ├── utils/                 # Utilitários
│       │   ├── validators.py      # Validadores
│       │   ├── formatters.py      # Formatadores
│       │   └── helpers.py         # Funções auxiliares
│       ├── websockets/            # WebSockets
│       │   ├── chat.py            # WebSockets para chat
│       │   ├── notifications.py   # WebSockets para notificações
│       │   └── kanban.py          # WebSockets para kanban
│       ├── static/                # Arquivos estáticos
│       ├── templates/             # Templates
│       └── main.py                # Ponto de entrada
└── frontend/
    └── aura-frontend/
        ├── public/                # Arquivos públicos
        │   ├── logo.png           # Logo Aura
        │   └── favicon.ico        # Favicon
        ├── src/
            ├── assets/            # Recursos estáticos
            │   ├── images/        # Imagens
            │   ├── icons/         # Ícones
            │   └── fonts/         # Fontes
            ├── components/        # Componentes React
            │   ├── common/        # Componentes comuns
            │   │   ├── Button.tsx
            │   │   ├── Input.tsx
            │   │   ├── Modal.tsx
            │   │   ├── Dropdown.tsx
            │   │   ├── Card.tsx
            │   │   └── Tooltip.tsx
            │   ├── layout/        # Componentes de layout
            │   │   ├── Sidebar.tsx
            │   │   ├── Header.tsx
            │   │   ├── Footer.tsx
            │   │   └── Window.tsx # Janela estilo macOS
            │   ├── auth/          # Componentes de autenticação
            │   ├── dashboard/     # Componentes de dashboard
            │   ├── chat/          # Componentes de chat
            │   ├── kanban/        # Componentes de kanban
            │   ├── flow/          # Componentes de fluxos
            │   ├── contact/       # Componentes de contatos
            │   ├── broadcast/     # Componentes de transmissão
            │   └── ai/            # Componentes de IA
            ├── contexts/          # Contextos React
            │   ├── AuthContext.tsx
            │   ├── ThemeContext.tsx
            │   ├── ChatContext.tsx
            │   ├── KanbanContext.tsx
            │   └── FlowContext.tsx
            ├── hooks/             # Hooks personalizados
            │   ├── useAuth.ts
            │   ├── useChat.ts
            │   ├── useKanban.ts
            │   ├── useFlow.ts
            │   └── useWebSocket.ts
            ├── pages/             # Páginas
            │   ├── Login.tsx
            │   ├── Register.tsx
            │   ├── Dashboard.tsx
            │   ├── Chat.tsx
            │   ├── Kanban.tsx
            │   ├── FlowEditor.tsx
            │   ├── Contacts.tsx
            │   ├── Broadcast.tsx
            │   ├── Groups.tsx
            │   ├── Automation.tsx
            │   ├── Settings.tsx
            │   └── AIAssistant.tsx
            ├── services/          # Serviços de API
            │   ├── api.ts         # Cliente de API base
            │   ├── authService.ts
            │   ├── chatService.ts
            │   ├── kanbanService.ts
            │   ├── flowService.ts
            │   ├── contactService.ts
            │   ├── broadcastService.ts
            │   └── aiService.ts
            ├── styles/            # Estilos
            │   ├── theme.css      # Tema macOS Leopard
            │   ├── variables.css  # Variáveis CSS
            │   ├── animations.css # Animações
            │   └── global.css     # Estilos globais
            ├── utils/             # Utilitários
            │   ├── formatters.ts
            │   ├── validators.ts
            │   └── helpers.ts
            ├── App.css            # Estilos do App
            ├── App.tsx            # Componente principal
            ├── index.css          # Estilos de índice
            └── index.tsx          # Ponto de entrada
```

## Detalhamento dos Módulos

### Backend

#### 1. Autenticação e Usuários
- **Funcionalidades**:
  - Registro e login de usuários
  - Autenticação JWT com refresh tokens
  - Recuperação de senha
  - Verificação de email
  - Perfis e permissões (RBAC)
  - Sessões múltiplas
  - Auditoria de login

- **Endpoints**:
  - `POST /api/auth/register` - Registro de usuário
  - `POST /api/auth/login` - Login de usuário
  - `POST /api/auth/refresh` - Renovar token
  - `POST /api/auth/forgot-password` - Solicitar recuperação
  - `POST /api/auth/reset-password` - Redefinir senha
  - `GET /api/auth/me` - Perfil do usuário atual
  - `PUT /api/auth/me` - Atualizar perfil
  - `PUT /api/auth/change-password` - Alterar senha

#### 2. Chat ao Vivo
- **Funcionalidades**:
  - WebSockets para comunicação em tempo real
  - Histórico de conversas
  - Suporte a mídia (imagens, áudios, vídeos)
  - Indicador de digitação
  - Status de leitura
  - Arquivamento de conversas
  - Busca em mensagens

- **Endpoints**:
  - `GET /api/chat/conversations` - Lista de conversas
  - `GET /api/chat/conversations/:id` - Detalhes de conversa
  - `POST /api/chat/conversations` - Criar conversa
  - `GET /api/chat/conversations/:id/messages` - Mensagens
  - `POST /api/chat/conversations/:id/messages` - Enviar mensagem
  - `PUT /api/chat/conversations/:id/archive` - Arquivar conversa
  - `PUT /api/chat/conversations/:id/unarchive` - Desarquivar
  - `GET /api/chat/conversations/search` - Buscar em mensagens

- **WebSockets**:
  - `/ws/chat` - Canal de chat em tempo real
  - Eventos: `message`, `typing`, `read`, `online`

#### 3. Kanban
- **Funcionalidades**:
  - Quadros, colunas e cartões
  - Etiquetas coloridas
  - Atribuição de responsáveis
  - Datas de vencimento
  - Comentários
  - Anexos
  - Histórico de alterações

- **Endpoints**:
  - `GET /api/kanban/boards` - Lista de quadros
  - `GET /api/kanban/boards/:id` - Detalhes de quadro
  - `POST /api/kanban/boards` - Criar quadro
  - `PUT /api/kanban/boards/:id` - Atualizar quadro
  - `DELETE /api/kanban/boards/:id` - Excluir quadro
  - `GET /api/kanban/boards/:id/columns` - Colunas do quadro
  - `POST /api/kanban/boards/:id/columns` - Criar coluna
  - `PUT /api/kanban/columns/:id` - Atualizar coluna
  - `DELETE /api/kanban/columns/:id` - Excluir coluna
  - `GET /api/kanban/columns/:id/cards` - Cartões da coluna
  - `POST /api/kanban/columns/:id/cards` - Criar cartão
  - `PUT /api/kanban/cards/:id` - Atualizar cartão
  - `DELETE /api/kanban/cards/:id` - Excluir cartão
  - `PUT /api/kanban/cards/:id/move` - Mover cartão

- **WebSockets**:
  - `/ws/kanban` - Canal de kanban em tempo real
  - Eventos: `card_created`, `card_updated`, `card_moved`, `card_deleted`

#### 4. Fluxos de Conversa
- **Funcionalidades**:
  - Editor visual de fluxos
  - Nós de mensagem, condição, espera, ação
  - Conexões entre nós
  - Variáveis e expressões
  - Testes e simulações
  - Ativação/desativação
  - Métricas de desempenho

- **Endpoints**:
  - `GET /api/flow/flows` - Lista de fluxos
  - `GET /api/flow/flows/:id` - Detalhes de fluxo
  - `POST /api/flow/flows` - Criar fluxo
  - `PUT /api/flow/flows/:id` - Atualizar fluxo
  - `DELETE /api/flow/flows/:id` - Excluir fluxo
  - `PUT /api/flow/flows/:id/activate` - Ativar fluxo
  - `PUT /api/flow/flows/:id/deactivate` - Desativar fluxo
  - `POST /api/flow/flows/:id/test` - Testar fluxo
  - `GET /api/flow/flows/:id/metrics` - Métricas do fluxo
  - `GET /api/flow/nodes/types` - Tipos de nós disponíveis

#### 5. Contatos e Audiência
- **Funcionalidades**:
  - Gerenciamento de contatos
  - Tags e segmentação
  - Campos personalizados
  - Histórico de interações
  - Importação/exportação
  - Listas de distribuição
  - Segmentação dinâmica

- **Endpoints**:
  - `GET /api/contact/contacts` - Lista de contatos
  - `GET /api/contact/contacts/:id` - Detalhes de contato
  - `POST /api/contact/contacts` - Criar contato
  - `PUT /api/contact/contacts/:id` - Atualizar contato
  - `DELETE /api/contact/contacts/:id` - Excluir contato
  - `GET /api/contact/contacts/search` - Buscar contatos
  - `POST /api/contact/contacts/import` - Importar contatos
  - `GET /api/contact/contacts/export` - Exportar contatos
  - `GET /api/audience/segments` - Segmentos de audiência
  - `POST /api/audience/segments` - Criar segmento
  - `GET /api/audience/segments/:id/contacts` - Contatos do segmento

#### 6. Transmissão
- **Funcionalidades**:
  - Campanhas de mensagens
  - Agendamento
  - Modelos de mensagem
  - Personalização de conteúdo
  - Métricas de entrega
  - Limitação de taxa
  - Opt-out automático

- **Endpoints**:
  - `GET /api/broadcast/campaigns` - Lista de campanhas
  - `GET /api/broadcast/campaigns/:id` - Detalhes de campanha
  - `POST /api/broadcast/campaigns` - Criar campanha
  - `PUT /api/broadcast/campaigns/:id` - Atualizar campanha
  - `DELETE /api/broadcast/campaigns/:id` - Excluir campanha
  - `POST /api/broadcast/campaigns/:id/schedule` - Agendar campanha
  - `POST /api/broadcast/campaigns/:id/send` - Enviar campanha
  - `GET /api/broadcast/campaigns/:id/metrics` - Métricas da campanha
  - `GET /api/broadcast/templates` - Modelos de mensagem
  - `POST /api/broadcast/templates` - Criar modelo

#### 7. Integração WhatsApp
- **Funcionalidades**:
  - Webhooks para recebimento
  - Envio de mensagens e mídia
  - QR Code para conexão
  - Status de conexão
  - Múltiplas contas
  - Limitações e quotas
  - Sincronização de status

- **Endpoints**:
  - `POST /api/whatsapp/webhook` - Webhook para recebimento
  - `GET /api/whatsapp/accounts` - Contas conectadas
  - `POST /api/whatsapp/accounts` - Adicionar conta
  - `GET /api/whatsapp/accounts/:id/qrcode` - QR Code para conexão
  - `GET /api/whatsapp/accounts/:id/status` - Status da conexão
  - `POST /api/whatsapp/send/text` - Enviar texto
  - `POST /api/whatsapp/send/media` - Enviar mídia
  - `GET /api/whatsapp/limits` - Limites e quotas

#### 8. IA e Automação
- **Funcionalidades**:
  - Processamento de linguagem natural
  - Respostas automáticas
  - Classificação de intenções
  - Extração de entidades
  - Aprendizado e treinamento
  - Integração com LLMs
  - Análise de sentimento

- **Endpoints**:
  - `POST /api/ai/analyze` - Analisar mensagem
  - `POST /api/ai/generate-response` - Gerar resposta
  - `GET /api/ai/intents` - Lista de intenções
  - `POST /api/ai/intents` - Criar intenção
  - `POST /api/ai/train` - Treinar modelo
  - `GET /api/ai/training/status` - Status do treinamento
  - `POST /api/automation/rules` - Criar regra de automação
  - `GET /api/automation/rules` - Listar regras

### Frontend

#### 1. Design System
- **Componentes Base**:
  - Botões (primário, secundário, terciário)
  - Inputs (texto, número, data, select)
  - Modais e diálogos
  - Cards e painéis
  - Tabs e navegação
  - Tooltips e popovers
  - Janelas estilo macOS (com botões coloridos)
  - Dock inferior

- **Estilo macOS Leopard**:
  - Gradientes Aqua
  - Reflexos e transparências
  - Sombras e elevação
  - Ícones e ilustrações
  - Animações e transições
  - Tipografia
  - Paleta de cores

#### 2. Autenticação
- **Páginas e Componentes**:
  - Login
  - Registro
  - Recuperação de senha
  - Perfil de usuário
  - Configurações de conta
  - Alteração de senha

#### 3. Dashboard
- **Páginas e Componentes**:
  - Visão geral
  - Widgets personalizáveis
  - Gráficos e estatísticas
  - Atividade recente
  - Tarefas pendentes
  - Notificações

#### 4. Chat
- **Páginas e Componentes**:
  - Lista de conversas
  - Interface de chat
  - Envio de mídia
  - Emojis e reações
  - Indicador de digitação
  - Status de leitura
  - Busca em mensagens

#### 5. Kanban
- **Páginas e Componentes**:
  - Lista de quadros
  - Visualização de quadro
  - Drag and drop de cartões
  - Criação e edição de cartões
  - Filtros e busca
  - Etiquetas e cores
  - Atribuição de responsáveis

#### 6. Editor de Fluxos
- **Páginas e Componentes**:
  - Canvas interativo
  - Paleta de nós
  - Conexão de nós
  - Propriedades de nós
  - Validação e teste
  - Visualização de métricas
  - Ativação/desativação

#### 7. Contatos e Audiência
- **Páginas e Componentes**:
  - Lista de contatos
  - Detalhes de contato
  - Importação/exportação
  - Tags e segmentação
  - Histórico de interações
  - Campos personalizados
  - Segmentos de audiência

#### 8. Transmissão
- **Páginas e Componentes**:
  - Lista de campanhas
  - Criação de campanha
  - Agendamento
  - Seleção de audiência
  - Modelos de mensagem
  - Personalização
  - Métricas e relatórios

#### 9. IA e Automação
- **Páginas e Componentes**:
  - Assistente de IA
  - Treinamento de intenções
  - Regras de automação
  - Respostas automáticas
  - Análise de sentimento
  - Métricas de desempenho

## Interfaces e Contratos

### API RESTful
- Formato: JSON
- Autenticação: Bearer Token (JWT)
- Versionamento: `/api/v1/...`
- Paginação: `?page=1&limit=20`
- Ordenação: `?sort=field:asc`
- Filtragem: `?filter[field]=value`
- Códigos de status: 200, 201, 400, 401, 403, 404, 500

### WebSockets
- Protocolo: Socket.IO
- Autenticação: Token na conexão
- Canais: chat, notifications, kanban
- Eventos: message, typing, card_moved, etc.
- Reconexão automática

### Integração WhatsApp
- Webhook: Recebimento de eventos
- API: Envio de mensagens e mídia
- QR Code: Conexão de dispositivo
- Status: Sincronização de estado

## Cronograma de Implementação

### Fase 1: Fundações Robustas (Dias 1-3)
- Configuração avançada de ambientes
- Implementação completa de autenticação
- Design system detalhado
- Estrutura de dados e modelos

### Fase 2: Funcionalidades Core (Dias 4-7)
- Chat ao vivo com WebSockets
- Kanban completo com drag and drop
- Dashboard interativo
- Contatos e audiência

### Fase 3: Funcionalidades Avançadas (Dias 8-12)
- Editor de fluxos visual
- Sistema de transmissão
- Integração WhatsApp
- IA e automação

### Fase 4: Polimento e Documentação (Dias 13-15)
- Testes de integração
- Otimizações de performance
- Documentação detalhada
- Empacotamento final

## Considerações Técnicas

### Segurança
- Autenticação JWT com refresh tokens
- Proteção contra CSRF
- Validação de entrada
- Sanitização de saída
- Rate limiting
- Proteção contra ataques comuns (XSS, SQL Injection)

### Performance
- Caching de dados frequentes
- Otimização de consultas
- Lazy loading de componentes
- Code splitting
- Compressão de assets
- Minificação de código

### Escalabilidade
- Arquitetura modular
- Separação de responsabilidades
- Injeção de dependências
- Padrões de design
- Código testável
- Documentação inline

### Acessibilidade
- Semântica HTML
- Contraste adequado
- Navegação por teclado
- Suporte a leitores de tela
- Estados de foco visíveis
- Textos alternativos

## Próximos Passos

1. Criar estrutura de diretórios conforme planejado
2. Implementar componentes base do design system
3. Desenvolver sistema de autenticação completo
4. Implementar dashboard interativo
5. Desenvolver módulos core (chat, kanban, contatos)
6. Implementar funcionalidades avançadas
7. Integrar todos os componentes
8. Realizar testes e otimizações
9. Documentar e empacotar
