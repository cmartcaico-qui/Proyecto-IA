# Límites de autonomía del agente ProjectPulse

**Proyecto:** ProjectPulse

## 1. Herramientas y nivel de riesgo

ProjectPulse es una solución de inteligencia artificial generativa orientada al seguimiento de proyectos mediante el análisis de actas, correos electrónicos y documentos.

Su objetivo es identificar compromisos, responsables, fechas de cumplimiento, pendientes y riesgos, facilitando el seguimiento mediante checklist, semáforos y alertas.

Para establecer sus límites de autonomía se consideran las siguientes herramientas:

| Herramienta propuesta | Riesgo | Justificación |
|---|---|---|
| `identificar_compromisos` | Bajo | Extrae compromisos, responsables y fechas sin modificar la información original. |
| `identificar_pendientes` | Bajo | Identifica actividades que requieren seguimiento. Solo realiza análisis. |
| `evaluar_riesgos` | Bajo | Detecta posibles retrasos, incumplimientos e información faltante sin modificar registros. |
| `actualizar_seguimiento` | Medio | Modificaría estados, responsables o fechas en el registro de seguimiento. Los cambios deberían poder revertirse. |
| `enviar_alertas` | Alto | Enviaría comunicaciones externas que podrían contener información incorrecta o llegar a destinatarios equivocados. |


Esta clasificación corresponde al diseño previsto de ProjectPulse. Las herramientas de escritura y notificación todavía requieren implementación e integración.

### Herramientas implementadas en ProjectPulse

En el archivo `src/agente_projectpulse.py` se integraron
las siguientes herramientas:

| Herramienta | Riesgo | Estado |
|---|---|---|
| `generar_reporte` | Bajo | Implementada. Analiza el texto mediante la cadena de ProjectPulse. |
| `identificar_alertas` | Bajo | Implementada. Analiza riesgos y alertas a partir del texto proporcionado. |
| `proponer_actualizacion` | Bajo en su implementación actual | Implementada como simulación. Prepara propuestas, pero no modifica registros. |

Las tres herramientas utilizan esquemas de validación
con Pydantic.

La actualización real de compromisos y el envío
de comunicaciones externas siguen pendientes
de implementación.

Una futura herramienta de actualización tendrá
mayor nivel de riesgo porque podrá modificar
información del seguimiento.

## 2. Herramientas que requieren aprobación humana

El agente podrá analizar información y proponer acciones de seguimiento sin solicitar autorización para cada consulta de bajo riesgo.

Sin embargo, las acciones que puedan generar consecuencias sobre la gestión de proyectos necesitarán controles adicionales.

Se establecen los siguientes criterios:

- **Identificación de compromisos, pendientes y riesgos:** ejecución automática, con resultados verificables respecto de la fuente original.
- **Actualización de registros:** revisión de cambios relevantes, especialmente modificaciones de responsables, fechas y compromisos previamente confirmados.
- **Envío de alertas externas:** aprobación humana obligatoria antes de enviar correos o notificaciones.

Las herramientas de riesgo alto deberán incorporar un mecanismo de confirmación explícita.

Si la aprobación es rechazada o no se obtiene una autorización válida, la acción no deberá ejecutarse. La implementación actual permite aprobar o rechazar propuestas simuladas mediante consola, sin modificar información real. Los controles de tiempo de espera y autorización de acciones efectivas quedan pendientes.

Este mecanismo seguirá el patrón de supervisión humana desarrollado en los ejercicios genéricos del Bloque 23, donde se implementaron funciones para solicitar y registrar aprobaciones.

### Alcance de la supervisión humana implementada

Actualmente, las herramientas `generar_reporte`,
`identificar_alertas` y `proponer_actualizacion`
no ejecutan modificaciones sobre sistemas externos.

La herramienta `proponer_actualizacion` únicamente
prepara una propuesta que debe verificarse.

Se implementó una función independiente,
`solicitar_aprobacion`, que permite probar
decisiones de aprobación y rechazo mediante consola.

Las decisiones se registran en un archivo JSONL
y no producen modificaciones reales.

Este mecanismo es una simulación de supervisión
humana. No constituye todavía una autorización
integrada a herramientas de escritura o envío
de comunicaciones.

La implementación de controles de aprobación
con tiempo límite, junto con acciones reales,
corresponde a una etapa posterior.

## 3. Revisión de trazas

Se propone registrar las decisiones del agente mediante un archivo de trazabilidad en formato JSONL, siguiendo el mecanismo desarrollado en las clases.

El diseño de trazabilidad contempla los siguientes campos. La implementación actual registra los correspondientes a cada consulta o decisión; el identificador de sesión y la vinculación completa entre ambos tipos de registros quedan pendientes.

- Fecha y hora de la interacción.
- Identificador de sesión.
- Solicitud realizada.
- Herramientas utilizadas.
- Argumentos entregados a las herramientas.
- Observaciones obtenidas.
- Respuesta final del agente.
- Aprobación o rechazo, cuando corresponda.

**Frecuencia de revisión:** semanalmente, mediante una muestra de las interacciones, y revisión individual de las acciones de riesgo alto.

Durante la revisión se buscarán los siguientes comportamientos:

