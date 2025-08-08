import sqlite3

DB_NOME = "lyria.db"

def criar_banco():
    conn = sqlite3.connect(DB_NOME)
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        nome TEXT PRIMARY KEY
    );
    """)

    # Tabela de mensagens da conversa
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        pergunta TEXT,
        resposta TEXT,
        FOREIGN KEY(usuario) REFERENCES usuarios(nome)
    );
    """)

    # Tabela de memórias (informações importantes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        texto TEXT,
        FOREIGN KEY(usuario) REFERENCES usuarios(nome)
    );
    """)

    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_banco()
