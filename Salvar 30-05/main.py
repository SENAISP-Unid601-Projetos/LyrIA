import requests
import sqlite3
import time
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv
from classificador_busca_web import deve_buscar_na_web
import threading
from queue import Queue

# --- Carregar variáveis de ambiente do arquivo .env ---
load_dotenv()

# --- Configurações ---
LIMITE_HISTORICO = 12
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "mistral"
ACTIVATION_WORDS = ["lyria", "olá", "oi", "alô"]
INTERRUPTION_WORDS = ["lyria", "pare de falar", "para de falar"]
TIMEOUT_INATIVIDADE = 60 # Segundos

# --- Variáveis de Estado Global ---
# Usadas para comunicação entre as threads de fala e escuta
is_speaking = False
last_interaction_time = time.time()
user_input_queue = Queue() # Fila para armazenar a entrada do usuário
tts_queue = Queue() # Fila para requisições de fala (Text-to-Speech)
stop_speaking_event = threading.Event()

# --- Inicializações ---
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        # Tente selecionar uma voz em português se disponível
        br_voice = next((v for v in voices if "brazil" in v.name.lower() or "portuguese" in v.name.lower()), voices[0])
        engine.setProperty('voice', br_voice.id)
    engine.setProperty('rate', 170)
except Exception as e:
    print(f"Erro ao inicializar o pyttsx3: {e}")
    engine = None

recognizer = sr.Recognizer()
recognizer.energy_threshold = 400
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = False

# --- Conexão com Banco de Dados ---
conn = sqlite3.connect("lyria.db", check_same_thread=False) # Habilitado para threads
cursor = conn.cursor()

# --- Funções do Banco (mantidas) ---
def carregar_memorias(usuario):
    cursor.execute("SELECT texto FROM memorias WHERE usuario = ?", (usuario,))
    return [linha[0] for linha in cursor.fetchall()]

def carregar_conversas(usuario):
    cursor.execute("SELECT pergunta, resposta FROM mensagens WHERE usuario = ? ORDER BY id ASC", (usuario,))
    return [{"pergunta": p, "resposta": r} for p, r in cursor.fetchall()]

def salvar_conversa(usuario, pergunta, resposta):
    cursor.execute("INSERT INTO mensagens (usuario, pergunta, resposta) VALUES (?, ?, ?)", (usuario, pergunta,resposta))
    conn.commit()

# --- Funções de Voz (Refatoradas para Fila e Thread Dedicada) ---
def tts_worker():
    """Thread dedicada que pega texto de uma fila e o fala, evitando conflitos."""
    if engine:
        # A função de callback para interrupção
        def onWord(name, location, length):
            if stop_speaking_event.is_set():
                engine.stop()
        engine.connect('started-word', onWord)

    while True:
        try:
            texto = tts_queue.get()
            if texto is None:  # Sinal para terminar a thread
                break
            
            global is_speaking
            is_speaking = True
            stop_speaking_event.clear()
            
            engine.say(texto)
            engine.runAndWait()
            is_speaking = False
        except Exception as e:
            print(f"Erro na thread de TTS: {e}")
            is_speaking = False

def falar(texto):
    """Coloca um texto na fila para ser falado, interrompendo a fala atual se houver."""
    # Se estiver falando, interrompe a fala atual e limpa a fila de falas pendentes
    if is_speaking:
        while not tts_queue.empty():
            try:
                tts_queue.get_nowait()
            except Queue.Empty:
                continue
        stop_speaking_event.set()
        # Uma pequena pausa para garantir que o evento de parada seja processado
        time.sleep(0.1)

    tts_queue.put(texto)

