from transformers import pipeline
import torch
from pathlib import Path
import json
import re
import random

class LyrIA:
    def __init__(self):
        self.model = pipeline(
            "text-generation",
            model="pierreguillou/gpt2-small-portuguese",
            device=0 if torch.cuda.is_available() else -1
        )
        self.carregar_dialogos(Path(__file__).parent.parent / "data/dialogs.json")
        self.palavras_proibidas = ["gato", "gatos", "exemplo", "etc"]

    def carregar_dialogos(self, arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            self.dialogs = json.load(f)

    def responder(self, pergunta):
        pergunta = pergunta.lower()
        
        # Verifica palavras-chave primeiro
        for palavra, tipo_resposta in self.dialogs["palavras_chave"].items():
            if palavra in pergunta:
                return random.choice(self.dialogs[tipo_resposta])
        
        # Geração com IA com prompt melhorado
        prompt = f"""
        [Contexto: Você é a LyrIA, uma assistente virtual educada e útil]
        Usuário: {pergunta}
        LyrIA:"""
        
        resposta = self.model(
            prompt,
            max_length=60,
            temperature=0.5,
            num_beams=2,
            no_repeat_ngram_size=2,
            do_sample=False
        )[0]['generated_text']
        
        # Extrai e filtra a resposta
        resposta = resposta.split("LyrIA:")[1].strip()
        return self.filtrar_resposta(resposta)

    def filtrar_resposta(self, texto):
        """Remove respostas sem sentido e adiciona identidade"""
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        if any(palavra in texto.lower() for palavra in self.palavras_proibidas):
            return self.dialogs["padrao"]
            
        if not texto.endswith(('- LyrIA', '!')):
            texto += " - LyrIA"
            
        return texto.capitalize()