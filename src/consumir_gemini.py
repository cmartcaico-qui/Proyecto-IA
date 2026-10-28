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

import time

import json
import re

load_dotenv()

# Constantes
# Modelo por defecto de ProjectPulse
MODELO = "gemini-3.1-flash-lite"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

# Función para crear la solicitud
def armar_peticion(pregunta, modelo=MODELO, system_instruction=None, response_schema=None):  #obtiene url y body
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")

    url = f"{URL_BASE}{modelo}:generateContent?key={API_KEY}"

    body = {"contents": [{"parts": [{"text": pregunta}]}]}

    if system_instruction is not None:
        body["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    if response_schema is not None:
        body["generationConfig"] = {"responseMimeType": "application/json", "responseSchema": response_schema}

    return url, body

# Función que envía la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)  # Establece un tiempo de espera de 30 segundos
    except requests.exceptions.Timeout:
            raise RuntimeError("La solicitud a la API de Gemini ha excedido el tiempo de espera.")
    except requests.exceptions.RequestException:
        raise RuntimeError("Error al enviar la solicitud a la API de Gemini.")

    if respuesta.status_code in (401, 403):
        raise ValueError("Credencial inválida o sin permisos para acceder a la API de Gemini. Verifica tu clave de API y los permisos asociados.")
    if respuesta.status_code >=500:
        raise TimeoutError("El proveedor no pudo procesar la solicitud. Intenta nuevamente más tarde.")
    if respuesta.status_code == 429:
        raise TimeoutError("Límite de solicitudes excedido. Intenta nuevamente más tarde.")

    if respuesta.status_code != 200:
        segundos = respuesta.headers.get("Retry-After")
        mensaje = f"Límite excedido. Reintentar en {segundos} segundos." if segundos else "Límite excedido. Reintentar más tarde."
        raise RuntimeError(
        f"Error en la respuesta. Status Code: {respuesta.status_code}. "
        f"Detalle: {respuesta.text}"
    )

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

def parsear_respuesta_json(texto, claves_requeridas=None):

    #claves_requeridas = ["categoria", "nivel"]

    texto_limpio = texto.strip()

    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)

    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido.")

    if claves_requeridas:
        faltantes = [
            clave
            for clave in claves_requeridas
            if clave not in datos
        ]

        if faltantes:
            raise ValueError(
                f"La respuesta no tiene la estructura esperada. "
                f"Faltan las claves: {faltantes}"
            )

    return datos

# Función principal
def obtener_dato_de_prueba(pregunta): #Es el orquestador, confirma la conexión con la API de Gemini y genera contenido basado en la pregunta proporcionada
   
    response_schema = {
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
                "required": ["responsable", "accion", "fecha"]
            }
        },
        "alertas": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "tipo": {"type": "STRING"},
                    "detalle": {"type": "STRING"},
                    "nivel": {"type": "STRING"}
                },
                "required": ["tipo", "detalle", "nivel"]
            }
        },
        "pendientes": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        },
        "estado": {
            "type": "STRING"
        },
        "sugerencias": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        }
    },
    "required": [
        "compromisos",
        "alertas",
        "pendientes",
        "estado",
        "sugerencias"
    ]
}
   
    system_instruction = (
    "Eres ProjectPulse, un asistente especializado en seguimiento de proyectos. "
    "Analiza únicamente la información entregada. "
    "Identifica compromisos, alertas, responsables, fechas y estado del proyecto. "
    "No inventes información que no aparezca en el texto. "
    "No afirmes que realizaste acciones, configuraste recordatorios o contactaste personas. "
    "Si sugieres una acción, debes identificarla claramente como una sugerencia."
)

    url, body = armar_peticion(pregunta, system_instruction = system_instruction, response_schema = response_schema)
    datos = enviar_peticion(url, body)
    costo=calcular_costo(datos, 0.00000025, 0.00000150) #precio de entrada y salida en dólares
    print(f"Costo de la operación: ${costo:.6f} USD")
    texto = extraer_texto(datos)

    datos_formateados = parsear_respuesta_json(
        texto,
        [
            "compromisos",
            "alertas",
            "pendientes",
            "estado",
            "sugerencias"
        ]
    )

    return datos_formateados

#def calcular_costo(datos:dict, precio_entrada:float, precio_salida:float) -> float
def calcular_costo(datos, precio_entrada, precio_salida):
    #datos=datos["candidates"][0]["metadata"]["tokenUsage"]
    uso=datos["usageMetadata"]
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0) #revisar si existe o no, si no existe, asignar 0
    costo=(tokens_entrada*precio_entrada)+((tokens_salida+tokens_razonamiento)*precio_salida)
    return costo

if __name__ == "__main__":
    try:
        print(obtener_dato_de_prueba("""
El informe debe entregarse el viernes.
Carolina enviará los datos pendientes el miércoles.
Existe riesgo de retraso porque falta validar la información con el cliente.
"""))
    except (ValueError, RuntimeError, TimeoutError) as error:
        print(f"No se pudo completar la operación: {error}")