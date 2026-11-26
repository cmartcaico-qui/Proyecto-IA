import json
from datetime import datetime, timezone

from prompts.banco import BANCO_DE_PROMPTS
from consumir_gemini import (
    armar_peticion,
    enviar_peticion,
    extraer_texto,
    parsear_respuesta_json,
    MODELO,
)

ARCHIVO_RESULTADOS = "evaluacion_formato_projectpulse.jsonl"

# 20 casos ficticios de seguimiento de ProjectPulse.
# Son textos de prueba, no documentos reales de colegios.

casos = [
    # 7 casos: extraer compromisos
    (0, "Carolina enviará el informe el viernes."),
    (0, "El equipo actualizará los registros el lunes."),
    (0, "Se acordó entregar la propuesta el miércoles."),
    (0, "Pedro revisará las actividades antes del jueves."),
    (0, "La coordinación enviará el acta mañana."),
    (0, "María consolidará los resultados el martes."),
    (0, "El instructor entregará los materiales el viernes."),

    # 7 casos: detectar alertas
    (1, "El plazo venció y el informe no fue entregado."),
    (1, "Faltan datos para completar el reporte."),
    (1, "La plataforma presenta fallas que impiden avanzar."),
    (1, "La asistencia está bajo el mínimo requerido."),
    (1, "El cliente aún no valida la información necesaria."),
    (1, "El proyecto avanza sin riesgos identificados."),
    (1, "La revisión pendiente podría retrasar la entrega."),

    # 6 casos: generar estado del proyecto
    (2, "Todas las actividades terminaron dentro del plazo."),
    (2, "Existen pendientes, pero el proyecto continúa."),
    (2, "Una falla crítica mantiene detenido el proyecto."),
    (2, "El informe está listo y no existen bloqueos."),
    (2, "Falta una validación que podría retrasar el cierre."),
    (2, "El plazo venció y una actividad crítica sigue pendiente."),
]

def validar_estructura(datos, nombre):
    #Comprueba estructura y tipos, no veracidad factual.
    if not isinstance(datos, dict):
        return False, "La respuesta no es un objeto JSON"

    if nombre == "extraer_compromisos":
        items = datos.get("compromisos")
        campos = ("responsable", "accion", "fecha")

    elif nombre == "detectar_alertas":
        items = datos.get("alertas")
        campos = ("tipo", "detalle", "nivel")

    else:
        if not isinstance(datos.get("estado"), str):
            return False, "Estado ausente o no es texto"

        if datos["estado"].lower() not in (
            "verde", "amarillo", "rojo"
        ):
            return False, "Estado fuera de los valores permitidos"

        if not isinstance(datos.get("justificacion"), str):
            return False, "Justificación ausente"

        pasos = datos.get("proximos_pasos")

        if not isinstance(pasos, list):
            return False, "Próximos pasos no es una lista"

        if not all(isinstance(p, str) for p in pasos):
            return False, "Próximos pasos contiene valores inválidos"

        return True, "Estructura válida"

    if not isinstance(items, list):
        return False, "La categoría esperada no contiene una lista"

    for item in items:
        if not isinstance(item, dict):
            return False, "Elemento no es un objeto"

        for campo in campos:
            if not isinstance(item.get(campo), str):
                return False, f"Campo inválido: {campo}"

        if nombre == "detectar_alertas":
            if item["nivel"].lower() not in (
                "bajo", "medio", "alto"
            ):
                return False, "Nivel de alerta inválido"

    return True, "Estructura válida"

if __name__ == "__main__":
    resultados = []

    with open(ARCHIVO_RESULTADOS, "w", encoding="utf-8") as archivo:

        for numero, (indice, texto) in enumerate(casos, start=1):
            prompt = BANCO_DE_PROMPTS[indice]

            print(
                f"\nCaso {numero}/20: {prompt['nombre']}"
            )

            registro = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "numero": numero,
                "modelo": MODELO,
                "tipo": prompt["nombre"],
                "consulta": texto,
                "respuesta": None,
                "estado": "error_api",
                "cumple_formato": None,
                "observacion": "",
            }

            try:
                url, body = armar_peticion(
                    pregunta=texto,
                    modelo=MODELO,
                    system_instruction=prompt["system_instruction"],
                    response_schema=prompt["response_schema"],
                )

                respuesta = enviar_peticion(url, body)
                texto_respuesta = extraer_texto(respuesta)

                registro["respuesta"] = texto_respuesta
                registro["estado"] = "evaluado"

                try:
                    datos = parsear_respuesta_json(
                        texto_respuesta,
                        prompt["claves_esperadas"],
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

            archivo.write(
                json.dumps(registro, ensure_ascii=False) + "\n"
            )
            archivo.flush()

            resultados.append(registro)

            print(
                "Resultado:",
                registro["cumple_formato"],
                "-",
                registro["observacion"],
            )


    evaluadas = [
        r for r in resultados
        if r["estado"] == "evaluado"
    ]

    fallas = [
        r for r in evaluadas
        if r["cumple_formato"] is False
    ]

    print("\n========== RESUMEN ==========")
    print("Casos preparados:", len(casos))
    print("Respuestas evaluadas:", len(evaluadas))
    print("Fallas de formato:", len(fallas))
    print("Errores de API:", len(resultados) - len(evaluadas))

    if evaluadas:
        porcentaje = len(fallas) / len(evaluadas) * 100
        print(f"Porcentaje de fallas: {porcentaje:.1f}%")

    if len(evaluadas) == 20:
        print(
            "Criterio de formato (3 o más fallas):",
            len(fallas) >= 3
        )
    else:
        print("Muestra incompleta: faltan respuestas reales.")

    print("Resultados guardados en:", ARCHIVO_RESULTADOS)
