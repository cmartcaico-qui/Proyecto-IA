# Decisión de arquitectura: elección de modelo

**Fecha de la comparación:** Jueves 22 de octubre de 2026  
**Nombre de la miniaplicación:** ProjectPulse

## Modelo elegido

Elegí el modelo: **Gemini 3.1 Flash Lite**.

Mi miniaplicación sirve para apoyar el seguimiento y gestión de proyectos mediante el análisis de información proveniente de reuniones, documentos, actas y reportes, permitiendo identificar compromisos, riesgos, pendientes y estado general de avance.

Los requisitos que necesito cumplir son:

- Identificar correctamente compromisos, riesgos, pendientes y estado general de un proyecto.
- Entregar respuestas claras, útiles y fáciles de interpretar para apoyar el seguimiento y la toma de decisiones.
- Mantener un equilibrio adecuado entre calidad de respuesta, latencia y costo.

## Diagrama de arquitectura

[Diagrama de Arquitectura](diagrama_arquitectura.png)

## Comparación de candidatos

Para comparar los modelos se utilizaron las siguientes condiciones de evaluación:

1. Utilizar exactamente el mismo prompt para todos los modelos.
2. Ejecutar cuatro veces la misma petición con cada modelo para medir la variación de latencia.
3. Evaluar costo, latencia y calidad de la respuesta para una tarea representativa de ProjectPulse.

### Prompt utilizado

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

| Criterio | Gemini 3.6 Flash | Gemini 3 Flash Preview | Gemini 3.1 Flash Lite |
|---|---|---|---|
| Tarifa de entrada en USD por millón de tokens | 0.75 USD | 0.50 USD | 0.25 USD |
| Tarifa de salida en USD por millón de tokens | 3.75 USD | 3.00 USD | 1.50 USD |
| Latencias observadas en segundos | 6.55, 6.05, 7.09, 7.55 | 4.31, 4.07, 6.99, 5.11 | 7.26, 5.02, 5.16, 2.92 |
| Latencia promedio en segundos | 6.81 | 5.12 | 5.09 |
| Calidad para ProjectPulse | 4/4 respuestas correctas | 4/4 respuestas correctas | 4/4 respuestas correctas |

### Fuente de las tarifas

- Gemini 3.6 Flash: documentación oficial de precios de Gemini API.
- Gemini 3 Flash Preview: documentación oficial de precios de Gemini API.
- Gemini 3.1 Flash Lite: documentación oficial de precios de Gemini API.

### Criterio de calidad utilizado

Se consideró correcta una respuesta cuando identificó adecuadamente los cuatro elementos solicitados para ProjectPulse:

1. Dos compromisos.
2. Un riesgo.
3. Un pendiente.
4. Un estado general coherente del proyecto.

Los tres modelos identificaron correctamente estos elementos en las cuatro ejecuciones realizadas.

### Observación sobre las pruebas

Las pruebas se realizaron utilizando exactamente el mismo prompt para todos los modelos. Cada modelo fue ejecutado cuatro veces, ya que la latencia puede variar entre peticiones.

La calidad se evaluó considerando si cada respuesta identificaba correctamente los compromisos, el riesgo, el pendiente y el estado general solicitado para una tarea representativa de ProjectPulse.

## Justificación

Elegí el modelo **Gemini 3.1 Flash Lite** porque, para la tarea evaluada de ProjectPulse, logró identificar correctamente los compromisos, riesgos, pendientes y estado general del proyecto en las cuatro ejecuciones realizadas.

Lo que observé en las pruebas fue que los tres modelos entregaron resultados correctos y comparables en términos de calidad. Sin embargo, Gemini 3.1 Flash Lite obtuvo la menor latencia promedio, con **5.09 segundos**, y presentó un costo por petición considerablemente menor que los otros dos modelos evaluados.

El criterio más relevante para mi decisión fue mantener un equilibrio entre calidad, latencia y costo. Al no observar una mejora significativa en la calidad de los modelos de mayor costo para esta tarea específica, Gemini 3.1 Flash Lite resulta suficiente para las necesidades actuales de ProjectPulse.

Una limitación de esta elección es que la comparación se realizó sobre una tarea representativa y acotada de ProjectPulse. En tareas futuras de mayor complejidad podría ser necesario volver a evaluar si el modelo mantiene el mismo nivel de calidad.

## Alternativa descartada y por qué

Descarté **Gemini 3.6 Flash** y **Gemini 3 Flash Preview** como modelos principales para esta etapa de ProjectPulse porque, aunque ambos entregaron respuestas correctas, no mostraron una mejora observable en calidad respecto de Gemini 3.1 Flash Lite para la tarea evaluada.

Gemini 3.6 Flash presentó además la mayor latencia promedio y el mayor costo por petición. Gemini 3 Flash Preview mejoró considerablemente la latencia respecto de Gemini 3.6 Flash, pero continuó teniendo un costo superior al de Gemini 3.1 Flash Lite sin entregar una ventaja clara en la calidad observada.