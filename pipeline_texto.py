import re
import json
from collections import Counter
from cliente import consultar_modelo

def limpiar_texto(texto: str) -> str:
    # Convierte el texto a minúsculas
    texto = texto.lower()

    # Elimina signos de puntuación, pero mantiene letras, números y espacios
    texto = re.sub(r"[^\w\s]", "", texto)

    # Reemplaza varios espacios seguidos por uno solo
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto
print(limpiar_texto("¡Hola, Mundo!"))

def tokenizar(texto_limpio: str) -> list[str]:
    # Divide el texto ya limpio en palabras separadas
    return texto_limpio.split()
print(tokenizar("hola mundo"))

def procesar_texto(texto: str) -> list[str]:
    # Primero limpiamos el texto
    texto_limpio = limpiar_texto(texto)

    # Luego lo dividimos en palabras
    return tokenizar(texto_limpio)

def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    # Cuenta cuántas veces aparece cada token en referencia y respuesta
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)

    # Toma solo las coincidencias, respetando repeticiones
    interseccion = conteo_referencia & conteo_respuesta

    # Suma la cantidad total de coincidencias
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    # Cuenta las coincidencias entre ambas listas de tokens
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    # Evita división por cero si alguna lista está vacía
    if not tokens_respuesta or not tokens_referencia:
        return {
            "precision": 0.0,
            "cobertura": 0.0,
            "f1": 0.0
        }

    # De todo lo que respondió el modelo, cuánto coincide con la referencia
    precision = coincidencias / len(tokens_respuesta)

    # De todo lo que debía aparecer, cuánto sí apareció
    cobertura = coincidencias / len(tokens_referencia)

    # Combina precisión y cobertura en un solo valor
    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    return {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1
    }

def calcular_metricas(
    texto_referencia: str,
    texto_respuesta: str
) -> dict[str, float]:

    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia,
        tokens_respuesta
    )

if __name__ == "__main__":
    print(procesar_texto("El Cielo, es AZUL!"))

    referencia = "El cielo es azul."
    respuesta = "el cielo es azul"

    tokens_referencia = referencia.split()
    tokens_respuesta = respuesta.split()

    comunes = set(tokens_referencia) & set(tokens_respuesta)

    if tokens_referencia:
        proporcion = len(comunes) / len(set(tokens_referencia))
    else:
        proporcion = 0.0

    print(f"Coincidencia texto crudo: {proporcion:.0%}")

    tokens_referencia = procesar_texto(referencia)
    tokens_respuesta = procesar_texto(respuesta)

    comunes = set(tokens_referencia) & set(tokens_respuesta)

    if tokens_referencia:
        proporcion = len(comunes) / len(set(tokens_referencia))
    else:
        proporcion = 0.0

    print(f"Coincidencia texto procesado: {proporcion:.0%}")


    casos = [
    (
        "¿Qué es un proyecto?",
        "Un proyecto es un conjunto de actividades planificadas que buscan alcanzar un objetivo dentro de un plazo definido."
    ),
    (
        "¿Qué es un compromiso dentro de un proyecto?",
        "Un compromiso es una tarea o acción acordada que tiene un responsable y una fecha de cumplimiento."
    ),
    (
        "¿Qué es un riesgo en la gestión de proyectos?",
        "Un riesgo es una situación que puede afectar el cumplimiento de los objetivos, plazos o resultados de un proyecto."
    ),
    (
        "¿Qué es un pendiente dentro de un proyecto?",
        "Un pendiente es una tarea o acción que aún no ha sido completada y requiere seguimiento."
    ),
    (
        "¿Qué es un responsable dentro de un proyecto?",
        "Un responsable es la persona encargada de ejecutar o supervisar una tarea o compromiso."
    ),
    (
        "¿Qué es una fecha de cumplimiento?",
        "Una fecha de cumplimiento es el plazo definido para completar una tarea, compromiso o entrega."
    ),
    (
        "¿Qué es un hito de proyecto?",
        "Un hito es un evento o punto relevante que marca un avance importante dentro de un proyecto."
    ),
    (
        "¿Qué es una alerta en la gestión de proyectos?",
        "Una alerta es una señal que indica que una tarea, riesgo o plazo requiere atención."
    ),
    (
        "¿Qué significa que una tarea esté atrasada?",
        "Una tarea está atrasada cuando no se ha completado dentro del plazo definido."
    ),
    (
        "¿Qué es el seguimiento de compromisos?",
        "El seguimiento de compromisos consiste en revisar su avance, responsable, plazo y estado de cumplimiento."
    ),
    (
        "¿Qué es el estado de un proyecto?",
        "El estado de un proyecto resume su nivel de avance, pendientes, riesgos y compromisos principales."
    ),
    (
        "¿Qué es un semáforo de proyecto?",
        "Un semáforo de proyecto utiliza niveles como verde, amarillo y rojo para representar el estado o nivel de riesgo."
    ),
    (
        "¿Qué representa el color verde en un semáforo de proyecto?",
        "El color verde indica que el proyecto o tarea avanza de acuerdo con lo planificado y sin alertas relevantes."
    ),
    (
        "¿Qué representa el color amarillo en un semáforo de proyecto?",
        "El color amarillo indica que existe una alerta o riesgo que requiere seguimiento."
    ),
    (
        "¿Qué representa el color rojo en un semáforo de proyecto?",
        "El color rojo indica una situación crítica, un atraso importante o un riesgo que requiere atención inmediata."
    ),
    (
        "¿Qué información debería tener un compromiso?",
        "Un compromiso debería incluir una acción, un responsable, una fecha de cumplimiento y un estado."
    ),
    (
        "¿Qué información debería tener un riesgo?",
        "Un riesgo debería incluir una descripción, su posible impacto, su nivel de criticidad y las acciones de seguimiento."
    ),
    (
        "¿Para qué sirve identificar compromisos en un acta de reunión?",
        "Identificar compromisos permite saber qué acciones deben realizarse, quién es responsable y cuándo deben cumplirse."
    ),
    (
        "¿Para qué sirve identificar riesgos en un proyecto?",
        "Identificar riesgos permite anticipar situaciones que podrían afectar los objetivos, plazos o resultados del proyecto."
    ),
    (
        "¿Para qué sirve ProjectPulse?",
        "ProjectPulse sirve para identificar compromisos, riesgos, pendientes y plazos de un proyecto y facilitar su seguimiento."
    ),
]

    resultados = []

    for numero, (consulta, referencia) in enumerate(casos, start=1):
        respuesta = consultar_modelo(consulta)

        metricas = calcular_metricas(referencia, respuesta)

        resultados.append({
            "consulta": consulta,
            "referencia": referencia,
            "respuesta": respuesta,
            **metricas
        })

        print(f"[Caso {numero}] Métricas:", metricas)

    with open(
        "resultados_metricas.json",
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            resultados,
            archivo,
            indent=2,
            ensure_ascii=False
        )

    referencia = procesar_texto("El gato duerme en el sofá.")
    respuesta = procesar_texto("El gato duerme en el sillón todo el día.")

    coincidencias = contar_coincidencias(referencia, respuesta)

    print("Coincidencias:", coincidencias)

    resultado = calcular_precision_cobertura_f1(referencia, respuesta)

    print(resultado)

