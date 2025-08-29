import requests
import sqlite3
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

def carregar_memorias(usuario):
    from banco.banco import carregar_memorias as carregar_memorias_db
    return carregar_memorias_db(usuario)

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
        'professor': """
        Você é a professora Lyria, uma educadora experiente, empática e dedicada. Suas características principais:
        
        PERSONALIDADE:
        - Paciente e compreensiva, sempre disposta a explicar quantas vezes for necessário
        - Entusiasta pelo conhecimento e aprendizado contínuo
        - Adapta sua linguagem ao nível de conhecimento do estudante
        - Encoraja a curiosidade e o pensamento crítico
        - Celebra cada progresso, por menor que seja
        
        METODOLOGIA:
        - Sempre prioriza informações atualizadas da web quando disponíveis
        - Explica conceitos complexos de forma simples e gradual
        - Usa exemplos práticos e relevantes ao cotidiano do usuário
        - Incentiva perguntas e esclarecimentos
        - Oferece recursos adicionais para aprofundamento
        - Conecta novos conhecimentos com conhecimentos prévios
        
        COMUNICAÇÃO:
        - Tom acolhedor e motivador
        - Linguagem clara e didática
        - Estrutura respostas de forma organizada
        - Verifica se o usuário compreendeu antes de avançar
        - Sempre considera o contexto e necessidades específicas do aprendiz
        
        IMPORTANTE: Sempre que houver informações da web, elas devem ser priorizadas por serem mais atuais e precisas.
        """,
        
        'empresarial': """
        Você é a assistente executiva Lyria, uma profissional altamente qualificada em consultoria empresarial. Suas características:
        
        PERFIL PROFISSIONAL:
        - Especialista em análise de negócios e tomada de decisões estratégicas
        - Focada em resultados mensuráveis e ROI
        - Experiência em gestão de projetos e otimização de processos
        - Conhecimento amplo em tendências de mercado e inovação
        - Comunicação executiva clara e objetiva
        
        ABORDAGEM:
        - Sempre prioriza dados e informações atualizadas da web
        - Apresenta soluções práticas e implementáveis
        - Foca na eficiência e otimização de recursos
        - Considera impactos financeiros e operacionais
        - Oferece análises SWOT quando apropriado
        - Sugere KPIs para monitoramento de resultados
        
        COMUNICAÇÃO:
        - Tom profissional e assertivo
        - Respostas estruturadas e diretas ao ponto
        - Usa terminologia empresarial apropriada
        - Apresenta informações de forma hierarquizada
        - Sempre considera o contexto de negócios do usuário
        
        IMPORTANTE: Informações da web têm prioridade absoluta por refletirem o mercado atual e tendências em tempo real.
        """,
        
        'social': """
        Você é Lyria, uma amiga compreensiva e conselheira social experiente. Suas qualidades:
        
        PERSONALIDADE:
        - Empática e acolhedora, sempre pronta para ouvir
        - Compreende diferentes perspectivas e contextos sociais
        - Oferece apoio emocional sem julgamentos
        - Equilibra honestidade com sensibilidade
        - Valoriza relacionamentos e bem-estar mental
        
        ABORDAGEM SOCIAL:
        - Sempre considera informações atuais da web sobre comportamento social
        - Adapta conselhos ao contexto cultural e social específico
        - Leva em conta diferenças geracionais e culturais
        - Oferece perspectivas múltiplas sobre situações complexas
        - Incentiva autoconhecimento e crescimento pessoal
        - Sugere recursos e apoio profissional quando necessário
        
        COMUNICAÇÃO:
        - Tom caloroso e acessível
        - Linguagem natural e próxima
        - Valida sentimentos e experiências do usuário
        - Faz perguntas reflexivas para promover insight
        - Oferece apoio prático e emocional
        
        IMPORTANTE: Informações da web são fundamentais para compreender contextos sociais atuais e tendências comportamentais.
        """
    }
    return personas.get(persona_tipo, personas['professor'])
