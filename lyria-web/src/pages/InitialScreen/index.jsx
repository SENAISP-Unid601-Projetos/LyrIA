import { useState } from 'react'; // Importa o useState
import './Styles/styles.css';
import { Link } from 'react-router-dom';
import Galaxy from '../../components/Galaxy/Galaxy.jsx';
import { FaTimes } from "react-icons/fa"; // Ícone para o botão de fechar
import BlurText from "../../components/BlurText/BlurText.jsx";


function InitialScreen() {
  // Estado para controlar a visibilidade do modal de informações
  const [isInfoVisible, setInfoVisible] = useState(false);

  // Função para mostrar ou esconder o modal
  const toggleInfoModal = () => {
    setInfoVisible(!isInfoVisible);

    };

    const handleAnimationComplete = () => {
  console.log('Animation completed!');
};
  

  return (
    <div className="App">
      <header className="app-header">
        <Link to={'/'}>
        <div className="logo">
          <b>LYRIA</b>
        </div>
        </Link>
        <nav>
          <Link to={'/RegistrationAndLogin'}>
          <p>Entrar</p>
          </Link>
          <a href="#">Contato</a>
        </nav>
      </header>

      <div className="galaxy-background">
        <Galaxy
          mouseRepulsion={false}
          mouseInteraction={false}
          density={1}
          glowIntensity={0.4}
          saturation={0.6}
          hueShift={210}
        />
      </div>

      <div className="main-content">

  <BlurText 
  text= "Conheça LyrIA"
  delay={150}
  animateBy="words"
  direction="top"
  onAnimationComplete={handleAnimationComplete}
  className="blur"
/>
     
        <span id="espaço"></span>
        <div className="container_espaço">
          <Link className="linkSemEstilo" to={'/chat'}>
          <button id="comecar">
            Começar
          </button>
          </Link>
          {/* Botão "Saiba Mais" agora abre o modal */}
          <button id="sobre" onClick={toggleInfoModal}>
            Saiba Mais
          </button>
        </div>
      </div>

      {/* Modal de informações que aparece condicionalmente */}
      {isInfoVisible && (
        <div className="info-modal-backdrop">
          <div className="info-modal-content">
            <button className="close-modal-btn" onClick={toggleInfoModal}>
              <FaTimes />
            </button>
            <h2>Sobre a LyrIA</h2>
            <p>
              LyrIA é uma assistente virtual de última geração, projetada para ser sua companheira em um universo de conhecimento e criatividade.
            </p>
            <p>
              Nossa missão é fornecer respostas rápidas, insights valiosos e ajudar você a explorar novas ideias de forma intuitiva e eficiente. Construída com as mais recentes tecnologias de inteligência artificial, a LyrIA aprende e se adapta às suas necessidades.
            </p>
            <h3>Funcionalidades Principais:</h3>
            <ul>
              <li>Respostas instantâneas e precisas.</li>
              <li>Assistência criativa para seus projetos.</li>
              <li>Interface amigável e personalizável.</li>
              <li>Integração com diversas ferramentas.</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default InitialScreen;