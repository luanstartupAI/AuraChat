# 🎨 DESIGN SYSTEM - AURACHAT

## 🎯 VISÃO GERAL

Baseado no design do **macOS Leopard**, o Design System do AuraChat combina:
- **Elegância** - Design minimalista e moderno
- **Funcionalidade** - Interface intuitiva e eficiente
- **Consistência** - Padrões unificados em toda aplicação
- **Acessibilidade** - Inclusivo para todos os usuários

## 🎨 PALETA DE CORES

### 🌈 **Cores Primárias**
```css
:root {
  /* macOS Leopard Inspired Colors */
  --primary-blue: #007AFF;      /* iOS Blue */
  --primary-green: #34C759;     /* Success Green */
  --primary-orange: #FF9500;    /* Warning Orange */
  --primary-red: #FF3B30;       /* Error Red */
  --primary-purple: #AF52DE;    /* Purple */
  --primary-pink: #FF2D92;      /* Pink */
  
  /* Neutrals */
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-200: #E5E7EB;
  --gray-300: #D1D5DB;
  --gray-400: #9CA3AF;
  --gray-500: #6B7280;
  --gray-600: #4B5563;
  --gray-700: #374151;
  --gray-800: #1F2937;
  --gray-900: #111827;
  
  /* Background Colors */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F9FAFB;
  --bg-tertiary: #F3F4F6;
  --bg-dark: #1F2937;
  
  /* Border Colors */
  --border-light: #E5E7EB;
  --border-medium: #D1D5DB;
  --border-dark: #9CA3AF;
}
```

### 🎭 **Estados de Cores**
```css
/* Interactive States */
--hover-blue: #0056CC;
--active-blue: #004499;
--disabled-gray: #D1D5DB;

/* Status Colors */
--success: #34C759;
--warning: #FF9500;
--error: #FF3B30;
--info: #007AFF;
```

## 📝 TIPOGRAFIA

### 🔤 **Hierarquia de Fontes**
```css
/* Font Family */
--font-sans: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### 📊 **Componentes de Texto**
```tsx
// Heading Components
<Heading size="h1">Título Principal</Heading>
<Heading size="h2">Subtítulo</Heading>
<Heading size="h3">Seção</Heading>

// Text Components
<Text size="lg" weight="semibold">Texto Importante</Text>
<Text size="base" weight="normal">Texto Normal</Text>
<Text size="sm" color="muted">Texto Secundário</Text>
```

## 🧩 COMPONENTES BASE

### 🔘 **Botões**
```tsx
// Button Variants
<Button variant="primary">Ação Principal</Button>
<Button variant="secondary">Ação Secundária</Button>
<Button variant="outline">Ação Outline</Button>
<Button variant="ghost">Ação Ghost</Button>
<Button variant="danger">Ação Perigosa</Button>

// Button Sizes
<Button size="sm">Pequeno</Button>
<Button size="md">Médio</Button>
<Button size="lg">Grande</Button>

// Button States
<Button loading>Carregando...</Button>
<Button disabled>Desabilitado</Button>
```

### 📝 **Inputs**
```tsx
// Input Types
<Input placeholder="Digite aqui..." />
<Input type="email" placeholder="email@exemplo.com" />
<Input type="password" placeholder="Senha" />
<Input type="search" placeholder="Buscar..." />

// Input States
<Input error="Campo obrigatório" />
<Input success="Válido!" />
<Input disabled placeholder="Desabilitado" />

// Input Sizes
<Input size="sm" placeholder="Pequeno" />
<Input size="md" placeholder="Médio" />
<Input size="lg" placeholder="Grande" />
```

### 🎯 **Cards**
```tsx
// Card Variants
<Card>
  <CardHeader>
    <CardTitle>Título do Card</CardTitle>
    <CardDescription>Descrição do card</CardDescription>
  </CardHeader>
  <CardContent>
    Conteúdo do card
  </CardContent>
  <CardFooter>
    <Button>Ação</Button>
  </CardFooter>
</Card>

// Interactive Card
<Card hoverable>
  <CardContent>
    Card com hover effect
  </CardContent>
</Card>
```

## 🎨 COMPONENTES ESPECÍFICOS

### 💬 **Chat Components**
```tsx
// Message Bubble
<MessageBubble 
  type="sent" 
  content="Olá! Como posso ajudar?"
  timestamp="10:30"
  status="read"
/>

<MessageBubble 
  type="received" 
  content="Preciso de ajuda com meu pedido"
  timestamp="10:31"
  avatar="/avatar.jpg"
/>

// Chat Input
<ChatInput 
  onSend={handleSend}
  placeholder="Digite sua mensagem..."
  attachments={true}
  emoji={true}
/>
```

### 📊 **Dashboard Components**
```tsx
// Stat Card
<StatCard 
  title="Conversas Ativas"
  value={42}
  change={+12}
  trend="up"
  icon="chat"
/>

