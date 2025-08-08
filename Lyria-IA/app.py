from flask import Flask, request, jsonify
from testeDaIa import carregar_conversas, carregar_memorias, salvar_conversa, perguntar_ollama, buscar_na_web

app = Flask(__name__)

@app.route('/Lyria/conversar', methods=['POST'])
def conversar():
    data = request.get_json()
    if not data:
        return jsonify({"erro": "Nenhum dado recebido"}), 400

    usuario = data.get('usuario')
    pergunta = data.get('pergunta')
    persona = data.get('persona')

    if not all([usuario, pergunta, persona]):
        return jsonify({"erro": "Os campos 'usuario', 'pergunta' e 'persona' são obrigatórios"}), 400

    conversas = carregar_conversas(usuario)
    memorias = carregar_memorias(usuario)
    
    contexto_web = buscar_na_web(pergunta)
    resposta = perguntar_ollama(pergunta, conversas, memorias, persona, contexto_web)

    salvar_conversa(usuario, pergunta, resposta)
    
    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)