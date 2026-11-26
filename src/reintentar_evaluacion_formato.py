
import json
from pathlib import Path

from prompts.banco import BANCO_DE_PROMPTS
from consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    parsear_respuesta_json,
    MODELO,
)
from evaluacion_formato_projectpulse import validar_estructura

ARCHIVO = Path("evaluacion_formato_projectpulse.jsonl")

registros = [
    json.loads(linea)
    for linea in ARCHIVO.read_text(encoding="utf-8").splitlines()
    if linea.strip()
]

pendientes = [
    registro for registro in registros
    if registro["estado"] == "error_api"
]

print("Casos pendientes:", [r["numero"] for r in pendientes])

for registro in pendientes:
    numero = registro["numero"]
    prompt = next(
        p for p in BANCO_DE_PROMPTS
        if p["nombre"] == registro["tipo"]
    )

    print(f"\nReintentando caso {numero}...")

    try:
        url, body = armar_peticion(
            pregunta=registro["consulta"],
            modelo=MODELO,
            system_instruction=prompt["system_instruction"],
            response_schema=prompt["response_schema"],
        )

        respuesta = enviar_peticion(url, body)
        texto = extraer_texto(respuesta)

        registro["respuesta"] = texto
        registro["estado"] = "evaluado"

        try:
            datos = parsear_respuesta_json(
                texto, prompt["claves_esperadas"]
            )
            cumple, detalle = validar_estructura(
                datos, prompt["nombre"]
            )
            registro["cumple_formato"] = cumple
            registro["observacion"] = detalle

        except (ValueError, TypeError) as error:
            registro["cumple_formato"] = False
            registro["observacion"] = str(error)

    except (ValueError, RuntimeError, TimeoutError) as error:
        registro["observacion"] = str(error)

    print(
        f"Caso {numero}:",
        registro["cumple_formato"],
        registro["observacion"],
    )

# Guardar los registros conservando los 20 casos originales
ARCHIVO.write_text(
    "".join(
        json.dumps(r, ensure_ascii=False) + "\n"
        for r in registros
    ),
    encoding="utf-8",
)

evaluadas = [r for r in registros if r["estado"] == "evaluado"]
fallas = [r for r in evaluadas if r["cumple_formato"] is False]

print("\n========== RESUMEN ==========")
print("Total de casos:", len(registros))
print("Respuestas evaluadas:", len(evaluadas))
print("Fallas de formato:", len(fallas))
print("Errores de API:", len(registros) - len(evaluadas))

if len(evaluadas) == 20:
    print("Criterio de formato:", len(fallas) >= 3)
else:
    print("Todavía quedan consultas pendientes.")
