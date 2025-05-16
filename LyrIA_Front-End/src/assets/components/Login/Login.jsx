import { useState } from 'react';
import styles from './LoginStyles.jsx'; 

export default function Login() {
  // Estados para controle do formulário
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Credenciais válidas (simulando um banco de dados)
  const validCredentials = {
    email: 'usuario@exemplo.com',
    password: 'senha123'
  };

  // Função de submit
  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // Validação simples
    if (!email || !password) {
      setError('Preencha todos os campos!');
      return;
    }

    setIsLoading(true);

    // Simulando requisição assíncrona
    setTimeout(() => {
      if (email === validCredentials.email && password === validCredentials.password) {
        alert('Login bem-sucedido! Redirecionando...');
        // Aqui você redirecionaria para /chat na prática
        window.location.href = '/chat'; // Simples (use React Router no mundo real)
      } else {
        setError('E-mail ou senha incorretos!');
      }
      setIsLoading(false);
    }, 1500); // Delay para simular API
  };

  return (
    <div className={styles.container}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <h2>Login</h2>
        
        {error && <div className={styles.error}>{error}</div>}

        <input
          type="email"
          placeholder="Seu e-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
        />

        <input
          type="password"
          placeholder="Sua senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
        />

        <button 
          type="submit" 
          disabled={isLoading}
          className={styles.button}
        >
          {isLoading ? 'Carregando...' : 'Entrar'}
        </button>
      </form>
    </div>
  );
}