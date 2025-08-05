import React from 'react';
import '../../styles/theme.css';

interface InputProps {
  type?: 'text' | 'password' | 'email' | 'number' | 'tel' | 'url' | 'search';
  placeholder?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
  onFocus?: (e: React.FocusEvent<HTMLInputElement>) => void;
  name?: string;
  id?: string;
  disabled?: boolean;
  required?: boolean;
  className?: string;
  error?: string;
  label?: string;
  icon?: React.ReactNode;
  autoFocus?: boolean;
  maxLength?: number;
}

const Input: React.FC<InputProps> = ({
  type = 'text',
  placeholder,
  value,
  onChange,
  onBlur,
  onFocus,
  name,
  id,
  disabled = false,
  required = false,
  className = '',
  error,
  label,
  icon,
  autoFocus = false,
  maxLength
}) => {
  const inputId = id || name;
  
  return (
    <div className="leopard-input-container">
      {label && (
        <label htmlFor={inputId} className="leopard-input-label">
          {label}
          {required && <span className="leopard-input-required">*</span>}
        </label>
      )}
      
      <div className={`leopard-input-wrapper ${icon ? 'leopard-input-with-icon' : ''}`}>
        {icon && <div className="leopard-input-icon">{icon}</div>}
        
        <input
          type={type}
          id={inputId}
          name={name}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          onFocus={onFocus}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          className={`leopard-input ${error ? 'leopard-input-error' : ''} ${className}`}
          autoFocus={autoFocus}
          maxLength={maxLength}
        />
      </div>
      
      {error && <div className="leopard-input-error-message">{error}</div>}
    </div>
  );
};

export default Input;
