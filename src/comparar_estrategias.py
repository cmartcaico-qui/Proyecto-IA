#Comparación de estrategias de personalización

def recomendar_estrategia(respuestas):
    puntos = {
        "RAG": 0,
        "Fine-tuning completo": 0,
        "PEFT": 0
    }

    if respuestas["informacion_cambia_seguido"]:
        puntos["RAG"] += 3

    if respuestas["problema_de_formato_o_tono"]:
        puntos["PEFT"] += 2
        puntos["Fine-tuning completo"] += 1

    if respuestas["dataset_grande_y_de_calidad"]:
        puntos["Fine-tuning completo"] += 2
        puntos["PEFT"] += 1

    if respuestas["presupuesto_limitado_o_iterar_rapido"]:
        puntos["RAG"] += 2
        puntos["PEFT"] += 1

    if respuestas["necesita_multiples_variantes"]:
        puntos["PEFT"] += 2

    # Identificar el puntaje más alto
    maximo = max(puntos.values())

    # Conservar todas las técnicas que alcancen ese puntaje
    ganadoras = [
        tecnica for tecnica, puntaje in puntos.items()
        if puntaje == maximo
    ]

    return puntos, ganadoras


# Ejemplo de la clase: clasificador de errores
respuestas_caso2 = {
    "informacion_cambia_seguido": False,
    "problema_de_formato_o_tono": True,
    "dataset_grande_y_de_calidad": True,
    "presupuesto_limitado_o_iterar_rapido": False,
    "necesita_multiples_variantes": False
}

puntos, ganadoras = recomendar_estrategia(respuestas_caso2)

print("Puntajes:", puntos)
print("Técnicas recomendadas:", ganadoras)

# Análisis de sensibilidad: cambiar una respuesta a la vez

print("\nAnálisis de sensibilidad:")

for clave in respuestas_caso2:
    variante = dict(respuestas_caso2)

    # Invertir solo una respuesta
    variante[clave] = not variante[clave]

    # Recalcular los puntajes
    puntos_v, ganadoras_v = recomendar_estrategia(variante)

    # Comprobar si cambian las técnicas recomendadas
    cambio = "CAMBIA" if set(ganadoras_v) != set(ganadoras) else "igual"

    print(
        f"{clave} -> {variante[clave]}: "
        f"{ganadoras_v} [{cambio}]"
    )

# Segundo caso: bot de atención al cliente

respuestas_caso1 = {
    "informacion_cambia_seguido": True,
    "problema_de_formato_o_tono": True,
    "dataset_grande_y_de_calidad": False,
    "presupuesto_limitado_o_iterar_rapido": True,
    "necesita_multiples_variantes": False,
}

puntos1, ganadoras1 = recomendar_estrategia(respuestas_caso1)

print("\nSegundo caso:")
print("Puntajes:", puntos1)
print("Técnicas recomendadas:", ganadoras1)

