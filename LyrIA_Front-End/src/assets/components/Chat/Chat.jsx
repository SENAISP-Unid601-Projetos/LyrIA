import { useState, useEffect, useRef } from 'react';
import { styles } from './ChatStyles';

export default function Chat() {
  // Gerenciamento de estado
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [started, setStarted] = useState(false);
  const messagesEndRef = useRef(null);

  /**
   * Envia uma mensagem
   * @param {Event} e - Evento de submit do formulário
   */
  const sendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    if (!started) setStarted(true);

    const userMessage = { 
      sender: 'user', 
      text: input,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages((prev) => [...prev, userMessage]);

    setTimeout(() => {
      const botReply = { 
        sender: 'bot', 
        text: fakeAiReply(input),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, botReply]);
    }, 600);

    setInput('');
  };

  /**
   * Simula respostas da IA
   * @param {string} question - Mensagem do usuário
   * @returns {string} Resposta da IA
   */
  const fakeAiReply = (question) => {
    const lowerQuestion = question.toLowerCase();
    if (lowerQuestion.includes('oi')) return 'Oi, tudo bem? 😊';
    if (lowerQuestion.includes('tempo')) return 'O tempo está ótimo para codar!';
    return 'Desculpe, ainda estou aprendendo! 🤖';
  };

  // Rolagem automática para a última mensagem
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  /**
   * Reseta o chat para o estado inicial
   */
  const resetChat = () => {
    setMessages([]);
    setStarted(false);
    setInput('');
  };

  // Tela inicial (antes do chat começar)
  if (!started) {
    return (
      <div style={styles.appContainer}>
        {/* Sidebar fixa */}
        <div style={styles.sidebar}>
          <div style={{ marginBottom: '2rem' }}>
            <h2 style={styles.sidebarTitle}>deepseek</h2>
            <button style={styles.newChatButton}>
              Novo chat
            </button>
          </div>

          {/* Histórico de conversas */}
          <div style={{ marginBottom: '2rem' }}>
            <h3 style={styles.sidebarSectionTitle}>Hoje</h3>
            <div style={styles.chatHistoryItem}>
              Problema de layout no header...
            </div>
          </div>

          {/* Rodapé da sidebar */}
          <div style={styles.sidebarFooter}>
            <div style={{ marginBottom: '1rem', cursor: 'pointer' }}>Baixar App (NOVO)</div>
            <div style={{ cursor: 'pointer' }}>Meu Perfil</div>
          </div>
        </div>

        {/* Conteúdo principal */}
        <div style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          overflow: 'hidden'
        }}>
          <header style={styles.header}>
            LyrIA Teste
          </header>

          <div style={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '1rem',
          }}>
            <div style={styles.welcomeScreen}>
              <h1 style={styles.welcomeTitle}>
                Como posso ajudar?
              </h1>
              
              <form onSubmit={sendMessage} style={{ 
                width: '75%',
                margin: '0 auto',
              }}>
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Pergunte alguma coisa..."
                  style={styles.inputField}
                />
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Tela do chat (quando já começou)
  return (
    <div style={styles.appContainer}>
      {/* Sidebar fixa */}
      <div style={styles.sidebar}>
        <div style={{ marginBottom: '2rem' }}>
          <h2 style={styles.sidebarTitle}>deepseek</h2>
          <button 
            onClick={resetChat}
            style={styles.newChatButton}
          >
            Novo chat
          </button>
        </div>

        {/* Rodapé da sidebar */}
        <div style={styles.sidebarFooter}>
          <div style={{ marginBottom: '1rem', cursor: 'pointer' }}>Baixar App (NOVO)</div>
          <div style={{ cursor: 'pointer' }}>Meu Perfil</div>
        </div>
      </div>

      {/* Área principal do chat */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
        <header style={styles.header}>
          LyrIA Teste
        </header>

        {/* Container das mensagens */}
        <div style={styles.messagesContainer}>
          <div style={styles.messagesWrapper}>
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  ...styles.messageRow,
                  ...(msg.sender === 'user' && styles.userMessageRow)
                }}
              >
                <div
                  style={{
                    ...styles.messageBubble,
                    ...(msg.sender === 'user' ? styles.userMessage : styles.botMessage)
                  }}
                >
                  <div style={styles.messageMeta}>
                    {msg.sender === 'user' ? 'Você' : 'LyrIA'} • {msg.timestamp}
                  </div>
                  <div>{msg.text}</div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Formulário de envio */}
        <form onSubmit={sendMessage} style={styles.inputForm}>
          <div style={styles.inputContainer}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Digite sua mensagem..."
              style={styles.inputField}
            />
            <button
              type="submit"
              style={styles.sendButton}
            >
              →
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}