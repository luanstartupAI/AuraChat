import React, { useState, useEffect } from 'react';
// import { useAuth } from '../contexts/AuthContext'; // Assuming AuthContext provides user info
// import { getSettings, updateSetting } from '../services/settingsService'; // Assuming a service file
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { toast } from '@/hooks/use-toast'; // Assuming use-toast hook is set up

const Settings: React.FC = () => {
    // const { user } = useAuth(); // Get user info if needed for profile
    const [profileName, setProfileName] = useState('');
    const [profileEmail, setProfileEmail] = useState('');
    const [whatsappApiKey, setWhatsappApiKey] = useState('');
    const [whatsappPhoneId, setWhatsappPhoneId] = useState('');
    const [whatsappWebhookSecret, setWhatsappWebhookSecret] = useState('');
    const [generalTheme, setGeneralTheme] = useState('system'); // Example setting
    const [isLoading, setIsLoading] = useState(false);

    // Mock function to simulate fetching settings - replace with actual API call
    const fetchSettings = async () => {
        setIsLoading(true);
        console.log("Fetching settings...");
        // Replace with: const response = await getSettings();
        // Mock data:
        await new Promise(resolve => setTimeout(resolve, 500)); // Simulate network delay
        const mockSettings = {
            "WHATSAPP_API_KEY": "mock_api_key_123",
            "WHATSAPP_PHONE_ID": "mock_phone_id_456",
            "WHATSAPP_WEBHOOK_SECRET": "mock_secret_789",
            "GENERAL_THEME": "dark",
            // Mock user data - fetch from user context or separate endpoint
            "USER_FULL_NAME": "Admin User",
            "USER_EMAIL": "admin@aura.com"
        };
        setWhatsappApiKey(mockSettings.WHATSAPP_API_KEY || '');
        setWhatsappPhoneId(mockSettings.WHATSAPP_PHONE_ID || '');
        setWhatsappWebhookSecret(mockSettings.WHATSAPP_WEBHOOK_SECRET || '');
        setGeneralTheme(mockSettings.GENERAL_THEME || 'system');
        setProfileName(mockSettings.USER_FULL_NAME || '');
        setProfileEmail(mockSettings.USER_EMAIL || '');
        console.log("Settings loaded.");
        setIsLoading(false);
    };

    // Mock function to simulate updating a setting - replace with actual API call
    const handleUpdateSetting = async (key: string, value: string) => {
        setIsLoading(true);
        console.log(`Updating setting: ${key}`);
        try {
            // Replace with: await updateSetting(key, value);
            await new Promise(resolve => setTimeout(resolve, 300)); // Simulate network delay
            toast({
                title: "Sucesso",
                description: `Configuração '${key}' atualizada.`,
            });
        } catch (error) {
            console.error(`Error updating setting ${key}:`, error);
            toast({
                title: "Erro",
                description: `Falha ao atualizar a configuração '${key}'.`,
                variant: "destructive",
            });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchSettings();
    }, []);

    const handleProfileSave = () => {
        // Add logic to update user profile via API if needed
        console.log("Profile save clicked (implement API call if needed)");
        toast({ title: "Perfil", description: "Funcionalidade de salvar perfil a ser implementada." });
    };

    return (
        <div className="p-4 md:p-6 lg:p-8">
            <h1 className="text-2xl font-semibold mb-6">Configurações</h1>
            <Tabs defaultValue="profile" className="w-full">
                <TabsList className="grid w-full grid-cols-3 mb-4">
                    <TabsTrigger value="profile">Perfil</TabsTrigger>
                    <TabsTrigger value="integrations">Integrações</TabsTrigger>
                    <TabsTrigger value="general">Geral</TabsTrigger>
                </TabsList>

                {/* Profile Tab */}
                <TabsContent value="profile">
                    <Card>
                        <CardHeader>
                            <CardTitle>Perfil do Usuário</CardTitle>
                            <CardDescription>Gerencie as informações do seu perfil.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="profileName">Nome Completo</Label>
                                <Input id="profileName" value={profileName} onChange={(e) => setProfileName(e.target.value)} disabled={isLoading} />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="profileEmail">Email</Label>
                                <Input id="profileEmail" type="email" value={profileEmail} disabled /> {/* Usually email is not editable here */}
                            </div>
                            {/* Add password change fields if necessary */}
                            <Button onClick={handleProfileSave} disabled={isLoading}>
                                {isLoading ? 'Salvando...' : 'Salvar Alterações'}
                            </Button>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* Integrations Tab */}
                <TabsContent value="integrations">
                    <Card>
                        <CardHeader>
                            <CardTitle>Integração WhatsApp</CardTitle>
                            <CardDescription>Configure suas credenciais da API do WhatsApp Business.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="whatsappApiKey">API Key</Label>
                                <Input id="whatsappApiKey" type="password" value={whatsappApiKey} onChange={(e) => setWhatsappApiKey(e.target.value)} disabled={isLoading} />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="whatsappPhoneId">Phone Number ID</Label>
                                <Input id="whatsappPhoneId" value={whatsappPhoneId} onChange={(e) => setWhatsappPhoneId(e.target.value)} disabled={isLoading} />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="whatsappWebhookSecret">Webhook Verification Token</Label>
                                <Input id="whatsappWebhookSecret" type="password" value={whatsappWebhookSecret} onChange={(e) => setWhatsappWebhookSecret(e.target.value)} disabled={isLoading} />
                            </div>
                            <Button
                                onClick={() => {
                                    handleUpdateSetting('WHATSAPP_API_KEY', whatsappApiKey);
                                    handleUpdateSetting('WHATSAPP_PHONE_ID', whatsappPhoneId);
                                    handleUpdateSetting('WHATSAPP_WEBHOOK_SECRET', whatsappWebhookSecret);
                                }}
                                disabled={isLoading}
                            >
                                {isLoading ? 'Salvando...' : 'Salvar Credenciais WhatsApp'}
                            </Button>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* General Tab */}
                <TabsContent value="general">
                    <Card>
                        <CardHeader>
                            <CardTitle>Configurações Gerais</CardTitle>
                            <CardDescription>Ajustes gerais da aplicação.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="generalTheme">Tema da Aplicação</Label>
                                <select
                                    id="generalTheme"
                                    value={generalTheme}
                                    onChange={(e) => setGeneralTheme(e.target.value)}
                                    className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    disabled={isLoading}
                                >
                                    <option value="system">Sistema</option>
                                    <option value="light">Claro</option>
                                    <option value="dark">Escuro</option>
                                </select>
                            </div>
                            {/* Add other general settings like notifications, language, etc. */}
                            <Button onClick={() => handleUpdateSetting('GENERAL_THEME', generalTheme)} disabled={isLoading}>
                                {isLoading ? 'Salvando...' : 'Salvar Configurações Gerais'}
                            </Button>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default Settings;

