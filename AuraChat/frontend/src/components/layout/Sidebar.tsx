import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { PhosphorIcon } from '@phosphor-icons/react';
import '../../styles/theme.css';

interface SidebarItemProps {
  to: string;
  icon: React.ReactNode;
  label: string;
}

const SidebarItem: React.FC<SidebarItemProps> = ({ to, icon, label }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link to={to} className={`leopard-sidebar-item ${isActive ? 'active' : ''}`}>
      <span className="leopard-sidebar-icon">{icon}</span>
      <span className="leopard-sidebar-item-text">{label}</span>
    </Link>
  );
};

const Sidebar: React.FC = () => {
  return (
    <div className="leopard-sidebar">
      <div className="leopard-sidebar-logo">
        <img src="/logo.png" alt="Aura" width="40" height="40" />
      </div>
      
      <div className="leopard-sidebar-items">
        <SidebarItem to="/dashboard" icon={<PhosphorIcon weight="fill" icon="House" />} label="Dashboard" />
        <SidebarItem to="/chat" icon={<PhosphorIcon weight="fill" icon="ChatCircle" />} label="Chat" />
        <SidebarItem to="/kanban" icon={<PhosphorIcon weight="fill" icon="Kanban" />} label="Kanban" />
        <SidebarItem to="/flow-editor" icon={<PhosphorIcon weight="fill" icon="FlowArrow" />} label="Fluxos" />
        <SidebarItem to="/contacts" icon={<PhosphorIcon weight="fill" icon="AddressBook" />} label="Contatos" />
        <SidebarItem to="/broadcast" icon={<PhosphorIcon weight="fill" icon="Megaphone" />} label="Transmissão" />
        <SidebarItem to="/groups" icon={<PhosphorIcon weight="fill" icon="Users" />} label="Grupos" />
        <SidebarItem to="/ai-assistant" icon={<PhosphorIcon weight="fill" icon="Robot" />} label="IA" />
        <SidebarItem to="/settings" icon={<PhosphorIcon weight="fill" icon="Gear" />} label="Configurações" />
      </div>
      
      <div className="leopard-sidebar-footer">
        <SidebarItem to="/profile" icon={<PhosphorIcon weight="fill" icon="User" />} label="Perfil" />
        <SidebarItem to="/logout" icon={<PhosphorIcon weight="fill" icon="SignOut" />} label="Sair" />
      </div>
    </div>
  );
};

export default Sidebar;
