import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  House, 
  ChatCircle, 
  Kanban, 
  Robot, 
  FlowArrow, 
  BroadcastTower, 
  Users, 
  UserCircle, 
  Gear, 
  Question,
  Phone
} from 'phosphor-react';

interface SidebarProps {
  collapsed?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed = false }) => {
  const location = useLocation();
  const iconSize = 24;
  const iconWeight = "regular";

  const menuItems = [
    { path: '/', label: 'Dashboard', icon: <House size={iconSize} weight={iconWeight} /> },
    { path: '/chat', label: 'Bate Papo', icon: <ChatCircle size={iconSize} weight={iconWeight} /> },
    { path: '/whatsapp', label: 'WhatsApp', icon: <Phone size={iconSize} weight={iconWeight} /> },
    { path: '/kanban', label: 'Kanban', icon: <Kanban size={iconSize} weight={iconWeight} /> },
    { path: '/ai', label: 'Atendimento (IA)', icon: <Robot size={iconSize} weight={iconWeight} /> },
    { path: '/flows', label: 'Fluxos de Conversa', icon: <FlowArrow size={iconSize} weight={iconWeight} /> },
    { path: '/broadcast', label: 'Transmissão', icon: <BroadcastTower size={iconSize} weight={iconWeight} /> },
    { path: '/audience', label: 'Audiência', icon: <Users size={iconSize} weight={iconWeight} /> },
    { path: '/groups', label: 'Gerente de Grupo', icon: <UserCircle size={iconSize} weight={iconWeight} /> },
    { path: '/settings', label: 'Configurações', icon: <Gear size={iconSize} weight={iconWeight} /> },
    { path: '/support', label: 'Suporte', icon: <Question size={iconSize} weight={iconWeight} /> },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <img src="/logo.png" alt="Aura Logo" />
        {!collapsed && <span style={{ marginLeft: '10px', fontSize: '20px', fontWeight: 'bold' }}>Aura</span>}
      </div>
      
      <ul className="sidebar-menu">
        {menuItems.map((item) => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={`sidebar-menu-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="sidebar-menu-item-icon">{item.icon}</span>
              {!collapsed && <span>{item.label}</span>}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
