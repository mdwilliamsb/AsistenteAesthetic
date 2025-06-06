from respuesta_asistente_gpt import generar_respuesta_asistente

print("🧪 Simulador del Asistente Aesthetic Center")
print("Escribe un mensaje como si fueras un paciente (o 'salir' para terminar):")

while True:
    mensaje = input("\nPaciente: ")
    if mensaje.lower() in ["salir", "exit"]:
        print("👋 Finalizando simulador.")
        break
    respuesta = generar_respuesta_asistente(mensaje)
    print(f"Asistente: {respuesta}\n")
