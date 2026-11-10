from unittest.mock import MagicMock

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from orquestacion_projectpulse import (
    construir_paso_clasificacion,
    construir_bifurcacion,
    construir_cadena_alertas_segura,
    procesar_solicitud_segura,
)

def test_clasificacion_normaliza_categoria():

    # Simulando el modelo Gemini
    modelo_falso = MagicMock()

    # Gemini responde con mayúsculas y espacios
    modelo_falso.return_value = AIMessage(
        content=" ALERTAS \n"
    )

    # Clasificación con modelo falso
    paso = construir_paso_clasificacion(modelo_falso)

    # Simulando una solicitud a ProjectPulse
    resultado = paso.invoke({
        "solicitud": "Identifica los riesgos del proyecto"
    })

    # A ver si normaliza correctamente
    assert resultado == "alertas"

    # A ver si el modelo se llamó una vez
    assert modelo_falso.call_count == 1

# PRUEBAS DE ENRUTAMIENTO

def crear_rutas_falsas():
    # Estas rutas no llaman a Gemini
    return construir_bifurcacion(
        RunnableLambda(lambda x: "RUTA_ALERTAS"),
        RunnableLambda(lambda x: "RUTA_PENDIENTES"),
        RunnableLambda(lambda x: "RUTA_REPORTE")
    )


def test_enrutamiento_alertas():
    bifurcacion = crear_rutas_falsas()

    resultado = bifurcacion.invoke({
        "clasificacion": "alertas",
        "texto": "Faltan registros de asistencia"
    })

    assert resultado == "RUTA_ALERTAS"


def test_enrutamiento_pendientes():
    bifurcacion = crear_rutas_falsas()

    resultado = bifurcacion.invoke({
        "clasificacion": "pendientes",
        "texto": "Falta entregar el informe"
    })

    assert resultado == "RUTA_PENDIENTES"


def test_enrutamiento_reporte():
    bifurcacion = crear_rutas_falsas()

    resultado = bifurcacion.invoke({
        "clasificacion": "reporte",
        "texto": "Reunión de seguimiento del proyecto"
    })

    assert resultado == "RUTA_REPORTE"


def test_enrutamiento_categoria_desconocida():
    bifurcacion = crear_rutas_falsas()

    resultado = bifurcacion.invoke({
        "clasificacion": "desconocida",
        "texto": "Información del proyecto"
    })

    assert resultado == "RUTA_REPORTE"

def test_fallback_alertas_ante_error():

    # Fallo de conexión
    def provocar_error(x):
        raise ConnectionError("Error de red simulado")

    # Cadena que siempre falla
    cadena_falsa = RunnableLambda(provocar_error)

    # Se con el fallback
    cadena_segura = construir_cadena_alertas_segura(
        cadena_falsa
    )

    resultado = cadena_segura.invoke({
        "clasificacion": "alertas",
        "texto": "Faltan registros de asistencia"
    })

    # Se comprueba que devolvió la respuesta de respaldo
    assert "no se pueden analizar las alertas" in resultado.lower()
    assert "no se han verificado riesgos" in resultado.lower()


def test_error_clasificacion_no_detiene_projectpulse(caplog):

    # Error en la clasificación
    def clasificacion_con_error(x):
        raise ConnectionError(
            "Error simulado durante la clasificación"
        )

    paso_clasificacion_falso = RunnableLambda(
        clasificacion_con_error
    )

    # Cadena donde falla la clasificación
    cadena_falsa = (
        RunnablePassthrough.assign(
            clasificacion=paso_clasificacion_falso
        )
        | crear_rutas_falsas()
    )

    # Ejecutamos ProjectPulse con protección general
    resultado = procesar_solicitud_segura(
        cadena_falsa,
        "Identifica los riesgos del proyecto",
        "Faltan registros de asistencia"
    )

    # Verificamos que devuelve una respuesta segura
    assert "no podemos procesar" in resultado.lower()

    # Verificamos que el error quedó registrado
    assert "Error al procesar la solicitud" in caplog.text
