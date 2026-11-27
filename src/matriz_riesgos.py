def puntaje_riesgo(probabilidad, impacto):
    return probabilidad * impacto


def categoria_riesgo(puntaje):
    if puntaje >= 15:
        return "CRITICO"

    if puntaje >= 9:
        return "ALTO"

    if puntaje >= 4:
        return "MEDIO"

    return "BAJO"

mis_riesgos = [
    {
        "riesgo": "Inyeccion de instrucciones maliciosas en documentos recuperados por RAG",
        "probabilidad": 4,
        "impacto": 4,
        "mitigacion": "Filtro de patrones y delimitacion del contexto (Bloque 31)"
    },
    {
        "riesgo": "Respuestas sobre compromisos sin respaldo en los documentos",
        "probabilidad": 3,
        "impacto": 4,
        "mitigacion": "Prompt que exige citas y reconoce contexto insuficiente (Bloque 31)"
    },
    {
        "riesgo": "Exposicion de datos personales contenidos en documentos academicos",
        "probabilidad": 3,
        "impacto": 5,
        "mitigacion": "Evitar textos completos en logs y registrar huellas (Bloque 31)"
    },
    {
        "riesgo": "Activacion de una nueva version del prompt sin autorizacion",
        "probabilidad": 2,
        "impacto": 4,
        "mitigacion": "Registro de versiones y supervision con interrupt (Bloque 32)"
    },
    {
        "riesgo": "Fechas o responsables incorrectos en informes de seguimiento",
        "probabilidad": 3,
        "impacto": 4,
        "mitigacion": (
        "Trazabilidad de consultas y fuentes mediante logging (Bloque 31). "
        "Control propuesto: validacion humana de fechas y responsables antes de distribuir informes."
        )
    }
]

# Calcular el puntaje y la categoria de cada riesgo
for r in mis_riesgos:
    r["puntaje"] = puntaje_riesgo(
        r["probabilidad"],
        r["impacto"]
    )

    r["categoria"] = categoria_riesgo(r["puntaje"])

# Mostrar los riesgos ordenados de mayor a menor
for r in sorted(mis_riesgos, key=lambda x: -x["puntaje"]):
    print(f"{r['categoria']:8} ({r['puntaje']:2}) - {r['riesgo']}")

def esta_en_el_limite(probabilidad, impacto):
    categoria_actual = categoria_riesgo(
        puntaje_riesgo(probabilidad, impacto)
    )

    vecinos = [
        (probabilidad + 1, impacto),
        (probabilidad - 1, impacto),
        (probabilidad, impacto + 1),
        (probabilidad, impacto - 1),
    ]

    for p2, i2 in vecinos:
        if not (1 <= p2 <= 5 and 1 <= i2 <= 5):
            continue

        if categoria_riesgo(puntaje_riesgo(p2, i2)) != categoria_actual:
            return True

    return False

# Identificar los riesgos que estan al limite
for r in mis_riesgos:
    r["al_limite"] = esta_en_el_limite(
        r["probabilidad"],
        r["impacto"]
    )

    if r["al_limite"]:
        print("Revisar con otra persona:", r["riesgo"])

# Puntos de supervision para riesgos ALTOS y CRITICOS
puntos_supervision = {
    "Inyeccion de instrucciones maliciosas en documentos recuperados por RAG":
        "Detener la consulta si se detectan instrucciones sospechosas y solicitar revision humana antes de reincorporar el documento.",

    "Exposicion de datos personales contenidos en documentos academicos":
        "Solicitar autorizacion humana antes de compartir informes que contengan datos personales de estudiantes.",

    "Respuestas sobre compromisos sin respaldo en los documentos":
        "Solicitar revision humana antes de utilizar un compromiso que no tenga respaldo documental verificable.",

    "Fechas o responsables incorrectos en informes de seguimiento":
        "Solicitar validacion humana de fechas y responsables antes de distribuir el informe."
}

print("\n--- PUNTOS DE SUPERVISION ---")

for r in mis_riesgos:
    if r["categoria"] in ("ALTO", "CRITICO"):
        print("\nRiesgo:", r["riesgo"])
        print("Supervision:", puntos_supervision[r["riesgo"]])

print("\n--- VALIDACION DE LA MATRIZ ---")

for r in mis_riesgos:
    print("\nRiesgo:", r["riesgo"])
    print("Probabilidad:", r["probabilidad"])
    print("Impacto:", r["impacto"])
    print("Puntaje:", r["puntaje"])
    print("Categoria:", r["categoria"])
    print("Mitigacion:", r["mitigacion"])

    if r["categoria"] in ("ALTO", "CRITICO"):
        print("Punto de supervision:", puntos_supervision[r["riesgo"]])