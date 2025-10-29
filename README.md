# 🤖 LyrIA - Sua Assistente Virtual Inteligente

<p align="center">
<strong>Projeto de Conclusão de Curso - SENAI "Antonio Adolpho Lobbe" - São Carlos/SP</strong>
</p>

<p align="center">
<img alt="Status do Projeto" src="https://img.shields.io/badge/status-Em%20Desenvolvimento-yellow">
<img alt="Linguagem Principal" src="https://img.shields.io/badge/principal-Python%20%26%20JS-blue?logo=python&logoColor=white&color=blueviolet">
<img alt="Licença" src="https://img.shields.io/badge/license-MIT-blue">
</p>

---

## Sobre o Projeto

LyrIA é uma **assistente virtual inteligente** desenvolvida como projeto de conclusão do curso de **Técnico em Desenvolvimento de Sistemas**.
A aplicação possui **interface web moderna** e **back-end robusto**, utilizando **LLM (Large Language Model)** para gerar respostas dinâmicas e contextuais.

O objetivo é proporcionar uma experiência de **conversação natural**, capaz de responder perguntas gerais e buscar informações atualizadas na web para garantir precisão.

---

## Funcionalidades

* **Interface de Chat Interativa** – Front-end em **React**, responsivo e intuitivo.
* **IA com LLM (Gemma via Ollama)** – Respostas ricas e contextuais.
* **Busca Inteligente na Web** – Classificador com **Scikit-learn** que decide quando buscar dados pela **SerpAPI**.
* **Personas Customizáveis** – Defina diferentes estilos de resposta (ex: professora, assistente empresarial).
* **Memória e Histórico** – Conversas salvas em **SQLite** para manter o contexto.
* **Autenticação de Usuário** – Login e cadastro para personalização.
* **Tema Claro e Escuro** – Ajuste visual para maior conforto.

---

## 📸 Screenshots

<p align="center">
<img src="https://github.com/user-attachments/assets/f0568557-3819-455e-915e-58d9f5b480e4" alt="Tela Inicial do LyrIA" width="700"/>
<br>
<em>📌 Tela Inicial</em>
</p>

<p align="center">
<img src="https://github.com/user-attachments/assets/bb634e4c-4ea1-4845-a64d-91c049feffc4" alt="Tela de Chat do LyrIA" width="700"/>
<br>
<em> Interface de Chat em Ação</em>
</p>

---

## Tecnologias Utilizadas

### Front-End (lyria-web)

| Tecnologia       | Descrição                                     |
| ---------------- | --------------------------------------------- |
| **React**        | Biblioteca para construção da interface.      |
| **Vite**         | Build rápido e otimizado.                     |
| **Axios**        | Cliente HTTP para comunicação com o back-end. |
| **React Router** | Gerenciamento de rotas (Home, Chat, Login).   |
| **CSS**          | Estilização moderna e componentizada.         |

### Back-End (backEnd)

| Tecnologia         | Descrição                                              |
| ------------------ | ------------------------------------------------------ |
| **Python**         | Linguagem principal do servidor.                       |
| **Flask**          | Micro-framework web para API RESTful.                  |
| **Ollama (Gemma)** | Execução do modelo de linguagem localmente.            |
| **Scikit-learn**   | Classificação para decidir buscas na web.              |
| **SQLite**         | Banco de dados para histórico de usuários e conversas. |

---

##  Como Executar

###  Pré-requisitos

* **Node.js** (v18+)
* **Python** (v3.10+)
* **Ollama** com modelo `gemma3n` instalado → `ollama pull gemma3n`

---

### Configuração do Back-End

```bash
# Clone o repositório
git clone <URL_DO_SEU_REPOSITORIO>

# Acesse a pasta do back-end
cd LyrIA-279c132dc1e8fa9840e3c120c6c09ec38c535368/backEnd

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Instale as dependências
pip install -r requirements.txt

# Crie o banco de dados
python banco/banco.py

# Inicie o servidor Flask
flask run --port 5000
```

---

### Configuração do Front-End

```bash
# Acesse a pasta do front-end
cd ../lyria-web

# Instale as dependências
npm install

# Inicie a aplicação
npm run dev
```

🔗 Acesse no navegador: **[http://localhost:5173](http://localhost:5173)**

---

## Equipe

Este projeto foi desenvolvido com dedicação pela equipe:

* 👨‍💻 Antony
* 👨‍💻 Gabriel Cardoso
* 👨‍💻 João Gabriel
* 👩‍💻 Juliana
* 👩‍💻 Raissa
* 👩‍💻 Vitoria

