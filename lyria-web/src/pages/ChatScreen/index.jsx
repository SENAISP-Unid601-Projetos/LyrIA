import { useState, useEffect, useRef, memo } from "react";
import "./Styles/styles.css";
// --- ÍCONES ATUALIZADOS ---
import {
  FiSend,
  FiPlus,
  FiPaperclip,
  FiMic,
  FiUser,
  FiCopy,
  FiCheck,
  FiClock,
  FiX,
} from "react-icons/fi";
import { FaVolumeUp, FaVolumeMute } from "react-icons/fa"; // Ícones para controle de volume
import { RiRobot2Line } from "react-icons/ri";
import { Link } from "react-router-dom";
import AnimatedBotMessage from "../../components/AnimatedBotMessage";
import Galaxy from "../../components/Galaxy/Galaxy";

// --- ADICIONADO: INTEGRAÇÃO COM AZURE AI SPEECH SERVICE ---
import {
  SpeechConfig,
  AudioConfig,
  SpeechRecognizer,
  SpeechSynthesizer,
  ResultReason,
} from "microsoft-cognitiveservices-speech-sdk";

// --- ADICIONADO: CONFIGURAÇÃO DO SERVIÇO DE FALA ---
// Lembre-se de criar um arquivo .env.local na raiz do projeto com suas chaves
const speechConfig = SpeechConfig.fromSubscription(
  import.meta.env.VITE_SPEECH_KEY,
  import.meta.env.VITE_SPEECH_REGION
);
speechConfig.speechRecognitionLanguage = "pt-BR";
// A voz da IA será definida dinamicamente pelo estado 'selectedVoice'

// --- ADICIONADO: LISTA DE VOZES DISPONÍVEIS ---
const availableVoices = [
  { value: "pt-BR-FranciscaNeural", label: "LyrIA" },
  { value: "pt-BR-BrendaNeural", label: "Brenda" },
  { value: "pt-BR-GiovanaNeural", label: "Giovana" },
  { value: "pt-BR-LeticiaNeural", label: "Leticia" },
  { value: "pt-BR-AntonioNeural", label: "Antonio" },
  { value: "pt-BR-DonatoNeural", label: "Leonardo" },
];

// --- Base de Conhecimento (sem alteração) ---
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

