import requests
import json

url = "http://localhost:5000/Lyria/conversar"

testes = [
    {
        "usuario": "maria",
        "pergunta": "Qual a capital do Brasil?",
        "persona": "Você é a professora Lyria, responda de forma didática e empática."
    },
    {
        "usuario": "joao",
        "pergunta": "Quem descobriu o Brasil?",
        "persona": "Você é a professora Lyria, responda de forma didática e empática."
    },
    {
        "usuario": "maria",
        "pergunta": "Explique a teoria da relatividade de forma simples.",
        "persona": "Você é a professora Lyria, responda de forma didática e empática."
    },
    {
        "usuario": "maria",
        "pergunta": ""
    }
]

for teste in testes:
    try:
        response = requests.post(url, json=teste)
        response.raise_for_status()
        print("Status:", response.status_code)
        print("Resposta:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à API: {e}")
