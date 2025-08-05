import React from 'react';
import '../../styles/theme.css';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
  icon?: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'secondary',
  size = 'md',
  fullWidth = false,
  disabled = false,
  onClick,
  type = 'button',
  className = '',
  icon
}) => {
  const getBaseClasses = () => {
    return 'leopard-button';
  };

  const getVariantClasses = () => {
    switch (variant) {
      case 'primary':
        return 'leopard-button-primary';
      case 'danger':
        return 'leopard-button-danger';
      case 'success':
        return 'leopard-button-success';
      default:
        return '';
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return 'leopard-button-sm';
      case 'lg':
        return 'leopard-button-lg';
      default:
        return '';
    }
  };

  const getWidthClasses = () => {
    return fullWidth ? 'w-full' : '';
  };

  const classes = [
    getBaseClasses(),
    getVariantClasses(),
    getSizeClasses(),
    getWidthClasses(),
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled}
    >
      {icon && <span className="leopard-button-icon">{icon}</span>}
      {children}
    </button>
  );
};

export default Button;
