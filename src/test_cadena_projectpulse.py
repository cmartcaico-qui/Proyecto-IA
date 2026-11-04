
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage

from cadena_projectpulse import construir_cadena


def test_cadena_conecta_tres_pasos():

    # Simulamos a Gemini
    modelo_falso = MagicMock()

    # Definimos las tres respuestas simuladas
    modelo_falso.side_effect = [
        AIMessage(
            content="Compromiso: entregar informe el viernes."
        ),
        AIMessage(
            content="Riesgo: faltan registros de asistencia."
        ),
        AIMessage(
            content="COMPROMISOS: entregar informe.\n"
                    "PENDIENTES: registros de asistencia.\n"
                    "ALERTAS: posible retraso."
        )
    ]

    # Construimos la cadena utilizando el modelo falso
    cadena = construir_cadena(modelo_falso)

    # Ejecutamos la cadena
    resultado = cadena.invoke(
        {"texto": "Acta de reunión de seguimiento."}
    )

    # Comprobamos que se ejecutaron los tres pasos
    assert modelo_falso.call_count == 3

    # Comprobamos el resultado final
    assert "COMPROMISOS" in resultado
    assert "PENDIENTES" in resultado
    assert "ALERTAS" in resultado
