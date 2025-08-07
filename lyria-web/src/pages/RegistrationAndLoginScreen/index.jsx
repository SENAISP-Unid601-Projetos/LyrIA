import React from 'react';
import './Styles/styles.css';

const RegistrationScreen = () => {
  return (
    <div className="container">
      
      <main className="main-content">
        <div className="registration-card">
          <h1 className="registration-title">CADASTRAR-SE</h1>
          
          <div className="brand-section">
            <h2 className="brand-name">LYRIA</h2>
            <p className="brand-subtitle">SUA ASSISTENTE VIRTUAL</p>
          </div>
          
          <form className="registration-form">
            <div className="form-group">
              <input 
                type="text" 
                placeholder="Nome completo" 
                className="form-input"
              />
            </div>
            
            <div className="form-group">
              <input 
                type="email" 
                placeholder="Email" 
                className="form-input"
              />
            </div>
            
            <div className="form-group">
              <input 
                type="password" 
                placeholder="Senha" 
                className="form-input"
              />
            </div>
            
            <div className="form-group">
              <input 
                type="password" 
                placeholder="Confirmar senha" 
                className="form-input"
              />
            </div>
            
            <button type="submit" className="submit-button">
              Criar Conta
            </button>
          </form>
        </div>
        <div className ="containerV2">

        </div>

      </main>
      
    </div>
  );
};

export default RegistrationScreen;