import sqlite3

DB_NOME = "lyria.db"

def criar_banco():
    conn = sqlite3.connect(DB_NOME)
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha_hash TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ultimo_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabela de conversas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        mensagens TEXT NOT NULL,
        iniciado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    );
    """)

    # Tabela de user_requests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        conversa_id INTEGER NOT NULL,
        conteudo TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY(conversa_id) REFERENCES conversas(id)
    );
    """)

    # Tabela de ai_responses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER NOT NULL,
        conteudo TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modelo_usado TEXT,
        tokens INTEGER,
        FOREIGN KEY(request_id) REFERENCES user_requests(id)
    );    
    """)

    # Tabela de mensagens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversa_id INTEGER NOT NULL,
        request_id INTEGER NOT NULL,
        response_id INTEGER NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(conversa_id) REFERENCES conversas(id),
        FOREIGN KEY(request_id) REFERENCES user_requests(id),
        FOREIGN KEY(response_id) REFERENCES ai_responses(id)
    );
    """)

    # Tabela de memórias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        chave TEXT NOT NULL,
        valor TEXT NOT NULL,
        tipo TEXT,
        relevancia INTEGER DEFAULT 0,
        conversa_origem INTEGER,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expira_em TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
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
