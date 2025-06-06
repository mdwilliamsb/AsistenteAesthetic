from models import SessionLocal, Paciente, Conversacion
from sqlalchemy.orm import joinedload
import datetime

# Obtener o crear paciente
def obtener_o_crear_paciente(wa_id, nombre=None):
    db = SessionLocal()
    paciente = db.query(Paciente).filter(Paciente.telefono == wa_id).first()
    if not paciente:
        paciente = Paciente(telefono=wa_id, nombre=nombre or "Desconocido", historial="")
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
    db.close()
    return paciente

# Guardar conversación
def guardar_conversacion(wa_id, mensaje, respuesta):
    db = SessionLocal()
    paciente = db.query(Paciente).filter(Paciente.telefono == wa_id).first()
    if not paciente:
        paciente = obtener_o_crear_paciente(wa_id)
        paciente = db.query(Paciente).filter(Paciente.telefono == wa_id).first()
    conversacion = Conversacion(
        paciente_id=paciente.id,
        mensaje=mensaje,
        respuesta=respuesta,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(conversacion)
    db.commit()
    db.close()

# Obtener historial para GPT
def obtener_historial(wa_id, limite=5):
    db = SessionLocal()
    paciente = db.query(Paciente)        .options(joinedload(Paciente.conversaciones))        .filter(Paciente.telefono == wa_id).first()
    if not paciente or not paciente.conversaciones:
        db.close()
        return ""
    conversaciones = sorted(paciente.conversaciones, key=lambda x: x.timestamp)[-limite:]
    historial = ""
    for conv in conversaciones:
        historial += f"Paciente: {conv.mensaje}\n"
        historial += f"Asistente: {conv.respuesta}\n"
    db.close()
    return historial.strip()
