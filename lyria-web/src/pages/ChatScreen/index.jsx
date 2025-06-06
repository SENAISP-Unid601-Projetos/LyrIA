import { useState } from "react";
import "./Styles/styles.css";
import { FaHome, FaPlus } from "react-icons/fa";
import { FiSun, FiMoon, FiUser } from "react-icons/fi";
import { LuPaperclip, LuMic } from "react-icons/lu";

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Olá, eu sou sua assistente virtual LyrIA, gostaria de algo?",
    },
    { sender: "user", text: "Olá!" },
    { sender: "user", text: "Como vai seu dia? Ah, e por que LyrIA??" },
    {
      sender: "bot",
      text: "Olá, vai tudo ótimo, e com você? Bom. Escolhi o nome LyrIA inspirado na constelação Lyra, que representa algo brilhante, grande e claro no céu noturno. Assim como as estrelas dessa constelação iluminam a noite com seu brilho intenso, minha IA tem o propósito de trazer clareza, inovação e um toque futurístico para quem a utiliza.",
    },
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
  };

  return (
    <div className="chatbot-container">
      <aside className="sidebar">
        <h2> LyrIA</h2>
        <nav>
          <div>
            <FaHome />
            <p>Início</p>
          </div>
          <div>
            <FaPlus />
            <p>Novo chat</p>
          </div>
        </nav>
        <div className="sidebar-footer">
          <p>Hoje</p>
          <hr />
          <p>Nome LyrIA após...</p>
        </div>
      </aside>

      <main className="chat-area">
        <header className="chat-header">
          <div className="user-info">
            <FiUser className="user-icon" />
            <span>João Gabriel</span>
          </div>
          <div className="chat-actions">
            <button>
              <FiSun className="chat-actions-icon" />
            </button>
            <button>
              <FiMoon className="chat-actions-icon" />
            </button>
          </div>
          <button className="share-btn">
            <p>Compartilhar</p>
          </button>
        </header>
        <div className="chat-body">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <footer className="chat-input-container">
          {/* Ícone de anexo */}
          <LuPaperclip className="icon" />

          <textarea placeholder="Message to slothpilot..." rows="1" />
          {/* Novo container para as ações */}
          <div className="chat-input-actions">
            <LuMic className="icon" />
            <button>Send ➤</button>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default Chatbot;
