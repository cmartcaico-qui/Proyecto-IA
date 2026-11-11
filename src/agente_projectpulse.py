from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field, ValidationError

import json
from datetime import datetime
from pathlib import Path

# Reutilizando componentes ya existentes
from cadena_projectpulse import construir_cadena, texto_prueba
from orquestacion_projectpulse import cadena_alertas_segura

# === CONFIGURACIÓN ===

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

# Cadena para generar reportes
cadena_reporte = construir_cadena(modelo)


# === VALIDACIÓN DE ARGUMENTOS ===

class ArgumentosAnalisisProyecto(BaseModel):
    """
    Define y valida los argumentos que reciben
    las herramientas de análisis de ProjectPulse.
    """

    texto: str = Field(
        min_length=1,
        description=(
            "Texto original del acta, correo o documento "
            "del proyecto que se debe analizar. "
            "Debe contener información proporcionada "
            "por el usuario o una fuente verificable. "
            "No se debe inventar ni completar información."
        )
    )

# === HERRAMIENTAS ===

@tool(args_schema=ArgumentosAnalisisProyecto)
def generar_reporte(texto: str) -> str:
    """
    Genera un reporte general de seguimiento de proyectos.
    Usar cuando se soliciten compromisos, pendientes,
    responsables, fechas y alertas en un reporte completo.
    """
    return cadena_reporte.invoke({"texto": texto})

@tool(args_schema=ArgumentosAnalisisProyecto)
def identificar_alertas(texto: str) -> str:
    """
    Identifica riesgos y problemas respaldados por el texto.
    Usar cuando se solicite analizar riesgos,
    posibles retrasos o situaciones de alerta.
    """
    return cadena_alertas_segura.invoke({"texto": texto})

# === SUPERVISIÓN HUMANA ===

class ArgumentosActualizacion(BaseModel):
    compromiso: str = Field(
        min_length=1,
        description="Compromiso que se propone actualizar."
    )

    nuevo_estado: str = Field(
        min_length=1,
        description="Nuevo estado propuesto para el compromiso."
    )

    evidencia: str = Field(
        min_length=1,
        description="Información que respalda el cambio propuesto."
    )

@tool(args_schema=ArgumentosActualizacion)
def proponer_actualizacion(
    compromiso: str,
    nuevo_estado: str,
    evidencia: str
) -> str:
    """
    Prepara una propuesta de actualización de un compromiso.
    No modifica datos ni ejecuta cambios.
    La propuesta requiere revisión y aprobación humana.
    """

    return (
        "PROPUESTA DE ACTUALIZACIÓN\n"
        f"Compromiso: {compromiso}\n"
        f"Estado propuesto: {nuevo_estado}\n"
        f"Evidencia declarada: {evidencia}\n"
        "Estado de la acción: NO EJECUTADA\n"
        "Aprobación humana: PENDIENTE\n"
        "La evidencia debe verificarse antes de aprobar."
    )

# === LISTA DE HERRAMIENTAS ===

herramientas = [
    generar_reporte,
    identificar_alertas,
    proponer_actualizacion
]

# === PLANTILLA ===

