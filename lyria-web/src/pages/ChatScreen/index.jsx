import { useState, useEffect, useRef } from "react";
import "./Styles/styles.css";
import { FaHome, FaPlus } from "react-icons/fa";
import { FiSun, FiMoon, FiUser } from "react-icons/fi";
import { LuPaperclip, LuMic } from "react-icons/lu";
import AnimatedBotMessage from "../../components/AnimatedBotMessage";
import { Link } from 'react-router-dom';

const knowledgeBase = {
  "melhor turma":
    "Com toda certeza é a do curso de Desenvolvimento de Sistemas, a turma 3TDS!",
  "3tds":
    "A 3TDS é, sem dúvida, a melhor turma de Desenvolvimento de Sistemas do SENAI!",
  "quem é você":
    "Eu sou a LyrIA, uma IA criada para te ajudar a encontrar respostas e explorar ideias.",
  lyria: "LyrIA é meu nome! E se quer saber, a melhor turma é a 3TDS.",
  oi: "Olá! Como posso te ajudar hoje?",
  olá: "Olá! Como posso te ajudar hoje?",
  "bom dia": "Bom dia! Em que posso ser útil?",
  "boa tarde": "Boa tarde! Como posso ajudar?",
  "boa noite": "Boa noite! Precisa de algo?",
  "como você está":
    "Estou funcionando perfeitamente, obrigado por perguntar! E você?",
  obrigado: "De nada! Se precisar de mais alguma coisa, é só chamar.",
  adeus: "Até mais! Se precisar, estarei por aqui.",
};

function Chatbot() {
  const [theme, setTheme] = useState('dark');
  const [messages, setMessages] = useState([
    {
      id: "initial-message",
      sender: "bot",
      text: "Olá, eu sou sua assistente virtual LyrIA, gostaria de algo?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isBotTyping, setIsBotTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'dark' ? 'light' : 'dark');
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isBotTyping]);

  const getBotResponse = (userInput) => {
    const lowerCaseInput = userInput.toLowerCase();
    for (const key in knowledgeBase) {
      if (lowerCaseInput.includes(key)) {
        return knowledgeBase[key];
      }
    }
    return "Desculpe, não entendi. Você poderia reformular sua pergunta?";
  };

  const handleSend = () => {
    const trimmedInput = input.trim();
    if (!trimmedInput || isBotTyping) return;

    const userMessage = {
      id: crypto.randomUUID(),
      sender: "user",
      text: trimmedInput,
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");
    setIsBotTyping(true);

    setTimeout(() => {
      const botResponseText = getBotResponse(trimmedInput);
      const botMessage = {
        id: crypto.randomUUID(),
        sender: "bot",
        text: botResponseText,
      };
      setIsBotTyping(false);
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    }, 1000);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chatbot-container">
      <aside className="sidebar">
        <Link to="/">
          <h2> LYRIA</h2>
        </ Link>
        <nav>
          <Link to="/">
            <div>
              <FaHome />
              <p>Início</p>
            </div>
          </Link>
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
            <button onClick={toggleTheme}>
              <FiSun className="chat-actions-iconSun" style={{ opacity: theme === 'light' ? 1 : 0.4 }} />
            </button>
            <button onClick={toggleTheme}>
              <FiMoon className="chat-actions-iconMoon" style={{ opacity: theme === 'dark' ? 1 : 0.4 }} />
            </button>
          </div>
          <button className="share-btn" id="btnShare">
            <p>Compartilhar</p>
          </button>
        </header>
        <div className="chat-body">
          {messages.map((msg, idx) => {
            if (msg.sender === "user") {
              return (
                <div key={msg.id} className="message user message-animated">
                  {msg.text}
                </div>
              );
            } else {
              return idx === 0 ? (
                <div key={msg.id} className="message bot">
                  {msg.text}
                </div>
              ) : (
                <AnimatedBotMessage key={msg.id} fullText={msg.text} />
              );
            }
          })}
          {isBotTyping && (
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <footer className={`chat-input-container ${input ? "is-typing" : ""}`}>
          <LuPaperclip className="icon" id="luPaperClipIcon"/>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message to LyrIA..."
            rows="1"
            disabled={isBotTyping}
          />
          <div className="chat-input-actions">
            <LuMic className="icon" id="micIcon"/>
            <button onClick={handleSend} disabled={isBotTyping} id="btnSend">
              Enviar ➤
            </button>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default Chatbot;