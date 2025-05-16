import requests
import sqlite3
import os
from classificador_busca_web import deve_buscar_na_web

LIMITE_HISTORICO = 20
SERPAPI_KEY = "11480a6923b283bdc1a34c6243b975f4664be3aaab350aecc4da71bc6af80f62"

# Banco de dados
conn = sqlite3.connect("lyria.db")
cursor = conn.cursor()

# === Funções do banco ===
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

# === Funções de linguagem ===
def gerar_prompt(conversas, memorias, nova_pergunta, persona, contexto_web=None):
    prompt = persona + "\n"

    if memorias:
        prompt += "Informações importantes sobre o usuário:\n" + "\n".join(memorias) + "\n"

    if contexto_web:
        prompt += "Informações da web:\n" + contexto_web + "\n"

    for troca in conversas:
        prompt += f"Usuário: {troca['pergunta']}\nLyria: {troca['resposta']}\n"

    prompt += f"Usuário: {nova_pergunta}\nLyria:"
    return prompt

def resumir_conversas(conversas, modelo='gemma3:1b'):
    texto = "\n".join([f"Usuário: {c['pergunta']}\nLyria: {c['resposta']}" for c in conversas])
    prompt = "Resuma essa conversa em poucas frases, mantendo apenas as informações importantes e que devem ser lembradas:\n" + texto + "\nResumo:"
    payload = {
        'model': modelo,
        'prompt': prompt,
        'stream': False
    }
    response = requests.post('http://localhost:11434/api/generate', json=payload)
    return response.json()['response']

def perguntar_ollama(pergunta, conversas, memorias, persona, modelo='gemma3:1b', contexto_web=None):
    prompt_completo = gerar_prompt(conversas, memorias, pergunta, persona, contexto_web)
    payload = {
        'model': modelo,
        'prompt': prompt_completo,
        'stream': False
    }
    response = requests.post('http://localhost:11434/api/generate', json=payload)
    return response.json()['response']

# === Pesquisa na Web com SerpAPI ===
def buscar_na_web(pergunta):
    url = "https://serpapi.com/search"
    params = {
        "q": pergunta,
        "hl": "pt-br",
        "gl": "br",
        "api_key": SERPAPI_KEY
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        resultados = data.get("organic_results", [])
        trechos = [item.get("snippet", "") for item in resultados if "snippet" in item]
        return "\n".join(trechos[:3])  # pega até 3 snippets
    except Exception as e:
        print(f"Erro na busca web: {e}")
        return None

# === Execução ===
entrada = input("Do que você precisa?\n1. Professor\n2. Empresa\nEscolha: ")
if entrada == '1':
    persona = 'Você é a professora Lyria...'
elif entrada == '2':
    persona = 'Você é a Lyria, uma assistente virtual empresarial...'
else:
    print("Opção inválida.")
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

    contexto_web = None
    if deve_buscar_na_web(entrada):
        print("🔎 Pesquisando na web...")
        contexto_web = buscar_na_web(entrada)

    resposta = perguntar_ollama(entrada, conversas, memorias, persona, contexto_web=contexto_web)
    print("Lyria:", resposta)

    salvar_conversa(usuario, entrada, resposta)

    if len(conversas) + 1 > LIMITE_HISTORICO:
        resumo = resumir_conversas(conversas + [{"pergunta": entrada, "resposta": resposta}])
        salvar_resumo(usuario, resumo)
        limpar_conversas(usuario)

conn.close()
