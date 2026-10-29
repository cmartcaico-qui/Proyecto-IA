import re
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


    consulta = "¿Qué es Python?"

    referencia = "Python es un lenguaje de programación interpretado."

    respuesta = consultar_modelo(consulta)

    crudo_ref = referencia.split()
    crudo_resp = respuesta.split()

    comunes_crudo = set(crudo_ref) & set(crudo_resp)

    pct_crudo = len(comunes_crudo) / len(set(crudo_ref))

    tokens_ref = procesar_texto(referencia)
    tokens_resp = procesar_texto(respuesta)

    comunes = set(tokens_ref) & set(tokens_resp)

    pct_proc = len(comunes) / len(set(tokens_ref))

    print(f"[Caso 1] Coincidencia texto crudo: {pct_crudo:.1%}")
    print(f"[Caso 1] Coincidencia texto procesado: {pct_proc:.1%}")

    consulta = "¿Qué es un compromiso dentro de un proyecto?"

    referencia = "Un compromiso es una tarea o acción acordada que tiene un responsable y una fecha de cumplimiento."

    respuesta = consultar_modelo(consulta)

    crudo_ref = referencia.split()
    crudo_resp = respuesta.split()

    comunes_crudo = set(crudo_ref) & set(crudo_resp)

    pct_crudo = len(comunes_crudo) / len(set(crudo_ref))

    tokens_ref = procesar_texto(referencia)
    tokens_resp = procesar_texto(respuesta)

    comunes = set(tokens_ref) & set(tokens_resp)

    pct_proc = len(comunes) / len(set(tokens_ref))

    print(f"[Caso 2] Coincidencia texto crudo: {pct_crudo:.1%}")
    print(f"[Caso 2] Coincidencia texto procesado: {pct_proc:.1%}")

    consulta = "¿Qué es un riesgo en la gestión de proyectos?"

    referencia = "Un riesgo es una situación que puede afectar el cumplimiento de los objetivos, plazos o resultados de un proyecto."

    respuesta = consultar_modelo(consulta)

    crudo_ref = referencia.split()
    crudo_resp = respuesta.split()

    comunes_crudo = set(crudo_ref) & set(crudo_resp)

    pct_crudo = len(comunes_crudo) / len(set(crudo_ref))

    tokens_ref = procesar_texto(referencia)
    tokens_resp = procesar_texto(respuesta)

    comunes = set(tokens_ref) & set(tokens_resp)

    pct_proc = len(comunes) / len(set(tokens_ref))

    print(f"[Caso 3] Coincidencia texto crudo: {pct_crudo:.1%}")
    print(f"[Caso 3] Coincidencia texto procesado: {pct_proc:.1%}")