import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "editais.db"

def criar_tabela_flexivel():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS editais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            arquivo_pdf TEXT,
            prompt TEXT,
            conteudo_json TEXT,
            data_processamento TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def salvar_json_flexivel(json_data: dict, arquivo_pdf: str, prompt: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO editais (arquivo_pdf, prompt, conteudo_json)
        VALUES (?, ?, ?)
    """, (
        arquivo_pdf,
        prompt,
        json.dumps(json_data, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()


import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "editais.db"

def listar_editais():
    """
    Retorna todos os editais do banco como lista de dicts.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, arquivo_pdf, prompt, conteudo_json, data_processamento FROM editais ORDER BY data_processamento DESC")
    rows = c.fetchall()
    conn.close()

    editais = []
    for row in rows:
        id_, arquivo_pdf, prompt, conteudo_json, data_processamento = row
        try:
            conteudo = json.loads(conteudo_json)
        except json.JSONDecodeError:
            conteudo = {}  # caso o JSON esteja mal formatado
        editais.append({
            "id": id_,
            "arquivo_pdf": arquivo_pdf,
            "prompt": prompt,
            "conteudo_json": conteudo,
            "data_processamento": data_processamento
        })

    return editais

