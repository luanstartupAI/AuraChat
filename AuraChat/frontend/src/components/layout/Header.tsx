import React from 'react';
import '../../styles/theme.css';

interface HeaderProps {
  title?: string;
  username?: string;
  userAvatar?: string;
  onProfileClick?: () => void;
  onNotificationsClick?: () => void;
  notificationsCount?: number;
}

const Header: React.FC<HeaderProps> = ({
  title = 'Aura',
  username,
  userAvatar,
  onProfileClick,
  onNotificationsClick,
  notificationsCount = 0
}) => {
  return (
    <header className="leopard-header">
      <div className="leopard-header-title">
        {title}
      </div>
      
      <div className="leopard-header-actions">
        {notificationsCount > 0 && (
          <div 
            className="leopard-header-notifications" 
            onClick={onNotificationsClick}
          >
            <span className="leopard-header-notifications-icon">
              <i className="ph-bell"></i>
            </span>
            <span className="leopard-header-notifications-count">
              {notificationsCount}
            </span>
          </div>
        )}
        
        <div className="leopard-header-user" onClick={onProfileClick}>
          {userAvatar ? (
            <img 
              src={userAvatar} 
              alt={username || 'Usuário'} 
              className="leopard-header-user-avatar" 
            />
          ) : (
            <div className="leopard-header-user-avatar-placeholder">
              {username ? username.charAt(0).toUpperCase() : 'U'}
            </div>
          )}
          <span className="leopard-header-username">{username}</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
