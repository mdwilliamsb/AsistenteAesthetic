from db.models import crear_tablas
from db.utils import obtener_citas_del_dia
from datetime import datetime, timedelta

crear_tablas()

def enviar_recordatorios():
    mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    citas = obtener_citas_del_dia(mañana)
    print(f"🔔 Recordatorios de cita para mañana ({mañana}):
")
    for cita in citas:
        print(f"Paciente ID {cita[1]} tiene cita con {cita[4]} a las {cita[3]}")

enviar_recordatorios()
