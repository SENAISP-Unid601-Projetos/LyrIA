import requests
import json

url = "http://localhost:5000/Lyria/conversar"

data = {
    "usuario": "maria",
    "pergunta": "Qual a capital do Brasil?",
    "persona": "Você é a professora Lyria, responda de forma didática e empática, tratando o usuário como um aluno."
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  
    
    print("Status da Requisição:", response.status_code)
    print("Resposta da API:", response.json())

except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro ao tentar se conectar à API: {e}")