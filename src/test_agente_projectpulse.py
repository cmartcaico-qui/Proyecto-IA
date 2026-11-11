
import json
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

import agente_projectpulse as proyecto


# === PRUEBA 1: VALIDACIÓN PYDANTIC ===

def test_rechaza_texto_vacio():
    with pytest.raises(ValidationError):
        proyecto.generar_reporte.invoke({"texto": ""})


# === PRUEBA 2: RECHAZO HUMANO ===

def test_rechazo_humano(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "RECHAZAR")

    decision = proyecto.solicitar_aprobacion(
        "Entrega del informe",
        "Completado",
        "Evidencia simulada"
    )

    assert decision == "RECHAZADA"


# === PRUEBA 3: APROBACIÓN SIMULADA ===

def test_aprobacion_simulada(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "APROBAR")

    decision = proyecto.solicitar_aprobacion(
        "Entrega del informe",
        "Completado",
        "Evidencia simulada"
    )

    assert decision == "APROBADA_SIMULADA"


# === PRUEBA 4: REGISTRO DE DECISIÓN ===

def test_registro_decision_jsonl(tmp_path, monkeypatch):
    archivo = tmp_path / "trazas_prueba.jsonl"
    monkeypatch.setattr(proyecto, "ARCHIVO_TRAZAS", archivo)

    proyecto.registrar_traza(
        accion="proponer_actualizacion",
        compromiso="Entrega del informe",
        nuevo_estado="Completado",
        evidencia="Evidencia simulada",
        decision="RECHAZADA"
    )

    registro = json.loads(
        archivo.read_text(encoding="utf-8").strip()
    )

    assert registro["decision_humana"] == "RECHAZADA"
    assert registro["ejecutada"] is False
    assert registro["tipo_ejecucion"] == "simulacion"


# === PRUEBA 5: REGISTRO DE HERRAMIENTAS ===

def test_registro_herramientas_jsonl(tmp_path, monkeypatch):
    archivo = tmp_path / "trazas_prueba.jsonl"
    monkeypatch.setattr(proyecto, "ARCHIVO_TRAZAS", archivo)

    accion = SimpleNamespace(
        tool="identificar_alertas",
        tool_input={"texto": "Texto simulado"}
    )

    resultado = {
        "intermediate_steps": [
            (accion, "Riesgo respaldado por el texto")
        ],
        "output": "Respuesta de prueba"
    }

    proyecto.registrar_traza_agente(
        numero_consulta=1,
        solicitud="Identifica riesgos",
        resultado=resultado
    )

    registro = json.loads(
        archivo.read_text(encoding="utf-8").strip()
    )

    assert registro["tipo_registro"] == "consulta_agente"
    assert len(registro["acciones"]) == 1
    assert registro["acciones"][0]["herramienta"] == "identificar_alertas"
    assert registro["respuesta_final"] == "Respuesta de prueba"
