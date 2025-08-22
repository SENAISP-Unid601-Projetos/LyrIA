from flask import Flask, request, jsonify
from flask_cors import CORS
from testeDaIa import perguntar_ollama, buscar_na_web, get_persona_texto
from banco.banco import (
    pegarPersonaEscolhida, 
    escolherApersona, 
    criarUsuario, 
    procurarUsuarioPorEmail, 
    pegarHistorico,
    criar_banco,
    salvarMensagem,
    carregar_conversas,
    carregar_memorias
)
from classificadorDaWeb.classificador_busca_web import deve_buscar_na_web

criar_banco()

app = Flask(__name__)
CORS(app)

@app.route('/Lyria/<usuario>/conversar', methods=['POST'])
def conversar(usuario):
    data = request.get_json()
    if not data or 'pergunta' not in data:
        return jsonify({"erro": "Campo 'pergunta' é obrigatório"}), 400
    pergunta = data['pergunta']
    persona_tipo = pegarPersonaEscolhida(usuario)
    if not persona_tipo:
        return jsonify({"erro": "Usuário não tem persona definida"}), 400
    
    try:
        conversas = carregar_conversas(usuario)
        memorias = carregar_memorias(usuario)
        contexto_web = None
        if deve_buscar_na_web(pergunta):
            contexto_web = buscar_na_web(pergunta)
        persona = get_persona_texto(persona_tipo)
        resposta = perguntar_ollama(pergunta, conversas, memorias, persona, contexto_web)
        salvarMensagem(usuario, pergunta, resposta, modelo_usado="ollama", tokens=None)
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
        return jsonify({"erro": "Persona inválida. Use 'professor' ou 'empresarial'"}), 400

    try:
        escolherApersona(persona, usuario)
        return jsonify({"sucesso": "Persona atualizada com sucesso"})
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar persona: {str(e)}"}), 500

@app.route('/Lyria/usuarios', methods=['POST'])
def criar_usuario_route():
    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({"erro": "Campos 'nome' e 'email' são obrigatórios"}), 400

    nome = data['nome']
    email = data['email']
    persona = data.get('persona', 'professor')
    senha_hash = data.get('senha_hash')
    
    if persona not in ['professor', 'empresarial']:
        return jsonify({"erro": "Persona inválida. Use 'professor' ou 'empresarial'"}), 400

    try:
        usuario_id = criarUsuario(nome, email, persona, senha_hash)
        return jsonify({
            "sucesso": "Usuário criado com sucesso", 
            "id": usuario_id,
            "persona": persona
        }), 201
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
        limite = request.args.get('limite', 10, type=int)
        if limite > 50:  
            limite = 50
            
        historico = pegarHistorico(usuario, limite)
        return jsonify({"historico": historico})
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar histórico: {str(e)}"}), 500

@app.route('/Lyria/personas', methods=['GET'])
def listar_personas():
    personas = {
        "professor": "Modo didático e empático para ensino e aprendizagem",
        "empresarial": "Modo profissional e objetivo para ambiente corporativo"
    }
    return jsonify({"personas": personas})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)