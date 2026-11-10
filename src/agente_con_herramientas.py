from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool  #herramientas
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)
from langchain_core.prompts import(
    ChatPromptTemplate, #me permite agregar system_instructions y user(human)
    MessagesPlaceholder #me ayuda a tener un historial
)
load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

#Tool/herramienta, es ua función común de python. Descripción en lenguaje natural, será lo que el modelo lea (pronpt) para decidir si elige o no esa herramienta

@tool
def buscar_en_documentacion(consulta:str) -> str:
    """
    Busca información relevante de la documentación internadel producto.
    Usar cuando la pregunta es sobre cómo funciona algo del sistema.
    """
    documentacion = {
        "reintentos": "El cliente reintenta hasta 3 veces ante un TimeError, con espera creciente.",
        "costos": "El costo se calcula a partir de total TokenCount, según la tarifa vigente" 
    }

    for  clave, texto in documentacion.items():
        if clave in consulta.lower():
            return texto
    return "No se encontró  información sobre esa consulta en la documentación."

@tool
def calcular(expresion:str) -> str:
    """
    Evalua una expresión aritmética, como '350 + 250'.
    Usar cuando la pregunta requiere un cálculo numérico.
    """
    permitido = set("0123456789+-*/(). ")
    
    if not set (expresion) <= permitido:
            return "Expresión no permitida."
    try:
         return str(eval(expresion))
    except Exception as e:
         return f"Error al evaluar: {e}"

herramientas = [buscar_en_documentacion, calcular]   #lista de herramientas

#Plantilla system_instructions
promp_agente = ChatPromptTemplate.from_messages([
    (
        "system", "Eres un asistente que responde preguntas usando herramientas disponibles cuando las necesites."
    ),
    (
        "human", "{entrada}"
    ),
    MessagesPlaceholder("agent_scratchpad") #MessagePlaceholder es el espacio donde langchain va anotando los pasos/ciclos, razona-actua-observar, qué herramietas llamó y que devolvieron
])

#Agente: modelo, herramientas, Prompt, formato
agente = create_tool_calling_agent(
     modelo, herramientas, promp_agente
)

#Orquestador: es el que controla el ciclo entre razonar-actuar-observar
ejecutor_agente = AgentExecutor(
    agent=agente,
    tools=herramientas,
    verbose=True, #Imprime los pasos que va siguiendo
)

resultado = ejecutor_agente.invoke(
    {"entrada": "¿Cuánto es 343+219?"}
)

print("Respuesta Final:", resultado["output"][0]["text"])