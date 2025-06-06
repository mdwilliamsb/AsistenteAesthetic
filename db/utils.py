import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "aesthetic.db"

def obtener_o_crear_paciente(telefono, nombre=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM pacientes WHERE telefono = ?", (telefono,))
    resultado = cursor.fetchone()

    if resultado:
        paciente_id = resultado[0]
    else:
        cursor.execute("INSERT INTO pacientes (telefono, nombre) VALUES (?, ?)", (telefono, nombre))
        paciente_id = cursor.lastrowid
        conn.commit()

    conn.close()
    return paciente_id

def guardar_cita(paciente_id, fecha, hora, especialista):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO citas (paciente_id, fecha, hora, especialista)
        VALUES (?, ?, ?, ?)
    """, (paciente_id, fecha, hora, especialista))

    conn.commit()
    conn.close()
