import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>&copy; {new Date().getFullYear()} Lyria - Todos os direitos reservados</p>
        <div className="footer-links">
          <a href="/termos">Termos de Uso</a>
          <a href="/privacidade">Política de Privacidade</a>
          <a href="/suporte">Suporte</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;