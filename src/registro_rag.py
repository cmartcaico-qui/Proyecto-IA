import time
import json
from contextlib import contextmanager
from datetime import datetime, timezone

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from rag_indexer import cargar_vectorstore, formatear_contexto

load_dotenv()

PROMPT_TEMPLATE = """Responde la pregunta usando SOLO el contexto de abajo.
Cita la fuente de cada afirmación con su número entre corchetes, como [1].
Si el contexto no alcanza para responder, dilo explícitamente.

Contexto:
{contexto}

Pregunta:
{pregunta}

Respuesta:
"""

# Diccionario para almacenar los tiempos de ejecución
tiempos = {}

@contextmanager
def medir(etapa):
    """
    Mide cuánto demora en ejecutarse una etapa del RAG.
    """
    inicio = time.perf_counter()

    yield

    tiempos[etapa] = time.perf_counter() - inicio

def calcular_costo(tokens_entrada, tokens_salida,
                  tarifa_entrada_x1M, tarifa_salida_x1M):
    """
    Calcula el costo estimado de una consulta,
    utilizando las tarifas por millón de tokens.
    """

    costo_entrada = (tokens_entrada / 1_000_000) * tarifa_entrada_x1M
    costo_salida = (tokens_salida / 1_000_000) * tarifa_salida_x1M

    return costo_entrada + costo_salida

if __name__ == "__main__":
    CARPETA_DB = "vectorstore_ejemplo"
    K = 6

    # Cargar el vectorstore que ya tenemos
    vs = cargar_vectorstore(CARPETA_DB)

    #pregunta = "¿Cuántos reintentos realiza el cliente ante un fallo de conexión?"
    #pregunta = "¿Qué sucede cuando se supera el límite de peticiones por minuto?"
    pregunta = "¿Cuántos créditos consume una operación de escritura?"

    # Medir la recuperación de información
    with medir("embed_y_busqueda"):
        retriever = vs.as_retriever(search_kwargs={"k": K})
        chunks = retriever.invoke(pregunta)

    # Construir el prompt con los fragmentos recuperados
    with medir("armado_prompt"):
        contexto, citas = formatear_contexto(chunks)

        prompt = PROMPT_TEMPLATE.format(
            contexto=contexto,
            pregunta=pregunta
        )

    # Crear el modelo Gemini
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite"
    )

    # Medir cuánto demora Gemini en generar la respuesta
    with medir("generacion"):
        respuesta = chat_model.invoke(prompt)

    # Mostrar la respuesta generada
    print("\nRespuesta de Gemini:")
    print(respuesta.content)

    # Mostrar los tokens consumidos
    print("\nTokens utilizados:")
    print(respuesta.usage_metadata)

    # Mostrar los chunks recuperados
    print("\nChunks recuperados:")
    for chunk in chunks:
        print(chunk.page_content)

    # Mostrar cuánto demoró la recuperación
    print("\nTiempos registrados:")
    for etapa, segundos in tiempos.items():
        print(f"{etapa}: {segundos * 1000:.2f} ms")

    # Extraer solamente el texto de la respuesta
    if isinstance(respuesta.content, list):
        texto_respuesta = " ".join(
            bloque["text"]
            for bloque in respuesta.content
            if isinstance(bloque, dict) and bloque.get("type") == "text"
        )
    else:
        texto_respuesta = respuesta.content

    # Calcular el costo usando los tokens de esta consulta
    tokens = respuesta.usage_metadata

    costo_estimado = None

    if tokens:
        costo_estimado = calcular_costo(
            tokens_entrada=tokens["input_tokens"],
            tokens_salida=tokens["output_tokens"],
            tarifa_entrada_x1M=0.30,
            tarifa_salida_x1M=2.50
        )

    # Crear un registro de la consulta
    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pregunta": pregunta,
        "k": K,
        "respuesta": texto_respuesta,
        "tiempos_ms": {
            etapa: round(segundos * 1000, 2)
            for etapa, segundos in tiempos.items()
        },
        "tiempo_total_ms": round(sum(tiempos.values()) * 1000, 2),
        "tokens": respuesta.usage_metadata,
        "costo_estimado_usd_ejemplo": costo_estimado
    }

    # Guardar la consulta en formato JSONL
    with open("registros_latencia_costo.jsonl", "a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")

    print("\nRegistro guardado correctamente.")


    # Obtener tokens reales de la consulta
    tokens = respuesta.usage_metadata

    if tokens:
        costo = calcular_costo(
            tokens_entrada=tokens["input_tokens"],
            tokens_salida=tokens["output_tokens"],
            tarifa_entrada_x1M=0.30,
            tarifa_salida_x1M=2.50
        )

        print(f"\nCosto estimado de ejemplo: ${costo:.6f} USD")
