import React from 'react';
import '../../styles/theme.css';

interface WindowProps {
  title: string;
  children: React.ReactNode;
  onClose?: () => void;
  onMinimize?: () => void;
  onMaximize?: () => void;
  className?: string;
  width?: string | number;
  height?: string | number;
}

const Window: React.FC<WindowProps> = ({
  title,
  children,
  onClose,
  onMinimize,
  onMaximize,
  className = '',
  width = '100%',
  height = 'auto'
}) => {
  const style = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height
  };

  return (
    <div className={`leopard-window ${className}`} style={style}>
      <div className="leopard-window-titlebar">
        <div className="leopard-window-buttons">
          <div 
            className="leopard-window-button leopard-window-button-close" 
            onClick={onClose}
            title="Fechar"
          />
          <div 
            className="leopard-window-button leopard-window-button-minimize" 
            onClick={onMinimize}
            title="Minimizar"
          />
          <div 
            className="leopard-window-button leopard-window-button-maximize" 
            onClick={onMaximize}
            title="Maximizar"
          />
        </div>
        <div className="leopard-window-title">{title}</div>
      </div>
      <div className="leopard-window-content">
        {children}
      </div>
    </div>
  );
};

export default Window;
