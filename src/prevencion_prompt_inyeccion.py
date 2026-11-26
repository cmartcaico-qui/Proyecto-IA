import re

# Patrones que pueden indicar un intento de modificar las instrucciones
PATRONES_SOSPECHOSOS = [
    r"ignora(?:r|\s+las)?\s+(?:todas\s+las\s+)?instrucciones\s+(?:anteriores|previas)",
    r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions",
    r"olvida\s+(?:todo\s+lo\s+)?anterior",
    r"nuevo\s+sistema\s*:",
    r"system\s*prompt\s*:",
    r"revela\s+tu\s+prompt",
]

def detectar_inyeccion(texto):
    texto_normalizado = texto.lower()

    return [
        patron
        for patron in PATRONES_SOSPECHOSOS
        if re.search(patron, texto_normalizado)
    ]

def filtrar_documentos_sospechosos(documentos):
    limpios = []
    descartados = []

    for documento in documentos:
        patrones = detectar_inyeccion(documento.page_content)

        if patrones:
            descartados.append((documento, patrones))
        else:
            limpios.append(documento)

    return limpios, descartados