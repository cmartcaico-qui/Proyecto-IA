import json
import time

from prompts.banco import BANCO_DE_PROMPTS

from consumir_gemini import (MODELO, armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json)
registro = {}

try:
    #leer el archivo y guardarlo en una variable
    for prompt in BANCO_DE_PROMPTS:

        exitos = 0
        intentos = 3

        print("\n" + "=" * 70)
        print(f"PROBANDO PROMPT: {prompt['nombre']}")
        print(f"MODELO: {MODELO}")
        print("=" * 70)

        for intento in range(intentos):

            print(f"\n--- Intento {intento + 1} de {intentos} ---")

            try:
                url, body = armar_peticion(
                    pregunta=prompt["ejemplo_usuario"],
                    modelo=MODELO,
                    system_instruction=prompt["system_instruction"],
                    response_schema=prompt["response_schema"]
                )

                respuesta = enviar_peticion(url, body)

                texto = extraer_texto(respuesta)

                datos = parsear_respuesta_json(
                    texto,
                    prompt["claves_esperadas"]
                )

                exitos += 1

                print("Resultado: RESPUESTA VÁLIDA")
                print(f"Respuesta: {datos}")

            except ValueError as error:
                print("Resultado: RESPUESTA NO VÁLIDA")
                print(f"Detalle: {error}")

            except RuntimeError as error:
                print("Resultado: ERROR EN LA API")
                print(f"Detalle: {error}")

            time.sleep(2)

        print("\n" + "-" * 50)
        print(f"RESUMEN: {prompt['nombre']}")
        print(f"Respuestas válidas: {exitos}/{intentos}")
        print("-" * 50)

        registro[prompt["nombre"]] = {
            "exitos": exitos,
            "intentos": intentos
        }

    with open(
        "prompts/registro_resultados.json",
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            registro,
            archivo,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("VALIDACIÓN TERMINADA")
    print("=" * 70)

    for nombre, resultado in registro.items():
        print(
            f"{nombre}: "
            f"{resultado['exitos']}/{resultado['intentos']} respuestas válidas"
        )

    print("\nRegistro guardado en prompts/registro_resultados.json")


except (ValueError, RuntimeError) as error:
    print("\nNo se pudo completar la operación:", error)