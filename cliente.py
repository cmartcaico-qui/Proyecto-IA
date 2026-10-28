import time #vamos a indicar que lo vuelva intentar luego de cierta cantidad de segundos
from typing import Callable, Any

from src.consumir_gemini import armar_peticion, extraer_texto, enviar_peticion

def con_reintento(                                #función, intentos, espera_segundos. Valor de retorno: CUALQUIERA
	funcion: Callable[[], Any],
	intentos: int = 3,                            #iterar la cantidad de intentos
	espera_segundos: int = 2,
) -> Any:
	for intento in range(intentos):        #intentar ejecutar la función
		try:
			return funcion()
		except TimeoutError:                      #TimeoutError:
			if intento == intentos-1:
				raise                             #raise
			print(f"Intento {intento+1} de {intentos} falló por límite de uso/servidor. Reintentando...")
			time.sleep(espera_segundos)             #time.sleep(cantidad_segundos)

#cómo lo ejecuto?
url, cuerpo = armar_peticion("Hola")

respuesta = con_reintento(
    lambda: enviar_peticion(url, cuerpo)             #lambda = "guarda esta acción para ejecutarla después"
)

texto = extraer_texto(respuesta)

print(texto)