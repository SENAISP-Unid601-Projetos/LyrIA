import requests
import sqlite3
import time
import pyttsx3
import speech_recognition as sr
import wave
import os
from classificadorDaWeb.classificador_busca_web import deve_buscar_na_web

# Configurações
LIMITE_HISTORICO = 12
SERPAPI_KEY = "11480a6923b283bdc1a34c6243b975f4664be3aaab350aecc4da71bc6af80f62"
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "mistral"
ACTIVATION_WORDS = ["lyria", "olá", "oi", "alô"]

# Inicializações
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 400
recognizer.pause_threshold = 0.8

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'banco', 'lyria.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Funções do banco (mantidas)
def carregar_memorias(usuario):
    cursor.execute("SELECT texto FROM memorias WHERE usuario = ?", (usuario,))
    return [linha[0] for linha in cursor.fetchall()]

def carregar_conversas(usuario):
    cursor.execute("SELECT pergunta, resposta FROM mensagens WHERE usuario = ? ORDER BY id ASC", (usuario,))
    return [{"pergunta": p, "resposta": r} for p, r in cursor.fetchall()]

def salvar_conversa(usuario, pergunta, resposta):
    cursor.execute("INSERT INTO mensagens (usuario, pergunta, resposta) VALUES (?, ?, ?)", (usuario, pergunta, resposta))
    conn.commit()

# Funções de voz melhoradas
def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def ouvir_microfone():
    with sr.Microphone() as source:
        print("\nAguardando ativação... (diga 'Lyria' ou 'Olá')")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            texto = recognizer.recognize_google(audio, language='pt-BR').lower()
            
            if any(palavra in texto for palavra in ACTIVATION_WORDS):
                falar("Sim, estou ouvindo")
                print("Diga sua mensagem...")
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)
                texto = recognizer.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {texto}")
                return texto
            elif "sair" in texto:
                return "sair"
            return ""
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Erro áudio: {e}")
            return ""

# Funções Ollama (mantidas)
def perguntar_ollama(pergunta, conversas, memorias, persona, contexto_web=None):
    prompt = f"{persona}\nHistórico:\n"
    for msg in conversas[-LIMITE_HISTORICO:]:
        prompt += f"Usuário: {msg['pergunta']}\nLyria: {msg['resposta']}\n"
    prompt += f"Usuário: {pergunta}\nLyria:"
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={'model': OLLAMA_MODEL, 'prompt': prompt, 'stream': False},
            timeout=30
        )
        return response.json().get('response', "Não entendi")
    except Exception:
        return "Erro de conexão"

def buscar_na_web(pergunta):
    try:
        params = {"q": pergunta, "hl": "pt-br", "gl": "br", "api_key": SERPAPI_KEY}
        res = requests.get("https://serpapi.com/search", params=params, timeout=10)
        trechos = [r.get("snippet", "") for r in res.json().get("organic_results", [])[:2]]
        return " ".join(trechos)
    except Exception:
        return None

# Menu principal
print("Do que você precisa?")
print("1. Professor")
print("2. Empresarial")
escolha = input("Escolha: ").strip()

if escolha == '1':
    persona = "Você é a professora Lyria, responda de forma didática e empática, tratando o usuário como um aluno. Responda de forma curta e pergunte se o aluno deseja mais informações, se sim então você poderá explicar o assunto extensivamente e de forma didática. De forma alguma fale palavras de baixo calão e sempre seja gentil e simpática. Caso a pesquisa na web diga algo contrário do que você sabe, prefira o que foi pesquisado pois pode estar mais atualizado."
elif escolha == '2':
    persona = "Você é a assistente Lyria, responda de forma profissional e objetiva. Seja clara e responda de forma curta, somente se extendendo caso o usuário diga que quer isso, então pergunte sempre se ele quer saber mais. Caso a pesquisa na web diga algo contrário do que você sabe, prefira o que foi pesquisado pois pode estar mais atualizado."
else:
    print("Opção inválida")
    exit()

print("\nModo de interação:")
print("1. Apenas texto")
print("2. Voz e texto")
modo = input("Escolha: ").strip()

usuario = input("Informe seu nome: ").strip().lower()
cursor.execute("INSERT OR IGNORE INTO usuarios (nome) VALUES (?)", (usuario,))
conn.commit()

# Loop principal
if modo == '1':
    print("\nModo texto ativo (digite 'sair' para encerrar)")
    while True:
        entrada = input("Você: ").strip()
        if entrada.lower() == 'sair':
            break
            
        resposta = perguntar_ollama(entrada, carregar_conversas(usuario), 
                                 carregar_memorias(usuario), persona)
        print(f"Lyria: {resposta}")
        salvar_conversa(usuario, entrada, resposta)

else:
    print("\nModo voz ativo (diga 'Lyria' ou 'Olá' para ativar, 'Sair' para encerrar)")
    falar("Modo voz ativado. Diga Lyria ou Olá quando quiser falar comigo.")
    
    while True:
        entrada = ouvir_microfone()
        
        if entrada == "sair":
            falar("Até logo!")
            break
        elif not entrada:
            continue
            
        # Processa a pergunta
        contexto_web = buscar_na_web(entrada) if deve_buscar_na_web(entrada) else None
        resposta = perguntar_ollama(entrada, carregar_conversas(usuario),
                                 carregar_memorias(usuario), persona, contexto_web)
        
        print(f"Lyria: {resposta}")
        falar(resposta)
        salvar_conversa(usuario, entrada, resposta)

conn.close()