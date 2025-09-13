import os
from dotenv import load_dotenv, find_dotenv
import json
import psycopg2
from datetime import datetime
from groq import Groq

from variables import config

load_dotenv(find_dotenv())

def bbdd(p_tema,edad_invitados,numero_invitados,presupuesto,lugar,r_tema,r_musica,r_decoracion,r_juegos,r_comida,r_bebidas):

    conn = psycopg2.connect(**config)
    cursor= conn.cursor()

    query = """INSERT INTO preguntas_respuestas (p_tema, edad_invitados, numero_invitados, presupuesto, lugar, fecha,
            r_tema, r_musica, r_decoracion, r_juegos, r_comida, r_bebidas) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    cursor.execute(query,(p_tema, edad_invitados, numero_invitados, presupuesto, lugar, datetime.now(),
        r_tema, r_musica, r_decoracion, r_juegos, r_comida, r_bebidas))
    
    conn.commit()
    cursor.close()
    conn.close()

    return "ok"


def llm(p_tema,edad_invitados,numero_invitados,presupuesto,lugar):
    
    client = Groq(
        api_key=os.environ.get("KEY_GROQ"),
    )

    system_prompt = """
            Eres un organizador de fiestas temáticas. 
            Tu misión es crear planes completos de fiestas adaptados a la temática, la edad de los invitados y el número de personas.

            Reglas:
            - SOLO puedes responder sobre fiestas, celebraciones y organización de eventos. Responde en castellano de España.
            - Si el usuario pregunta por otro tema, responde:
            "Solo puedo ayudarte a organizar fiestas temáticas. ¿Quieres que te sugiera ideas para una celebración?"
            - LÍMITE: máximo 4 elementos en cada lista y solo strings (sin descripciones largas).
            - Debes devolver SIEMPRE un JSON válido con esta estructura:

            {
            "música": ["string", "..."],
            "decoración": ["string", "..."],
            "juegos": ["string", "..."],
            "comida": ["string", "..."],
            "bebidas": ["string", "..."]
            }

            Detalles:
            - Ajusta la música, juegos y decoración a la temática. Se riguroso con la música y las actividades sugeridas que sean de la temática.
            - La comida y las bebidas deben ser adecuadas a la edad de los invitados. Si es de adultos, sugiere 1 coctel. Si es de niños o adolescentes, nada de alcholo
            - Escala las sugerencias según el número de invitados (ej. cantidad de comida o tipo de juegos).
            - Responde SOLO con json (sin texto fuera del json)


            Ejemplo de salida:
                    {
            "tema": "Años 80",
            "música": [ "Queen", "Glam Metal", "Madonna"
            ],
            "decoración": [
                "Globos de neón",
                "Carteles retro ochenteros"
            ],
            "juegos": [
                "Concurso de baile estilo ochentero",
                "Trivia musical de los 80"
            ],
            "comida": [
                "Mini hamburguesas",
                "Palomitas de colores"
            ],
            "bebidas": [
                "Cóctel Blue Lagoon",
                "Refrescos clásicos (Coca-Cola en botellas de vidrio)"
            ]
            }
        """
    
    user_prompt = f"""
        Temática: {p_tema}
        Edad de invitados: {edad_invitados}
        Número de invitados: {numero_invitados}
        Presupuesto: {presupuesto}
        Lugar: {lugar}
        """.strip()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role":"user",
                "content": user_prompt
            }
        ],
        model="openai/gpt-oss-20b",
        max_tokens=1500,
        temperature=0.2,
        response_format={"type": "json_object"},
        stream=False,
    )

    text = chat_completion.choices[0].message.content
    data = json.loads(text)
    return data