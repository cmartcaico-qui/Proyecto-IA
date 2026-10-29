import pytest
import cliente
from unittest.mock import Mock, patch

from cliente import con_reintento, registrar_costo, consultar_modelo
from src.consumir_gemini import enviar_peticion, calcular_costo

@pytest.fixture(autouse=True)
def reiniciar_costo_total():
    cliente.costo_total_sesion = 0
    yield

def test_enviar_peticion_credencial_invalida():
    # Respuesta falsa para no llamar realmente a la API
    respuesta_falsa = Mock()

    # Simulamos que la API responde con error 401
    respuesta_falsa.status_code = 401

    # Reemplazo temporal requests.post por respuesta falsa
    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        
        # Esperamos que enviar_peticion lance un ValueError
        with pytest.raises(ValueError):

            # Se ejecuta la función con datos de prueba
            enviar_peticion("https://url-falsa.com", {"contents": []})

def test_enviar_peticion_limite_de_uso():
    # Se crea una respuesta falsa para no llamar realmente a la API
    respuesta_falsa = Mock()

    # Se simula que la API responde con error 429
    respuesta_falsa.status_code = 429
    respuesta_falsa.headers = {}

    # Reemplazo temporal de requests.post por nuestra respuesta falsa
    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):

        # Que enviar_peticion lance un TimeoutError
        with pytest.raises(TimeoutError):

            # Se ejecuta la función con datos de prueba
            enviar_peticion("https://url-falsa.com", {"contents": []})

def test_enviar_peticion_exito():
    # Crear una respuesta falsa
    respuesta_falsa = Mock()

    # Se simula una respuesta exitosa de la API
    respuesta_falsa.status_code = 200

    # Se simula el JSON que devolvería Gemini
    respuesta_falsa.json.return_value = {"candidates": [{"content": {"parts": [{"text": "Respuesta simulada"}]}}]}

    # Se reemplaza requests.post por la respuesta falsa
    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        respuesta = enviar_peticion("https://url-falsa.com", {"contents": []})

    # Comprobamos que la función devuelve el JSON esperado
    assert respuesta["candidates"][0]["content"]["parts"][0]["text"] == "Respuesta simulada"

def test_con_reintento_funciona():
    # Contador para saber cuántas veces se ejecutó la función
    intentos_realizados = {"cantidad": 0}

    # Función falsa que falla dos veces y funciona en el tercer intento
    def funcion_inestable():
        intentos_realizados["cantidad"] += 1

        if intentos_realizados["cantidad"] < 3:
            raise TimeoutError("Error temporal simulado")

        return "Éxito"

    # Se evita esperar realmente durante la prueba
    with patch("cliente.time.sleep"):
        resultado = con_reintento(funcion_inestable, intentos=3, espera_base=2, espera_maxima=10)

    # Funcionó?
    assert resultado == "Éxito"

    # Se ejecutó 3 veces?
    assert intentos_realizados["cantidad"] == 3

def test_con_reintento_no_reintenta_value_error():
    # Contador para saber cuántas veces se ejecuta la función
    intentos_realizados = {"cantidad": 0}

    # Función falsa que siempre lanza ValueError
    def funcion_con_error():
        intentos_realizados["cantidad"] += 1
        raise ValueError("Credencial inválida")

    # Se espera que el ValueError se propague directamente
    with pytest.raises(ValueError):
        con_reintento(funcion_con_error)

    # Comprobar que solo se intentó una vez
    assert intentos_realizados["cantidad"] == 1

def test_con_reintento_agota_intentos():
    # Contador que permite saber cuántas veces se ejecutó la función
    intentos_realizados = {"cantidad": 0}

    # Función falsa que siempre falla con TimeoutError
    def funcion_que_falla():
        intentos_realizados["cantidad"] += 1
        raise TimeoutError("Error temporal simulado")

    # Par evitar las esperas reales durante la prueba
    with patch("cliente.time.sleep"):

        # Esperamos que, después de agotar los intentos, se propague TimeoutError
        with pytest.raises(TimeoutError):
            con_reintento(funcion_que_falla, intentos=3, espera_base=2, espera_maxima=10)

    # Comprobando que efectivamente lo intentó 3 veces
    assert intentos_realizados["cantidad"] == 3

def test_registrar_costo_acumula():
    
    # Respuesta falsa con uso de tokens
    respuesta_falsa = {"usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5, "thoughtsTokenCount": 0}}

    # Registramos dos operaciones
    cliente.registrar_costo(respuesta_falsa)
    cliente.registrar_costo(respuesta_falsa)

    # Calculamos cuánto debería costar una operación
    costo_unitario = calcular_costo(respuesta_falsa, 0.00000025, 0.00000150)

    # Comprobamos que el acumulado sea el doble
    assert cliente.costo_total_sesion == costo_unitario * 2

def test_consultar_modelo_exito():
    # Simulamos la respuesta que devolvería enviar_peticion
    respuesta_falsa = {"usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5, "thoughtsTokenCount": 0}, "candidates": [{"content": {
                    "parts": [{"text": "Respuesta simulada"}]}}]}

    # Simulamos armar_peticion para no depender de la construcción real
    with patch("cliente.armar_peticion", return_value=("https://url-falsa.com", {"contents": []})):

        # Simulamos enviar_peticion
        with patch("cliente.enviar_peticion", return_value=respuesta_falsa):

            # Simulamos registrar_costo para no mezclar esta prueba con el acumulado
            with patch("cliente.registrar_costo"):

                resultado = consultar_modelo("Hola")

    # Comprobamos que consultar_modelo devuelve el texto esperado
    assert resultado == "Respuesta simulada"

def test_consultar_modelo_convierte_error():
    # Simulando una petición válida
    with patch("cliente.armar_peticion", return_value=("https://url-falsa.com", {"contents": []})):

        # Simulando que todos los reintentos terminan en TimeoutError
        with patch("cliente.con_reintento", side_effect=TimeoutError("Error temporal simulado")):

            # que consultar_modelo transforme el error en RuntimeError
            with pytest.raises(RuntimeError) as error:
                consultar_modelo("Hola")

    # Comprobando que el mensaje sea claro
    assert "varios intentos" in str(error.value)