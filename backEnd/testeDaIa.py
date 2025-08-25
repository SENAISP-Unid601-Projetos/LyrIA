import requests
import sqlite3
import pyttsx3
import speech_recognition as sr
import os
from classificadorDaWeb.classificador_busca_web import deve_buscar_na_web
from banco.banco import (
    carregar_conversas, 
    salvarMensagem, 
    pegarPersonaEscolhida,
    escolherApersona,
    criarUsuario,
    criar_banco
)

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

def carregar_memorias(usuario):
    from banco.banco import carregar_memorias as carregar_memorias_db
    return carregar_memorias_db(usuario)

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
    LIMITE_HISTORICO_REDUZIDO = 6
    
    prompt_parts = [persona]
    
    if conversas:
        prompt_parts.append("Histórico recente:")
        for msg in conversas[-LIMITE_HISTORICO_REDUZIDO:]:
            prompt_parts.append(f"Usuário: {msg['pergunta']}")
            prompt_parts.append(f"Lyria: {msg['resposta']}")
    
    if contexto_web:
        contexto_limitado = contexto_web[:500]  
        prompt_parts.append(f"Info web atual: {contexto_limitado}")
    
    prompt_parts.append(f"Usuário: {pergunta}")
    prompt_parts.append("Lyria:")
    
    prompt = "\n".join(prompt_parts)
    
    payload = {
        'model': OLLAMA_MODEL,
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': 0.7,      
            'top_p': 0.9,           
            'num_predict': 200,     
            'stop': ['\n\nUsuário:', 'Usuário:']  
        }
    }
    
    try:
        print(f"Enviando para Ollama... (prompt: {len(prompt)} chars)")
        
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=60,  
            headers={'Content-Type': 'application/json'}
        )
        
        response.raise_for_status()
        data = response.json()
        
        resposta = data.get('response', '').strip()
        
        if not resposta:
            return "Desculpe, não consegui gerar uma resposta adequada."
        
        if resposta.startswith('Lyria:'):
            resposta = resposta[6:].strip()
            
        return resposta
        
    except requests.exceptions.Timeout:
        print("Timeout - Ollama demorou mais que 45s")
        return "Desculpe, estou processando mais devagar hoje. Pode repetir a pergunta?"
        
    except requests.exceptions.ConnectionError:
        print("Erro de conexão - Ollama pode estar offline")
        return "Não consegui me conectar ao sistema. Verifique se o Ollama está rodando."
        
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e.response.text}")
        return "Houve um problema no processamento. Tente novamente."
        
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return "Erro interno. Tente novamente em alguns instantes."

def verificar_ollama_status():
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            modelos = response.json().get('models', [])
            modelo_existe = any(m.get('name', '').startswith(OLLAMA_MODEL.split(':')[0]) for m in modelos)
            return {
                'status': 'online',
                'modelo_existe': modelo_existe,
                'modelos_disponiveis': [m.get('name') for m in modelos]
            }
        else:
            return {'status': 'erro', 'detalhes': f'HTTP {response.status_code}'}
            
    except requests.exceptions.ConnectionError:
        return {'status': 'offline', 'detalhes': 'Não foi possível conectar'}
    except Exception as e:
        return {'status': 'erro', 'detalhes': str(e)}

def buscar_na_web(pergunta):
    try:
        params = {"q": pergunta, "hl": "pt-br", "gl": "br", "api_key": SERPAPI_KEY}
        res = requests.get("https://serpapi.com/search", params=params, timeout=10)
        res.raise_for_status()
        
        resultados = res.json().get("organic_results", [])
        trechos = [r.get("snippet", "") for r in resultados[:2] if r.get("snippet")]
        return " ".join(trechos) if trechos else None
        
    except Exception as e:
        print(f"Erro na busca web: {e}")
        return None

def get_persona_texto(persona_tipo):
    personas = {
        'professor': "Você é a professora Lyria, responda de forma didática e empática. Ajude o usuário a aprender de forma clara e motivadora.",
        'empresarial': "Você é a assistente Lyria, responda de forma profissional e objetiva. Foque em soluções práticas e eficiência.",
        'social': "Você é a amiga Lyria, responda de forma empática, sempre tentando ajudar a pessoa de acordo com o seu contexto social"
    }
    return personas.get(persona_tipo, personas['professor'])

if __name__ == "__main__":
    criar_banco()
    
    print("Do que você precisa?")
    print("1. Professor")
    print("2. Empresarial")
    escolha = input("Escolha: ").strip()

    if escolha == '1':
        persona_tipo = 'professor'
    elif escolha == '2':
        persona_tipo = 'empresarial'
    else:
        print("Opção inválida")
        exit()

    print("\nModo de interação:")
    print("1. Apenas texto")
    print("2. Voz e texto")
    modo = input("Escolha: ").strip()

    usuario = input("Informe seu nome: ").strip().lower()
    
    try:
        criarUsuario(usuario, f"{usuario}@local.com", persona_tipo)
    except:
        escolherApersona(persona_tipo, usuario)
    
    persona = get_persona_texto(persona_tipo)

    if modo == '1':
        print("\nModo texto ativo (digite 'sair' para encerrar)")
        while True:
            entrada = input("Você: ").strip()
            if entrada.lower() == 'sair':
                break
                
            contexto_web = None
            if deve_buscar_na_web(entrada):
                contexto_web = buscar_na_web(entrada)
                
            resposta = perguntar_ollama(
                entrada, 
                carregar_conversas(usuario), 
                carregar_memorias(usuario), 
                persona,
                contexto_web
            )
            
            print(f"Lyria: {resposta}")
            salvarMensagem(usuario, entrada, resposta, modelo_usado="ollama", tokens=None)

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
                
            contexto_web = None
            if deve_buscar_na_web(entrada):
                contexto_web = buscar_na_web(entrada)
                
            resposta = perguntar_ollama(
                entrada,
                carregar_conversas(usuario),
                carregar_memorias(usuario), 
                persona, 
                contexto_web
            )
            
            print(f"Lyria: {resposta}")
            falar(resposta)
            salvarMensagem(usuario, entrada, resposta, modelo_usado="ollama", tokens=None)