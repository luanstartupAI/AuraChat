import React, { useState, useEffect, useCallback } from 'react';
import {
    getWebhooks, createWebhook, updateWebhook, deleteWebhook
} from '@/services/automationService';
import { Button } from "@/components/ui/button";
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
    Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "@/hooks/use-toast";
import { PlusCircle, Edit, Trash2, Copy, Check } from 'lucide-react';
import { Badge } from "@/components/ui/badge";

// Define available webhook events (should match backend Enum)
const WEBHOOK_EVENTS = [
    { value: "message.received", label: "Mensagem Recebida" },
    { value: "message.sent", label: "Mensagem Enviada" },
    { value: "contact.created", label: "Contato Criado" },
    { value: "contact.updated", label: "Contato Atualizado" },
    { value: "group.updated", label: "Grupo Atualizado" },
    // Add other events as they become available
];

interface Webhook {
    id: number;
    url: string;
    event: string;
    is_active: boolean;
    has_secret?: boolean; // From API response
    secret?: string; // Only available on creation response
    created_at?: string;
}

const Automation: React.FC = () => {
    const [webhooks, setWebhooks] = useState<Webhook[]>([]);
    const [selectedWebhook, setSelectedWebhook] = useState<Webhook | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalMode, setModalMode] = useState<'create' | 'edit'>('create');
    
    // Form state
    const [currentUrl, setCurrentUrl] = useState("");
    const [currentEvent, setCurrentEvent] = useState("");
    const [currentIsActive, setCurrentIsActive] = useState(true);
    const [generateSecret, setGenerateSecret] = useState(false);
    const [createdSecret, setCreatedSecret] = useState<string | null>(null);
    const [copied, setCopied] = useState(false);

    const fetchWebhooks = useCallback(async () => {
        setIsLoading(true);
        try {
            const fetchedWebhooks = await getWebhooks();
            setWebhooks(fetchedWebhooks || []);
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao buscar webhooks.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchWebhooks();
    }, [fetchWebhooks]);

    const resetForm = () => {
        setCurrentUrl("");
        setCurrentEvent("");
        setCurrentIsActive(true);
        setGenerateSecret(false);
        setCreatedSecret(null);
        setCopied(false);
    };

    const handleOpenModal = (mode: 'create' | 'edit', webhook: Webhook | null = null) => {
        setModalMode(mode);
        setSelectedWebhook(webhook);
        setCurrentUrl(webhook?.url || "");
        setCurrentEvent(webhook?.event || "");
        setCurrentIsActive(webhook?.is_active ?? true);
        setGenerateSecret(false); // Reset secret generation option
        setCreatedSecret(null); // Clear any previously created secret
        setCopied(false);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedWebhook(null);
        resetForm();
    };

    const handleSaveWebhook = async () => {
        setIsLoading(true);
        setCreatedSecret(null); // Clear previous secret before saving
        setCopied(false);

        try {
            if (modalMode === 'create') {
                const payload = {
                    url: currentUrl,
                    event: currentEvent,
                    generate_secret: generateSecret,
                };
                const response = await createWebhook(payload);
                if (response.webhook?.secret) {
                    setCreatedSecret(response.webhook.secret);
                }
                toast({ title: "Sucesso", description: "Webhook criado com sucesso." });
                // Keep modal open if secret was generated, otherwise close
                if (!response.webhook?.secret) {
                    handleCloseModal();
                }
            } else if (selectedWebhook) {
                const payload = {
                    url: currentUrl,
                    is_active: currentIsActive,
                    // Event cannot be updated via PUT in the current backend implementation
                };
                await updateWebhook(selectedWebhook.id, payload);
                toast({ title: "Sucesso", description: "Webhook atualizado com sucesso." });
                handleCloseModal();
            }
            fetchWebhooks(); // Refresh list
        } catch (error: any) {
            const errorMsg = error.response?.data?.message || `Falha ao ${modalMode === 'create' ? 'criar' : 'atualizar'} webhook.`;
            toast({ title: "Erro", description: errorMsg, variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteWebhook = async (webhookId: number) => {
        if (!window.confirm("Tem certeza que deseja excluir este webhook?")) return;
        setIsLoading(true);
        try {
            await deleteWebhook(webhookId);
            toast({ title: "Sucesso", description: "Webhook excluído com sucesso." });
            fetchWebhooks(); // Refresh list
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao excluir webhook.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    const handleCopyToClipboard = () => {
        if (createdSecret) {
            navigator.clipboard.writeText(createdSecret).then(() => {
                setCopied(true);
                setTimeout(() => setCopied(false), 2000); // Reset copied state after 2s
            }, (err) => {
                toast({ title: "Erro", description: "Falha ao copiar o segredo.", variant: "destructive" });
                console.error('Could not copy text: ', err);
            });
        }
    };

    return (
        <div className="p-4 md:p-6 lg:p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold">Automação - Webhooks</h1>
                <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                    <DialogTrigger asChild>
                        <Button onClick={() => handleOpenModal('create')}>
                            <PlusCircle className="mr-2 h-4 w-4" /> Novo Webhook
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-lg">
                        <DialogHeader>
                            <DialogTitle>{modalMode === 'create' ? 'Criar Novo Webhook' : 'Editar Webhook'}</DialogTitle>
                            <DialogDescription>
                                {modalMode === 'create' ? 'Configure um novo webhook para receber notificações de eventos.' : 'Edite a URL ou o status do webhook.'}
                            </DialogDescription>
                        </DialogHeader>
                        
                        {createdSecret ? (
                            <div className="py-4 space-y-4">
                                <p className="text-sm font-medium text-green-600">Webhook criado com sucesso!</p>
                                <Label>Segredo Gerado (Copie Agora)</Label>
                                <div className="flex items-center space-x-2">
                                    <Input value={createdSecret} readOnly className="font-mono" />
                                    <Button variant="outline" size="icon" onClick={handleCopyToClipboard} title="Copiar Segredo">
                                        {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
                                    </Button>
                                </div>
                                <p className="text-xs text-destructive">Atenção: Este segredo não será exibido novamente. Copie-o e guarde-o em local seguro.</p>
                            </div>
                        ) : (
                            <div className="grid gap-4 py-4">
                                <div className="space-y-2">
                                    <Label htmlFor="webhookUrl">URL do Webhook</Label>
                                    <Input id="webhookUrl" value={currentUrl} onChange={(e) => setCurrentUrl(e.target.value)} placeholder="https://seu-servidor.com/webhook" disabled={isLoading} />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="webhookEvent">Evento Gatilho</Label>
                                    <Select 
                                        value={currentEvent}
                                        onValueChange={setCurrentEvent}
                                        disabled={isLoading || modalMode === 'edit'} // Event usually not editable
                                    >
                                        <SelectTrigger id="webhookEvent" disabled={modalMode === 'edit'}>
                                            <SelectValue placeholder="Selecione um evento" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {WEBHOOK_EVENTS.map(event => (
                                                <SelectItem key={event.value} value={event.value}>{event.label}</SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                    {modalMode === 'edit' && <p className="text-xs text-muted-foreground">O evento não pode ser alterado. Crie um novo webhook se necessário.</p>}
                                </div>
                                {modalMode === 'create' && (
                                    <div className="flex items-center space-x-2 pt-2">
                                        <Checkbox id="generateSecret" checked={generateSecret} onCheckedChange={(checked) => setGenerateSecret(Boolean(checked))} disabled={isLoading} />
                                        <Label htmlFor="generateSecret" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                            Gerar Segredo de Verificação?
                                        </Label>
                                    </div>
                                )}
                                {modalMode === 'edit' && (
                                    <div className="flex items-center space-x-2 pt-2">
                                        <Switch id="webhookActive" checked={currentIsActive} onCheckedChange={setCurrentIsActive} disabled={isLoading} />
                                        <Label htmlFor="webhookActive">Ativo</Label>
                                    </div>
                                )}
                            </div>
                        )}
                        
                        <DialogFooter>
                            <Button variant="outline" onClick={handleCloseModal}>Cancelar</Button>
                            {!createdSecret && (
                                <Button onClick={handleSaveWebhook} disabled={isLoading || !currentUrl || (modalMode === 'create' && !currentEvent)}>
                                    {isLoading ? 'Salvando...' : (modalMode === 'create' ? 'Criar Webhook' : 'Salvar Alterações')}
                                </Button>
                            )}
                            {createdSecret && (
                                 <Button onClick={handleCloseModal}>Fechar</Button>
                            )}
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {isLoading && webhooks.length === 0 ? (
                <p>Carregando webhooks...</p>
            ) : (
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>URL</TableHead>
                            <TableHead>Evento</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Segredo</TableHead>
                            <TableHead className="text-right">Ações</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {webhooks.map((webhook) => (
                            <TableRow key={webhook.id}>
                                <TableCell className="font-mono text-sm max-w-xs truncate" title={webhook.url}>{webhook.url}</TableCell>
                                <TableCell>{WEBHOOK_EVENTS.find(e => e.value === webhook.event)?.label || webhook.event}</TableCell>
                                <TableCell>
                                    <Badge variant={webhook.is_active ? 'default' : 'outline'}>
                                        {webhook.is_active ? 'Ativo' : 'Inativo'}
                                    </Badge>
                                </TableCell>
                                <TableCell>
                                    {webhook.has_secret ? (
                                        <Badge variant="secondary">Configurado</Badge>
                                    ) : (
                                        <Badge variant="outline">Nenhum</Badge>
                                    )}
                                </TableCell>
                                <TableCell className="text-right">
                                    <Button variant="ghost" size="icon" onClick={() => handleOpenModal('edit', webhook)} title="Editar Webhook">
                                        <Edit className="h-4 w-4" />
                                    </Button>
                                    <Button variant="ghost" size="icon" onClick={() => handleDeleteWebhook(webhook.id)} disabled={isLoading} title="Excluir Webhook">
                                        <Trash2 className="h-4 w-4 text-red-500" />
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            )}
            
            {/* Section for Automation Rules (Placeholder) */}
            {/* <div className="mt-12">
                <h2 className="text-xl font-semibold mb-4">Regras de Automação (Em Breve)</h2>
                <p className="text-muted-foreground">Gerencie regras para automatizar ações baseadas em gatilhos.</p>
            </div> */}

        </div>
    );
};

export default Automation;

