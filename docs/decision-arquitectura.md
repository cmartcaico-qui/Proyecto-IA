# Decisión de arquitectura: elección de modelo

Fecha de la comparación: Martes 20 de Octubre del 2026  
Nombre de la miniaplicación: "ProjectPulse"

## Modelo elegido

Elegí el modelo: Pendiente de definir luego de las pruebas.

Mi miniaplicación sirve para: apoyar el seguimiento y gestión de proyectos mediante el análisis de información proveniente de reuniones, documentos, actas y reportes, permitiendo identificar compromisos, riesgos, pendientes y estado general de avance.

Los requisitos que necesito cumplir son:

* Identificar correctamente compromisos, riesgos, pendientes y estado general de un proyecto.
* Entregar respuestas claras, útiles y fáciles de interpretar para apoyar el seguimiento y la toma de decisiones.
* Mantener un equilibrio adecuado entre calidad de respuesta, latencia y costo.

## Diagrama de arquitectura

[Diagrama de Arquitectura](docs/diagrama_arquitectura.png)

## Comparación de candidatos

- Estas son las preguntas y condiciones con las cuales se midieron los modelos:

* Preguntas y/o condiciones:

1. Utilizar exactamente el mismo prompt para todos los modelos.
2. Ejecutar al menos cuatro veces la misma petición con cada modelo para medir la variación de latencia.
3. Evaluar costo, latencia y calidad de la respuesta para una tarea representativa de ProjectPulse.

Prompt utilizado:

> A partir del siguiente resumen de una reunión de proyecto, identifica:
>
> 1. Dos compromisos.
> 2. Un riesgo.
> 3. Un pendiente.
> 4. El estado general del proyecto.
>
> Resumen:
> El equipo confirmó que el informe debe entregarse el viernes.
> Carolina enviará los datos pendientes el miércoles.
> Existe riesgo de retraso porque aún falta validar la información con el cliente.
> La integración técnica está funcionando, pero falta completar las pruebas finales.

| Criterio | Gemini 3.6 Flash | Gemini 3 Flash | Gemini 3.1 Flash Lite |
|---|---|---|---|
| Tarifa de entrada en USD por millón de tokens | Pendiente | Pendiente | Pendiente |
| Tarifa de salida en USD por millón de tokens | Pendiente | Pendiente | Pendiente |
| Latencias observadas en segundos | Pendiente | Pendiente | Pendiente |
| Latencia promedio en segundos | Pendiente | Pendiente | Pendiente |
| Calidad para ProjectPulse | Pendiente | Pendiente | Pendiente |

Fuente de las tarifas:

- Gemini 3.6 Flash: documentación oficial de precios de Gemini API.
- Gemini 3 Flash: documentación oficial de precios de Gemini API.
- Gemini 3.1 Flash Lite: documentación oficial de precios de Gemini API.

Observación sobre las pruebas:

Las pruebas se realizarán utilizando exactamente el mismo prompt para todos los modelos. Cada modelo será ejecutado al menos cuatro veces, ya que la latencia puede variar entre peticiones. La calidad será evaluada considerando si la respuesta identifica correctamente los compromisos, riesgos, pendientes y estado general solicitado para una tarea representativa de ProjectPulse.

## Justificación

Elegimos el modelo _______ porque para nuestra aplicación _______.

Lo que observé en las pruebas fue _______.

El criterio más relevante para mi decisión fue _______.

Una limitación que encontré en mi elección fue _______.

## Alternativa descartada y por qué

Descarté el/los modelos _______ porque _______.