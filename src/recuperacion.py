
from pathlib import Path
from dotenv import load_dotenv
from rag_indexer import cargar_vectorstore, formatear_contexto
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

CARPETA_DB = Path(__file__).resolve().parent / "vectorstore_manual_b26"

PROMPT_TEMPLATE = """
Eres un asistente de consulta documental.

Responde la pregunta usando SOLO el contexto proporcionado.

Instrucciones:
- No inventes información.
- Cita la fuente de cada afirmación con [1], [2], etc.
- Si el contexto no permite responder, indícalo expresamente.
- Responde de forma clara y precisa.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:
"""


def construir_prompt(pregunta, persist_directory, k=3):
    
    vectorstore = cargar_vectorstore(str(persist_directory))

    # Verificar que existen documentos
    total = vectorstore._collection.count()
    if total == 0:
        raise ValueError("La colección no contiene documentos indexados.")

    # Crear el recuperador semántico
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )

    # Recuperar los chunks relevantes
    chunks_recuperados = retriever.invoke(pregunta)

    # Preparar el contexto y sus fuentes
    contexto, citas = formatear_contexto(chunks_recuperados)

    # Construir el prompt dinámico
    prompt = PROMPT_TEMPLATE.format(
        contexto=contexto,
        pregunta=pregunta
    )

    return prompt, citas


if __name__ == "__main__":
    #pregunta = "¿Qué sucede cuando las credenciales de API son inválidas?"
    #pregunta = "¿Cuántos reintentos realiza el cliente cuando falla la conexión?"
    #pregunta = "¿Cuál es el horario de atención de la tienda los domingos?"
    pregunta = "¿Qué errores HTTP no activan reintentos automáticos?"
    prompt, citas = construir_prompt(
        pregunta=pregunta,
        persist_directory=CARPETA_DB,
        k=3
    )

    print("\n--- PROMPT GENERADO ---")
    print(prompt)

    print("\n--- FUENTES RECUPERADAS ---")
    print(citas)

        # Enviar el prompt construido a Gemini
    modelo = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0
    )

    respuesta = modelo.invoke(prompt)

    print("\n--- RESPUESTA DE GEMINI ---")
    print(respuesta.text)