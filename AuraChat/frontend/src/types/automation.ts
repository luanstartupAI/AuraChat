// Tipos para Sistema de Automação

export type NodeType = 
  | 'trigger' 
  | 'action' 
  | 'condition' 
  | 'delay' 
  | 'ai' 
  | 'webhook' 
  | 'variable' 
  | 'template';

export interface NodeData {
  label: string;
  description: string;
  icon: string;
  color: string;
  config: any;
}

export interface FlowNode {
  id: string;
  type: NodeType;
  position: { x: number; y: number };
  data: NodeData;
}

export interface Connection {
  id: string;
  source: string;
  target: string;
  sourceHandle?: string;
  targetHandle?: string;
}

export interface Flow {
  id: string;
  name: string;
  description?: string;
  nodes: FlowNode[];
  connections: Connection[];
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Configurações específicas dos nós
export interface TriggerConfig {
  event: 'message_received' | 'time_based' | 'webhook' | 'manual';
  filters?: {
    field: string;
    operator: string;
    value: any;
  }[];
}

export interface ActionConfig {
  action: 'send_message' | 'send_template' | 'update_contact' | 'create_chat' | 'assign_agent';
  params: Record<string, any>;
}

export interface ConditionConfig {
  operator: 'equals' | 'contains' | 'starts_with' | 'ends_with' | 'regex' | 'ai_classify';
  field: string;
  value: any;
  ai_prompt?: string;
}

export interface DelayConfig {
  duration: number; // milliseconds
  type: 'fixed' | 'random' | 'business_hours';
}

export interface AIConfig {
  model: 'gemini' | 'openai' | 'custom';
  prompt: string;
  temperature?: number;
  max_tokens?: number;
  output_format?: 'text' | 'json' | 'structured';
}

export interface WebhookConfig {
  url: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
  timeout?: number;
}

export interface VariableConfig {
  name: string;
  value: any;
  type: 'string' | 'number' | 'boolean' | 'array' | 'object';
  scope: 'flow' | 'global' | 'contact';
}

export interface TemplateConfig {
  template_name: string;
  params: Record<string, any>;
  language?: string;
}