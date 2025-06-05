// src/components/Header/index.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Styles/styles.css';

function Header() {
  return (
    <header className="main-header">
      <div className="header-container">
        <h1 className="logo">LYRIA</h1>
        <nav className="main-nav">
          <Link to="/">Página Inicial</Link>
          <Link to="/solve">Sobre</Link>
          <Link to="/chat">Chat</Link>
          <Link to="/criteria">Critérios</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;