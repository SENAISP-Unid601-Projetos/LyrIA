import { useState } from 'react';
import './Styles/styles.css';

function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Olá, eu sou sua assistente virtual LyrIA, gostaria de algo?' },
    { sender: 'user', text: 'Olá!' },
    { sender: 'user', text: 'Como vai seu dia? Ah, e por que LyrIA??' },
    {
      sender: 'bot',
      text: 'Olá, vai tudo ótimo, e com você? Bom. Escolhi o nome LyrIA inspirado na constelação Lyra, que representa algo brilhante, grande e claro no céu noturno. Assim como as estrelas dessa constelação iluminam a noite com seu brilho intenso, minha IA tem o propósito de trazer clareza, inovação e um toque futurístico para quem a utiliza.'
    },
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    setInput('');
    // Aqui você poderá integrar com backend IA futuramente
  };

  return (
    <div className="chatbot-container">
      <aside className="sidebar">
        <h2>LyrIA</h2>
        <nav>
          <button>Início</button>
          <button>Novo chat</button>
        </nav>
        <footer>
          <button>Ajuda</button>
          <button>Nova LyrIA após...</button>
        </footer>
      </aside>
      <main className="chat-area">
        <header className="chat-header">
          <div className="user-info">
            <span className="user-icon">👤</span>
            <span>João Gabriel</span>
          </div>
          <div className="chat-actions">
            <button>⚙️</button>
            <button>📞</button>
          </div>
          <button className="share-btn">Compartilhar</button>
        </header>
        <div className="chat-body">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <footer className="chat-input">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Message to LyrIA..."
          />
          <button onClick={handleSend}>Send ➤</button>
        </footer>
      </main>
    </div>
  );
}

export default Chatbot;
