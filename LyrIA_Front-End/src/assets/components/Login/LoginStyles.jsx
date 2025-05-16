import { useState } from 'react';

export default function Login() {
  // Estados do formulário
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Estilos em JSX
  const styles = {
    container: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: 'linear-gradient(135deg, #1e1e1e, #2a2a2a)'
    },
    form: {
      background: '#2a2a2a',
      padding: '2rem',
      borderRadius: '8px',
      width: '300px',
      boxShadow: '0 4px 16px rgba(0,0,0,0.3)'
    },
    title: {
      color: '#f5f5f5',
      textAlign: 'center',
      marginBottom: '1.5rem'
    },
    input: {
      width: '100%',
      padding: '0.8rem',
      marginBottom: '1rem',
      border: 'none',
      borderRadius: '4px',
      background: '#333',
      color: '#fff',
      outline: 'none'
    },
    button: {
      width: '100%',
      padding: '0.8rem',
      background: 'linear-gradient(90deg, #4caf50, #2e7d32)',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      fontWeight: 'bold',
      transition: 'all 0.3s'
    },
    buttonDisabled: {
      opacity: 0.7,
      cursor: 'not-allowed'
    },
    error: {
      color: '#ff4444',
      marginBottom: '1rem',
      fontSize: '0.9rem',
      textAlign: 'center'
    }
  };

  // Validação simulada
  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Preencha todos os campos!');
      return;
    }

    setIsLoading(true);

    // Simulando requisição à API
    setTimeout(() => {
      if (email === 'admin@exemplo.com' && password === '123456') {
        alert('Login bem-sucedido!');
        // Redirecionamento real usaria React Router
        window.location.href = '/chat';
      } else {
        setError('Credenciais inválidas!');
      }
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.form}>
        <h2 style={styles.title}>Acesse sua conta</h2>
        
        {error && <div style={styles.error}>{error}</div>}

        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />

        <button
          type="submit"
          style={{
            ...styles.button,
            ...(isLoading && styles.buttonDisabled)
          }}
          disabled={isLoading}
        >
          {isLoading ? 'Carregando...' : 'Entrar'}
        </button>
      </form>
    </div>
  );
}