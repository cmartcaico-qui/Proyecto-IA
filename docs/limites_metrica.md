# Límites de la métrica de evaluación

## Qué mide

La métrica compara la coincidencia de palabras entre una respuesta generada y una referencia previamente definida. Para ello utiliza precisión, cobertura y F1, considerando también las repeticiones de palabras.

La métrica permite identificar cuánto vocabulario de la referencia aparece en la respuesta y cuánto contenido adicional contiene la respuesta, pero no evalúa directamente si ambas expresan el mismo significado.

## Modos de falla conocidos

### 1. Una respuesta correcta y extensa puede obtener un F1 muy bajo

En varios casos revisados, la respuesta del modelo fue correcta y completa, pero obtuvo un F1 bajo porque desarrolló el concepto con muchas palabras adicionales que no aparecían en la referencia.

Ejemplo: en la consulta "¿Para qué sirve identificar riesgos en un proyecto?", la respuesta fue evaluada como factualmente correcta, completa y sin contradicciones, pero obtuvo un F1 de 0.0371.

Esto muestra que un F1 bajo no necesariamente significa que la respuesta sea incorrecta.

### 2. La información adicional disminuye la precisión aunque sea pertinente

La métrica penaliza las explicaciones adicionales porque compara las palabras de la respuesta con una referencia mucho más breve.

Ejemplo: en "¿Qué es un responsable dentro de un proyecto?", la respuesta explicó correctamente el rol del responsable y además incorporó funciones y la matriz RACI. La revisión manual la calificó como correcta y completa, pero obtuvo un F1 de 0.0460.

Por lo tanto, una respuesta más detallada puede obtener una puntuación menor aunque aporte información correcta.

### 3. La métrica puede dar una valoración baja cuando la respuesta cubre el significado con una formulación diferente

En "¿Qué significa que una tarea esté atrasada?", el modelo explicó correctamente que una tarea atrasada es aquella que superó su plazo sin completarse. La revisión manual la calificó como correcta, completa y sin contradicciones, pero obtuvo un F1 de 0.0381.

Esto evidencia que la coincidencia de palabras no representa completamente la similitud de significado.

### 4. La revisión manual puede detectar diferencias de completitud que el F1 no explica por sí solo

En la consulta "¿Qué es el estado de un proyecto?", la respuesta fue factualmente correcta y no presentó contradicciones, pero la completitud fue calificada como parcial porque no desarrolló directamente los pendientes y compromisos principales incluidos en la referencia.

Su F1 fue de 0.0458.

Esto demuestra que el número por sí solo no permite determinar qué información específica está presente o ausente.

### 5. Un F1 relativamente mayor tampoco debe interpretarse automáticamente como una respuesta perfecta

El caso con mayor F1 de la muestra fue "¿Qué representa el color verde en un semáforo de proyecto?", con un F1 de 0.1162.

La revisión manual confirmó que en este caso la respuesta era correcta, completa y sin contradicciones. Sin embargo, incluso el valor más alto obtenido sigue siendo bajo en términos absolutos debido a la diferencia de extensión entre las referencias breves y las respuestas detalladas del modelo.

Por este motivo, los valores de F1 deben interpretarse de manera relativa dentro de este pipeline y no como una medida absoluta de calidad.

## Muestra revisada

Se generaron 20 respuestas utilizando `consultar_modelo`, y para cada una se calcularon precisión, cobertura y F1 mediante `calcular_metricas`.

Para la revisión manual se seleccionaron 10 casos:

- los 5 resultados con menor F1;
- los 5 resultados con mayor F1.

Cada caso fue evaluado según tres criterios:

- corrección factual;
- completitud;
- contradicción.

Además, se agregó una nota cualitativa para explicar la evaluación realizada.

La revisión mostró que varias respuestas con F1 muy bajo eran, al mismo tiempo, factualmente correctas, completas y sin contradicciones. El principal patrón observado fue que las respuestas generadas eran considerablemente más extensas que las referencias, reduciendo la precisión y, por consecuencia, el F1.

## Recomendación de uso

En este pipeline, el F1 debe utilizarse como una señal comparativa inicial y no como un criterio único para determinar la calidad de una respuesta.

Puede ser útil para ordenar resultados, detectar diferencias entre ejecuciones y seleccionar casos que requieren revisión.

Sin embargo, para ProjectPulse se recomienda complementar siempre la métrica automática con revisión cualitativa cuando la respuesta contenga información relevante para la gestión del proyecto, especialmente compromisos, responsables, fechas, riesgos, pendientes o alertas.

Una puntuación baja no debe utilizarse automáticamente para descartar una respuesta, ya que la revisión realizada mostró casos correctos con valores de F1 bajos.