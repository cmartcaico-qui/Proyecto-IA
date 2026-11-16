
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Corpus de ejemplo de la clase 25
corpus_ejemplo = [
    "Los pedidos se pueden cancelar dentro de las primeras 24 horas despues de "
    "realizados, sin costo adicional.",

    "Las devoluciones se aceptan hasta 30 dias despues de la entrega, siempre que "
    "el producto este sin usar.",

    "El reembolso se procesa en un plazo de 5 a 10 dias habiles despues de recibir "
    "el producto devuelto.",

    "Los productos en oferta o liquidacion no tienen devolucion, salvo defecto de "
    "fabrica.",

    "El envio de una devolucion corre por cuenta del cliente, excepto cuando el "
    "producto llego danado.",
]

# Dividir los textos en chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20
)

chunks = splitter.create_documents(corpus_ejemplo)

# Mostrar los resultados
print(f"{len(chunks)} chunks generados")

for i, chunk in enumerate(chunks):
    print(f"--- chunk {i} ({len(chunk.page_content)} caracteres) ---")
    print(chunk.page_content)

# Verificar integridad
vacios = [
    i for i, c in enumerate(chunks)
    if not c.page_content.strip()
]

textos = [c.page_content for c in chunks]

hay_duplicados = len(textos) != len(set(textos))

total_chars_chunks = sum(len(c.page_content) for c in chunks)
total_chars_corpus = sum(len(d) for d in corpus_ejemplo)

print("Chunks vacíos:", vacios)
print("Hay duplicados:", hay_duplicados)
print("Caracteres en chunks:", total_chars_chunks)
print("Caracteres originales:", total_chars_corpus)

from rag_indexer import indexar_corpus, cargar_vectorstore

# Carpeta independiente para esta prueba
CARPETA_DB = "vectorstore_bloque25"
"""
# Indexar el corpus y guardar los embeddings
indexar_corpus(
    corpus=corpus_ejemplo,
    persist_directory=CARPETA_DB,
    chunk_size=150,
    chunk_overlap=20
)
"""
#print("Indexación terminada.")

# Recuperar la base de datos ya existente
vs = cargar_vectorstore(CARPETA_DB)

# Verificar cuántos chunks están almacenados
print("Chunks almacenados:", vs._collection.count())

# Consultar el contenido
datos = vs.get()

print("IDs almacenados:", datos["ids"])

for i, texto in enumerate(datos["documents"], start=1):
    print(f"Documento {i}: {texto}")