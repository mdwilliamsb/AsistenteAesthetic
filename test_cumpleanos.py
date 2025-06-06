from db.models import crear_tablas
from db.utils import obtener_o_crear_paciente
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "db" / "aesthetic.db"
crear_tablas()

def felicitar_cumpleaños():
    hoy = datetime.now().strftime("%m-%d")  # Solo mes y día
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, telefono, fecha_nacimiento FROM pacientes WHERE fecha_nacimiento IS NOT NULL")
    pacientes = cursor.fetchall()
    conn.close()

    print("🎂 Cumpleañeros de hoy:
")
    for nombre, telefono, fecha in pacientes:
        if fecha and hoy == fecha[5:]:  # Comparar mes-día
            print(f"🎉 ¡Hoy es cumpleaños de {nombre}! (Tel: {telefono})")

felicitar_cumpleaños()
