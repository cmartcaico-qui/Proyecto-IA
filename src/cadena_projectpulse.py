from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def construir_cadena(modelo):

    # PASO 1: Extraer compromisos

    plantilla_compromisos = PromptTemplate.from_template(
        "Lee la siguiente acta de reunión e identifica:\n"
        "1. Los compromisos y tareas acordadas.\n"
        "2. Los responsables y fechas mencionadas.\n"
        "3. Las situaciones informadas que podrían afectar "
        "el cumplimiento de los compromisos.\n\n"
        "No inventes información y no omitas problemas "
        "mencionados explícitamente en el texto.\n\n"
        "{texto}"
    )

    paso_compromisos = plantilla_compromisos | modelo | StrOutputParser()


    # PASO 2: Detectar riesgos y pendientes

    plantilla_riesgos = PromptTemplate.from_template(
        "Analiza los siguientes compromisos de un proyecto. "
        "Identifica posibles riesgos, tareas pendientes y situaciones "
        "que podrían afectar el cumplimiento de los compromisos. "
        "Utiliza solamente la información proporcionada. "
        "Si no hay evidencia de un riesgo, indícalo. "
        "Responde en lenguaje sencillo.\n\n"
        "{compromisos}"
    )

    paso_riesgos = plantilla_riesgos | modelo | StrOutputParser()


    # PASO 3: Generar reporte de seguimiento

    plantilla_reporte = PromptTemplate.from_template(
        "A partir del siguiente análisis de compromisos y riesgos, "
        "genera un reporte breve de seguimiento del proyecto.\n\n"
        "Organiza la información en tres secciones:\n"
        "1. COMPROMISOS: tareas, responsables y fechas.\n"
        "2. PENDIENTES: actividades o información que falta.\n"
        "3. ALERTAS: riesgos identificados y su posible impacto.\n\n"
        "No inventes información. "
        "Si falta un responsable o una fecha, indícalo. "
        "Utiliza un lenguaje claro y directo.\n\n"
        "No generes alertas basadas en suposiciones o dependencias "
        "que no estén explícitamente respaldadas por el texto.\n\n"
        "{analisis}"
    )

    paso_reporte = plantilla_reporte | modelo | StrOutputParser()


    # CADENA COMPLETA DE PROJECTPULSE

    cadena_tres_pasos = (
        paso_compromisos
        | (lambda compromisos: {"compromisos": compromisos})
        | paso_riesgos
        | (lambda analisis: {"analisis": analisis})
        | paso_reporte
    )

    return cadena_tres_pasos

# TEXTO DE PRUEBA

texto_prueba = """
Durante la reunión de seguimiento se acordó que el equipo
académico entregará el informe de avance el viernes.

Claudia deberá revisar la documentación pendiente antes
del jueves.

Se informó que todavía faltan los registros de asistencia
de algunos estudiantes, lo que podría retrasar la
elaboración del informe.
"""
# EJECUTAR CADENA COMPLETA

if __name__ == "__main__":

    load_dotenv()

    modelo = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite"
    )

    cadena = construir_cadena(modelo)

    respuesta = cadena.invoke(
        {"texto": texto_prueba}
    )

    print("\n=== REPORTE PROJECTPULSE ===")
    print(respuesta)