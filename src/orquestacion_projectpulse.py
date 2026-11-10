from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from cadena_projectpulse import construir_cadena

import logging

load_dotenv()

# CONFIGURACIÓN DEL REGISTRO DE ERRORES

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="errores_projectpulse.log",
    filemode="a",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)

# PASO 1: CLASIFICAR LA SOLICITUD

plantilla_clasificacion = PromptTemplate.from_template(
    "Eres el clasificador de solicitudes de ProjectPulse.\n"
    "Clasifica la siguiente solicitud en una sola categoría:\n\n"
    "reporte: si se pide un seguimiento general del proyecto.\n"
    "alertas: si se pide identificar riesgos o retrasos.\n"
    "pendientes: si se pide identificar tareas pendientes.\n\n"
    "Responde únicamente con una de estas palabras: "
    "reporte, alertas o pendientes.\n\n"
    "Solicitud: {solicitud}"
)

def construir_paso_clasificacion(modelo):
    return (
        plantilla_clasificacion
        | modelo
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )

paso_clasificacion = construir_paso_clasificacion(modelo)

# PASO 2: CREAR LAS RUTAS

# Ruta 1: Reporte general
# Reutilizando la cadena de tres pasos

cadena_reporte = construir_cadena(modelo)

# Ruta 2: Alertas
cadena_alertas = (
    PromptTemplate.from_template(
        "Eres el analista de riesgos de ProjectPulse.\n\n"

        "Analiza el siguiente texto de seguimiento "
        "de un proyecto e identifica únicamente riesgos "
        "y problemas respaldados por el texto.\n\n"

        "REGLAS OBLIGATORIAS:\n"
        "1. Distingue los hechos de las interpretaciones.\n"
        "2. No inventes dependencias entre tareas, "
        "personas o fechas.\n"
        "3. Que dos tareas tengan fechas cercanas "
        "no significa que una dependa de la otra.\n"
        "4. No afirmes que una persona necesita "
        "información de otra tarea, salvo que "
        "el texto lo indique expresamente.\n"
        "5. No conviertas una tarea pendiente "
        "en un riesgo si no existe evidencia "
        "de un problema o posible incumplimiento.\n"
        "6. Si una relación no está confirmada, "
        "no la presentes como un hecho.\n"
        "7. No inventes responsables, fechas "
        "ni consecuencias.\n\n"

        "FORMATO DE RESPUESTA:\n"
        "RIESGOS CONFIRMADOS POR EL TEXTO:\n"
        "- Describe cada riesgo y su evidencia.\n\n"

        "IMPACTO:\n"
        "- Explica solamente los impactos "
        "mencionados o directamente respaldados.\n\n"

        "INFORMACIÓN NO CONFIRMADA:\n"
        "- Indica brevemente qué relaciones "
        "importantes no pueden establecerse "
        "con la información disponible, "
        "sin desarrollar escenarios hipotéticos.\n\n"

        "Si no hay riesgos respaldados por "
        "el texto, indícalo claramente.\n\n"

        "TEXTO DEL PROYECTO:\n{texto}"
    )
    | modelo
    | StrOutputParser()
)

# Ruta 3: Pendientes
cadena_pendientes = (
    PromptTemplate.from_template(
        "Analiza el siguiente texto de seguimiento.\n"
        "Identifica los compromisos y las tareas pendientes.\n"
        "Indica responsables y fechas si están mencionados.\n"
        "Si falta información, indícalo.\n"
        "No inventes información.\n\n"
        "Texto: {texto}"
    )
    | modelo
    | StrOutputParser()
)

# PASO 3: FALLBACK PARA LA RUTA DE ALERTAS

def respaldo_alertas(x):
    logger.warning(
        "Se activó el fallback de alertas. Error: %s",
        x.get("error")
    )

    return (
        "No se pueden analizar las alertas "
        "en este momento. No se han verificado riesgos. "
        "Intenta nuevamente más tarde."
    )

respuesta_respaldo_alertas = RunnableLambda(
    respaldo_alertas
)

# Permite proteger cualquier cadena de alertas
def construir_cadena_alertas_segura(cadena):
    return cadena.with_fallbacks(
        [respuesta_respaldo_alertas],
        exception_key="error"
    )

# Protege la ruta real
cadena_alertas_segura = construir_cadena_alertas_segura(
    cadena_alertas
)

# PASO 4: ENRUTAMIENTO DE PROJECTPULSE

def construir_bifurcacion(
    cadena_alertas,
    cadena_pendientes,
    cadena_reporte
):
    return RunnableBranch(
        (
            lambda x: x["clasificacion"] == "alertas",
            cadena_alertas
        ),
        (
            lambda x: x["clasificacion"] == "pendientes",
            cadena_pendientes
        ),
        cadena_reporte
    )

bifurcacion = construir_bifurcacion(
    cadena_alertas_segura,
    cadena_pendientes,
    cadena_reporte
)

cadena_con_enrutamiento = (
    RunnablePassthrough.assign(
        clasificacion=(
            lambda x: {"solicitud": x["solicitud"]}
        )
        | paso_clasificacion
    )
    | bifurcacion
)

# MANEJO GENERAL DE ERRORES

def procesar_solicitud_segura(cadena, solicitud, texto):

    try:
        return cadena.invoke({
            "solicitud": solicitud,
            "texto": texto
        })

    except Exception:
        logger.exception(
            "Error al procesar la solicitud"
        )

        return (
            "No podemos procesar la solicitud "
            "en este momento. Intenta nuevamente más tarde."
        )

# PRUEBA INICIAL

if __name__ == "__main__":

    texto_prueba = """
    Durante la reunión de seguimiento se acordó que
    el equipo académico entregará el informe el viernes.

    Claudia deberá revisar la documentación pendiente
    antes del jueves.

    Se informó que todavía faltan registros de asistencia,
    lo que podría retrasar la elaboración del informe.
    """

    resultado = procesar_solicitud_segura(
        cadena_con_enrutamiento,
        "Genera un reporte general de seguimiento del proyecto",
        texto_prueba
    )
    
    print("\n=== RESULTADO PROJECTPULSE ===")
    print(resultado)
    
    # PRUEBA DE FALLBACK CON ERROR SIMULADO

    def provocar_error(x):
        raise ConnectionError("Error de conexión simulado")

    cadena_con_error = RunnableLambda(provocar_error)

    cadena_prueba_segura = cadena_con_error.with_fallbacks(
        [respuesta_respaldo_alertas]
    )

    resultado_fallback = cadena_prueba_segura.invoke({
        "solicitud": "Identifica los riesgos del proyecto",
        "texto": texto_prueba
    })

    print("\n=== PRUEBA DE FALLBACK ===")
    print(resultado_fallback)
