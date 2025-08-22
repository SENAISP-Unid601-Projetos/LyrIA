import requests
import sqlite3
import pyttsx3
import speech_recognition as sr
import os
from classificadorDaWeb.classificador_busca_web import deve_buscar_na_web

LIMITE_HISTORICO = 12
SERPAPI_KEY = "11480a6923b283bdc1a34c6243b975f4664be3aaab350aecc4da71bc6af80f62"
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "gemma3n:latest"
ACTIVATION_WORDS = ["lyria", "olá", "oi", "alô"]

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
conn = sqlite3.connect(db_path, check_same_thread=False) 
cursor = conn.cursor()

def carregar_memorias(usuario):
    cursor.execute("SELECT texto FROM memorias WHERE usuario = ?", (usuario,))
    return [linha[0] for linha in cursor.fetchall()]

def carregar_conversas(usuario):
    cursor.execute("SELECT pergunta, resposta FROM mensagens WHERE usuario = ? ORDER BY id ASC", (usuario,))
    return [{"pergunta": p, "resposta": r} for p, r in cursor.fetchall()]

def salvar_conversa(usuario, pergunta, resposta):
    cursor.execute("INSERT INTO mensagens (usuario, pergunta, resposta) VALUES (?, ?, ?)", (usuario, pergunta, resposta))
    conn.commit()

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

def perguntar_ollama(pergunta, conversas, memorias, persona, contexto_web=None):
    prompt = f"{persona}\nHistórico:\n"
    for msg in conversas[-LIMITE_HISTORICO:]:
        prompt += f"Usuário: {msg['pergunta']}\nLyria: {msg['resposta']}\n"
    
    if contexto_web:
        prompt += f"Contexto de pesquisa na web, considere isso ACIMA dos dados que você tem pois estão mais atualizados: {contexto_web}\n"
        
    prompt += f"Usuário: {pergunta}\nLyria:"
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={'model': OLLAMA_MODEL, 'prompt': prompt, 'stream': False},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get('response', "Não entendi")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar Ollama: {e}")
        return "Erro de conexão"

def buscar_na_web(pergunta):
    try:
        params = {"q": pergunta, "hl": "pt-br", "gl": "br", "api_key": SERPAPI_KEY}
        res = requests.get("https://serpapi.com/search", params=params, timeout=10)
        trechos = [r.get("snippet", "") for r in res.json().get("organic_results", [])[:2]]
        return " ".join(trechos)
    except Exception:
        return None

if __name__ == "__main__":
    print("Do que você precisa?")
    print("1. Professor")
    print("2. Empresarial")
    escolha = input("Escolha: ").strip()

    if escolha == '1':
        persona = "Você é a professora Lyria, responda de forma didática e empática..."
    elif escolha == '2':
        persona = "Você é a assistente Lyria, responda de forma profissional e objetiva..."
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
                
            contexto_web = buscar_na_web(entrada) if deve_buscar_na_web(entrada) else None
            resposta = perguntar_ollama(entrada, carregar_conversas(usuario),
                                     carregar_memorias(usuario), persona, contexto_web)
            
            print(f"Lyria: {resposta}")
            falar(resposta)
            salvar_conversa(usuario, entrada, resposta)

    conn.close()
