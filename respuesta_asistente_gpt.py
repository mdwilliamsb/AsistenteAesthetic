import logging
from openai import OpenAI
from asistente_contexto import cargar_contexto_asistente

gpt = OpenAI()

def generar_respuesta_asistente(mensaje_usuario: str) -> str:
    try:
        contexto = cargar_contexto_asistente()

        # Armar contexto humanizado
        resumen_equipo = "\n".join([
            f"- {p['nombre']}: {p['especialidad']}" 
            for p in contexto['equipo'] if p.get('disponible', True)
        ])

        resumen_servicios = contexto['faq'].get("¿Qué servicios ofrecen?", "")
        info_extra = "Este bot actúa como asistente humano, no da diagnósticos, y sugiere agendar cuando es necesario."

        prompt = (
            f"Eres la asistente virtual de Aesthetic Center. Tu tono es humano, profesional y cálido.
"
            f"Puedes redirigir con amabilidad según el caso y responder preguntas comunes.

"
            f"Profesionales disponibles:
{resumen_equipo}

"
            f"Servicios destacados:
{resumen_servicios}

"
            f"{info_extra}

"
            f"Mensaje del paciente:
"{mensaje_usuario}""
        )

        respuesta = gpt.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Actúas como una asistente humana en WhatsApp para una clínica estética y médica. "
                        "Respondes preguntas frecuentes con empatía, rediriges según la especialidad y nunca das diagnósticos. "
                        "Si se trata de una sucursal con personal rotativo, indicas que se puede agendar y se confirmará con quién será atendido."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        return respuesta.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"❌ Error generando respuesta GPT: {e}")
        return "Lo siento, hubo un error. ¿Podrías intentarlo más tarde?"