prompt_agente = ChatPromptTemplate.from_messages([
    (
        "system",
        """Eres ProjectPulse, un asistente especializado
        en seguimiento y control de proyectos.

        REGLAS OBLIGATORIAS:

        1. Utiliza exclusivamente la información proporcionada
        y los resultados de las herramientas.

        2. No inventes compromisos, responsables, fechas,
        actividades, estados ni riesgos.

        3. Identifica únicamente compromisos expresados
        en la documentación.

        4. Si un responsable o una fecha no aparece,
        indica "No especificado".

        5. Diferencia claramente:
        - COMPROMISO: actividad o tarea acordada.
        - PENDIENTE: actividad que aún requiere cumplimiento.
        - RIESGO: situación respaldada por evidencia que
            podría afectar el cumplimiento de un compromiso.

        6. No conviertas automáticamente un pendiente
        en un riesgo.

        7. No inventes relaciones de dependencia entre
        personas, tareas o fechas.

        8. No afirmes que un compromiso está atrasado
        si no existe evidencia suficiente.

        9. No conviertas riesgos posibles en problemas
        confirmados.

        10. Si la información es ambigua o contradictoria,
            indica "Requiere verificación".

        11. Cada riesgo debe estar respaldado por evidencia
            identificable en el texto.

        12. Si no existen riesgos respaldados,
            indica "No se identifican riesgos con la
            información proporcionada".

        13. Si una herramienta no puede completar su análisis,
            informa la limitación. No presentes resultados
            incompletos como verificados.

        14. Nunca ejecutes modificaciones ni comunicaciones
            externas sin la autorización requerida.

        15. No asignes automáticamente el estado "Pendiente"
            a una actividad solo porque fue acordada.

        16. Si el documento no confirma su cumplimiento
            o incumplimiento, indica "Estado no informado".

        17. Conserva las expresiones de plazo originales.
            Por ejemplo, "antes del jueves" no equivale
            necesariamente a "jueves".

        18. No interpretes una fecha de compromiso como
            evidencia de retraso o incumplimiento.

        19. Diferencia entre:
            - Compromiso acordado.
            - Actividad pendiente confirmada.
            - Riesgo posible respaldado por evidencia.
            - Incumplimiento confirmado.

        20. No atribuyas un riesgo a un responsable
            cuando el texto solo identifica una situación
            que podría afectar su compromiso.

        21. El estado "No informado" no constituye por sí solo
            evidencia de riesgo, atraso ni incumplimiento.

        22. Cuando utilices información del historial, conserva
            las evidencias originales que respaldan cada riesgo.
            No analices únicamente un resumen de compromisos
            si este omite información relevante del documento.

        23. Si no cuentas con evidencia suficiente para
            identificar un riesgo, indica:
            "No se identifican riesgos respaldados
            por la información disponible".

        24. Cuando se solicite actualizar un compromiso,
            utiliza proponer_actualizacion para preparar
            una propuesta. No afirmes que el cambio fue
            realizado ni que fue aprobado.

        Si falta evidencia, solicita verificación.
        Tu prioridad es la precisión, la trazabilidad
        y la confiabilidad de la información."""
    ),
    MessagesPlaceholder("chat_history"),
    (
        "human",
        "Solicitud: {solicitud}\n\n"
        "Texto del proyecto:\n{texto}"
    ),
    MessagesPlaceholder("agent_scratchpad")
])

# === CONSTRUCCIÓN DEL AGENTE ===

agente = create_tool_calling_agent(
    modelo,
    herramientas,
    prompt_agente
)

# === EJECUTOR ===

ejecutor_agente = AgentExecutor(
    agent=agente,
    tools=herramientas,
    verbose=True,
    return_intermediate_steps=True
)

# === MEMORIA ===

historiales = {}

def obtener_historial(session_id: str):
    if session_id not in historiales:
        historiales[session_id] = InMemoryChatMessageHistory()

    return historiales[session_id]

# Respuesta de Gemini a texto
def limpiar_resultado(resultado):
    salida = resultado.get("output", "")

    if isinstance(salida, list):
        salida = "\n".join(
            bloque.get("text", "")
            for bloque in salida
            if isinstance(bloque, dict)
            and bloque.get("type") == "text"
        )

    return {**resultado, "output": salida}

# Conectar el ejecutor con el limpiador
cadena_agente = ejecutor_agente | RunnableLambda(
    limpiar_resultado
)

# Crear el agente con memoria
agente_con_memoria = RunnableWithMessageHistory(
    cadena_agente,
    obtener_historial,
    input_messages_key="solicitud",
    history_messages_key="chat_history",
    output_messages_key="output"
)

# === APROBACIÓN HUMANA ===

def solicitar_aprobacion(compromiso, nuevo_estado, evidencia):

    print("\n=== SUPERVISIÓN HUMANA ===")
    print("Compromiso:", compromiso)
    print("Estado propuesto:", nuevo_estado)
    print("Evidencia:", evidencia)
    print("Esta prueba no modifica información real.")

    decision = input(
        "\n¿Apruebas la propuesta? (APROBAR/RECHAZAR): "
    ).strip().upper()

    if decision == "APROBAR":
        print("\nPropuesta aprobada para simulación.")
        print("No se han modificado datos reales.")
        return "APROBADA_SIMULADA"

    elif decision == "RECHAZAR":
        print("\nPropuesta rechazada.")
        print("No se ha realizado ningún cambio.")
        return "RECHAZADA"

    else:
        print("\nRespuesta no válida.")
        print("La propuesta queda sin autorización.")
        return "SIN_AUTORIZACION"

