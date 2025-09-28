import React from 'react';
import './LoadingSpinner.scss';

interface LoadingSpinnerProps {
  message?: string;
  className?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  message = 'Loading...', 
  className = '' 
}) => {
  return (
    <div className={`loading-spinner ${className}`}>
      <div className="loading-spinner__spinner"></div>
      {message && <p className="loading-spinner__message">{message}</p>}
    </div>
  );
};

export default LoadingSpinner;
