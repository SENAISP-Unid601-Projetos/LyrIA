import React, { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { useNavigate } from "react-router-dom"; // Importe o useNavigate
import Galaxy from "../../components/Galaxy/Galaxy";
import "./Styles/styles.css";

function LoginRegisterPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);
  const navigate = useNavigate(); // Crie a função de navegação

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  // Função para lidar com o envio do formulário
  const handleAuth = (event) => {
    event.preventDefault(); // Previne o recarregamento da página
    // Aqui você adicionaria sua lógica de autenticação (chamar API, etc.)
    // Após a autenticação bem-sucedida, navegue para a página inicial
    navigate("/");
  };

  return (
    <div className="auth-body">
      <div className="galaxy-background">
        <Galaxy
          density={0.8}
          glowIntensity={0.4}
          saturation={0.8}  
          hueShift={220}
          starSpeed={0.3}
          mouseRepulsion={false}
          repulsionStrength={1.5}
        />
      </div>

      <div className={`form-container ${isLogin ? "login-active" : "register-active"}`}>
        <div className="form-content">
          <h2 className="form-title">{isLogin ? "Bem-vindo de Volta" : "Crie sua Conta"}</h2>
          <p className="form-subtitle">
            {isLogin
              ? "Entre para continuar sua jornada cósmica."
              : "Junte-se a nós e explore o universo LyrIA."}
          </p>

          {/* Adicionado o onSubmit para chamar a função handleAuth */}
          <form onSubmit={handleAuth}>
            {!isLogin && (
              <div className="input-group">
                <input type="text" placeholder="Nome" required />
              </div>
            )}
            <div className="input-group">
              <input type="email" placeholder="Email" required />
            </div>
            <div className="input-group">
              <input
                type={passwordVisible ? "text" : "password"}
                placeholder="Senha"
                required
              />
              <span
                className="password-toggle-icon"
                onClick={() => setPasswordVisible(!passwordVisible)}
              >
                {passwordVisible ? <FaEyeSlash /> : <FaEye />}
              </span>
            </div>
            {!isLogin && (
              <div className="input-group">
                <input
                  type={confirmPasswordVisible ? "text" : "password"}
                  placeholder="Confirmar Senha"
                  required
                />
                 <span
                className="password-toggle-icon"
                onClick={() => setConfirmPasswordVisible(!confirmPasswordVisible)}
              >
                {confirmPasswordVisible ? <FaEyeSlash /> : <FaEye />}
              </span>
              </div>
            )}

            {isLogin && (
                <a href="#" className="forgot-password">Esqueceu sua senha?</a>
            )}

            <button type="submit" className="submit-btn">
              {isLogin ? "ENTRAR" : "CADASTRAR"}
            </button>
          </form>

          <p className="toggle-form-text">
            {isLogin ? "Não tem uma conta?" : "Já possui uma conta?"}{" "}
            <span onClick={toggleForm}>{isLogin ? "Cadastre-se" : "Faça Login"}</span>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginRegisterPage;