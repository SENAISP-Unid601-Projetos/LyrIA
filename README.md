<p align="center">
<img src="https://github.com/user-attachments/assets/741e737c-f127-4a1a-b0d6-1b4d001cc8b6" alt="LyrIA Logo" width="200"/>
</p>

<h1 align="center">LyrIA - Sua Assistente Virtual Inteligente</h1>

<p align="center">
<img alt="Status do Projeto" src="https://img.shields.io/badge/status-Em%20Desenvolvimento-yellow">
<img alt="Linguagem Principal" src="https://img.shields.io/badge/principal-Python%20%26%20JS-blue?logo=python&logoColor=white&color=blueviolet">
<img alt="Licença" src="https://img.shields.io/badge/license-MIT-blue">
</p>

🤖 Sobre o Projeto
LyrIA é uma assistente virtual inteligente desenvolvida como projeto de conclusão do curso de Técnico em Desenvolvimento de Sistemas do SENAI "Antonio Adolpho Lobbe" em São Carlos-SP. A aplicação conta com uma interface web moderna e um back-end robusto que utiliza um modelo de linguagem de grande porte (LLM) para gerar respostas dinâmicas e contextuais.

O objetivo do LyrIA é oferecer uma experiência de conversação natural e útil, sendo capaz de responder a perguntas gerais e, quando necessário, buscar informações atualizadas na web para garantir a precisão das respostas.

📸 Screenshots
<p align="center">Adicione aqui um GIF ou imagens da tela de chat, login, etc. para mostrar o visual do projeto!</p>

✨ Funcionalidades
Interface de Chat Interativa: Front-end construído em React com uma experiência de usuário fluida e responsiva.

Inteligência Artificial com LLM: Respostas geradas pelo modelo Gemma através do Ollama, permitindo conversas ricas e coerentes.

Busca Inteligente na Web: Um classificador de intenção (usando scikit-learn) determina se a pergunta do usuário requer informações recentes e busca na web através da SerpAPI para fornecer dados atualizados.

Personas Customizáveis: O back-end permite definir diferentes "personas" para a IA, como "Professora" ou "Assistente Empresarial", alterando seu tom e estilo de resposta.

Memória e Histórico de Conversa: As conversas são salvas em um banco de dados SQLite para manter o contexto e a continuidade do diálogo.

Autenticação de Usuário: Sistema completo de login e cadastro para uma experiência personalizada.

Tema Claro e Escuro: A interface possui um seletor de tema (light/dark) para maior conforto visual.

🛠️ Tecnologias Utilizadas
O projeto é dividido em duas partes principais:

Front-End (lyria-web)
React: Biblioteca principal para a construção da interface.

Vite: Ferramenta de build para um ambiente de desenvolvimento rápido e otimizado.

Axios: Para realizar as chamadas à API do back-end de forma eficiente.

React Router: Para gerenciar as rotas da aplicação (Home, Chat, Login).

CSS: Estilização componentizada para uma interface moderna e organizada.

Back-End (backEnd)
Python: Linguagem principal para toda a lógica do servidor.

Flask: Micro-framework web para a criação da API RESTful.

Ollama (Gemma): Para rodar o modelo de linguagem de grande porte localmente.

Scikit-learn: Para treinar e utilizar o modelo de classificação que decide quando buscar na web.

SQLite: Banco de dados relacional para armazenar dados de usuários, conversas e memórias.

🚀 Como Executar o Projeto
Para rodar o projeto em sua máquina local, siga os passos abaixo.

Pré-requisitos
Node.js (versão 18 ou superior)

Python (versão 3.10 ou superior)

Ollama instalado e com o modelo gemma3n baixado (ollama pull gemma3n).

1. Back-End
Bash

# 1. Clone o repositório
git clone <URL_DO_SEU_REPOSITORIO>

# 2. Navegue até a pasta do back-end
cd LyrIA-279c132dc1e8fa9840e3c120c6c09ec38c535368/backEnd

# 3. Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Crie o banco de dados
python banco/banco.py

# 6. Inicie o servidor Flask
flask run --port 5000
2. Front-End
Bash

# 1. Em um novo terminal, navegue até a pasta do front-end
cd ../lyria-web

# 2. Instale as dependências
npm install

# 3. Inicie a aplicação React
npm run dev
Após seguir os passos, acesse http://localhost:5173 (ou a porta indicada no terminal) no seu navegador.

👥 Equipe
Este projeto foi desenvolvido com muito carinho e dedicação pela seguinte equipe de estudantes do SENAI São Carlos:

Antony

Gabriel Cardoso

João Gabriel

Juliana

Raissa

Vitoria
