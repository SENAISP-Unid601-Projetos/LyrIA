import random
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# ==== 1. Função para carregar dados do arquivo CSV ====

def carregar_dados_csv(arquivo):
    perguntas = []
    rotulos = []
    
    # Lê os dados do arquivo CSV
    with open(arquivo, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignora o cabeçalho
        for row in reader:
            perguntas.append(row[0])
            rotulos.append(int(row[1]))
    
    return perguntas, rotulos

# Carregar os dados do arquivo CSV
perguntas, rotulos = carregar_dados_csv('dados.csv')

# Embaralhar para evitar viés
random.shuffle(list(zip(perguntas, rotulos)))

# === 2. Vetorização com TF-IDF ===
vetor = TfidfVectorizer()
X = vetor.fit_transform(perguntas)
y = rotulos

# === 3. Treinamento e avaliação ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = LogisticRegression()
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred))

# === 4. Salvar modelo e vetor ===
joblib.dump(modelo, "modelo_busca_web.pkl")
joblib.dump(vetor, "vetor_busca_web.pkl")

# === 5. Função de inferência ===
def deve_buscar_na_web(pergunta):
    modelo = joblib.load("modelo_busca_web.pkl")
    vetor = joblib.load("vetor_busca_web.pkl")
    entrada = vetor.transform([pergunta])
    return bool(modelo.predict(entrada)[0])

# === 6. Testar perguntas manualmente ===
if __name__ == "__main__":
    while True:
        entrada = input("Digite uma pergunta (ou 'sair'): ")
        if entrada.lower() in ['sair', 'exit', 'quit']:
            break
        if deve_buscar_na_web(entrada):
            print("🔎 Esta pergunta requer busca na web.")
        else:
            print("📚 Esta pergunta pode ser respondida localmente.")
