import { useState } from 'react';
import Chat from './Chat.jsx';

export default function App() {
  const [resetKey, setResetKey] = useState(0); // Chave para forçar rerender do Chat

  const handleHeaderClick = () => {
    setResetKey(prevKey => prevKey + 1); // Atualiza a chave para rerender
  };

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100vh',
      backgroundColor: '#1e1e1e',
    }}>
      {/* Header clicável */}
      <header 
        onClick={handleHeaderClick}
        style={{
          backgroundColor: '#1e1e1e',
          padding: '3rem',
          borderBottom: '1px solid #333',
          textAlign: 'center',
          color: '#f5f5f5',
          fontSize: '1.2rem',
          fontWeight: 'bold',
          borderTopLeftRadius: '8px',
          borderTopRightRadius: '8px',
          cursor: 'pointer', // Muda o cursor para indicar que é clicável
          transition: 'background-color 0.2s',
          ':hover': {
            backgroundColor: '#2a2a2a',
          }
        }}
      >
        LyrIA Teste
      </header>

      {/* Área do chat com key para reset */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <Chat key={resetKey} /> {/* Quando key muda, o componente recria */}
      </div>
    </div>
  );
}