import React from 'react';
import './ErrorMessage.scss';

interface ErrorMessageProps {
  message: string;
  title?: string;
  className?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ 
  message, 
  title = 'Error', 
  className = '' 
}) => {
  return (
    <div className={`error-message ${className}`}>
      <div className="error-message__icon">⚠️</div>
      <div className="error-message__content">
        <h3 className="error-message__title">{title}</h3>
        <p className="error-message__text">{message}</p>
      </div>
    </div>
  );
};

export default ErrorMessage;
