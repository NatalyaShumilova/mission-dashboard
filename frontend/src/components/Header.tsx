import React from 'react';
import './Header.scss';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header__content">
        <div className="header__title">
          <h1>Mission Dashboard</h1>
          <span className="header__subtitle">Drone Mission Planning & Collaboration</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
