from comparar_estrategias import recomendar_estrategia
from pathlib import Path

# Problema que queremos resolver

problema = (
    "ProjectPulse ya cuenta con componentes para analizar información "
    "de seguimiento e identificar compromisos, pendientes y riesgos. "
    "Sin embargo, todavía no tiene integrado un mecanismo que permita "
    "consultar información actualizada de actas, informes y registros "
    "de seguimiento, manteniendo la evidencia de las fuentes utilizadas. "
    "Esta necesidad debe resolverse para avanzar hacia la generación "
    "de alertas, semáforos e informes de avance."
)

print("Problema de ProjectPulse:")
print(problema)


# Evaluación inicial de ProjectPulse
# False en criterios sin evidencia suficiente no significa
# que se haya demostrado que el problema no existe.

respuestas_mi_caso = {
    "informacion_cambia_seguido": False,
    "problema_de_formato_o_tono": False,
    "dataset_grande_y_de_calidad": False,
    "presupuesto_limitado_o_iterar_rapido": True,
    "necesita_multiples_variantes": False
}

puntos, ganadoras = recomendar_estrategia(respuestas_mi_caso)

print("\nEvaluación inicial de ProjectPulse:")
print("Puntajes:", puntos)
print("Técnicas candidatas:", ganadoras)

# Paso 3: Análisis de sensibilidad

variante = dict(respuestas_mi_caso)

# Simular que confirmamos actualizaciones mensuales
variante["informacion_cambia_seguido"] = True

puntos_variante, ganadoras_variante = recomendar_estrategia(variante)

print("\nEscenario con actualización mensual confirmada:")
print("Puntajes:", puntos_variante)
print("Técnicas candidatas:", ganadoras_variante)


# Paso 4: Generar el documento del CORE

def generar_esqueleto_decision(problema, puntos, ganadoras):
    lineas = [
        "# Decisión de personalización: ProjectPulse",
        "",
        "## 1. El problema",
        problema,
        "",
        "## 2. Resultado del método de decisión",
    ]

    for tecnica, puntaje in sorted(
        puntos.items(), key=lambda x: -x[1]
    ):
        lineas.append(f"- {tecnica}: {puntaje} puntos")

    if len(ganadoras) > 1:
        lineas.append("")
        lineas.append(
            f"**Empate entre: {', '.join(ganadoras)}**"
        )

    lineas.extend([
        "",
        "## 3. Técnica elegida y por qué",
        "[COMPLETAR: justificar la técnica elegida]",
        "",
        "## 4. Qué necesitarías para ejecutarla",
        "[COMPLETAR: cuantificar los documentos pendientes]",
    ])

    return "\n".join(lineas)


documento = generar_esqueleto_decision(
    problema,
    puntos,
    ganadoras
)

ruta_documento = Path("decision_personalizacion.md")

if not ruta_documento.exists():
    ruta_documento.write_text(documento, encoding="utf-8")
    print("\nDocumento generado: decision_personalizacion.md")
else:
    print("\nEl documento ya existe. No se sobrescribió.")
