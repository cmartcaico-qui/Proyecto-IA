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

load_dotenv()

def obtener_dato_de_prueba(pregunta): #pregunta = 
    api_key = os.getenv("GEMINI_API_KEY")
    modelo = "gemini-flash-latest"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
#Constantes
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#función para crear la solicitud
def armar_peticion(pregunta): #pregunta = "Confirma la conexion"
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}" #url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=MI API KEY"
    body = {
        "contents": [
        {
            "parts": [
            {
                "text": pregunta
            }
            ]
        "contents": 
            [{"parts": [{"text": pregunta}]}]
        }
        ]
    }
    return url, body

#armar_peticion_openai -> url, body

#función envía la petición
def enviar_peticion(url, body):
    respuesta = requests.post(url, json=body)
    datos = respuesta.json()
    return respuesta.json()

#funcion procesa y extrae dato
def extraer_texto(datos): #Gemini
    return datos["candidates"][0]["content"]["parts"][0]["text"]

def obtener_dato_de_prueba(pregunta): #pregunta = "Confirma la conexion"
    url, body = armar_peticion(pregunta) #obtiene url y body
    #url = resultado de armar_peticion
    #body = resultado de armar_peticion
    datos = enviar_peticion(url, body)
    return extraer_texto(datos)

print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión funciona"))