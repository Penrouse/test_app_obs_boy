import os
import psycopg2
import anthropic
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

DB_URL     = os.getenv("SUPABASE_DB_URL")
CLAUDE_KEY = os.getenv("ANTHROPIC_API_KEY")

_model  = None
_client = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=CLAUDE_KEY)
    return _client


def buscar_chunks(pregunta: str, top_k: int = 25, dimension: str = None) -> list[dict]:
    embedding = get_model().encode(pregunta).tolist()
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

    if dimension:
        query = """
            SELECT texto, anio, actividad, sector, tipo_precio, valor, fuente,
                   1 - (embedding <=> %s::vector) AS similitud
            FROM indicadores
            WHERE dimension = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        params = [embedding_str, dimension, embedding_str, top_k]
    else:
        query = """
            SELECT texto, anio, actividad, sector, tipo_precio, valor, fuente,
                   1 - (embedding <=> %s::vector) AS similitud
            FROM indicadores
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        params = [embedding_str, embedding_str, top_k]

    conn = psycopg2.connect(DB_URL)
    cur  = conn.cursor()
    cur.execute("SET ivfflat.probes = 5;")
    cur.execute(query, params)
    filas = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "texto":       f[0],
            "anio":        f[1],
            "actividad":   f[2],
            "sector":      f[3],
            "tipo_precio": f[4],
            "valor":       f[5],
            "fuente":      f[6],
            "similitud":   round(float(f[7]), 3),
        }
        for f in filas
    ]


def construir_prompt(pregunta: str, chunks: list[dict]) -> str:
    contexto = "\n\n".join(
        f"[{i+1}] {c['texto']}" for i, c in enumerate(chunks)
    )
    return f"""Eres un asistente especializado en indicadores económicos del departamento de Boyacá, Colombia.
Responde ÚNICAMENTE con base en el contexto provisto. Si la información no está en el contexto, dilo claramente.
Siempre menciona el año y la fuente al citar un dato. Responde en español.

INSTRUCCIONES ADICIONALES:
- Los datos están desagregados por actividad económica. Si preguntan por el total, suma los valores disponibles y aclara que es una suma parcial de las actividades en el contexto.
- Si hay datos de varios años, puedes calcular el crecimiento porcentual entre ellos.
- Sé concreto con los números: menciona valores en miles de millones de pesos.

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:"""


def responder(pregunta: str, dimension: str = None) -> dict:
    chunks = buscar_chunks(pregunta, top_k=6, dimension=dimension)

    if not chunks:
        return {
            "respuesta": "No encontré información relacionada en la base de datos.",
            "fuentes": [],
        }

    prompt  = construir_prompt(pregunta, chunks)
    mensaje = get_client().messages.create(
        model      = "claude-haiku-4-5",
        max_tokens = 1024,
        messages   = [{"role": "user", "content": prompt}],
    )

    return {
        "respuesta": mensaje.content[0].text,
        "fuentes":   chunks,
    }


if __name__ == "__main__":
    pregunta = "¿Cuál fue el PIB de Boyacá en 2023 y cuánto creció respecto a 2022?"
    print(f"\nPregunta: {pregunta}\n")
    resultado = responder(pregunta)
    print("Respuesta:")
    print(resultado["respuesta"])
    print("\nFuentes utilizadas:")
    for f in resultado["fuentes"][:3]:
        print(f"  - {f['texto'][:100]}... (similitud: {f['similitud']})")