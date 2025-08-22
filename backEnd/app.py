from flask import Flask, request, jsonify
from flask_cors import CORS
from testeDaIa import carregar_conversas, carregar_memorias, salvar_conversa, perguntar_ollama, buscar_na_web
from banco.banco import pegarPersonaEscolhida, escolherApersona, criarUsuario, procurarUsuarioPorEmail, pegarHistorico
import os

DB_NOME = os.path.join(os.path.dirname(__file__), "lyria.db")

app = Flask(__name__)
CORS(app)

@app.route('/Lyria/<usuario>/conversar', methods=['POST'])
def conversar(usuario):
    data = request.get_json()
    if not data or 'pergunta' not in data:
        return jsonify({"erro": "Campo 'pergunta' é obrigatório"}), 400
    
    pergunta = data['pergunta']
    persona = pegarPersonaEscolhida(usuario)
    if not persona:
        return jsonify({"erro": "Usuário não tem persona definida"}), 400
    
    try:
        conversas = carregar_conversas(usuario)
        memorias = carregar_memorias(usuario)
        contexto_web = buscar_na_web(pergunta)
        resposta = perguntar_ollama(pergunta, conversas, memorias, persona, contexto_web)
        salvar_conversa(usuario, pergunta, resposta)
        return jsonify({"resposta": resposta})
    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

@app.route('/Lyria/conversas/<usuario>', methods=['GET'])
def get_conversas(usuario):
    try:
        conversas = carregar_conversas(usuario)
        return jsonify({"conversas": conversas})
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar conversas: {str(e)}"}), 500

@app.route('/Lyria/<usuario>/PersonaEscolhida', methods=['GET'])
def get_persona_escolhida(usuario):
    try:
        persona = pegarPersonaEscolhida(usuario)
        if persona:
            return jsonify({"persona": persona})
        return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar persona: {str(e)}"}), 500

@app.route('/Lyria/<usuario>/PersonaEscolhida', methods=['POST'])
def set_persona_escolhida(usuario):
    data = request.get_json()
    if not data or 'persona' not in data:
        return jsonify({"erro": "Campo 'persona' é obrigatório"}), 400

    persona = data['persona']
    if persona not in ['professor', 'empresarial']:
        return jsonify({"erro": "Persona inválida"}), 400

    try:
        escolherApersona(persona, usuario)
        return jsonify({"sucesso": "Persona atualizada com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar persona: {str(e)}"}), 500

@app.route('/Lyria/usuarios', methods=['POST'])
def criar_usuario_route():
    # Garante que o banco e tabelas existam

    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({"erro": "Campos 'nome' e 'email' são obrigatórios"}), 400

    nome = data['nome']
    email = data['email']
    persona = data.get('persona', 'professor')
    senha_hash = data.get('senha_hash') 

    try:
        usuario_id = criarUsuario(nome, email, persona, senha_hash)
        return jsonify({"sucesso": "Usuário criado com sucesso", "id": usuario_id}), 201
    except Exception as e:
        if "UNIQUE constraint" in str(e):
            return jsonify({"erro": "Usuário já existe"}), 409
        return jsonify({"erro": f"Erro ao criar usuário: {str(e)}"}), 500

@app.route('/Lyria/usuarios/<usuarioEmail>', methods=['GET'])
def get_usuario(usuarioEmail):
    try:
        result = procurarUsuarioPorEmail(usuarioEmail)
        if result:
            return jsonify({"usuario": result})
        return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar usuário: {str(e)}"}), 500

@app.route('/Lyria/<usuario>/historico', methods=['GET'])
def get_historico_recente(usuario):
    try:
        historico = pegarHistorico(usuario)
        return jsonify({"historico": historico})
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar histórico: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
