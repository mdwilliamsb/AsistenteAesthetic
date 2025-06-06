import logging
from openai import OpenAI
from asistente_contexto import cargar_contexto_asistente
from db import obtener_historial, guardar_conversacion

gpt = OpenAI()

def generar_resumen_equipo(contexto):
    try:
        return "\n".join([
            f"- {p['nombre']}: {p['especialidad']}"
            for p in contexto['equipo'] if p.get('disponible', True)
        ])
    except Exception as e:
        logging.error(f"❌ Error generando resumen del equipo: {e}")
        return ""

def generar_prompt_asistente(contexto, mensaje_usuario, historial=""):
    try:
        resumen_equipo = generar_resumen_equipo(contexto)
        resumen_servicios = contexto['faq'].get("¿Qué servicios ofrecen?", "")
        info_extra = (
            "Este bot actúa como una asistente humana, no da diagnósticos, "
            "y sugiere agendar con la persona adecuada según el caso. "
            "Siempre responde con amabilidad, empatía y profesionalismo."
        )

        prompt = (
            f"Eres la asistente virtual de Aesthetic Center. Tu tono es humano, profesional y cálido.\n\n"
            f"{historial}\n\n"
            f"Profesionales disponibles:\n{resumen_equipo}\n\n"
            f"Servicios destacados:\n{resumen_servicios}\n\n"
            f"{info_extra}\n\n"
            f"Mensaje del paciente:\n\"{mensaje_usuario}\""
        )

        return prompt
    except Exception as e:
        logging.error(f"❌ Error generando prompt: {e}")
        return f"Mensaje del paciente: {mensaje_usuario}"

def generar_respuesta_asistente(mensaje_usuario: str, wa_id: str) -> str:
    try:
        contexto = cargar_contexto_asistente()
        historial = obtener_historial(wa_id)
        prompt = generar_prompt_asistente(contexto, mensaje_usuario, historial)

        respuesta = gpt.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres una asistente virtual especializada en atención al cliente de una clínica estética. "
                        "No das diagnósticos médicos, pero sabes orientar sobre servicios, especialistas y horarios. "
                        "Siempre respondes de forma clara, profesional y empática."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        texto_respuesta = respuesta.choices[0].message.content.strip()
        guardar_conversacion(wa_id, mensaje_usuario, texto_respuesta)
        return texto_respuesta

    except Exception as e:
        logging.error(f"❌ Error generando respuesta con GPT: {e}")
        return "Lo siento, hubo un problema al generar la respuesta. Intenta nuevamente más tarde."
