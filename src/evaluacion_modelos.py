import time
import consumir_gemini


def evaluar_modelo(
    nombre_modelo,
    pregunta,
    precio_entrada,
    precio_salida,
    repeticiones=4
):
    """
    Evalúa un modelo utilizando la misma pregunta varias veces.

    Mide:
    - latencia de cada petición
    - costo de cada petición
    - respuesta generada
    - latencia promedio
    - costo total
    """

    print("=" * 70)
    print(f"EVALUANDO MODELO: {nombre_modelo}")
    print("=" * 70)

    latencias = []
    costos = []

    for i in range(1, repeticiones + 1):

        print(f"\n--- Intento {i} de {repeticiones} ---")

        # 1. Armar la petición para el modelo que estamos evaluando
        try:

            url, body = consumir_gemini.armar_peticion(pregunta, nombre_modelo)

            # 2. Medir latencia
            inicio = time.perf_counter()

            datos = consumir_gemini.enviar_peticion(url, body)

            fin = time.perf_counter()

            latencia = fin - inicio
            latencias.append(latencia)

            # 3. Calcular costo
            costo = consumir_gemini.calcular_costo(datos, precio_entrada, precio_salida)

            costos.append(costo)

            # 4. Extraer la respuesta
            respuesta = consumir_gemini.extraer_texto(datos)

            # 5. Mostrar resultado
            print(f"Latencia: {latencia:.2f} segundos")
            print(f"Costo: ${costo:.6f} USD")
            print("Respuesta:")
            print(respuesta)

        except (ValueError, RuntimeError) as error:
            print(f"Intento {i} falló: {error}")

        time.sleep(2)

    # 6. Calcular resumen
    latencia_promedio = sum(latencias) / len(latencias)
    costo_total = sum(costos)
    costo_promedio = costo_total / len(costos)

    print("\n" + "-" * 70)
    print(f"RESUMEN: {nombre_modelo}")
    print("-" * 70)

    print("Latencias:", [round(latencia, 2) for latencia in latencias])

    print(f"Latencia promedio: {latencia_promedio:.2f} segundos")

    print(f"Costo promedio por petición: ${costo_promedio:.6f} USD")

    print(f"Costo total ({repeticiones} peticiones): "f"${costo_total:.6f} USD")

    print()


pregunta_prueba = """
A partir del siguiente resumen de una reunión de proyecto, identifica:

1. Dos compromisos.
2. Un riesgo.
3. Un pendiente.
4. El estado general del proyecto.

Resumen:
El equipo confirmó que el informe debe entregarse el viernes.
Carolina enviará los datos pendientes el miércoles.
Existe riesgo de retraso porque aún falta validar la información con el cliente.
La integración técnica está funcionando, pero falta completar las pruebas finales.
"""


modelos = [
    {
        "nombre": "gemini-3.6-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    },
    {
        "nombre": "gemini-3-flash-preview",
        "precio_entrada": 0.00000050,
        "precio_salida": 0.00000300
    },
    {
        "nombre": "gemini-3.1-flash-lite",
        "precio_entrada": 0.00000025,
        "precio_salida": 0.00000150
    }
]


for modelo in modelos:

    try:
        evaluar_modelo(
            nombre_modelo=modelo["nombre"],
            pregunta=pregunta_prueba,
            precio_entrada=modelo["precio_entrada"],
            precio_salida=modelo["precio_salida"],
            repeticiones=4
        )

    except (ValueError, RuntimeError) as error:
        print(
            f"No se pudo evaluar el modelo "
            f"{modelo['nombre']}: {error}"
        )