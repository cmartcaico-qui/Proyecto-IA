import json
from google.genai import types
from collections import Counter

# Paso 1: construir un dataset de ejemplo

ejemplos_raw = [
    (
        "TimeoutError: la conexion tardo mas de 10 segundos en responder.",
        {
            "categoria": "red",
            "accion_sugerida": "reintentar con backoff exponencial"
        }
    ),
    (
        "ValueError: la clave de API no tiene el formato esperado.",
        {
            "categoria": "autenticacion",
            "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"
        }
    ),
    (
        "429 RESOURCE_EXHAUSTED: se supero el limite de peticiones por minuto.",
        {
            "categoria": "cuota",
            "accion_sugerida": "esperar y reintentar, con backoff"
        }
    ),
    
    (
        "API key not valid. Please pass a valid API key.",
        {
            "categoria": "autenticacion",
            "accion_sugerida": "revisar GEMINI_API_KEY, no reintentar"
        }
    ),
    (
        "RuntimeError: Your system has an unsupported version of sqlite3.",
        {
            "categoria": "entorno",
            "accion_sugerida": "instalar pysqlite3-binary"
        }
    ),
    (
        "ModuleNotFoundError: No module named langchain_chroma.",
        {
            "categoria": "entorno",
            "accion_sugerida": "instalar dependencia faltante"
        }
    ),
    (
        "PermissionError al crear la carpeta del vector store.",
        {
            "categoria": "entorno",
            "accion_sugerida": "revisar permisos de escritura"
        }
    ),
    (
        "InvalidArgumentError: Collection expecting embedding with dimension of 768, got 1536.",
        {
            "categoria": "consistencia_indice",
            "accion_sugerida": "reindexar con el mismo modelo de embeddings"
        }
    )
]

# Convertir los ejemplos al formato que utiliza el SDK
examples = [
    types.TuningExample(
        text_input=texto,
        output=json.dumps(salida, ensure_ascii=False)
    )
    for texto, salida in ejemplos_raw
]
"""
print(len(examples), "ejemplos construidos")
print(examples[0])
"""
if __name__ == "__main__":
    print(len(examples), "ejemplos construidos")
    print(examples[0])

# Paso 2: Validar el dataset

def validar_dataset(examples, claves_esperadas=("categoria", "accion_sugerida")):
    problemas = []
    vistos = set()

    for i, ej in enumerate(examples):

        # Comprobar que la entrada no esté vacía
        if not ej.text_input or not ej.text_input.strip():
            problemas.append(f"ejemplo {i}: text_input vacío")

        # Comprobar que la salida no esté vacía
        if not ej.output or not ej.output.strip():
            problemas.append(f"ejemplo {i}: output vacío")
            continue

        # Comprobar si la entrada está duplicada
        if ej.text_input in vistos:
            problemas.append(f"ejemplo {i}: text_input duplicado")

        vistos.add(ej.text_input)

        # Verificar que la salida sea un JSON válido
        try:
            salida = json.loads(ej.output)
        except json.JSONDecodeError:
            problemas.append(f"ejemplo {i}: output no es JSON válido")
            continue

        # Verificar los campos obligatorios
        for clave in claves_esperadas:
            if clave not in salida:
                problemas.append(
                    f'ejemplo {i}: output no tiene la clave "{clave}"'
                )

    return problemas

"""
# Ejecutar la validación
problemas = validar_dataset(examples)

print(f"\n{len(examples)} ejemplos, {len(problemas)} problemas encontrados")

for problema in problemas:
    print(" -", problema)
"""

# Ejecutar la validación solo cuando se ejecuta este archivo
if __name__ == "__main__":
    problemas = validar_dataset(examples)

    print(f"\n{len(examples)} ejemplos, {len(problemas)} problemas encontrados")

    for problema in problemas:
        print(" -", problema)

# Paso 3: Comprobar el balance del dataset

def chequear_balance(ejemplos_raw):
    categorias = Counter(
        salida["categoria"] for _, salida in ejemplos_raw
    )
    return categorias

"""
balance = chequear_balance(ejemplos_raw)

print("\nBalance de categorías:")

for categoria, cuenta in balance.most_common():
    print(f"{categoria}: {cuenta}")

maximo = max(balance.values())
minimo = min(balance.values())

print(f"\nCategoría más representada: {maximo} ejemplos")
print(f"Categoría menos representada: {minimo} ejemplos")
print(f"Razón max/min: {maximo / minimo:.1f}x")
"""

if __name__ == "__main__":
    balance = chequear_balance(ejemplos_raw)

    print("\nBalance de categorías:")

    for categoria, cuenta in balance.most_common():
        print(f"{categoria}: {cuenta}")

    maximo = max(balance.values())
    minimo = min(balance.values())

    print(f"\nCategoría más representada: {maximo} ejemplos")
    print(f"Categoría menos representada: {minimo} ejemplos")
    print(f"Razón max/min: {maximo / minimo:.1f}x")

"""
# Paso 4: Comprobar que el validador detecta errores

examples_rotos = examples + [
    types.TuningExample(
        text_input="",
        output='{"categoria": "red"}'
    ),
    types.TuningExample(
        text_input=ejemplos_raw[0][0],
        output="no es json"
    )
]

problemas2 = validar_dataset(examples_rotos)

print("\nPrueba con errores intencionales:")
print(f"{len(examples_rotos)} ejemplos, {len(problemas2)} problemas encontrados")

for problema in problemas2:
    print(" -", problema)
"""

# Paso 4: Comprobar que el validador detecta errores

if __name__ == "__main__":
    examples_rotos = examples + [
        types.TuningExample(
            text_input="",
            output='{"categoria": "red"}'
        ),
        types.TuningExample(
            text_input=ejemplos_raw[0][0],
            output="no es json"
        )
    ]

    problemas2 = validar_dataset(examples_rotos)

    print("\nPrueba con errores intencionales:")
    print(f"{len(examples_rotos)} ejemplos, {len(problemas2)} problemas encontrados")

    for problema in problemas2:
        print(" -", problema)
