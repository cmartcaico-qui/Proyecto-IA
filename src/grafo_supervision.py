import uuid
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class Estado(TypedDict):
    version_nueva: str
    aprobado: bool


def proponer_version(estado: Estado):
    print(
        "Nodo: proponer_version, version propuesta:",
        estado["version_nueva"]
    )
    return {}


def punto_supervision(estado: Estado):
    decision = interrupt({
        "motivo": "Aprobar una nueva version del prompt de ProjectPulse",
        "version_propuesta": estado["version_nueva"]
    })

    return {"aprobado": decision}


def desplegar(estado: Estado):
    print("Nodo: desplegar. Aprobado =", estado["aprobado"])

    if estado["aprobado"]:
        print(
            "-> Version",
            estado["version_nueva"],
            "autorizada para ProjectPulse"
        )
    else:
        print(
            "-> Cambio RECHAZADO. "
            "Se mantiene la version anterior de ProjectPulse."
        )

    return {}


def nuevo_thread_id(prefijo="despliegue"):
    return f"{prefijo}-{uuid.uuid4().hex[:8]}"


def resolver(app, config, aprobar: bool):
    snapshot = app.get_state(config)

    if not snapshot.next:
        raise ValueError(
            "Este proceso no tiene ninguna aprobacion pendiente"
        )

    return app.invoke(
        Command(resume=aprobar),
        config=config
    )


if __name__ == "__main__":
    print("--- SUPERVISION HUMANA DE PROJECTPULSE ---")

    grafo = StateGraph(Estado)

    grafo.add_node("proponer_version", proponer_version)
    grafo.add_node("punto_supervision", punto_supervision)
    grafo.add_node("desplegar", desplegar)

    grafo.add_edge(START, "proponer_version")
    grafo.add_edge("proponer_version", "punto_supervision")
    grafo.add_edge("punto_supervision", "desplegar")
    grafo.add_edge("desplegar", END)

    app = grafo.compile(checkpointer=InMemorySaver())

    # PROCESO 1: APROBACION
    config = {
        "configurable": {
            "thread_id": nuevo_thread_id()
        }
    }

    resultado = app.invoke(
        {
            "version_nueva": "3a1af342e5cc",
            "aprobado": False
        },
        config=config
    )

    print("Estado tras interrupcion:", resultado)

    snapshot = app.get_state(config)
    print("Siguiente nodo pendiente:", snapshot.next)
    print("Detalle de interrupcion:", snapshot.interrupts[0].value)

    print("\nReanudando con aprobacion humana")

    resultado_aprobado = resolver(app, config, True)
    print("Estado final:", resultado_aprobado)

    # PROCESO 2: RECHAZO
    config2 = {
        "configurable": {
            "thread_id": nuevo_thread_id()
        }
    }

    app.invoke(
        {
            "version_nueva": "v3-prueba",
            "aprobado": False
        },
        config=config2
    )

    print("\nReanudando con rechazo humano")

    resultado_rechazado = resolver(app, config2, False)
    print("Estado final del rechazo:", resultado_rechazado)