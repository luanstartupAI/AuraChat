import React, { useState, useEffect, useCallback } from 'react';
import {
    getCampaigns, createCampaign, updateCampaign, cancelCampaign, getCampaignDetails
} from '@/services/broadcastService';
import { getGroups } from '@/services/groupService'; // To select target group
import { Button } from "@/components/ui/button";
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
    Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "@/hooks/use-toast";
import { PlusCircle, Edit, XCircle, Eye, Calendar as CalendarIcon } from 'lucide-react';
import { format } from "date-fns";
import { ptBR } from "date-fns/locale"; // Import ptBR locale
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface Group {
    id: number;
    name: string;
}

interface Campaign {
    id: number;
    name: string;
    status: string;
    message_preview?: string;
    message_content?: string; // For details view
    target_group_id: number | null;
    target_group_name?: string | null;
    scheduled_at: string | null;
    created_at?: string;
    updated_at?: string; // For details view
}

const Broadcast: React.FC = () => {
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [groups, setGroups] = useState<Group[]>([]);
    const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
    const [modalMode, setModalMode] = useState<'create' | 'edit'>('create');
    
    // Form state
    const [currentName, setCurrentName] = useState("");
    const [currentMessage, setCurrentMessage] = useState("");
    const [currentTargetGroupId, setCurrentTargetGroupId] = useState<string>("");
    const [currentScheduledAt, setCurrentScheduledAt] = useState<Date | undefined>(undefined);

    const fetchCampaigns = useCallback(async () => {
        setIsLoading(true);
        try {
            const fetchedCampaigns = await getCampaigns();
            setCampaigns(fetchedCampaigns || []);
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao buscar campanhas.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    }, []);

    const fetchGroupsForSelect = useCallback(async () => {
        try {
            const fetchedGroups = await getGroups();
            setGroups(fetchedGroups || []);
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao buscar grupos para seleção.", variant: "destructive" });
        }
    }, []);

    useEffect(() => {
        fetchCampaigns();
        fetchGroupsForSelect();
    }, [fetchCampaigns, fetchGroupsForSelect]);

    const resetForm = () => {
        setCurrentName("");
        setCurrentMessage("");
        setCurrentTargetGroupId("");
        setCurrentScheduledAt(undefined);
    };

    const handleOpenModal = (mode: 'create' | 'edit', campaign: Campaign | null = null) => {
        setModalMode(mode);
        setSelectedCampaign(campaign);
        setCurrentName(campaign?.name || "");
        setCurrentMessage(campaign?.message_content || ""); // Needs full content for edit
        setCurrentTargetGroupId(campaign?.target_group_id?.toString() || "");
        setCurrentScheduledAt(campaign?.scheduled_at ? new Date(campaign.scheduled_at) : undefined);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedCampaign(null);
        resetForm();
    };

    const handleSaveCampaign = async () => {
        if (!currentTargetGroupId) {
             toast({ title: "Erro", description: "Selecione um grupo de destino.", variant: "destructive" });
             return;
        }
        
        setIsLoading(true);
        const payload = {
            name: currentName,
            message_content: currentMessage,
            target_group_id: parseInt(currentTargetGroupId, 10),
            scheduled_at: currentScheduledAt ? currentScheduledAt.toISOString() : null,
        };

        try {
            if (modalMode === 'create') {
                await createCampaign(payload);
                toast({ title: "Sucesso", description: "Campanha criada com sucesso." });
            } else if (selectedCampaign) {
                // Only allow editing certain fields or based on status
                if (selectedCampaign.status !== 'draft' && selectedCampaign.status !== 'scheduled') {
                     toast({ title: "Erro", description: `Não é possível editar campanha com status '${selectedCampaign.status}'.`, variant: "destructive" });
                     setIsLoading(false);
                     return;
                }
                await updateCampaign(selectedCampaign.id, payload);
                toast({ title: "Sucesso", description: "Campanha atualizada com sucesso." });
            }
            handleCloseModal();
            fetchCampaigns(); // Refresh list
        } catch (error: any) {
            const errorMsg = error.response?.data?.message || `Falha ao ${modalMode === 'create' ? 'criar' : 'atualizar'} campanha.`;
            toast({ title: "Erro", description: errorMsg, variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    const handleCancelCampaign = async (campaignId: number) => {
        if (!window.confirm("Tem certeza que deseja cancelar esta campanha agendada?")) return;
        setIsLoading(true);
        try {
            await cancelCampaign(campaignId);
            toast({ title: "Sucesso", description: "Campanha cancelada com sucesso." });
            fetchCampaigns(); // Refresh list
        } catch (error: any) {
             const errorMsg = error.response?.data?.message || "Falha ao cancelar campanha.";
            toast({ title: "Erro", description: errorMsg, variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    // --- Details Modal Logic ---
    const handleOpenDetailsModal = async (campaign: Campaign) => {
        setIsLoading(true);
        setIsDetailsModalOpen(true);
        setSelectedCampaign(campaign); // Set basic info first
        try {
            const detailedCampaign = await getCampaignDetails(campaign.id);
            setSelectedCampaign(detailedCampaign); // Update with full details
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao buscar detalhes da campanha.", variant: "destructive" });
            setIsDetailsModalOpen(false); // Close modal on error
            setSelectedCampaign(null);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCloseDetailsModal = () => {
        setIsDetailsModalOpen(false);
        setSelectedCampaign(null);
    };

    const getStatusBadgeVariant = (status: string): "default" | "secondary" | "destructive" | "outline" => {
        switch (status) {
            case 'completed': return 'default'; // Greenish in default theme
            case 'sending': return 'default';
            case 'scheduled': return 'secondary'; // Bluish
            case 'draft': return 'outline'; // Greyish
            case 'failed': return 'destructive'; // Red
            case 'cancelled': return 'destructive';
            default: return 'outline';
        }
    };

    return (
        <div className="p-4 md:p-6 lg:p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold">Transmissão</h1>
                <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                    <DialogTrigger asChild>
                        <Button onClick={() => handleOpenModal('create')}>
                            <PlusCircle className="mr-2 h-4 w-4" /> Nova Campanha
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-lg">
                        <DialogHeader>
                            <DialogTitle>{modalMode === 'create' ? 'Criar Nova Campanha' : 'Editar Campanha'}</DialogTitle>
                            <DialogDescription>
                                {modalMode === 'create' ? 'Preencha os detalhes para criar uma nova campanha de transmissão.' : 'Edite os detalhes da campanha (apenas rascunhos ou agendadas).'}
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="space-y-2">
                                <Label htmlFor="campaignName">Nome da Campanha</Label>
                                <Input id="campaignName" value={currentName} onChange={(e) => setCurrentName(e.target.value)} disabled={isLoading || (modalMode === 'edit' && selectedCampaign?.status !== 'draft' && selectedCampaign?.status !== 'scheduled')} />
                            </div>
                             <div className="space-y-2">
                                <Label htmlFor="targetGroup">Grupo de Destino</Label>
                                <Select 
                                    value={currentTargetGroupId}
                                    onValueChange={setCurrentTargetGroupId}
                                    disabled={isLoading || (modalMode === 'edit' && selectedCampaign?.status !== 'draft' && selectedCampaign?.status !== 'scheduled')}
                                >
                                    <SelectTrigger id="targetGroup">
                                        <SelectValue placeholder="Selecione um grupo" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {groups.map(group => (
                                            <SelectItem key={group.id} value={group.id.toString()}>{group.name}</SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="message">Mensagem</Label>
                                <Textarea id="message" value={currentMessage} onChange={(e) => setCurrentMessage(e.target.value)} rows={5} disabled={isLoading || (modalMode === 'edit' && selectedCampaign?.status !== 'draft' && selectedCampaign?.status !== 'scheduled')} />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="schedule">Agendar Envio (Opcional)</Label>
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <Button
                                            variant={"outline"}
                                            className={cn(
                                                "w-full justify-start text-left font-normal",
                                                !currentScheduledAt && "text-muted-foreground"
                                            )}
                                             disabled={isLoading || (modalMode === 'edit' && selectedCampaign?.status !== 'draft' && selectedCampaign?.status !== 'scheduled')}
                                        >
                                            <CalendarIcon className="mr-2 h-4 w-4" />
                                            {currentScheduledAt ? format(currentScheduledAt, "PPP HH:mm", { locale: ptBR }) : <span>Não agendado (enviar agora ou salvar como rascunho)</span>}
                                        </Button>
                                    </PopoverTrigger>
                                    <PopoverContent className="w-auto p-0">
                                        <Calendar
                                            mode="single"
                                            selected={currentScheduledAt}
                                            onSelect={setCurrentScheduledAt}
                                            initialFocus
                                        />
                                        {/* Basic Time Picker - Consider a dedicated library for better UX */}
                                        <div className="p-2 border-t">
                                            <Input 
                                                type="time" 
                                                step="60" // Only hours and minutes
                                                defaultValue={currentScheduledAt ? format(currentScheduledAt, "HH:mm") : "09:00"}
                                                onChange={(e) => {
                                                    const time = e.target.value;
                                                    const [hours, minutes] = time.split(':').map(Number);
                                                    setCurrentScheduledAt(prev => {
                                                        const newDate = prev ? new Date(prev) : new Date();
                                                        newDate.setHours(hours, minutes, 0, 0);
                                                        return newDate;
                                                    });
                                                }}
                                            />
                                        </div>
                                        <Button variant="ghost" size="sm" className="w-full justify-center" onClick={() => setCurrentScheduledAt(undefined)}>Limpar Agendamento</Button>
                                    </PopoverContent>
                                </Popover>
                                <p className="text-xs text-muted-foreground">
                                    Se não agendado, a campanha será criada como rascunho ou enviada imediatamente (dependendo da lógica do backend).
                                </p>
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={handleCloseModal}>Cancelar</Button>
                            <Button onClick={handleSaveCampaign} disabled={isLoading || !currentName || !currentMessage || !currentTargetGroupId}>
                                {isLoading ? 'Salvando...' : (modalMode === 'create' ? 'Criar Campanha' : 'Salvar Alterações')}
                            </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {isLoading && campaigns.length === 0 ? (
                <p>Carregando campanhas...</p>
            ) : (
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Nome</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Grupo</TableHead>
                            <TableHead>Agendado Para</TableHead>
                            <TableHead>Mensagem (Prévia)</TableHead>
                            <TableHead className="text-right">Ações</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {campaigns.map((campaign) => (
                            <TableRow key={campaign.id}>
                                <TableCell className="font-medium">{campaign.name}</TableCell>
                                <TableCell>
                                    <Badge variant={getStatusBadgeVariant(campaign.status)}>{campaign.status.toUpperCase()}</Badge>
                                </TableCell>
                                <TableCell>{campaign.target_group_name || `ID: ${campaign.target_group_id}` || '-'}</TableCell>
                                <TableCell>{campaign.scheduled_at ? format(new Date(campaign.scheduled_at), "dd/MM/yy HH:mm", { locale: ptBR }) : '-'}</TableCell>
                                <TableCell className="text-sm text-muted-foreground">{campaign.message_preview || '-'}</TableCell>
                                <TableCell className="text-right">
                                    <Button variant="ghost" size="icon" onClick={() => handleOpenDetailsModal(campaign)} title="Ver Detalhes">
                                        <Eye className="h-4 w-4" />
                                    </Button>
                                    {(campaign.status === 'draft' || campaign.status === 'scheduled') && (
                                        <Button variant="ghost" size="icon" onClick={() => handleOpenModal('edit', campaign)} title="Editar Campanha">
                                            <Edit className="h-4 w-4" />
                                        </Button>
                                    )}
                                    {campaign.status === 'scheduled' && (
                                        <Button variant="ghost" size="icon" onClick={() => handleCancelCampaign(campaign.id)} disabled={isLoading} title="Cancelar Agendamento">
                                            <XCircle className="h-4 w-4 text-red-500" />
                                        </Button>
                                    )}
                                    {/* Add delete button if implemented */}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            )}

            {/* Details Modal */}
            <Dialog open={isDetailsModalOpen} onOpenChange={setIsDetailsModalOpen}>
                <DialogContent className="sm:max-w-lg">
                    <DialogHeader>
                        <DialogTitle>Detalhes da Campanha: {selectedCampaign?.name}</DialogTitle>
                        <DialogDescription>
                            Status: <Badge variant={getStatusBadgeVariant(selectedCampaign?.status || '')}>{selectedCampaign?.status?.toUpperCase()}</Badge> | 
                            Grupo: {selectedCampaign?.target_group_name || '-'}
                        </DialogDescription>
                    </DialogHeader>
                    <div className="py-4 space-y-4">
                         <div>
                            <Label className="font-semibold">Agendamento:</Label>
                            <p className="text-sm">{selectedCampaign?.scheduled_at ? format(new Date(selectedCampaign.scheduled_at), "dd/MM/yyyy 'às' HH:mm", { locale: ptBR }) : 'Não agendado'}</p>
                        </div>
                        <div>
                            <Label className="font-semibold">Mensagem Completa:</Label>
                            <ScrollArea className="h-40 w-full rounded-md border p-3 mt-1">
                                <p className="text-sm whitespace-pre-wrap">{isLoading ? 'Carregando...' : (selectedCampaign?.message_content || 'N/A')}</p>
                            </ScrollArea>
                        </div>
                        {/* Add campaign metrics here when available */}
                        {/* <div><Label className="font-semibold">Métricas:</Label><p>Enviados: X, Falhas: Y</p></div> */}
                         <div>
                            <Label className="font-semibold">Criada em:</Label>
                            <p className="text-sm">{selectedCampaign?.created_at ? format(new Date(selectedCampaign.created_at), "dd/MM/yyyy HH:mm", { locale: ptBR }) : '-'}</p>
                        </div>
                         <div>
                            <Label className="font-semibold">Última Atualização:</Label>
                            <p className="text-sm">{selectedCampaign?.updated_at ? format(new Date(selectedCampaign.updated_at), "dd/MM/yyyy HH:mm", { locale: ptBR }) : '-'}</p>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="secondary" onClick={handleCloseDetailsModal}>Fechar</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

        </div>
    );
};

export default Broadcast;

