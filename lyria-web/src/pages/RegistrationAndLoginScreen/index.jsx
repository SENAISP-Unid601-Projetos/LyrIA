import React, { useState } from "react";
import "./Styles/styles.css";

function LoginRegisterPage() {
  // Estado para controlar se o formulário de registro está ativo
  const [isRegisterActive, setRegisterActive] = useState(false);

  // Estados para controlar a visibilidade da senha
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false);

  // Função para alternar entre os formulários de login e registro
  const toggleForms = () => {
    setRegisterActive(!isRegisterActive);
  };

  return (
    <div className="login-body">
      <div className={`container ${isRegisterActive ? "register-active" : ""}`}>
        {/* Box roxa animada */}
        <div className="purple-box">
          <h1>LYRÍA</h1>
          <p>SUA ASSISTENTE VIRTUAL</p>
        </div>

        {/* Wrapper para os formulários */}
        <div className="form-wrapper">
          {/* Formulário de Login */}
          <div
            className={`form login-form ${isRegisterActive ? "hidden" : ""}`}
          >
            <h2>Login</h2>

            <div className="input-field">
              <div className="input-decoration"></div>
              <input
                type="email"
                placeholder="Email"
                className="login-input"
                required
              />
            </div>

            <div className="input-field">
              <div className="input-decoration"></div>
              <div className="password-container">
                <input
                  type={passwordVisible ? "text" : "password"}
                  placeholder="Senha"
                  className="login-input"
                  required
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setPasswordVisible(!passwordVisible)}
                >
                  <i
                    className={`fas ${
                      passwordVisible ? "fa-eye-slash" : "fa-eye"
                    }`}
                  ></i>
                </button>
              </div>
            </div>

            <div className="checkbox-container">
              <input type="checkbox" id="remember" />
              <label htmlFor="remember">Manter-me logado</label>
              <a href="#" className="help-link">
                Precisa de ajuda?
              </a>
            </div>

            <button>ENTRAR</button>

            <span onClick={toggleForms} className="switch-link">
              Não possui uma conta? Crie uma agora!
            </span>
          </div>

          {/* Formulário de Cadastro */}
          <div
            className={`form register-form ${isRegisterActive ? "" : "hidden"}`}
          >
            <h2>CADASTRAR-SE</h2>

            <div className="input-field">
              <div className="input-decoration"></div>
              <input
                type="text"
                placeholder="Nome"
                className="compact-input"
                required
              />
            </div>

            <div className="input-field">
              <div className="input-decoration"></div>
              <input
                type="email"
                placeholder="Email"
                className="compact-input"
                required
              />
            </div>

            <div className="form-row">
              <div className="input-field" style={{ flex: 1 }}>
                <div className="input-decoration"></div>
                <div className="password-container">
                  <input
                    type={passwordVisible ? "text" : "password"}
                    placeholder="Senha"
                    className="compact-input"
                    required
                  />
                  <button
                    type="button"
                    className="toggle-password"
                    onClick={() => setPasswordVisible(!passwordVisible)}
                  >
                    <i
                      className={`fas ${
                        passwordVisible ? "fa-eye-slash" : "fa-eye"
                      }`}
                    ></i>
                  </button>
                </div>
              </div>

              <div className="input-field" style={{ flex: 1 }}>
                <div className="input-decoration"></div>
                <div className="password-container">
                  <input
                    type={confirmPasswordVisible ? "text" : "password"}
                    placeholder="Confirmar senha"
                    className="compact-input"
                    required
                  />
                  <button
                    type="button"
                    className="toggle-password"
                    onClick={() =>
                      setConfirmPasswordVisible(!confirmPasswordVisible)
                    }
                  >
                    <i
                      className={`fas ${
                        confirmPasswordVisible ? "fa-eye-slash" : "fa-eye"
                      }`}
                    ></i>
                  </button>
                </div>
              </div>
            </div>

            <div className="terms-box">
              <input type="checkbox" id="terms-checkbox" required />
              <label htmlFor="terms-checkbox">
                <span className="terms-prefix">Concordo com os </span>
                <span className="terms-highlight">TERMOS de uso</span>
              </label>
            </div>

            <button className="compact-btn">CADASTRAR</button>
            <span onClick={toggleForms} className="switch-back">
              <i className="fas fa-arrow-right"></i> Voltar
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginRegisterPage;
