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

def pegarPersonaEscolhida(usuario):
    conn = sqlite3.connect(DB_NOME)
    cursor = conn.cursor()
    cursor.execute("SELECT persona_escolhida FROM usuarios WHERE nome = ?", (usuario,))
    result = cursor.fetchone()
    conn.close()
    return result

def escolherApersona(persona,usuario):
    conn = sqlite3.connect(DB_NOME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios SET persona_escolhida = ? WHERE nome = ?
    """, (persona, usuario))
        
    if cursor.rowcount == 0:
        cursor.execute("""
            INSERT INTO usuarios (nome, persona_escolhida) VALUES (?, ?)
        """, (usuario, persona))
        
    conn.commit()
    conn.close()

def criarUsuario(nome,email,persona):
    conn = sqlite3.connect(DB_NOME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nome, email, persona_escolhida) 
        VALUES (?, ?, ?)
    """, (nome, email, persona))
    conn.commit()
    conn.close()

def procurarUsuarioPorEmail(usuarioEmail):
    conn = sqlite3.connect(DB_NOME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (usuarioEmail,))
    result = cursor.fetchone()
    conn.close()
    return result

def pegarHistorico(usuario):
    conn = sqlite3.connect(DB_NOME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pergunta, resposta, timestamp 
        FROM mensagens 
        WHERE usuario = ? 
        ORDER BY id DESC 
        LIMIT 3
    """, (usuario,))
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    criar_banco()
