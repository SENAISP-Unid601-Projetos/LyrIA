import { useState, useEffect, useRef, memo } from "react";
import "./Styles/styles.css";
import { FiSend, FiPlus, FiPaperclip, FiMic, FiUser, FiCopy, FiCheck, FiClock, FiX } from "react-icons/fi";
import { RiRobot2Line } from "react-icons/ri";
import { Link } from "react-router-dom";
import AnimatedBotMessage from "../../components/AnimatedBotMessage";
import Galaxy from "../../components/Galaxy/Galaxy";

// --- Base de Conhecimento e Componentes Memoizados (sem alteração) ---
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
};

const MemoizedGalaxy = memo(() => (
  <div className="galaxy-background">
    <Galaxy
      mouseRepulsion={false}
      mouseInteraction={false}
      density={1}
      glowIntensity={0.55}
      saturation={0.6}
      hueShift={210}
    />
  </div>
));

// --- Painel de Histórico ---
const HistoryPanel = ({ isVisible, onClose }) => {
    // Dados de exemplo para o histórico
    const historyItems = [
        "Quem é você?",
        "Ideia de projeto React",
        "Melhor turma do SENAI",
        "Como funciona a LyrIA?",
        "Planetas do sistema solar",
        "Dicas de CSS",
    ];

    return (
        <aside className={`history-panel ${isVisible ? 'visible' : ''}`}>
            <div className="history-header">
                <h2>Histórico</h2>
                <button onClick={onClose} className="header-icon-btn"><FiX /></button>
            </div>
            <div className="history-list">
                {historyItems.map((item, index) => (
                    <div key={index} className="history-item">
                        {item}
                    </div>
                ))}
            </div>
        </aside>
    );
};


const PromptSuggestions = ({ onSuggestionClick }) => (
  <div className="suggestions-container">
    <div className="lyria-icon-large">
        <RiRobot2Line />
    </div>
    <h2>Como posso ajudar hoje?</h2>
    <div className="suggestions-grid">
      <div className="suggestion-card" onClick={() => onSuggestionClick("Quem é você?")}>
        <p><strong>Quem é você?</strong></p>
        <span>Descubra a identidade da LyrIA</span>
      </div>
      <div className="suggestion-card" onClick={() => onSuggestionClick("Qual a melhor turma do SENAI?")}>
        <p><strong>Qual a melhor turma?</strong></p>
        <span>Uma pergunta capciosa...</span>
      </div>
      <div className="suggestion-card" onClick={() => onSuggestionClick("Me dê uma ideia para um projeto React")}>
        <p><strong>Ideia de projeto</strong></p>
        <span>Para inspirar sua criatividade</span>
      </div>
       <div className="suggestion-card" onClick={() => onSuggestionClick("Como você funciona?")}>
        <p><strong>Como você funciona?</strong></p>
        <span>Explore os bastidores da IA</span>
      </div>
    </div>
  </div>
);


function ChatContent() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [isHistoryVisible, setHistoryVisible] = useState(false); // Estado para o histórico
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = `${scrollHeight}px`;
    }
  }, [input]);

  const initialBotMessage = {
      id: "initial-message",
      sender: "bot",
      text: "Olá, eu sou sua assistente virtual LyrIA. O que você gostaria de saber?",
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isBotTyping]);
  
  const handleCopyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getBotResponse = (userInput) => {
    const lowerCaseInput = userInput.toLowerCase();
     if (lowerCaseInput.includes("projeto react")) {
      return "Que tal um aplicativo de lista de tarefas (to-do list) com autenticação de usuário e armazenamento em nuvem?";
    }
    if (lowerCaseInput.includes("como você funciona")) {
      return "Eu funciono com base em uma base de conhecimento pré-definida. Quando você me envia uma mensagem, eu procuro por palavras-chave para encontrar a resposta mais relevante!";
    }
    for (const key in knowledgeBase) {
      if (lowerCaseInput.includes(key)) {
        return knowledgeBase[key];
      }
    }
    return "Desculpe, não entendi. Você poderia reformular sua pergunta?";
  };

  const handleSend = (textToSend) => {
    const trimmedInput = (typeof textToSend === 'string' ? textToSend : input).trim();
    if (!trimmedInput || isBotTyping) return;

    const userMessage = { id: crypto.randomUUID(), sender: "user", text: trimmedInput };
    const newMessages = messages.length === 0 ? [initialBotMessage, userMessage] : [...messages, userMessage];
    setMessages(newMessages);

    setInput("");
    setIsBotTyping(true);

    setTimeout(() => {
      const botResponseText = getBotResponse(trimmedInput);
      const botMessage = { id: crypto.randomUUID(), sender: "bot", text: botResponseText };
      setIsBotTyping(false);
      setMessages((prev) => [...prev, botMessage]);
    }, 1000);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => setMessages([]);

  return (
    <>
      <HistoryPanel isVisible={isHistoryVisible} onClose={() => setHistoryVisible(false)} />
      <main className={`galaxy-chat-area ${isHistoryVisible ? 'history-open' : ''}`}>
        <header className="galaxy-chat-header">
          {/* BOTÃO DE HISTÓRICO */}
          <button className="header-icon-btn" onClick={() => setHistoryVisible(true)}>
            <FiClock />
          </button>
          
          {/* TÍTULO COM LINK PARA HOME */}
          <Link to="/" className="header-title-link">
            <h1>LyrIA</h1>
          </Link>

          <button className="header-icon-btn" onClick={handleNewChat}><FiPlus /></button>
        </header>
        <div className="galaxy-chat-body">
          {messages.length === 0 ? (
            <PromptSuggestions onSuggestionClick={handleSend} />
          ) : (
            messages.map((msg, idx) => (
              <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
                <div className="avatar-icon">{msg.sender === 'bot' ? <RiRobot2Line /> : <FiUser />}</div>
                <div className="message-content">
                  <span className="sender-name">{msg.sender === 'bot' ? 'LyrIA' : 'Joao Cardoso'}</span>
                  {msg.sender === 'user' ? (
                      <div className="message user">{msg.text}</div>
                  ) : (
                      idx === 0 ? (
                          <div className="message bot">{msg.text}</div>
                      ) : (
                          <AnimatedBotMessage fullText={msg.text} />
                      )
                  )}
                  {msg.sender === 'bot' && (
                    <button className="copy-btn" onClick={() => handleCopyToClipboard(msg.text, msg.id)}>
                      {copiedId === msg.id ? <FiCheck /> : <FiCopy />}
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
          {isBotTyping && (
            <div className="message-wrapper bot">
               <div className="avatar-icon"><RiRobot2Line /></div>
               <div className="message-content">
                  <span className="sender-name">LyrIA</span>
                  <div className="typing-indicator"><span /><span /><span /></div>
               </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <footer className="galaxy-chat-input-container">
          <FiPaperclip className="input-icon" />
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digite sua mensagem para LyrIA..."
            rows="1"
            disabled={isBotTyping}
          />
           <FiMic className="input-icon" />
          <button onClick={() => handleSend()} disabled={!input.trim() || isBotTyping} className="send-btn">
            <FiSend />
          </button>
        </footer>
      </main>
    </>
  );
}

function Chatbot() {
  return (
    <div className="galaxy-chat-container"><MemoizedGalaxy /><ChatContent /></div>
  );
}

export default Chatbot;