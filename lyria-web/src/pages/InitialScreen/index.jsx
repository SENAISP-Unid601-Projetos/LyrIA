// src/pages/InitialScreen/index.jsx
import React from 'react';
import { ChatCircleDots } from 'phosphor-react';
import './Styles/styles.css';

// NOVO: Imports para o Header e Footer
// Por favor, ajuste o caminho se seus componentes estiverem em outra pasta!
import Header from '../../components/Header';
import Footer from '../../components/Footer';

function InitialScreen() {
  return (
    // O React permite retornar múltiplos elementos usando um Fragment (<> ... </>)
    // ou envolvendo tudo em uma div pai, como já está.
    <div className="initial-screen"> 
      
      {/* NOVO: Adicionado o componente Header no topo da página */}
      <Header />

      <div className="chess-layout">
        {/* Parte superior - dois quadrados grandes */}
        <div className="top-section">
          <div className="half white-bg"></div>
          <div className="half purple-bg"></div>
          
          {/* Imagem retangular sobreposta */}
          <div className="image-overlay">
            <img src="/img/LyrIA.webp" alt="YRIA" className="main-image" />
            
            {/* Texto e botão sobrepostos */}
            <div className="text-content">
              <h2 >MUDAMOS O MUNDO</h2>
              <h2>LYRIA</h2>
              <h3 id='effectword'>PARA UM NOVO MUNDO</h3>
              
              <button className="cta-button">
                <span>COMEÇAR</span>
                <div className="button-icon">
                  <ChatCircleDots size={22} weight="fill" />
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Parte inferior - cores invertidas com história */}
        <div className="bottom-section">
          <div className="half purple-bg">
            <div className="secundaryimage-overlay">
                <img src="/img/LyrIA.webp" alt="YRIA" className="secondary-image" />
              </div>
          </div>
          <div className="half white-bg history-container"> 	
            <div className="history-content">
              <h2 id='nossa-historia'>Nossa História</h2>
              <p>
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Nobis labore possimus consectetur illo non voluptatum ullam hic porro quibusdam necessitatibus?
              </p>
            </div>
            
          </div>
        </div>
      </div>

      {/* NOVO: Adicionado o componente Footer no final da página */}
      <Footer />

    </div>
  );
}

export default InitialScreen;