import json
from pathlib import Path

def cargar_contexto_asistente():
    json_path = Path(__file__).resolve().parent / "contexto_asistente.json"
    with open(json_path, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return datos