// Activity Feed
<ActivityFeed>
  <ActivityItem 
    type="message"
    user="João Silva"
    action="enviou uma mensagem"
    time="2 min atrás"
  />
</ActivityFeed>
```

### 🎛️ **Automation Components**
```tsx
// Flow Node
<FlowNode 
  type="trigger"
  title="Mensagem Recebida"
  icon="message"
  configurable={true}
/>

<FlowNode 
  type="action"
  title="Enviar Resposta"
  icon="send"
  configurable={true}
/>

// Flow Canvas
<FlowCanvas>
  <FlowNode />
  <FlowConnection />
</FlowCanvas>
```

## 🎨 LAYOUT SYSTEM

### 📐 **Grid System**
```css
/* Grid Breakpoints */
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;

/* Container Max Widths */
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1280px;
```

### 📱 **Responsive Layouts**
```tsx
// Layout Components
<Layout>
  <Sidebar />
  <MainContent>
    <Header />
    <PageContent />
  </MainContent>
</Layout>

// Responsive Grid
<Grid cols={1} md:cols={2} lg:cols={3}>
  <GridItem>Item 1</GridItem>
  <GridItem>Item 2</GridItem>
  <GridItem>Item 3</GridItem>
</Grid>
```

## 🎨 ANIMAÇÕES

### ✨ **Transitions**
```css
/* Transition Durations */
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 350ms;

/* Transition Easing */
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### 🎭 **Animation Components**
```tsx
// Fade In
<FadeIn>
  <Card>Conteúdo animado</Card>
</FadeIn>

// Slide In
<SlideIn direction="up">
  <Notification>Nova mensagem!</Notification>
</SlideIn>

// Scale
<Scale>
  <Button>Botão com escala</Button>
</Scale>
```

## 🎨 ICON SYSTEM

### 🎯 **Icon Library**
```tsx
// Icon Components
<Icon name="chat" size="sm" />
<Icon name="send" size="md" />
<Icon name="settings" size="lg" />

// Icon Categories
// Navigation
chat, dashboard, contacts, kanban, flows, broadcast, settings

// Actions
send, receive, edit, delete, add, search, filter

// Status
online, offline, busy, away, typing, read, delivered

// Communication
message, call, video, file, image, voice, location
```

## 🎨 THEME SYSTEM

### 🌙 **Theme Variants**
```tsx
// Theme Provider
<ThemeProvider theme="light">
  <App />
</ThemeProvider>

<ThemeProvider theme="dark">
  <App />
</ThemeProvider>

// Theme Colors
const lightTheme = {
  bg: '#FFFFFF',
  text: '#1F2937',
  border: '#E5E7EB',
  primary: '#007AFF'
}

const darkTheme = {
  bg: '#1F2937',
  text: '#F9FAFB',
  border: '#374151',
  primary: '#60A5FA'
}
```

## 🎨 ACCESSIBILITY

### ♿ **A11y Guidelines**
```tsx
// ARIA Labels
<Button aria-label="Enviar mensagem">
  <Icon name="send" />
</Button>

// Focus Management
<FocusTrap>
  <Modal>
    <ModalContent />
  </Modal>
</FocusTrap>

// Keyboard Navigation
<KeyboardNav>
  <MenuItem>Item 1</MenuItem>
  <MenuItem>Item 2</MenuItem>
</KeyboardNav>
```

## 🎨 USAGE GUIDELINES

### 📋 **Do's and Don'ts**

#### ✅ **DO**
- Use consistent spacing (8px grid)
- Maintain color contrast ratios (4.5:1 minimum)
- Provide loading states for async actions
- Include error states for form validation
- Use semantic HTML elements

#### ❌ **DON'T**
- Mix different design patterns
- Use too many colors in one interface
- Ignore mobile responsiveness
- Skip accessibility features
- Over-animate elements

### 📚 **Component Documentation**
```tsx
// Example Usage
<Card>
  <CardHeader>
    <CardTitle>Exemplo de Uso</CardTitle>
  </CardHeader>
  <CardContent>
    <Text>Este é um exemplo de como usar o componente Card.</Text>
  </CardContent>
</Card>
```

## 🎯 IMPLEMENTAÇÃO

### 📦 **Package Structure**
```
src/
├── components/
│   ├── ui/           # Base components
│   ├── layout/       # Layout components
│   ├── forms/        # Form components
│   ├── data/         # Data display components
│   └── feedback/     # Feedback components
├── styles/
│   ├── tokens.css    # Design tokens
│   ├── components.css # Component styles
│   └── utilities.css # Utility classes
└── hooks/
    ├── useTheme.ts   # Theme hook
    └── useMedia.ts   # Media query hook
```

Este Design System garante:
- ✅ **Consistência** - Padrões unificados
- ✅ **Escalabilidade** - Componentes reutilizáveis
- ✅ **Acessibilidade** - Inclusivo para todos
- ✅ **Performance** - Otimizado para velocidade
- ✅ **Manutenibilidade** - Fácil de atualizar