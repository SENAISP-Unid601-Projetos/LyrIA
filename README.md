LyrIA - Sua Assistente Virtual Inteligente
<p align="center">
<strong>Um projeto de conclusão de curso do SENAI São Carlos</strong>
</p>

<p align="center">
<img alt="Status do Projeto" src="https://img.shields.io/badge/status-Em%20Desenvolvimento-yellow">
<img alt="Linguagem Principal" src="https://img.shields.io/badge/principal-Python%20%26%20JS-blue?logo=python&logoColor=white&color=blueviolet">
<img alt="Licença" src="https://img.shields.io/badge/license-MIT-blue">
</p>

🤖 Sobre o Projeto
LyrIA é uma assistente virtual inteligente desenvolvida como projeto de conclusão do curso de Técnico em Desenvolvimento de Sistemas do SENAI "Antonio Adolpho Lobbe" em São Carlos-SP. A aplicação conta com uma interface web moderna e um back-end robusto que utiliza um modelo de linguagem de grande porte (LLM) para gerar respostas dinâmicas e contextuais.

O objetivo do LyrIA é oferecer uma experiência de conversação natural e útil, sendo capaz de responder a perguntas gerais e, quando necessário, buscar informações atualizadas na web para garantir a precisão das respostas.

✨ Funcionalidades Principais
🎨 Interface de Chat Interativa: Front-end construído em React com uma experiência de usuário fluida e responsiva.

🧠 Inteligência Artificial com LLM: Respostas geradas pelo modelo Gemma através do Ollama, permitindo conversas ricas e coerentes.

🌐 Busca Inteligente na Web: Um classificador de intenção (scikit-learn) determina se a pergunta requer informações recentes e busca na web através da SerpAPI para fornecer dados atualizados.

🎭 Personas Customizáveis: O back-end permite definir diferentes "personas" para a IA (como "Professora" ou "Assistente Empresarial"), alterando seu tom e estilo de resposta.

💾 Memória e Histórico: As conversas são salvas em um banco de dados SQLite para manter o contexto e a continuidade do diálogo.

🔐 Autenticação de Usuário: Sistema completo de login e cadastro para uma experiência personalizada.

🌗 Tema Claro e Escuro: A interface possui um seletor de tema (light/dark) para maior conforto visual.

📸 Screenshots
<p align="center">
<img src="https://github.com/user-attachments/assets/f0568557-3819-455e-915e-58d9f5b480e4" alt="Tela Inicial do LyrIA" width="700"/>
<br>
<em>Tela Inicial do Projeto</em>
</p>
<p align="center">
<img src="https://github.com/user-attachments/assets/bb634e4c-4ea1-4845-a64d-91c049feffc4" alt="Tela de Chat do LyrIA" width="700"/>
<br>
<em>Interface de Chat em Ação</em>
</p>

🛠️ Tecnologias Utilizadas
O projeto possui uma arquitetura moderna dividida em duas partes principais:

Front-End (lyria-web)
Tecnologia

Descrição

React

Biblioteca principal para a construção da interface.

Vite

Ferramenta de build para um ambiente de desenvolvimento rápido.

Axios

Cliente HTTP para realizar as chamadas à API do back-end.

React Router

Biblioteca para gerenciar as rotas da aplicação (Home, Chat, Login).

CSS

Estilização componentizada para uma interface moderna e organizada.

Back-End (backEnd)
Tecnologia

Descrição

Python

Linguagem principal para toda a lógica do servidor.

Flask

Micro-framework web para a criação da API RESTful.

Ollama (Gemma)

Plataforma para rodar o modelo de linguagem de grande porte localmente.

Scikit-learn

Utilizada para treinar o modelo de classificação que decide quando buscar na web.

SQLite

Banco de dados relacional para armazenar dados de usuários e conversas.

🚀 Como Executar o Projeto
Para rodar o projeto em sua máquina local, siga os passos abaixo.

Pré-requisitos
Node.js (versão 18 ou superior)

Python (versão 3.10 ou superior)

Ollama instalado e com o modelo gemma3n baixado (ollama pull gemma3n).

1. Configuração do Back-End
# Clone o repositório
git clone <URL_DO_SEU_REPOSITORIO>

# Navegue até a pasta do back-end
cd LyrIA-279c132dc1e8fa9840e3c120c6c09ec38c535368/backEnd

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Crie o banco de dados
python banco/banco.py

# Inicie o servidor Flask
flask run --port 5000

2. Configuração do Front-End
# Em um novo terminal, navegue até a pasta do front-end
cd ../lyria-web

# Instale as dependências
npm install

# Inicie a aplicação React
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
