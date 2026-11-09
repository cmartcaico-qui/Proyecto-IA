from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI #Modelo
from langchain_core.prompts import PromptTemplate #Plantilla -> Prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Parsea la respuesta y la transforma en solo textos
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda) #Bifurcaciones/Branches/Ramificaciones/crear una función lambda ejecutable

import logging #Generar un archivo de log con los errores que se presenten

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", #2026-06-20 12:34:56 [WARNING] main: No se pudo ejecutar x    
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="error.log", #Archivo donde se guardarán los errores
    filemode="a",  # Append mode, para no sobrescribir el archivo de log cada vez que se ejecuta el script
    encoding="utf-8",
    force=True
    )

logger = logging.getLogger(__name__)

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra: "
    "pregunta, queja o sugerencia. Responde solo con esa palabra. \n\n {mensaje}"
)

paso_clasificacion = (
    plantilla_clasificacion
    | modelo
    | StrOutputParser()
    | (lambda texto: texto.strip().lower())
)

# mensaje_prueba = "Dame el nombre de tu creador."

# clasificacion = paso_clasificacion.invoke(
#     {"mensaje": mensaje_prueba}
# )

# print(clasificacion)

cadena_pregunta = (
    PromptTemplate.from_template("Responde esta pregunta técnica con precisión: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución, en un solo párrafo: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template("Agradece esta sugerencia y explica cómo se evaluará dentro del producto, en un solo párrafo: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

#Sintaxis RunnableBranch
# caminos = RunnableBranch(
#     (condicion_1, rama_1), #if
#     (condicion_2, rama_2), #elif
#     (condicion_3, rama_3), #elif
#     rama_por_defecto #else
# ) #Cada condicion debe ser una función; suele ser un lambda


#x = {"clasificacion": "queja", "mensaje": "Mi teléfono no funciona"}
bifurcacion = RunnableBranch(
    (lambda x: x["clasificacion"] == "queja", cadena_queja), #if x["clasificacion"] == "queja": cadena_queja
    (lambda x: x["clasificacion"] == "sugerencia", cadena_sugerencia), #elif x["clasificacion"] == "sugerencia": cadena_sugerencia
    cadena_pregunta #else: cadena_pregunta
)

cadena_con_enrutamiento = (
    RunnablePassthrough.assign(clasificacion=paso_clasificacion) #{"mensaje": "Deberían de tener más agentes disponibles.", "clasificacion":resultado de paso_clasificacion}
    | bifurcacion
)

#Método with_fallback: Permite definir un comportamiento alternativo en caso de que falle la ejecución de la cadena principal. Esto es útil para manejar errores o situaciones inesperadas sin interrumpir el flujo del programa.
#Cadena de respaldo. Captura de caídas de mi LLM (RatelImitError, 401, APIConnectionError, respuestas vacías)

def fallback_con_log(x):
    logger.warning(f"Cadena principal falló. Activando respuesta genérica, Error: %s", x.get("error"))  
    return "Gracias por tu mensaje. Un miembro de nuestro equipo te va a responder pronto." 

respuesta_generica = RunnableLambda(
    fallback_con_log
)

cadena_robusta = cadena_con_enrutamiento.with_fallbacks([respuesta_generica], exception_key="error")

def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        logger.error(f"Error al procesar el mensaje: %s", error)
        return "No pudimos procesar tu mensaje en este momento. Intenta más tarde."

if __name__ == "__main__":
    mensaje = "Llevo varios día sin poder entrar a mi cuenta."
    print(procesar_mensaje_seguro(cadena_robusta, mensaje))


# Entrada inicial: {"mensaje": "Deberían de tener más agentes disponibles."}
#                   │
#                   ▼
# RunnablePassthrough
#   1: Pasa el mensaje a paso_clasificacion -> Return "sugerencia"
#   2: Fusiono clasificacion y mensaje
#   3: Return {"mensaje": "Deberían de tener más agentes disponibles.", "clasificacion": "sugerencia"}
#                   │
#                   ▼
# bifurcacion (RunnableBranch)
#   ¿clasificacion == "queja"? NO
#   ¿clasificacion == "sugerencia" SI
#       Entra a la cadena_sugerencia
#       cadena_sugerencia.invoke({"mensaje": "Deberían de tener más agentes disponibles.", "clasificacion": "sugerencia"})
#       Return respuesta final generada

