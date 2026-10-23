BANCO_DE_PROMPTS = [

    {
        "nombre": "extraer_compromisos",

        "system_instruction": (
            "Eres ProjectPulse, un asistente especializado en seguimiento de proyectos. "
            "Tu tarea es identificar compromisos explícitos en reuniones, actas, correos "
            "o reportes. No inventes responsables ni fechas. "
            "Si un responsable o una fecha no aparecen en el texto, indica 'No especificado'."
        ),

        "ejemplo_usuario": (
            "Durante la reunión se acordó que Carolina enviará los datos pendientes "
            "el miércoles. El equipo deberá entregar el informe final el viernes."
        ),

        "claves_esperadas": ["compromisos"],

        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "compromisos": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "responsable": {"type": "STRING"},
                            "accion": {"type": "STRING"},
                            "fecha": {"type": "STRING"}
                        },
                        "required": [
                            "responsable",
                            "accion",
                            "fecha"
                        ]
                    }
                }
            },
            "required": ["compromisos"]
        }
    },

    {
        "nombre": "detectar_alertas",

        "system_instruction": (
            "Eres ProjectPulse, un asistente especializado en seguimiento de proyectos. "
            "Tu tarea es detectar riesgos, retrasos, bloqueos o situaciones que requieran "
            "seguimiento. Analiza únicamente la información entregada y no inventes hechos. "
            "Clasifica cada alerta con nivel bajo, medio o alto."
        ),

        "ejemplo_usuario": (
            "El informe debe entregarse el viernes, pero aún falta validar la información "
            "con el cliente. Si la validación no se completa a tiempo, existe riesgo de retraso."
        ),

        "claves_esperadas": ["alertas"],

        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "alertas": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "tipo": {"type": "STRING"},
                            "detalle": {"type": "STRING"},
                            "nivel": {"type": "STRING"}
                        },
                        "required": [
                            "tipo",
                            "detalle",
                            "nivel"
                        ]
                    }
                }
            },
            "required": ["alertas"]
        }
    },

    {
        "nombre": "generar_estado_proyecto",

        "system_instruction": (
            "Eres ProjectPulse, un asistente especializado en seguimiento de proyectos. "
            "Evalúa el estado general del proyecto utilizando únicamente la información "
            "proporcionada. Clasifica el estado como verde, amarillo o rojo. "
            "Verde significa avance normal sin alertas relevantes. "
            "Amarillo significa que existen pendientes o riesgos que requieren seguimiento. "
            "Rojo significa que existe un bloqueo, incumplimiento o riesgo crítico. "
            "No inventes información."
        ),

        "ejemplo_usuario": (
            "La integración técnica está funcionando. El informe debe entregarse el viernes, "
            "pero aún falta completar las pruebas finales y validar información con el cliente."
        ),

        "claves_esperadas": [
            "estado",
            "justificacion",
            "proximos_pasos"
        ],

        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "estado": {
                    "type": "STRING"
                },
                "justificacion": {
                    "type": "STRING"
                },
                "proximos_pasos": {
                    "type": "ARRAY",
                    "items": {
                        "type": "STRING"
                    }
                }
            },
            "required": [
                "estado",
                "justificacion",
                "proximos_pasos"
            ]
        }
    }

]