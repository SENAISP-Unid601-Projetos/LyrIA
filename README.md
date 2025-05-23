# Sistema de Voz e Áudio para Assistente Virtual em Python

## Visão Geral

Este documento explica como implementar um sistema completo de reconhecimento e síntese de voz para um assistente virtual em Python, utilizando bibliotecas simples e eficientes.

## Dependências Necessárias

### Bibliotecas Python

Instale as seguintes bibliotecas via pip:

```bash
pip install speechrecognition pyttsx3 pyaudio
```

Caso encontre problemas ao instalar o PyAudio no Windows, utilize:

```bash
pip install pipwin
pipwin install pyaudio
```

## Componentes do Sistema

### 1. Reconhecimento de Voz (Entrada)

Responsável por capturar áudio do microfone e converter para texto.

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

def ouvir_microfone():
    """Captura áudio do microfone e converte para texto"""
    with sr.Microphone() as source:
        print("🎤 Fale agora...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
    
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {texto}")
        return texto
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
        return None
    except Exception as e:
        print(f"Erro no reconhecimento: {e}")
        return None
```

### 2. Síntese de Voz (Saída)

Responsável por converter texto em fala e reproduzir pelo alto-falante.

```python
import pyttsx3

engine = pyttsx3.init()

def configurar_voz():
    """Configura propriedades da voz sintetizada"""
    # Configurações padrão
    engine.setProperty('rate', 180)  # Velocidade da fala (120-200)
    engine.setProperty('volume', 1.0)  # Volume máximo (0.0 a 1.0)
    
    # Seleciona voz em português se disponível
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'pt' in voice.languages or 'portuguese' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    return engine

def falar(texto):
    """Sintetiza e reproduz o texto em voz alta"""
    print(f"Assistente: {texto}")
    engine.say(texto)
    engine.runAndWait()
```

## Implementação Completa

```python
import speech_recognition as sr
import pyttsx3
import time

class AssistenteVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self._configurar_voz()
        self.interromper_fala = False
    
    def _configurar_voz(self):
        """Configura propriedades da voz"""
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1.0)
        
        # Seleciona voz em português
        for voice in self.engine.getProperty('voices'):
            if 'pt' in voice.languages or 'portuguese' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def ouvir(self):
        """Ouve o microfone e retorna texto reconhecido"""
        with sr.Microphone() as source:
            print("\n🎤 Fale agora (diga 'parar' para interromper)...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                texto = self.recognizer.recognize_google(audio, language='pt-BR')
                
                if 'parar' in texto.lower():
                    self.interromper_fala = True
                    return None
                    
                print(f"Você disse: {texto}")
                return texto
            except sr.WaitTimeoutError:
                return None
            except Exception as e:
                print(f"Erro: {e}")
                return None
    
    def falar(self, texto):
        """Fala o texto com possibilidade de interrupção"""
        self.interromper_fala = False
        
        # Divide texto longo em partes
        partes = [texto[i:i+200] for i in range(0, len(texto), 200)]
        
        for parte in partes:
            if self.interromper_fala:
                print("(Fala interrompida)")
                return
                
            print(f"Assistente: {parte}")
            self.engine.say(parte)
            self.engine.runAndWait()
            time.sleep(0.1)

    def iniciar(self):
        """Loop principal do assistente"""
        print("Assistente ativado. Diga 'sair' para encerrar.")
        
        while True:
            comando = self.ouvir()
            
            if comando:
                if "sair" in comando.lower():
                    self.falar("Até logo!")
                    break
                
                resposta = f"Você disse: {comando}"
                self.falar(resposta)

if __name__ == "__main__":
    assistente = AssistenteVoz()
    assistente.iniciar()
```

## Funcionalidades Principais

1. **Reconhecimento de Voz**:
   - Captura áudio do microfone
   - Converte fala em texto usando a API do Google
   - Suporte ao idioma português do Brasil
   - Filtro de ruído ambiente

2. **Síntese de Voz**:
   - Conversão de texto para fala offline
   - Ajuste de velocidade e volume
   - Suporte a interrupção durante a fala
   - Divisão automática de textos longos

3. **Controles por Voz**:
   - Comando "parar" para interromper a fala atual
   - Comando "sair" para encerrar o programa

## Configuração Recomendada

1. **Microfone**:
   - Use um microfone de boa qualidade
   - Evite ambientes muito ruidosos

2. **Alto-falantes**:
   - Configure o volume do sistema adequadamente
   - Teste a qualidade da saída de áudio

3. **Otimizações**:
   - Ajuste `recognizer.adjust_for_ambient_noise()` conforme o ambiente
   - Modifique `engine.setProperty('rate')` para velocidade preferida

## Possíveis Erros e Soluções

1. **Microfone não detectado**:
   - Verifique as configurações de áudio do Windows
   - Conecte o microfone antes de iniciar o programa

2. **Voz em inglês**:
   - Instale pacotes de voz em português no Windows
   - Verifique se há vozes em português disponíveis:
     ```python
     print(engine.getProperty('voices'))
     ```

3. **Erros de instalação**:
   - Para problemas com PyAudio, use:
     ```bash
     pip install pipwin
     pipwin install pyaudio
     ```

Este sistema fornece uma base completa para implementação de assistentes virtuais com controle por voz em Python, podendo ser facilmente integrado a outras funcionalidades.