# === REGISTRO DE TRAZAS JSONL ===

ARCHIVO_TRAZAS = Path(__file__).resolve().parent / "trazas_projectpulse.jsonl"

def registrar_traza(accion, compromiso, nuevo_estado,
                    evidencia, decision):

    registro = {
        "fecha_hora": datetime.now().astimezone().isoformat(),
        "accion": accion,
        "compromiso": compromiso,
        "nuevo_estado": nuevo_estado,
        "evidencia_declarada": evidencia,
        "decision_humana": decision,
        "ejecutada": False,
        "tipo_ejecucion": "simulacion"
    }

    with open(ARCHIVO_TRAZAS, "a", encoding="utf-8") as archivo:
        archivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )

    print("\nTraza registrada correctamente.")

# === REGISTRO DE ACCIONES DEL AGENTE ===

def registrar_traza_agente(
    numero_consulta,
    solicitud,
    resultado
):
    acciones = []

    for accion, observacion in resultado["intermediate_steps"]:
        acciones.append({
            "herramienta": accion.tool,
            "argumentos": accion.tool_input,
            "observacion": observacion
        })

    registro = {
        "fecha_hora": datetime.now().astimezone().isoformat(),
        "tipo_registro": "consulta_agente",
        "numero_consulta": numero_consulta,
        "solicitud": solicitud,
        "acciones": acciones,
        "respuesta_final": resultado["output"]
    }

    with open(ARCHIVO_TRAZAS, "a", encoding="utf-8") as archivo:
        archivo.write(
            json.dumps(
                registro,
                ensure_ascii=False,
                default=str
            ) + "\n"
        )

    print(
        f"\nTraza de consulta {numero_consulta} registrada."
    )

# === PRUEBAS ===

if __name__ == "__main__":

    config = {
        "configurable": {
            "session_id": "proyecto_prueba_001"
        }
    }

    # === PRIMERA CONSULTA ===

    resultado1 = agente_con_memoria.invoke(
        {
            "solicitud": "Identifica los compromisos de esta reunión",
            "texto": texto_prueba
        },
        config=config
    )

    print("\n=== PRIMERA CONSULTA ===")
    print(resultado1["output"])

    registrar_traza_agente(
        numero_consulta=1,
        solicitud="Identifica los compromisos de esta reunión",
        resultado=resultado1
    )
    # === SEGUNDA CONSULTA ===

    resultado2 = agente_con_memoria.invoke(
        {
            "solicitud": "¿Cuál de esos compromisos presenta riesgos?",
            "texto": texto_prueba
        },
        config=config
    )

    print("\n=== SEGUNDA CONSULTA ===")
    print(resultado2["output"])

    registrar_traza_agente(
        numero_consulta=2,
        solicitud="¿Cuál de esos compromisos presenta riesgos?",
        resultado=resultado2
    )
    # === PRUEBA DE PYDANTIC ===

    try:
        generar_reporte.invoke({"texto": ""})

    except ValidationError:
        print("\n=== VALIDACIÓN PYDANTIC ===")
        print("Correcto: se rechazó un texto vacío.")

    else:
        print("\nERROR: Pydantic aceptó un texto vacío.")


    # === PRUEBA DE ACTUALIZACIÓN ===

    propuesta = proponer_actualizacion.invoke({
        "compromiso": "Entrega del informe de avance",
        "nuevo_estado": "Completado",
        "evidencia": "Ejemplo simulado para prueba"
    })

    print("\n=== PROPUESTA DE ACTUALIZACIÓN ===")
    print(propuesta)

    # === PRUEBA DE APROBACIÓN HUMANA ===

    decision = solicitar_aprobacion(
        compromiso="Entrega del informe de avance",
        nuevo_estado="Completado",
        evidencia="Ejemplo simulado para prueba"
    )

    print("\n=== RESULTADO DE LA SUPERVISIÓN ===")
    print("Decisión:", decision)

    # === GUARDAR LA DECISIÓN EN JSONL ===

    registrar_traza(
        accion="proponer_actualizacion",
        compromiso="Entrega del informe de avance",
        nuevo_estado="Completado",
        evidencia="Ejemplo simulado para prueba",
        decision=decision
    )
