import React, { useState, useEffect, useCallback } from 'react';
import {
    getGroups, createGroup, updateGroup, deleteGroup, 
    getGroupDetails, addContactToGroup, removeContactFromGroup, getContacts
} from '@/services/groupService'; // Assuming groupService handles API calls
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
import { toast } from "@/hooks/use-toast";
import { PlusCircle, Edit, Trash2, UserPlus, X } from 'lucide-react';
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

interface Contact {
    id: number;
    name: string;
    phone_number: string;
}

interface Group {
    id: number;
    name: string;
    description: string | null;
    contacts_count?: number;
    created_at?: string;
    contacts?: Contact[]; // Added for details view
}

const GroupManager: React.FC = () => {
    const [groups, setGroups] = useState<Group[]>([]);
    const [selectedGroup, setSelectedGroup] = useState<Group | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
    const [isAddContactModalOpen, setIsAddContactModalOpen] = useState(false);
    const [modalMode, setModalMode] = useState<	'create	' | 	'edit	'>(	'create	');
    const [currentName, setCurrentName] = useState("");
    const [currentDescription, setCurrentDescription] = useState("");
    const [searchTerm, setSearchTerm] = useState("");
    const [availableContacts, setAvailableContacts] = useState<Contact[]>([]);
    const [contactsToAdd, setContactsToAdd] = useState<Set<number>>(new Set());

    const fetchGroups = useCallback(async () => {
        setIsLoading(true);
        try {
            const fetchedGroups = await getGroups();
            setGroups(fetchedGroups || []);
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao buscar grupos.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchGroups();
    }, [fetchGroups]);

    const handleOpenModal = (mode: 	'create	' | 	'edit	', group: Group | null = null) => {
        setModalMode(mode);
        setSelectedGroup(group);
        setCurrentName(group?.name || "");
        setCurrentDescription(group?.description || "");
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedGroup(null);
        setCurrentName("");
        setCurrentDescription("");
    };

    const handleSaveGroup = async () => {
        setIsLoading(true);
        try {
            if (modalMode === 	'create	') {
                await createGroup(currentName, currentDescription);
                toast({ title: "Sucesso", description: "Grupo criado com sucesso." });
            } else if (selectedGroup) {
                await updateGroup(selectedGroup.id, currentName, currentDescription);
                toast({ title: "Sucesso", description: "Grupo atualizado com sucesso." });
            }
            handleCloseModal();
            fetchGroups(); // Refresh list
        } catch (error) {
            toast({ title: "Erro", description: `Falha ao ${modalMode === 	'create	' ? 	'criar	' : 	'atualizar	'} grupo.`, variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteGroup = async (groupId: number) => {
        if (!window.confirm("Tem certeza que deseja excluir este grupo?")) return;
        setIsLoading(true);
        try {
            await deleteGroup(groupId);
            toast({ title: "Sucesso", description: "Grupo excluído com sucesso." });
            fetchGroups(); // Refresh list
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao excluir grupo.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    // --- Details Modal Logic ---
    const handleOpenDetailsModal = async (group: Group) => {
        setIsLoading(true);
        setIsDetailsModalOpen(true);
        setSelectedGroup(group); // Set basic info first
        try {
            const detailedGroup = await getGroupDetails(group.id);
            setSelectedGroup(detailedGroup); // Update with full details including contacts
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao buscar detalhes do grupo.", variant: "destructive" });
            setIsDetailsModalOpen(false); // Close modal on error
            setSelectedGroup(null);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCloseDetailsModal = () => {
        setIsDetailsModalOpen(false);
        setSelectedGroup(null);
    };

    // --- Add Contact Modal Logic ---
    const handleOpenAddContactModal = async (group: Group) => {
        setSelectedGroup(group);
        setSearchTerm("");
        setAvailableContacts([]);
        setContactsToAdd(new Set());
        setIsAddContactModalOpen(true);
        // Optionally pre-fetch some contacts or wait for search
    };

    const handleCloseAddContactModal = () => {
        setIsAddContactModalOpen(false);
        setSelectedGroup(null);
    };

    const handleSearchContacts = useCallback(async () => {
        if (!searchTerm) {
            setAvailableContacts([]);
            return;
        }
        setIsLoading(true);
        try {
            const fetchedContacts = await getContacts(searchTerm);
            // Filter out contacts already in the selected group
            const groupContactIds = new Set(selectedGroup?.contacts?.map(c => c.id) || []);
            setAvailableContacts(fetchedContacts.filter((c: Contact) => !groupContactIds.has(c.id)));
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao buscar contatos.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    }, [searchTerm, selectedGroup]);

    useEffect(() => {
        const delayDebounceFn = setTimeout(() => {
            if (isAddContactModalOpen) {
                handleSearchContacts();
            }
        }, 500); // Debounce search

        return () => clearTimeout(delayDebounceFn);
    }, [searchTerm, isAddContactModalOpen, handleSearchContacts]);

    const handleToggleContactSelection = (contactId: number) => {
        setContactsToAdd(prev => {
            const newSet = new Set(prev);
            if (newSet.has(contactId)) {
                newSet.delete(contactId);
            } else {
                newSet.add(contactId);
            }
            return newSet;
        });
    };

    const handleAddSelectedContacts = async () => {
        if (!selectedGroup || contactsToAdd.size === 0) return;
        setIsLoading(true);
        const promises = Array.from(contactsToAdd).map(contactId => 
            addContactToGroup(selectedGroup.id, contactId)
        );
        try {
            await Promise.all(promises);
            toast({ title: "Sucesso", description: `${contactsToAdd.size} contato(s) adicionado(s) ao grupo.` });
            handleCloseAddContactModal();
            // Refresh group details in the background or when details modal is opened next time
            fetchGroups(); // Refresh count in main list
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao adicionar contatos.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    const handleRemoveContact = async (groupId: number, contactId: number) => {
        if (!window.confirm("Remover este contato do grupo?")) return;
        setIsLoading(true);
        try {
            await removeContactFromGroup(groupId, contactId);
            toast({ title: "Sucesso", description: "Contato removido do grupo." });
            // Refresh details modal content
            const detailedGroup = await getGroupDetails(groupId);
            setSelectedGroup(detailedGroup);
             fetchGroups(); // Refresh count in main list
        } catch (error) {
            toast({ title: "Erro", description: "Falha ao remover contato.", variant: "destructive" });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="p-4 md:p-6 lg:p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold">Gerente de Grupo</h1>
                <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                    <DialogTrigger asChild>
                        <Button onClick={() => handleOpenModal(	'create	')}>
                            <PlusCircle className="mr-2 h-4 w-4" /> Novo Grupo
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px]">
                        <DialogHeader>
                            <DialogTitle>{modalMode === 	'create	' ? 	'Criar Novo Grupo	' : 	'Editar Grupo	'}</DialogTitle>
                            <DialogDescription>
                                {modalMode === 	'create	' ? 	'Preencha os detalhes para criar um novo grupo.	' : 	'Edite os detalhes do grupo.	'}
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="name" className="text-right">Nome</Label>
                                <Input id="name" value={currentName} onChange={(e) => setCurrentName(e.target.value)} className="col-span-3" />
                            </div>
                            <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="description" className="text-right">Descrição</Label>
                                <Textarea id="description" value={currentDescription} onChange={(e) => setCurrentDescription(e.target.value)} className="col-span-3" />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={handleCloseModal}>Cancelar</Button>
                            <Button onClick={handleSaveGroup} disabled={isLoading || !currentName}>
                                {isLoading ? 	'Salvando...	' : 	'Salvar	'}
                            </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>

            {isLoading && groups.length === 0 ? (
                <p>Carregando grupos...</p>
            ) : (
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Nome</TableHead>
                            <TableHead>Descrição</TableHead>
                            <TableHead className="text-center">Contatos</TableHead>
                            <TableHead className="text-right">Ações</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {groups.map((group) => (
                            <TableRow key={group.id}>
                                <TableCell className="font-medium cursor-pointer hover:underline" onClick={() => handleOpenDetailsModal(group)}>{group.name}</TableCell>
                                <TableCell>{group.description}</TableCell>
                                <TableCell className="text-center">{group.contacts_count ?? 	'-	'}</TableCell>
                                <TableCell className="text-right">
                                    <Button variant="ghost" size="icon" onClick={() => handleOpenAddContactModal(group)} title="Adicionar Contatos">
                                        <UserPlus className="h-4 w-4" />
                                    </Button>
                                    <Button variant="ghost" size="icon" onClick={() => handleOpenModal(	'edit	', group)} title="Editar Grupo">
                                        <Edit className="h-4 w-4" />
                                    </Button>
                                    <Button variant="ghost" size="icon" onClick={() => handleDeleteGroup(group.id)} disabled={isLoading} title="Excluir Grupo">
                                        <Trash2 className="h-4 w-4 text-red-500" />
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            )}

            {/* Details Modal */}
            <Dialog open={isDetailsModalOpen} onOpenChange={setIsDetailsModalOpen}>
                <DialogContent className="sm:max-w-md">
                    <DialogHeader>
                        <DialogTitle>Detalhes do Grupo: {selectedGroup?.name}</DialogTitle>
                        <DialogDescription>{selectedGroup?.description}</DialogDescription>
                    </DialogHeader>
                    <div className="py-4">
                        <h4 className="mb-2 font-semibold">Contatos no Grupo ({selectedGroup?.contacts?.length || 0})</h4>
                        <ScrollArea className="h-48 w-full rounded-md border p-2">
                            {isLoading && !selectedGroup?.contacts ? (
                                <p>Carregando contatos...</p>
                            ) : selectedGroup?.contacts && selectedGroup.contacts.length > 0 ? (
                                <ul className="space-y-1">
                                    {selectedGroup.contacts.map(contact => (
                                        <li key={contact.id} className="flex justify-between items-center text-sm p-1 rounded hover:bg-muted">
                                            <span>{contact.name} ({contact.phone_number})</span>
                                            <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => handleRemoveContact(selectedGroup.id, contact.id)} disabled={isLoading} title="Remover Contato">
                                                <X className="h-4 w-4 text-red-500" />
                                            </Button>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="text-sm text-muted-foreground">Nenhum contato neste grupo.</p>
                            )}
                        </ScrollArea>
                    </div>
                    <DialogFooter>
                         <Button variant="outline" onClick={() => handleOpenAddContactModal(selectedGroup!)} disabled={!selectedGroup}>
                            <UserPlus className="mr-2 h-4 w-4" /> Adicionar Contatos
                        </Button>
                        <Button variant="secondary" onClick={handleCloseDetailsModal}>Fechar</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Add Contact Modal */}
             <Dialog open={isAddContactModalOpen} onOpenChange={setIsAddContactModalOpen}>
                <DialogContent className="sm:max-w-lg">
                    <DialogHeader>
                        <DialogTitle>Adicionar Contatos a "{selectedGroup?.name}"</DialogTitle>
                        <DialogDescription>Busque e selecione os contatos para adicionar ao grupo.</DialogDescription>
                    </DialogHeader>
                    <div className="py-4 space-y-4">
                        <Input 
                            placeholder="Buscar contatos por nome ou telefone..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                        <ScrollArea className="h-64 w-full rounded-md border">
                            {isLoading && <p className="p-4 text-sm text-muted-foreground">Buscando...</p>}
                            {!isLoading && availableContacts.length === 0 && searchTerm && (
                                <p className="p-4 text-sm text-muted-foreground">Nenhum contato encontrado ou já estão no grupo.</p>
                            )}
                             {!isLoading && availableContacts.length === 0 && !searchTerm && (
                                <p className="p-4 text-sm text-muted-foreground">Digite para buscar contatos.</p>
                            )}
                            {availableContacts.length > 0 && (
                                <div className="p-1">
                                    {availableContacts.map(contact => (
                                        <div 
                                            key={contact.id} 
                                            className={`flex items-center justify-between p-2 rounded cursor-pointer hover:bg-muted ${contactsToAdd.has(contact.id) ? 'bg-muted' : ''}`}
                                            onClick={() => handleToggleContactSelection(contact.id)}
                                        >
                                            <Label htmlFor={`contact-${contact.id}`} className="flex-grow cursor-pointer">
                                                {contact.name} ({contact.phone_number})
                                            </Label>
                                            <Input 
                                                type="checkbox" 
                                                id={`contact-${contact.id}`} 
                                                checked={contactsToAdd.has(contact.id)} 
                                                readOnly
                                                className="ml-4 h-4 w-4 cursor-pointer"
                                            />
                                        </div>
                                    ))}
                                </div>
                            )}
                        </ScrollArea>
                        {contactsToAdd.size > 0 && (
                             <p className="text-sm text-muted-foreground">{contactsToAdd.size} contato(s) selecionado(s).</p>
                        )}
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={handleCloseAddContactModal}>Cancelar</Button>
                        <Button onClick={handleAddSelectedContacts} disabled={isLoading || contactsToAdd.size === 0}>
                            {isLoading ? 'Adicionando...' : `Adicionar ${contactsToAdd.size} Contato(s)`}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

        </div>
    );
};

export default GroupManager;

