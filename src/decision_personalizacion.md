# Decisión de personalización: ProjectPulse

## 1. El problema

ProjectPulse ya cuenta con componentes para analizar información de seguimiento e identificar compromisos, pendientes y riesgos. Sin embargo, todavía no tiene integrado un mecanismo que permita consultar información actualizada de actas, informes y registros de seguimiento, manteniendo la evidencia de las fuentes utilizadas.

Esta necesidad debe resolverse para avanzar hacia la generación de alertas, semáforos e informes de avance.

## 2. Resultado del método de decisión

Apliqué las cinco preguntas del método de decisión a la situación actual de ProjectPulse.

- **RAG: 2 puntos.**
- **PEFT: 1 punto.**
- **Fine-tuning completo: 0 puntos.**

La técnica mejor puntuada fue **RAG**.

### Justificación de las cinco respuestas

1. **Información que cambia frecuentemente: False.** Aunque ProjectPulse necesita trabajar con información que puede actualizarse, todavía no he comprobado la frecuencia de modificación de las fuentes durante los últimos tres meses. Por lo tanto, utilizo False de manera provisional.

2. **Problemas de formato o tono: False.** Todavía no he evaluado una muestra de 20 respuestas utilizando una pauta fija para comprobar si al menos 3 presentan problemas de formato o tono. Este criterio permanece pendiente de validación.

3. **Dataset grande y de calidad: False.** Actualmente tengo 10 ejemplos etiquetados de ProjectPulse en `dataset_tuning.py`, distribuidos entre compromisos, pendientes y alertas. No alcanzo los 200 ejemplos utilizados como referencia en el ejercicio.

4. **Presupuesto limitado o iteración rápida: True.** Establezco como requisito de ProjectPulse poder incorporar cambios documentales y comprobar sus efectos en menos de un día, sin realizar nuevos entrenamientos del modelo. Es un objetivo de diseño, no una medición de rendimiento ya realizada.

5. **Múltiples variantes del modelo: False.** Actualmente ProjectPulse contempla un único comportamiento general de seguimiento, sin requerir dos o más variantes entrenadas para distintos clientes o productos.

### Análisis de sensibilidad

Al cambiar únicamente `informacion_cambia_seguido` de False a True, RAG aumenta de 2 a 5 puntos, mientras PEFT mantiene 1 punto y fine-tuning completo 0 puntos.

RAG continúa siendo la técnica mejor puntuada. Este segundo resultado es hipotético, porque todavía falta verificar la frecuencia mensual de actualización documental.

## 3. Técnica elegida y por qué

Elijo **RAG como estrategia principal para ProjectPulse**, porque permite recuperar información desde documentos y proporcionarla como contexto a Gemini sin necesidad de entrenar nuevamente el modelo cuando cambia una fuente.

Actualmente desarrollé un laboratorio RAG utilizando Chroma y Gemini, con recuperación de fragmentos, respuestas con citas y medición de latencia y tokens. Sin embargo, todavía falta integrar este mecanismo con documentación operativa real de ProjectPulse.

No elijo **fine-tuning completo** porque actualmente cuento con 10 ejemplos de práctica, una cantidad inferior a los 200 ejemplos utilizados como referencia en el curso. Además, entrenar el modelo no resolvería directamente la necesidad de consultar información documental actualizada.

**PEFT** podría utilizarse posteriormente si las evaluaciones demostraran dificultades recurrentes en la consistencia del formato o de las clasificaciones. Permitiría ajustar el comportamiento entrenando una cantidad reducida de parámetros, pero actualmente no existe evidencia suficiente para justificar ese entrenamiento.

RAG resulta más adecuado para la necesidad evaluada porque aprovecha los componentes que ya desarrollé y evita incorporar un proceso de entrenamiento que requiere preparación de datos, recursos de cómputo y tiempo adicional.

## 4. Qué necesitarías para ejecutarla

Para incorporar RAG al funcionamiento operativo de ProjectPulse necesito seleccionar, preparar e indexar documentación real de seguimiento de proyectos.

Actualmente cuento con un laboratorio RAG desarrollado con un manual de usuario, pero no tengo documentos operativos reales integrados al agente ProjectPulse.

Como primera etapa, propongo un **corpus piloto de 3 documentos**:

1. Un acta de reunión con acuerdos y responsables.
2. Un registro de seguimiento con compromisos y fechas.
3. Un informe de avance con pendientes y posibles riesgos.

**Estado del piloto propuesto:**

- Documentos previstos: **3**.
- Documentos operativos integrados actualmente al RAG de ProjectPulse: **0**.
- Documentos pendientes de seleccionar, preparar e indexar: **3**.

Para implementar esta etapa necesitaría preparar los textos, dividirlos en fragmentos, generar embeddings, almacenarlos en Chroma e integrar el recuperador con el agente ProjectPulse.

Posteriormente, tendría que comprobar la identificación correcta de compromisos, responsables, plazos y riesgos, verificar las fuentes de cada respuesta y establecer un procedimiento de actualización documental.

Esta implementación aprovecharía el trabajo ya desarrollado con RAG, sin requerir inicialmente fine-tuning ni PEFT.