const HistoryPanel = ({ isVisible, onClose }) => {
  const historyItems = [
    "Quem é você?",
    "Ideia de projeto React",
    "Melhor turma do SENAI",
    "Como funciona a LyrIA?",
    "Planetas do sistema solar",
    "Dicas de CSS",
  ];
  return (
    <aside className={`history-panel ${isVisible ? "visible" : ""}`}>
      <div className="history-header">
        <h2>Histórico</h2>
        <button onClick={onClose} className="header-icon-btn">
          <FiX />
        </button>
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
      <div
        className="suggestion-card"
        onClick={() => onSuggestionClick("Quem é você?")}
      >
        <p>
          <strong>Quem é você?</strong>
        </p>
        <span>Descubra a identidade da LyrIA</span>
      </div>
      <div
        className="suggestion-card"
        onClick={() => onSuggestionClick("Qual a melhor turma do SENAI?")}
      >
        <p>
          <strong>Qual a melhor turma?</strong>
        </p>
        <span>Uma pergunta capciosa...</span>
      </div>
      <div
        className="suggestion-card"
        onClick={() =>
          onSuggestionClick("Me dê uma ideia para um projeto React")
        }
      >
        <p>
          <strong>Ideia de projeto</strong>
        </p>
        <span>Para inspirar sua criatividade</span>
      </div>
      <div
        className="suggestion-card"
        onClick={() => onSuggestionClick("Como você funciona?")}
      >
        <p>
          <strong>Como você funciona?</strong>
        </p>
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
  const [isHistoryVisible, setHistoryVisible] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // --- ADICIONADO: ESTADOS PARA CONTROLE DE VOZ ---
  const [isListening, setIsListening] = useState(false);
  const [isSpeechEnabled, setIsSpeechEnabled] = useState(true);
  const [selectedVoice, setSelectedVoice] = useState(availableVoices[0].value);

  // --- ADICIONADO: Efeito que atualiza a voz da IA quando o usuário a seleciona ---
  useEffect(() => {
    speechConfig.speechSynthesisVoiceName = selectedVoice;
  }, [selectedVoice]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
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

  // --- ADICIONADO: FUNÇÃO PARA A IA FALAR A RESPOSTA (SÍNTESE DE VOZ) ---
  const speakResponse = (text) => {
    if (!isSpeechEnabled) return; // Só fala se a opção estiver ativa
    const synthesizer = new SpeechSynthesizer(speechConfig);
    synthesizer.speakTextAsync(
      text,
      () => synthesizer.close(),
      (error) => {
        console.error("Erro na síntese de voz:", error);
        synthesizer.close();
      }
    );
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

  // --- MODIFICADO: handleSend agora chama a função speakResponse ---
  const handleSend = (textToSend) => {
    const trimmedInput = (
      typeof textToSend === "string" ? textToSend : input
    ).trim();
    if (!trimmedInput || isBotTyping || isListening) return;

    const userMessage = {
      id: crypto.randomUUID(),
      sender: "user",
      text: trimmedInput,
    };
    const newMessages =
      messages.length === 0
        ? [initialBotMessage, userMessage]
        : [...messages, userMessage];
    setMessages(newMessages);

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
      setMessages((prev) => [...prev, botMessage]);
      speakResponse(botResponseText); // <--- A IA FALA A RESPOSTA AQUI
    }, 1000);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  // --- ADICIONADO: FUNÇÃO PARA OUVIR O MICROFONE (RECONHECIMENTO DE VOZ) ---
  const handleMicClick = () => {
    if (isListening) return;

    const audioConfig = AudioConfig.fromDefaultMicrophoneInput();
    const recognizer = new SpeechRecognizer(speechConfig, audioConfig);

    setIsListening(true);
    setInput("Ouvindo... pode falar."); // Feedback visual para o usuário

    recognizer.recognizeOnceAsync(
      (result) => {
        if (result.reason === ResultReason.RecognizedSpeech) {
          const recognizedText = result.text;
          handleSend(recognizedText); // Envia o texto reconhecido diretamente
        } else {
          console.error(`Erro no reconhecimento: ${result.errorDetails}`);
          setInput("Não consegui entender. Tente novamente.");
          setTimeout(() => setInput(""), 2000);
        }
        recognizer.close();
        setIsListening(false);
      },
      (error) => {
        console.error(`Erro na sessão de reconhecimento: ${error}`);
        setInput("Erro ao acessar o microfone.");
        recognizer.close();
        setIsListening(false);
        setTimeout(() => setInput(""), 2000);
      }
    );
  };

  // --- ADICIONADO: FUNÇÕES PARA OS NOVOS CONTROLES DE VOZ ---
  const toggleSpeech = () => setIsSpeechEnabled((prev) => !prev);
  const handleVoiceChange = (event) => setSelectedVoice(event.target.value);
  const handleNewChat = () => setMessages([]);

  return (
    <>
      <HistoryPanel
        isVisible={isHistoryVisible}
        onClose={() => setHistoryVisible(false)}
      />
      <main
        className={`galaxy-chat-area ${isHistoryVisible ? "history-open" : ""}`}
      >
        <header className="galaxy-chat-header">
          <button
            className="header-icon-btn"
            onClick={() => setHistoryVisible(true)}
          >
            <FiClock />
          </button>

          <Link to="/" className="header-title-link">
            <h1>LyrIA</h1>
          </Link>

          {/* --- ADICIONADO: CONTROLES DE VOZ NO CABEÇALHO --- */}
          <div className="header-voice-controls">
            <select
              value={selectedVoice}
              onChange={handleVoiceChange}
              className="voice-select"
              title="Selecionar voz"
            >
              {availableVoices.map((voice) => (
                <option key={voice.value} value={voice.value}>
                  {voice.label}
                </option>
              ))}
            </select>
            <button
              onClick={toggleSpeech}
              className="header-icon-btn"
              title={isSpeechEnabled ? "Desativar voz" : "Ativar voz"}
            >
              {isSpeechEnabled ? <FaVolumeUp /> : <FaVolumeMute />}
            </button>
            <button
              className="header-icon-btn"
              onClick={handleNewChat}
              title="Novo Chat"
            >
              <FiPlus />
            </button>
          </div>
        </header>

        <div className="galaxy-chat-body">
          {messages.length === 0 ? (
            <PromptSuggestions onSuggestionClick={handleSend} />
          ) : (
            messages.map((msg, idx) => (
              <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
                <div className="avatar-icon">
                  {msg.sender === "bot" ? <RiRobot2Line /> : <FiUser />}
                </div>
                <div className="message-content">
                  <span className="sender-name">
                    {msg.sender === "bot" ? "LyrIA" : "Você"}
                  </span>
                  {msg.sender === "user" ? (
                    <div className="message user">{msg.text}</div>
                  ) : idx === 0 ? (
                    <div className="message bot">{msg.text}</div>
                  ) : (
                    <AnimatedBotMessage fullText={msg.text} />
                  )}
                  {msg.sender === "bot" && (
                    <button
                      className="copy-btn"
                      onClick={() => handleCopyToClipboard(msg.text, msg.id)}
                    >
                      {copiedId === msg.id ? <FiCheck /> : <FiCopy />}
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
          {isBotTyping && (
            <div className="message-wrapper bot">
              <div className="avatar-icon">
                <RiRobot2Line />
              </div>
              <div className="message-content">
                <span className="sender-name">LyrIA</span>
                <div className="typing-indicator">
                  <span />
                  <span />
                  <span />
                </div>
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
            disabled={isBotTyping || isListening} // Desabilita enquanto ouve
          />
          {/* --- MODIFICADO: Ícone de microfone agora tem funcionalidade e estilo dinâmico --- */}
          <FiMic
            className={`input-icon mic-icon ${isListening ? "listening" : ""}`}
            onClick={handleMicClick}
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isBotTyping || isListening}
            className="send-btn"
          >
            <FiSend />
          </button>
        </footer>
      </main>
    </>
  );
}

function Chatbot() {
  return (
    <div className="galaxy-chat-container">
      <MemoizedGalaxy />
      <ChatContent />
    </div>
  );
}

export default Chatbot;
