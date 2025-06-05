// src/components/HeroSection/index.jsx
import React from 'react';
import { ChatCircleDots } from 'phosphor-react';
import './styles.css';

function HeroSection() {
  return (
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
            <h2>MUDAMOS O MUNDO</h2>
            <h1>LYRIA</h1>
            <h3>PARA UM NOVO MUNDO</h3>
            
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
        <div className="half purple-bg"></div>
        <div className="half white-bg history-container">
          <div className="history-content">
            <h2>Nossa História</h2>
            <p>
              Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
              Lorem Ipsum has been the industry's standard dummy text ever since the 1960s, 
              when an unknown printer took a galley of type and scrambled it to make a type 
              specimen book. It has survived not only five centuries, but also the leap into 
              electronic typesetting, remaining essentially unchanged.
            </p>
          </div>
          <div className="image-center">
            <img src="/img/LyrIA.webp" alt="YRIA" className="secondary-image" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default HeroSection;