import { useState, useEffect, useRef } from "react";
import "./Styles/styles.css";
import { FaHome, FaPlus, FaVolumeUp, FaVolumeMute } from "react-icons/fa";
import { FiSun, FiMoon, FiUser } from "react-icons/fi";
import { LuPaperclip, LuMic } from "react-icons/lu";
import AnimatedBotMessage from "../../components/AnimatedBotMessage";
import { Link } from "react-router-dom";

// --- INTEGRAÇÃO COM AZURE AI SPEECH SERVICE ---
import {
  SpeechConfig,
  AudioConfig,
  SpeechRecognizer,
  SpeechSynthesizer,
  ResultReason,
} from "microsoft-cognitiveservices-speech-sdk";

// Configuração do Serviço de Fala (Voz)
const speechConfig = SpeechConfig.fromSubscription(
  import.meta.env.VITE_SPEECH_KEY,
  import.meta.env.VITE_SPEECH_REGION
);
speechConfig.speechRecognitionLanguage = "pt-BR";
// A voz padrão será definida pelo estado do componente
// --- FIM DA INTEGRAÇÃO ---


// --- BASE DE CONHECIMENTO E VOZES DISPONÍVEIS ---
const knowledgeBase = {
  "qual a previsão do tempo para hoje": "Hoje o dia está ensolarado com poucas nuvens.",
  "qual a temperatura": "A temperatura agora está em torno de 24 graus.",
  "vai chover amanhã": "Não há previsão de chuva para amanhã.",
  "melhor turma": "Com toda certeza é a do curso de Desenvolvimento de Sistemas, a turma 3TDS!",
  "quem é você": "Eu sou a LyrIA, uma IA criada para te ajudar.",
  "oi": "Olá! Como posso te ajudar?",
  "olá": "Olá! Em que posso ser útil?",
};

// Lista de vozes disponíveis para seleção
const availableVoices = [
    { value: "pt-BR-FranciscaNeural", label: "LyrIA" },
    { value: "pt-BR-BrendaNeural", label: "Brenda" },
    { value: "pt-BR-GiovanaNeural", label: "Giovana" },
    { value: "pt-BR-LeticiaNeural", label: "Leticia" },
    { value: "pt-BR-AntonioNeural", label: "Antonio" },
    { value: "pt-BR-DonatoNeural", label: "Leonardo" },
];

function Chatbot() {
  const [theme, setTheme] = useState("dark");
  const [messages, setMessages] = useState([
    {
      id: "initial-message",
      sender: "bot",
      text: "Olá, eu sou sua assistente virtual LyrIA, gostaria de algo?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isBotTyping, setIsBotTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef(null);

  // --- NOVOS ESTADOS PARA CONTROLE DE VOZ ---
  const [isSpeechEnabled, setIsSpeechEnabled] = useState(true);
  const [selectedVoice, setSelectedVoice] = useState(availableVoices[0].value);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "dark" ? "light" : "dark"));
  };

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  // Atualiza a configuração de voz quando o usuário seleciona uma nova
  useEffect(() => {
    speechConfig.speechSynthesisVoiceName = selectedVoice;
  }, [selectedVoice]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isBotTyping]);

  // --- FUNÇÕES DE VOZ E LÓGICA DO CHAT (ATUALIZADAS) ---

  const speakResponse = (text) => {
    // Só fala se a síntese de voz estiver ativada
    if (!isSpeechEnabled) return;

    const synthesizer = new SpeechSynthesizer(speechConfig);
    synthesizer.speakTextAsync(
      text,
      () => {
        synthesizer.close();
      },
      (error) => {
        console.error("Erro na síntese de voz:", error);
        synthesizer.close();
      }
    );
  };

  const getLocalResponse = (userInput) => {
    const lowerCaseInput = userInput.toLowerCase().trim();
    for (const key in knowledgeBase) {
      if (lowerCaseInput.includes(key)) {
        return knowledgeBase[key];
      }
    }
    return "Desculpe, não encontrei uma resposta para isso. Você pode tentar outra pergunta?";
  };

  const processUserInput = (text) => {
    if (!text) return;
    
    setIsBotTyping(true);
    setInput("");

    setTimeout(() => {
      const botResponseText = getLocalResponse(text);
      const botMessage = {
        id: crypto.randomUUID(),
        sender: "bot",
        text: botResponseText,
      };

      setIsBotTyping(false);
      setMessages((prevMessages) => [...prevMessages, botMessage]);
      speakResponse(botResponseText);
    }, 500);
  };

  const handleMicClick = () => {
    if (isListening) return;

    const audioConfig = AudioConfig.fromDefaultMicrophoneInput();
    const recognizer = new SpeechRecognizer(speechConfig, audioConfig);

    setIsListening(true);
    setInput("Ouvindo... pode falar.");

    recognizer.recognizeOnceAsync(
      (result) => {
        if (result.reason === ResultReason.RecognizedSpeech) {
          const recognizedText = result.text;
          const userMessage = {
            id: crypto.randomUUID(),
            sender: "user",
            text: recognizedText,
          };
          setMessages((prevMessages) => [...prevMessages, userMessage]);
          processUserInput(recognizedText);
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

  const handleSend = () => {
    const trimmedInput = input.trim();
    if (!trimmedInput || isBotTyping || isListening) return;

    const userMessage = {
      id: crypto.randomUUID(),
      sender: "user",
      text: trimmedInput,
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    processUserInput(trimmedInput);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };
  
  // --- NOVAS FUNÇÕES PARA CONTROLE DE VOZ ---
  const toggleSpeech = () => {
    setIsSpeechEnabled(prev => !prev);
  };

  const handleVoiceChange = (event) => {
    setSelectedVoice(event.target.value);
  };

  return (
    <div className="chatbot-container">
      <aside className="sidebar">
        <Link to="/">
          <h2>LYRIA</h2>
        </Link>
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
            {/* --- SELETOR DE VOZ --- */}
            <select value={selectedVoice} onChange={handleVoiceChange} className="voice-select">
                {availableVoices.map(voice => (
                    <option key={voice.value} value={voice.value}>{voice.label}</option>
                ))}
            </select>
            {/* --- BOTÃO PARA ATIVAR/DESATIVAR FALA --- */}
            <button onClick={toggleSpeech} className="theme-toggle-btn" title={isSpeechEnabled ? "Desativar voz" : "Ativar voz"}>
                {isSpeechEnabled ? <FaVolumeUp /> : <FaVolumeMute />}
            </button>
            <button onClick={toggleTheme} className="theme-toggle-btn">
              {theme === "dark" ? <FiSun /> : <FiMoon />}
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
          <LuPaperclip className="icon" id="luPaperClipIcon" />
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message to LyrIA..."
            rows="1"
            disabled={isBotTyping || isListening}
          />
          <div className="chat-input-actions">
            <LuMic
              className="icon"
              id="micIcon"
              onClick={handleMicClick}
              style={{ color: isListening ? "#007bff" : "inherit" }}
            />
            <button
              onClick={handleSend}
              disabled={isBotTyping || isListening || !input.trim()}
              id="btnSend"
            >
              Enviar ➤
            </button>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default Chatbot;