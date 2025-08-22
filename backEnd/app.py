from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from testeDaIa import carregar_conversas, carregar_memorias, salvar_conversa, perguntar_ollama, buscar_na_web
from banco.banco import pegarPersonaEscolhida,escolherApersona,criarUsuario,procurarUsuarioPorEmail,pegarHistorico

app = Flask(__name__)
CORS(app)  

@app.route('/Lyria/<usuario>/conversar', methods=['POST'])
def conversar(usuario):
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Nenhum dado recebido"}), 400
    
    pergunta = data.get('pergunta')
    persona = pegarPersonaEscolhida(usuario)
    
    if not all([pergunta, persona]):
        return jsonify({"erro": "Os campos 'pergunta' e 'persona' são obrigatórios"}), 400
    
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
        result = pegarPersonaEscolhida(usuario)
        if result:
            return jsonify({"persona": result["persona_escolhida"]})
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar persona: {str(e)}"}), 500

@app.route('/Lyria/<usuario>/PersonaEscolhida', methods=['POST'])
def set_persona_escolhida(usuario):
    data = request.get_json()
    if not data or 'persona' not in data:
        return jsonify({"erro": "Campo 'persona' é obrigatório"}), 400
    
    persona = data.get('persona')
    personas_validas = ['professor', 'empresarial']
    
    if persona not in personas_validas:
        return jsonify({"erro": f"Persona deve ser uma das opções: {personas_validas}"}), 400
    
    try:
        escolherApersona(persona,usuario)
        return jsonify({"sucesso": "Persona atualizada com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar persona: {str(e)}"}), 500

@app.route('/Lyria/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400
    
    nome = data.get('nome')
    email = data.get('email')
    persona = data.get('persona', 'professor')
    
    try:
        criarUsuario(nome,email,persona)
        return jsonify({"sucesso": "Usuário criado com sucesso", "id": cursor.lastrowid}), 201
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Usuário já existe"}), 409
    except Exception as e:
        return jsonify({"erro": f"Erro ao criar usuário: {str(e)}"}), 500

@app.route('/Lyria/usuarios/<usuario>', methods=['GET'])
def get_usuario(usuarioEmail):
    try:
        result = procurarUsuarioPorEmail(usuarioEmail)
        
        if result:
            usuario_data = {
                "id": result["id"],
                "nome": result["nome"],
                "email": result["email"],
                "persona_escolhida": result["persona_escolhida"]
            }
            return jsonify({"usuario": usuario_data})
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar usuário: {str(e)}"}), 500

@app.route('/Lyria/<usuario>/historico', methods=['GET'])
def get_historico_recente(usuario):
    try:
        results = pegarHistorico(usuario)
        
        historico = []
        for row in results:
            historico.append({
                "pergunta": row["pergunta"],
                "resposta": row["resposta"],
                "timestamp": row["timestamp"]
            })
        
        return jsonify({"historico": historico})
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar histórico: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)