1. Invocaciones repetidas e innecesarias de herramientas.
2. Compromisos identificados sin respaldo en los documentos.
3. Fechas o responsables asignados incorrectamente.
4. Alertas generadas a partir de información incompleta.
5. Respuestas finales que contradigan los resultados de las herramientas.
6. Acciones de riesgo alto sin autorización registrada.

La trazabilidad permitirá identificar errores, revisar las decisiones del agente y mejorar su funcionamiento.

### Evidencia de verificación del Bloque 23

Se verificó el funcionamiento de la trazabilidad
del agente ProjectPulse mediante el archivo local
`src/trazas_projectpulse.jsonl`.

Resultados obtenidos:

- 4 registros JSONL.
- 1 invocación registrada de `generar_reporte`.
- 1 invocación registrada de `identificar_alertas`.
- 1 decisión humana `RECHAZADA`.
- 1 decisión humana `APROBADA_SIMULADA`.

También se verificó la función `solicitar_aprobacion`
en `src/agente_projectpulse.py`:

- Línea 284: definición de la función.
- Línea 446: invocación durante la prueba.

La aprobación humana se utiliza actualmente
en una simulación independiente y no autoriza
modificaciones sobre sistemas reales.

Las trazas permanecen almacenadas localmente
y están excluidas de Git mediante `.gitignore`.

## 4. Procedimiento ante comportamientos inesperados

Si ProjectPulse presenta comportamientos incorrectos, se aplicará el siguiente procedimiento:

1. **Identificar el problema:** localizar la interacción en los registros disponibles.
2. **Revisar la traza:** comprobar las herramientas ejecutadas, sus argumentos y resultados.
3. **Verificar la fuente:** comparar los compromisos, responsables y fechas extraídos con el documento original.
4. **Contener el riesgo:** deshabilitar temporalmente la herramienta involucrada cuando pueda modificar información o generar comunicaciones incorrectas.
5. **Corregir:** ajustar las instrucciones del agente, la descripción de sus herramientas o las validaciones necesarias.
6. **Volver a probar:** ejecutar los casos de prueba correspondientes antes de habilitar nuevamente la funcionalidad.

Las acciones de riesgo alto permanecerán bloqueadas mientras no exista una autorización humana válida.


## 5. Estado actual y limitaciones

ProjectPulse se encuentra en desarrollo y cuenta
con una implementación funcional del agente
correspondiente a la Unidad 2.4.

### Funcionalidades implementadas

- Cadena de procesamiento de tres pasos para
  analizar información de proyectos.
- Clasificación y enrutamiento de solicitudes,
  incluyendo mecanismos de fallback.
- Agente con herramientas mediante LangChain
  y Gemini.
- Memoria conversacional temporal mediante
  `RunnableWithMessageHistory` e
  `InMemoryChatMessageHistory`.
- Validación de argumentos con Pydantic.
- Generación de propuestas simuladas de
  actualización de compromisos.
- Aprobación o rechazo humano mediante
  interacción en consola.
- Registro de decisiones humanas en JSONL.
- Registro de herramientas, argumentos,
  observaciones y respuestas finales en JSONL.

### Validación realizada

Se ejecutaron conjuntamente los archivos:

- `test_cadena_projectpulse.py`
- `test_orquestacion_projectpulse.py`
- `test_agente_projectpulse.py`

Resultado obtenido: **13 pruebas aprobadas**,
sin errores, con una advertencia de obsolescencia
de LangChain.

También se realizaron pruebas manuales de
las consultas del agente, memoria y decisiones
de aprobación y rechazo.

### Limitaciones actuales

- La memoria se almacena temporalmente y se
  pierde al finalizar el proceso.
- Las aprobaciones son simuladas y no están
  conectadas a una herramienta de escritura real.
- No se realizan modificaciones automáticas
  sobre planillas, actas ni sistemas externos.
- No se envían correos ni notificaciones reales.
- Las trazas JSONL se almacenan localmente.
- El registro de consultas todavía no incorpora
  explícitamente el identificador de sesión.
- La revisión semanal de trazas está definida
  como procedimiento previsto, pero no automatizada.
- La validación Pydantic controla la estructura
  de los argumentos, no la veracidad del contenido.
- Las respuestas generadas por el modelo pueden
  contener interpretaciones no respaldadas
  completamente por el documento original.
- No existe todavía una validación automática
  integral de la evidencia utilizada por el agente.
- La aprobación humana actual es una demostración
  independiente del flujo de ejecución del agente.
  No constituye todavía un mecanismo de autorización
  integrado a una herramienta que modifique
  información real. Las propuestas se registran
  como simulaciones y permanecen sin ejecución.

Por estas razones, los compromisos, fechas,
estados y riesgos identificados deben contrastarse
con sus fuentes antes de utilizarse para decisiones
operativas.

Las funciones de checklist, semáforos, recordatorios,
actualización efectiva del seguimiento y alertas
externas corresponden a etapas posteriores
del proyecto.

## 6. Conclusión

ProjectPulse busca apoyar la gestión y seguimiento de proyectos mediante la automatización del análisis de información y la identificación temprana de compromisos y riesgos.

Su autonomía estará limitada a las operaciones que puedan ejecutarse de manera segura, manteniendo supervisión humana sobre las acciones que modifiquen información relevante o generen comunicaciones externas.

El registro de decisiones, la validación de resultados y los mecanismos de aprobación permitirán avanzar hacia un sistema confiable, verificable y alineado con las necesidades de seguimiento de proyectos.