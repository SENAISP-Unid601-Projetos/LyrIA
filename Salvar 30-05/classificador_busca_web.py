import random
import csv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# --- Constantes ---
MODELO_PATH = "modelo_busca_web.pkl"
VETOR_PATH = "vetor_busca_web.pkl"
DADOS_PATH = os.path.join('testando', 'dados.csv')

# --- Funções de Treinamento ---
def carregar_dados_csv(arquivo):
    """Carrega perguntas e rótulos de um arquivo CSV."""
    perguntas = []
    rotulos = []
    try:
        with open(arquivo, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                perguntas.append(row[0])
                rotulos.append(int(row[1]))
    except FileNotFoundError:
        print(f"Erro: Arquivo de dados '{arquivo}' não encontrado.")
        return None, None
    return perguntas, rotulos

def treinar_e_salvar_modelo():
    """Carrega os dados, treina o modelo e o salva no disco."""
    print("Iniciando treinamento do modelo de classificação...")
    perguntas, rotulos = carregar_dados_csv(DADOS_PATH)
    if perguntas is None:
        return

    # Embaralha os dados para garantir que o treino e teste sejam representativos
    dados_combinados = list(zip(perguntas, rotulos))
    random.shuffle(dados_combinados)
    perguntas, rotulos = zip(*dados_combinados)

    vetorizador = TfidfVectorizer()
    X = vetorizador.fit_transform(perguntas)
    y = list(rotulos)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    modelo = LogisticRegression()
    modelo.fit(X_train, y_train)

    # Avalia o modelo
    y_pred = modelo.predict(X_test)
    print("\n--- Relatório de Classificação do Treinamento ---")
    print(classification_report(y_test, y_pred))
    print("-------------------------------------------------")

    # Salva o modelo e o vetorizador
    joblib.dump(modelo, MODELO_PATH)
    joblib.dump(vetorizador, VETOR_PATH)
    print(f"Modelo salvo em '{MODELO_PATH}' e vetorizador em '{VETOR_PATH}'.")

# --- Carregamento do Modelo (Executado apenas uma vez na importação) ---
try:
    modelo_classificador = joblib.load(MODELO_PATH)
    vetorizador_tfidf = joblib.load(VETOR_PATH)
    print("Modelo de classificação carregado com sucesso.")
except FileNotFoundError:
    print("Arquivos de modelo não encontrados. Execute este script diretamente para treiná-los.")
    modelo_classificador = None
    vetorizador_tfidf = None

# --- Função Principal de Predição ---
def deve_buscar_na_web(pergunta: str) -> bool:
    """
    Verifica se uma pergunta deve acionar uma busca na web.
    Carrega o modelo do disco se ele ainda não estiver na memória.
    """
    if not modelo_classificador or not vetorizador_tfidf:
        print("Aviso: Modelo de classificação não está carregado. Retornando False.")
        return False
    
    entrada_vetorizada = vetorizador_tfidf.transform([pergunta])
    predicao = modelo_classificador.predict(entrada_vetorizada)
    return bool(predicao[0])

# --- Bloco de Execução Principal (para treinar o modelo) ---
if __name__ == "__main__":
    print("Este script pode ser usado para treinar o modelo de classificação.")
    print("1. Treinar o modelo")
    print("2. Testar o modelo interativamente")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        treinar_e_salvar_modelo()
    elif escolha == '2':
        if not modelo_classificador:
            print("Você precisa treinar o modelo primeiro (opção 1).")
        else:
            print("\n--- Teste Interativo (digite 'sair' para encerrar) ---")
            while True:
                entrada = input("Digite uma pergunta: ")
                if entrada.lower() in ['sair', 'exit', 'quit']:
                    break
                if deve_buscar_na_web(entrada):
                    print("🔎 Esta pergunta requer busca na web.")
                else:
                    print("📚 Esta pergunta pode ser respondida localmente.")
    else:
        print("Opção inválida.")