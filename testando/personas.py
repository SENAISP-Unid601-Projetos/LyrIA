import requests
import sqlite3
import os

LIMITE_HISTORICO = 20

# Conexão com o banco de dados
conn = sqlite3.connect("lyria.db")
cursor = conn.cursor()

# Criação das tabelas, caso ainda não existam
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS memorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    texto TEXT,
    FOREIGN KEY (usuario) REFERENCES usuarios(nome)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    pergunta TEXT,
    resposta TEXT,
    FOREIGN KEY (usuario) REFERENCES usuarios(nome)
)''')

# Funções para carregar e salvar memórias e conversas
def carregar_memorias(usuario):
    cursor.execute("SELECT texto FROM memorias WHERE usuario = ?", (usuario,))
    return [linha[0] for linha in cursor.fetchall()]

def carregar_conversas(usuario):
    cursor.execute("SELECT pergunta, resposta FROM mensagens WHERE usuario = ? ORDER BY id ASC", (usuario,))
    return [{"pergunta": p, "resposta": r} for p, r in cursor.fetchall()]

def salvar_memoria(usuario, memoria):
    cursor.execute("INSERT INTO memorias (usuario, texto) VALUES (?, ?)", (usuario, memoria))
    conn.commit()

def salvar_conversa(usuario, pergunta, resposta):
    cursor.execute("INSERT INTO mensagens (usuario, pergunta, resposta) VALUES (?, ?, ?)", (usuario, pergunta, resposta))
    conn.commit()

def limpar_conversas(usuario):
    cursor.execute("DELETE FROM mensagens WHERE usuario = ?", (usuario,))
    conn.commit()

def salvar_resumo(usuario, resumo):
    salvar_memoria(usuario, resumo)

def gerar_prompt(conversas, memorias, nova_pergunta, persona):
    prompt = persona + "\n"

    if memorias:
        prompt += "Informações importantes sobre o usuário:\n"
        prompt += "\n".join(memorias) + "\n"

    for troca in conversas:
        prompt += f"Usuário: {troca['pergunta']}\nLyria: {troca['resposta']}\n"

    prompt += f"Usuário: {nova_pergunta}\nLyria:"
    return prompt

def resumir_conversas(conversas, modelo='gemma3:1b'):
    texto = "\n".join([f"Usuário: {c['pergunta']}\nLyria: {c['resposta']}" for c in conversas])
    prompt = (
        "Resuma essa conversa em poucas frases, mantendo apenas as informações importantes e que devem ser lembradas:\n" +
        texto + "\nResumo:"
    )
    payload = {
        'model': modelo,
        'prompt': prompt,
        'stream': False
    }
    response = requests.post('http://localhost:11434/api/generate', json=payload)
    return response.json()['response']

def perguntar_ollama(pergunta, conversas, memorias, persona, modelo='gemma3:1b'):
    prompt_completo = gerar_prompt(conversas, memorias, pergunta, persona)
    payload = {
        'model': modelo,
        'prompt': prompt_completo,
        'stream': False
    }
    response = requests.post('http://localhost:11434/api/generate', json=payload)
    return response.json()['response']

# Escolha da persona
entrada = input("Do que você precisa?\n1. Professor\n2. Empresa\nEscolha: ")
if entrada.lower() == '1':
    persona = 'Você é a professora Lyria, uma assistente virtual dedicada a apoiar professores no processo de ensino e aprendizado. Lyria fala português com clareza e é sempre empática, bondosa e paciente. Seu objetivo é educar os alunos de maneira objetiva e direta, sem perder o tom de uma pessoa amável e disposta a ajudar. Lyria sempre tenta simplificar as explicações, tornando conceitos complexos mais acessíveis, e está sempre pronta para ouvir as dúvidas com muita compreensão. Sua abordagem é tranquila e acolhedora, com respostas precisas, focadas em oferecer a melhor orientação possível para o aprendizado.'
elif entrada.lower() == '2':
    persona = 'Você é a Lyria, uma assistente virtual empresarial que atua como uma secretária eficiente e confiável. Lyria fala português com polidez e clareza. Ela é organizada, ágil e sempre pronta para ajudar com compromissos, informações corporativas, atendimento a clientes e tarefas administrativas. Sua comunicação é objetiva, cordial e profissional, mantendo sempre um tom acolhedor e respeitoso. Lyria tem foco em resolver problemas de forma prática e em oferecer suporte confiável no ambiente de negócios, tornando-se uma aliada indispensável na rotina empresarial.'
else:
    print("Opção inválida. Encerrando.")
    exit()

usuario = input("Informe seu nome de usuário: ").strip().lower()

cursor.execute("INSERT OR IGNORE INTO usuarios (nome) VALUES (?)", (usuario,))
conn.commit()

while True:
    entrada = input("Você: ")
    if entrada.lower() in ['sair', 'exit', 'quit']:
        break

    conversas = carregar_conversas(usuario)
    memorias = carregar_memorias(usuario)
    resposta = perguntar_ollama(entrada, conversas, memorias, persona)
    print("Lyria:", resposta)

    salvar_conversa(usuario, entrada, resposta)

    # Se o número de conversas ultrapassar o limite, resumir e limpar o histórico
    if len(conversas) + 1 > LIMITE_HISTORICO:
        resumo = resumir_conversas(conversas + [{"pergunta": entrada, "resposta": resposta}])
        salvar_resumo(usuario, resumo)
        limpar_conversas(usuario)

conn.close()
