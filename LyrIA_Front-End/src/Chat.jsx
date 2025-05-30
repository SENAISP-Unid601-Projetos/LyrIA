import { useState, useEffect, useRef } from 'react';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [started, setStarted] = useState(false);
  const messagesEndRef = useRef(null);

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

  const fakeAiReply = (question) => {
    if (question.toLowerCase().includes('oi')) return 'Oi, tudo bem? 😊';
    if (question.toLowerCase().includes('tempo')) return 'O tempo está ótimo para codar!';
    return 'Desculpe, ainda estou aprendendo! 🤖';
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const resetChat = () => {
    setMessages([]);
    setStarted(false);
    setInput('');
  };

  if (!started) {
    return (
      <div style={{
        height: '100vh',
        display: 'flex',
        color: '#f5f5f5',
        background: 'linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%)',
      }}>
        {/* Sidebar FIXA (sempre visível) */}
        <div style={{
          width: '260px',
          background: '#1a1a1a',
          padding: '1rem',
          borderRight: '1px solid #333',
          overflowY: 'auto'
        }}>
          <div style={{ marginBottom: '2rem' }}>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>deepseek</h2>
            <button style={{
              background: '#4caf50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              padding: '0.5rem 1rem',
              width: '100%',
              marginBottom: '2rem',
              cursor: 'pointer'
            }}>
              New chat
            </button>
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '0.5rem' }}>Today</h3>
            <div style={{ 
              background: '#2a2a2a', 
              padding: '0.75rem', 
              borderRadius: '4px',
              marginBottom: '0.5rem',
              cursor: 'pointer'
            }}>
              Problema de layout no header...
            </div>
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '0.5rem' }}>30 Days</h3>
            <div style={{ 
              background: '#2a2a2a', 
              padding: '0.75rem', 
              borderRadius: '4px',
              marginBottom: '0.5rem',
              cursor: 'pointer'
            }}>
              Correção de consulta SQL para fun...
            </div>
          </div>

          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '0.5rem' }}>2025-03</h3>
            <div style={{ 
              background: '#2a2a2a', 
              padding: '0.75rem', 
              borderRadius: '4px',
              marginBottom: '0.5rem',
              cursor: 'pointer'
            }}>
              JavaScript: Captura e exibe número
            </div>
            <div style={{ 
              background: '#2a2a2a', 
              padding: '0.75rem', 
              borderRadius: '4px',
              marginBottom: '0.5rem',
              cursor: 'pointer'
            }}>
              IA para criar imagens sugeridas
            </div>
          </div>

          <div style={{ 
            position: 'absolute', 
            bottom: '0', 
            left: '0', 
            width: '260px',
            padding: '1rem',
            borderTop: '1px solid #333'
          }}>
            <div style={{ marginBottom: '1rem', cursor: 'pointer' }}>Get App (NEW)</div>
            <div style={{ cursor: 'pointer' }}>My Profile</div>
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
          <header 
            style={{
              backgroundColor: '#1e1e1e',
              padding: '1.5rem',
              borderBottom: '1px solid #333',
              textAlign: 'center',
              color: '#f5f5f5',
              fontSize: '1.5rem',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
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
            <div style={{
              background: '#2a2a2a',
              padding: '3rem 2rem',
              borderRadius: '16px',
              boxShadow: '0 8px 16px rgba(0,0,0,0.2)',
              width: 'min(90vw, 550px)',
              textAlign: 'center',
            }}>
              <h1 style={{ 
                fontSize: '2rem', 
                margin: '0 auto 2rem auto',
                background: 'linear-gradient(90deg, #4caf50, #2196f3)',
                WebkitBackgroundClip: 'text',
                color: 'transparent',
                width: 'fit-content',
              }}>
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
                  style={{
                    width: '100%',
                    padding: '1rem',
                    borderRadius: '30px',
                    border: 'none',
                    backgroundColor: '#333',
                    color: '#fff',
                    fontSize: '1rem',
                    boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.2)',
                    outline: 'none',
                  }}
                />
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      display: 'flex',
      height: '100vh',
      color: '#f5f5f5',
      background: 'linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%)',
    }}>
      {/* Sidebar FIXA (sempre visível) */}
      <div style={{
        width: '260px',
        background: '#1a1a1a',
        padding: '1rem',
        borderRight: '1px solid #333',
        overflowY: 'auto'
      }}>
        <div style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>deepseek</h2>
          <button style={{
            background: '#4caf50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            padding: '0.5rem 1rem',
            width: '100%',
            marginBottom: '2rem',
            cursor: 'pointer'
          }}>
            New chat
          </button>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '0.5rem' }}>Today</h3>
          <div style={{ 
            background: '#2a2a2a', 
            padding: '0.75rem', 
            borderRadius: '4px',
            marginBottom: '0.5rem',
            cursor: 'pointer'
          }}>
            Problema de layout no header...
          </div>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '0.5rem' }}>30 Days</h3>
          <div style={{ 
            background: '#2a2a2a', 
            padding: '0.75rem', 
            borderRadius: '4px',
            marginBottom: '0.5rem',
            cursor: 'pointer'
          }}>
            Correção de consulta SQL para fun...
          </div>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '0.5rem' }}>2025-03</h3>
          <div style={{ 
            background: '#2a2a2a', 
            padding: '0.75rem', 
            borderRadius: '4px',
            marginBottom: '0.5rem',
            cursor: 'pointer'
          }}>
            JavaScript: Captura e exibe número
          </div>
          <div style={{ 
            background: '#2a2a2a', 
            padding: '0.75rem', 
            borderRadius: '4px',
            marginBottom: '0.5rem',
            cursor: 'pointer'
          }}>
            IA para criar imagens sugeridas
          </div>
        </div>

        <div style={{ 
          position: 'fixed', 
          bottom: '0', 
          left: '0', 
          width: '260px',
          padding: '1rem',
          borderTop: '1px solid #333',
          background: '#1a1a1a'
        }}>
          <div style={{ marginBottom: '1rem', cursor: 'pointer' }}>Get App (NEW)</div>
          <div style={{ cursor: 'pointer' }}>My Profile</div>
        </div>
      </div>

      {/* Conteúdo principal */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
        <header 
          style={{
            backgroundColor: '#1e1e1e',
            padding: '1.5rem',
            borderBottom: '1px solid #333',
            textAlign: 'center',
            color: '#f5f5f5',
            fontSize: '1.5rem',
            fontWeight: 'bold',
          }}
        >
          LyrIA Teste
        </header>

        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '1.5rem',
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            width: '100%',
          }}>
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  margin: '0.5rem 0',
                }}
              >
                <div
                  style={{
                    maxWidth: '70%',
                    background: msg.sender === 'user' 
                      ? 'linear-gradient(135deg, #4caf50 0%, #43a047 100%)' 
                      : 'linear-gradient(135deg, #333 0%, #424242 100%)',
                    color: '#fff',
                    padding: '12px 16px',
                    borderRadius: msg.sender === 'user' 
                      ? '18px 18px 4px 18px'
                      : '18px 18px 18px 4px',
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                  }}
                >
                  <div style={{
                    fontSize: '0.8rem',
                    opacity: 0.7,
                    marginBottom: '4px',
                    fontWeight: 'bold',
                  }}>
                    {msg.sender === 'user' ? 'Você' : 'LyrIA'} • {msg.timestamp}
                  </div>
                  <div>{msg.text}</div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

        <form onSubmit={sendMessage} style={{
          padding: '1.5rem',
          background: '#2a2a2a',
          borderTop: '1px solid #333',
        }}>
          <div style={{
            maxWidth: '1200px',
            margin: '0 auto',
            display: 'flex',
            gap: '1rem',
          }}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Digite sua mensagem..."
              style={{
                flex: 1,
                padding: '1rem',
                borderRadius: '30px',
                border: 'none',
                backgroundColor: '#333',
                color: '#fff',
                fontSize: '1rem',
                boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.2)',
                outline: 'none',
              }}
            />
            <button
              type="submit"
              style={{
                background: 'linear-gradient(135deg, #4caf50 0%, #43a047 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '50%',
                width: '50px',
                height: '50px',
                cursor: 'pointer',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
              }}
            >
              →
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}