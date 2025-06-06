from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)

DB_PATH = Path(__file__).resolve().parent / "db" / "aesthetic.db"

def felicitar_cumpleaños():
    hoy = datetime.now().strftime("%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, telefono, fecha_nacimiento FROM pacientes WHERE fecha_nacimiento IS NOT NULL")
    pacientes = cursor.fetchall()
    conn.close()

    for nombre, telefono, fecha in pacientes:
        if fecha and hoy == fecha[5:]:
            logging.info(f"🎂 Felicitación automática: ¡Hoy es cumpleaños de {nombre}! Tel: {telefono}")
            # Aquí puedes integrar una función enviar_respuesta(telefono, mensaje)

def recordar_citas():
    mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT citas.*, pacientes.telefono, pacientes.nombre FROM citas JOIN pacientes ON citas.paciente_id = pacientes.id WHERE fecha = ?", (mañana,))
    citas = cursor.fetchall()
    conn.close()

    for cita in citas:
        telefono = cita[-2]
        nombre = cita[-1]
        hora = cita[3]
        especialista = cita[4]
        mensaje = f"Hola {nombre}, te recordamos tu cita mañana a las {hora} con {especialista} en Aesthetic Center. ¡Te esperamos!"
        logging.info(f"📅 Recordatorio enviado a {nombre} ({telefono}) - {hora} con {especialista}")
        # enviar_respuesta(telefono, mensaje)  # <- debes integrar esta función

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(felicitar_cumpleaños, 'cron', hour=7, minute=0)
    scheduler.add_job(recordar_citas, 'cron', hour=7, minute=10)
    scheduler.start()
    logging.info("⏰ Scheduler iniciado con tareas programadas.")

# Para pruebas locales
if __name__ == "__main__":
    iniciar_scheduler()
    try:
        while True:
            pass  # Mantener la app corriendo
    except (KeyboardInterrupt, SystemExit):
        logging.info("⏹ Scheduler detenido.")
