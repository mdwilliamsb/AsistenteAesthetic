from fastapi import FastAPI
from webhook_asistente import router as webhook_router
from tareas_programadas import iniciar_scheduler

app = FastAPI(title="Asistente Aesthetic Center", version="1.0.0")

# Iniciar el scheduler con tareas automáticas al arrancar
iniciar_scheduler()

# Incluir el webhook del asistente
app.include_router(webhook_router)

@app.get("/", tags=["General"])
def home():
    return {
        "mensaje": "Asistente Aesthetic Center operativo. Webhook en /webhook. Tareas automáticas activas."
    }

# Para ejecución local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
