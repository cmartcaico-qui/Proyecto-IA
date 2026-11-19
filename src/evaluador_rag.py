from rag_indexer import cargar_vectorstore
from datetime import date

def precision_at_k(ids_recuperados: list[str], ids_relevantes: set[str]) -> float:
    """
    ids_recuperados: los que me trajo el retriever
    De los 'k' chunks que me trajo el retriever, ¿qué fracción realmente sirve?
    Devuelve 0.0 si el retriever no devolvió ningún id
    """
    if not ids_recuperados:
        return 0.0

    # Recorro los IDs recuperados y compruebo cuáles son relevantes
    acertados = [i for i in ids_recuperados if i in ids_relevantes]

    return len(acertados) / len(ids_recuperados)

def recall_at_k(ids_recuperados: list[str], ids_relevantes: set[str]) -> float | None:
    """
    Exhaustividad
    De todos los chunks relevantes que existen en mi corpus, ¿qué fracción logré rescatar?
    Devuelve None si la pregunta no tiene respuesta en el corpus (ids_relevantes es vacío)
    """
    if not ids_relevantes:
        return None

    acertados = [i for i in ids_recuperados if i in ids_relevantes]
    return len(acertados) / len(ids_relevantes)


def f1_score(precision: float, recall: float | None) -> float:
    """
    Media armónica entre precisión y exhaustividad: equilibrio entre ambas para comparar
    configuraciones distintas de k o chunk_size.
    """
    if recall is None or (precision + recall) == 0:
        return 0.0
       
    return 2 * precision * recall / (precision + recall)

def promediar(valores):
    """
    Calcula el promedio de las métricas, ignorando los None.
    """
    validos = [v for v in valores if v is not None]

    return sum(validos) / len(validos) if validos else 0.0

def evaluar_recuperacion(retriever, casos: list[dict], k: int = 3):
    """
    Correr cada caso del conjunto de evaluaciones contra el retriever real de Chroma
    y va a calcular precisión, recall y F1
    """
    resultados = []

    for caso in casos:
        #1.- Consultamos al retriever, cuáles son los chunks que me regresa la invocación. SI GASTA TOKENS
        chunks = retriever.invoke(caso["pregunta"])

        #2.- Extraer los IDs
        ids_recuperados = [c.id for c in chunks]

        #3.- Calculamos las métricas
        p = precision_at_k(ids_recuperados, caso["ids_relevantes"])
        r = recall_at_k(ids_recuperados, caso["ids_relevantes"])
        f1 = f1_score(p, r)

        #4.- Agregar esas métricas a los resultados
        resultados.append({
            "pregunta": caso["pregunta"],
            "ids_recuperados": ids_recuperados,
            "precision": p,
            "recall": r,
            "f1": f1
        })
    return resultados

def guardar_reporte(resultados, k):
    """
    Guarda las métricas de recuperación para comparar
    distintas configuraciones de RAG.
    """
    precision_promedio = promediar(
        r["precision"] for r in resultados
    )

    recall_promedio = promediar(
        r["recall"] for r in resultados
    )

    f1_promedio = promediar(
        r["f1"] for r in resultados
    )

    nombre_archivo = f"resultados_evaluacion_k{k}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(f"Fecha: {date.today()}\n")
        archivo.write(
            f"Configuración: k={k}, chunk_size=200, chunk_overlap=30\n\n"
        )

        for r in resultados:
            recall = (
                "n/a" if r["recall"] is None
                else f"{r['recall']:.2f}"
            )

            archivo.write(
                f"Precisión: {r['precision']:.2f} | "
                f"Recall: {recall} | "
                f"F1: {r['f1']:.2f} | "
                f"{r['pregunta']}\n"
            )

        archivo.write(
            f"\nPromedios:\n"
            f"Precisión: {precision_promedio:.3f}\n"
            f"Recall: {recall_promedio:.3f}\n"
            f"F1: {f1_promedio:.3f}\n"
        )

    print(f"\nReporte guardado en: {nombre_archivo}")

if __name__ == "__main__":
    CARPETA_DB = "vectorstore_ejemplo"
    K = 3

    vs = cargar_vectorstore(CARPETA_DB)
  
    casos_evaluacion = [
        {
            "pregunta": "¿Cuáles son los errores de credenciales inválidas?",
            "ids_relevantes": {
                "8938b823-a4f9-420d-bf57-a6135f1ab5a6",
                "dbaa4dce-a6e2-4b34-ae8a-ac148f5d7919",
                "4fd51473-0e31-4107-a21d-26743098e463"
            }
        },
        {
            "pregunta": "¿Cuántos reintentos realiza el cliente ante un fallo de conexión?",
            "ids_relevantes": {
                "752352be-41d0-47bf-aec3-635d91f20b1b",
                "5ec58783-7df3-41fd-ad4d-2ac50a616f62"
            }
        },
        {
            "pregunta": "¿Qué ocurre cuando se supera el límite de peticiones?",
            "ids_relevantes": {
                "c7d25858-18f9-4789-8b6c-4ff538d4d667",
                "d1d554e0-6833-4d9c-bd01-3d96be530636",
                "fc0d9336-6297-4905-98ef-52627ccbc106"
            }
        },
        {
            "pregunta": "¿Cuántos créditos consume una operación de escritura?",
            "ids_relevantes": {
                "48f6b641-5efd-49fe-8306-7674c3f2f069"
            }
        },
        {
            "pregunta": "¿Qué sucede cuando se agotan los tres intentos de conexión?",
            "ids_relevantes": {
                "bcbd0adb-03b9-4bb3-bf90-3364f35e57ca"
            }
        },
        {
            "pregunta": "¿Cuántos segundos espera el cliente en cada reintento?",
            "ids_relevantes": {
                "5ec58783-7df3-41fd-ad4d-2ac50a616f62"
            }
        },
        {
            "pregunta": "¿Qué debe verificarse si la API Key es inválida o el token ha expirado?",
            "ids_relevantes": {
                "4fd51473-0e31-4107-a21d-26743098e463"
            }
        },
        {
            "pregunta": "¿Qué ocurre cuando se ejecuta el método client.close()?",
            "ids_relevantes": {
                "20e3906a-40f8-4af0-96b2-75968ed42609"
            }
        }
    ]
    
    # Crear el retriever con el valor de K
    retriever = vs.as_retriever(search_kwargs={"k": K})

    # Evaluar las ocho preguntas
    resultados = evaluar_recuperacion(retriever, casos_evaluacion, K)

    # Mostrar los resultados
    for resultado in resultados:
        print(f"\nPregunta: {resultado['pregunta']}")
        print(f"IDs recuperados: {resultado['ids_recuperados']}")
        print(f"Precisión: {resultado['precision']:.2f}")

        if resultado["recall"] is None:
            print("Exhaustividad: No aplica")
        else:
            print(f"Exhaustividad: {resultado['recall']:.2f}")

        print(f"F1: {resultado['f1']:.2f}")

    # Guardar el reporte con los promedios
    guardar_reporte(resultados, K)
