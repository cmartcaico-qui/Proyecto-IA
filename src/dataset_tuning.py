import json
from collections import Counter
from google.genai import types
from laboratorio_dataset import validar_dataset, chequear_balance

# Dataset de ProjectPulse: clasificación de seguimiento

ejemplos_raw = [
    (
        "El equipo académico enviará el informe de avance el viernes.",
        {"categoria": "compromiso", "accion_sugerida": "registrar responsable y fecha"}
    ),
    (
        "La coordinación se comprometió a entregar las notas el jueves.",
        {"categoria": "compromiso", "accion_sugerida": "registrar responsable y fecha"}
    ),
    (
        "El instructor actualizará los materiales antes de la próxima clase.",
        {"categoria": "compromiso", "accion_sugerida": "registrar responsable y fecha"}
    ),
    (
        "La encargada enviará el listado de estudiantes durante la semana.",
        {"categoria": "compromiso", "accion_sugerida": "registrar responsable y fecha"}
    ),
    (
        "Falta consolidar los registros de asistencia.",
        {"categoria": "pendiente", "accion_sugerida": "incorporar a la lista de pendientes"}
    ),
    (
        "Todavía no se ha revisado el informe de certificación.",
        {"categoria": "pendiente", "accion_sugerida": "incorporar a la lista de pendientes"}
    ),
    (
        "Queda por completar la carga de actividades en la plataforma.",
        {"categoria": "pendiente", "accion_sugerida": "incorporar a la lista de pendientes"}
    ),
    (
        "El plazo del informe venció y no se ha recibido la entrega.",
        {"categoria": "alerta", "accion_sugerida": "generar alerta de incumplimiento"}
    ),
    (
        "La asistencia del curso está bajo el mínimo requerido.",
        {"categoria": "alerta", "accion_sugerida": "generar alerta de riesgo"}
    ),
    (
        "El retraso en la revisión podría afectar la certificación.",
        {"categoria": "alerta", "accion_sugerida": "generar alerta de riesgo"}
    )
]

# Convertir los datos al formato del SDK de Gemini
examples = [
    types.TuningExample(
        text_input=texto,
        output=json.dumps(salida, ensure_ascii=False)
    )
    for texto, salida in ejemplos_raw
]

print(len(examples), "ejemplos construidos")
print(examples[0])


# Validar el dataset de ProjectPulse
problemas = validar_dataset(
    examples,
    claves_esperadas=("categoria", "accion_sugerida")
)

print(f"\nValidación: {len(problemas)} problemas encontrados")

for problema in problemas:
    print(" -", problema)

# Revisar el balance de categorías
balance = chequear_balance(ejemplos_raw)

print("\nBalance de categorías:")

for categoria, cantidad in balance.most_common():
    print(f"{categoria}: {cantidad}")

# Probar el validador con errores intencionales

examples_rotos = examples + [
    types.TuningExample(
        text_input="",
        output='{"categoria": "alerta"}'
    ),
    types.TuningExample(
        text_input=ejemplos_raw[0][0],
        output="no es json"
    )
]

problemas_prueba = validar_dataset(examples_rotos)

print("\nPrueba con errores intencionales:")
print(f"{len(examples_rotos)} ejemplos, {len(problemas_prueba)} problemas encontrados")

for problema in problemas_prueba:
    print(" -", problema)