def ouvir_continuamente():
    """Escuta continuamente em uma thread de fundo e coloca a entrada na fila."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("\nOuvindo continuamente em segundo plano...")
        
        while True:
            try:
                audio = recognizer.listen(source)
                texto = recognizer.recognize_google(audio, language='pt-BR').lower()
                
                # Se a assistente estiver falando e uma palavra de interrupção for dita
                if is_speaking and any(palavra in texto for palavra in INTERRUPTION_WORDS):
                    print("--- Interrupção detectada! ---")
                    stop_speaking_event.set() # Sinaliza para a thread de fala parar
                else:
                    # Coloca o texto na fila para o loop principal processar
                    user_input_queue.put(texto)

            except sr.UnknownValueError:
                # Isso é normal, acontece quando há silêncio
                pass
            except Exception as e:
                print(f"Erro no reconhecimento de voz: {e}")
                time.sleep(1)

# --- Funções de Lógica e API (Refatoradas) ---
def perguntar_ollama(pergunta, conversas, memorias, persona, contexto_web=None):
    prompt = f"{persona}\n"
    if contexto_web:
        prompt += f"\nUse a seguinte informação da web para responder: '{contexto_web}'\n"
    
    prompt += "\nHistórico da Conversa:\n"
    for msg in conversas[-LIMITE_HISTORICO:]:
        prompt += f"Usuário: {msg['pergunta']}\nLyria: {msg['resposta']}\n"
    
    prompt += f"Usuário: {pergunta}\nLyria:"
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={'model': OLLAMA_MODEL, 'prompt': prompt, 'stream': False},
            timeout=90 # Aumentado para 90 segundos para dar mais tempo ao modelo
        )
        response.raise_for_status()
        return response.json().get('response', "Desculpe, não consegui processar a resposta.")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com o Ollama: {e}")
        return "Estou com problemas para me conectar ao meu cérebro. Tente novamente mais tarde."

def buscar_na_web(pergunta):
    if not SERPAPI_KEY:
        return "Chave da API SerpApi não configurada."
    try:
        params = {"q": pergunta, "hl": "pt-br", "gl": "br", "api_key": SERPAPI_KEY}
        res = requests.get("https://serpapi.com/search", params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        trechos = [r.get("snippet", "") for r in data.get("organic_results", [])[:3]]
        return " ".join(trechos) if trechos else None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar na web: {e}")
        return None

def processar_e_responder(entrada, usuario, persona):
    """Função unificada para processar entrada, buscar na web e obter resposta."""
    global last_interaction_time
    last_interaction_time = time.time() # Atualiza o tempo da última interação
    
    print(f"Você disse: {entrada}")
    contexto_web = None
    if deve_buscar_na_web(entrada):
        print("🔎 Buscando na web...")
        contexto_web = buscar_na_web(entrada)
    
    print("🧠 Pensando...")
    resposta = perguntar_ollama(entrada, carregar_conversas(usuario),
                               carregar_memorias(usuario), persona, contexto_web)
    
    print(f"Lyria: {resposta}")
    falar(resposta)
    salvar_conversa(usuario, entrada, resposta)

# --- Loop Principal ---
def main():
    print("Do que você precisa?")
    print("1. Professor")
    print("2. Empresa")
    escolha = input("Escolha: ").strip()

    if escolha == '1':
        persona = "Você é a professora Lyria, responda de forma didática e empática."
    elif escolha == '2':
        persona = "Você é a assistente Lyria, responda de forma profissional e objetiva."
    else:
        print("Opção inválida")
        return

    print("\nModo de interação:")
    print("1. Apenas texto")
    print("2. Voz e texto")
    modo = input("Escolha: ").strip()

    usuario = input("Informe seu nome: ").strip().lower()
    cursor.execute("INSERT OR IGNORE INTO usuarios (nome) VALUES (?)", (usuario,))
    conn.commit()

    # Inicia a thread de TTS em segundo plano
    thread_tts = threading.Thread(target=tts_worker)
    thread_tts.daemon = True
    thread_tts.start()

    if modo == '1':
        # Modo Texto
        print("\nModo texto ativo (digite 'sair' para encerrar)")
        while True:
            entrada = input("Você: ").strip()
            if entrada.lower() == 'sair':
                break
            processar_e_responder(entrada, usuario, persona)
    else:
        # Modo Voz
        print("\nModo voz ativo. Diga 'Lyria' ou 'Olá' para começar.")
        falar("Modo voz ativado. Diga Lyria ou Olá para começar a conversar.")
        
        is_active = False
        global last_interaction_time
        last_interaction_time = time.time()

        # Inicia a thread de escuta em segundo plano
        thread_escuta = threading.Thread(target=ouvir_continuamente)
        thread_escuta.daemon = True
        thread_escuta.start()

        while True:
            try:
                # Verifica se há algo na fila de entrada do usuário
                entrada = user_input_queue.get(timeout=1) # Espera 1 segundo
                
                if not is_active:
                    # Se não estiver ativo, verifica se a entrada contém uma palavra de ativação
                    if any(palavra in entrada for palavra in ACTIVATION_WORDS):
                        is_active = True
                        falar("Sim, estou ouvindo.")
                        last_interaction_time = time.time()
                        print("\n--- Modo de escuta contínua ATIVADO ---")
                else:
                    # Se já estiver ativo, processa qualquer entrada
                    if entrada.lower() == 'sair':
                        falar("Até logo!")
                        break
                    processar_e_responder(entrada, usuario, persona)

            except Exception: # A exceção aqui é Queue.Empty (timeout)
                # Se não houver entrada, verifica o timeout de inatividade
                if is_active and (time.time() - last_interaction_time > TIMEOUT_INATIVIDADE):
                    is_active = False
                    falar("Desativando por inatividade. Diga Lyria para me chamar novamente.")
                    print("\n--- Modo de escuta contínua DESATIVADO por inatividade ---")
    
    # --- Encerramento do programa ---
    tts_queue.put(None) # Sinaliza para a thread de TTS terminar
    thread_tts.join(timeout=2) # Espera a thread de TTS finalizar

    conn.close()
    print("Programa encerrado.")

if __name__ == "__main__":
    main()