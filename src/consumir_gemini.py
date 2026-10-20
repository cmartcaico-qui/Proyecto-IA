#import os #interactuar con nuestrosistema operativo
#import requests #realizar solicitudes HTTP
#from dotenv import load_dotenv #cargar variables de entorno desde un archivo .env

#load_dotenv() #cargar variables de entorno desde el archivo .env

#def obtener_dato_de_prueba(pregunta):
#    api_key=os.getenv("GEMINI_API_KEY") #obtener la clave de API de Gemini desde las variables de entorno
#    modelo="gemini-flash-latest" #modelo de Gemini que se va a utilizar



#    url=f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}" #URL de la API de Gemini para generar contenido que me convenga en el momento
#    body={
#        "contents": [
#            {
#                "parts": [
#                    {
#                        "text": pregunta
#                    }
#                ]
#            }
#        ]
#    }

#    respuesta=requests.post(url,json=body) #realizar una solicitud POST a la API de Gemini con el cuerpo de la solicitud en formato JSON
#    print(respuesta)
#    datos=respuesta.json() #convertir la respuesta de la API en un objeto JSON
#    return datos["candidates"][0]["content"]["parts"][0]["text"] #devolver el texto de la primera parte del contenido generado por la API

#print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión funciona"))

#REFACTORIZACIÓN DEL CÓDIGO PARA MEJORAR SU LEGIBILIDAD Y MANTENIBILIDAD

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Constantes
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

# Función para crear la solicitud
def armar_peticion(pregunta): #confirma la conexión con la API de Gemini y genera contenido basado en la pregunta proporcionada
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"

    body = {"contents":[{"parts": [{"text": pregunta}]}]}
    return url, body

# Función que envía la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)  # Establece un tiempo de espera de 30 segundos
    except requests.exceptions.RequestException:
        raise RuntimeError("Error al enviar la solicitud a la API de Gemini.")
    except requests.exceptions.Timeout:
        raise RuntimeError("La solicitud a la API de Gemini ha excedido el tiempo de espera.")

    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la respuesta. Status Code: {respuesta.status_code}")

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no es un JSON válido.")
    
# Función que procesa y extrae el dato
def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no recibe el formato esperado o no contiene datos.")

# Función principal
def obtener_dato_de_prueba(pregunta): #Es el orquestador, confirma la conexión con la API de Gemini y genera contenido basado en la pregunta proporcionada
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    costo=calcular_costo(datos, 0.00000075, 0.00000375) #precio de entrada y salida en dólares
    print(f"Costo de la operación: ${costo:.6f} USD")
    return extraer_texto(datos)

#def calcular_costo(datos:dict, precio_entrada:float, precio_salida:float) -> float
def calcular_costo(datos, precio_entrada, precio_salida):
    #datos=datos["candidates"][0]["metadata"]["tokenUsage"]
    uso=datos["usageMetadata"]
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso["thoughtsTokenCount"] #revisar si existe o no, si no existe, asignar 0
    costo=(tokens_entrada*precio_entrada)+((tokens_salida+tokens_razonamiento)*precio_salida)
    return costo

try:
    print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión funciona"))
except (ValueError, RuntimeError) as error:
    print(f"No se pudo completar la operación: {error}")