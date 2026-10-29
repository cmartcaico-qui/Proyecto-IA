import time #vamos a indicar que lo vuelva intentar luego de cierta cantidad de segundos
import random
from typing import Callable, Any

from src.consumir_gemini import (armar_peticion, extraer_texto, enviar_peticion, calcular_costo)

costo_total_sesion = 0

def con_reintento(                                #función, intentos, espera_segundos. Valor de retorno: CUALQUIERA
	funcion: Callable[[], Any],
	intentos: int = 3,                            #iterar la cantidad de intentos
	espera_base: int = 2,
	espera_maxima: int = 10,
) -> Any:
	for intento in range(intentos):        #intentar ejecutar la función
		try:
			return funcion()
		except TimeoutError:                      #TimeoutError:
			if intento == intentos-1:
				raise                             #raise
			espera = min(espera_base * (2 ** intento), espera_maxima)
			espera = espera + random.uniform(0, 1)
			print(f"Intento {intento+1} de {intentos} falló por límite de uso/servidor." f"Reintentando en {espera:.2f} segundos...")
			time.sleep(espera)             #time.sleep(cantidad_segundos)

def registrar_costo(respuesta: dict) -> float:
    global costo_total_sesion

    costo_estimado = calcular_costo(respuesta, 0.00000025, 0.00000150)

    costo_total_sesion += costo_estimado

    print(
        f"Costo de la operación: ${costo_estimado:.6f} USD "
        f"| Costo acumulado de la sesión: ${costo_total_sesion:.6f} USD"
    )

    return costo_estimado

#cómo lo ejecuto?
def consultar_modelo(pregunta):

	url, cuerpo = armar_peticion(pregunta)

	respuesta = con_reintento(
		lambda: enviar_peticion(url, cuerpo)             #lambda = "guarda esta acción para ejecutarla después"
	)
	registrar_costo(respuesta)

	texto = extraer_texto(respuesta)

	return texto

print(consultar_modelo("Hola"))
print(consultar_modelo("Cuéntame algo breve"))
print(consultar_modelo("¿Cuál es la capital de la Región de Los Lagos?"))