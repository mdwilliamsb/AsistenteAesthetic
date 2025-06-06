import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "aesthetic.db"

def crear_tablas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT UNIQUE,
            fecha_nacimiento TEXT,
            historial TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha TEXT,
            hora TEXT,
            especialista TEXT,
            confirmada BOOLEAN DEFAULT 0,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    ''')

    conn.commit()
    conn.close()
