[1mdiff --git a/src/comparar_estrategias.py b/src/comparar_estrategias.py[m
[1mindex c4d277f..20a8b85 100644[m
[1m--- a/src/comparar_estrategias.py[m
[1m+++ b/src/comparar_estrategias.py[m
[36m@@ -36,55 +36,56 @@[m [mdef recomendar_estrategia(respuestas):[m
 [m
     return puntos, ganadoras[m
 [m
[32m+[m[32mif __name__ == "__main__":[m
[32m+[m
[32m+[m[32m    # Ejemplo de la clase: clasificador de errores[m
[32m+[m[32m    respuestas_caso2 = {[m
[32m+[m[32m        "informacion_cambia_seguido": False,[m
[32m+[m[32m        "problema_de_formato_o_tono": True,[m
[32m+[m[32m        "dataset_grande_y_de_calidad": True,[m
[32m+[m[32m        "presupuesto_limitado_o_iterar_rapido": False,[m
[32m+[m[32m        "necesita_multiples_variantes": False[m
[32m+[m[32m    }[m
 [m
[31m-# Ejemplo de la clase: clasificador de errores[m
[31m-respuestas_caso2 = {[m
[31m-    "informacion_cambia_seguido": False,[m
[31m-    "problema_de_formato_o_tono": True,[m
[31m-    "dataset_grande_y_de_calidad": True,[m
[31m-    "presupuesto_limitado_o_iterar_rapido": False,[m
[31m-    "necesita_multiples_variantes": False[m
[31m-}[m
[31m-[m
[31m-puntos, ganadoras = recomendar_estrategia(respuestas_caso2)[m
[32m+[m[32m    puntos, ganadoras = recomendar_estrategia(respuestas_caso2)[m
 [m
[31m-print("Puntajes:", puntos)[m
[31m-print("Técnicas recomendadas:", ganadoras)[m
[32m+[m[32m    print("Puntajes:", puntos)[m
[32m+[m[32m    print("Técnicas recomendadas:", ganadoras)[m
 [m
[31m-# Análisis de sensibilidad: cambiar una respuesta a la vez[m
[32m+[m[32m    # Análisis de sensibilidad: cambiar una respuesta a la vez[m
 [m
[31m-print("\nAnálisis de sensibilidad:")[m
[32m+[m[32m    print("\nAnálisis de sensibilidad:")[m
 [m
[31m-for clave in respuestas_caso2:[m
[31m-    variante = dict(respuestas_caso2)[m
[32m+[m[32m    for clave in respuestas_caso2:[m
[32m+[m[32m        variante = dict(respuestas_caso2)[m
 [m
[31m-    # Invertir solo una respuesta[m
[31m-    variante[clave] = not variante[clave][m
[32m+[m[32m        # Invertir solo una respuesta[m
[32m+[m[32m        variante[clave] = not variante[clave][m
 [m
[31m-    # Recalcular los puntajes[m
[31m-    puntos_v, ganadoras_v = recomendar_estrategia(variante)[m
[32m+[m[32m        # Recalcular los puntajes[m
[32m+[m[32m        puntos_v, ganadoras_v = recomendar_estrategia(variante)[m
 [m
[31m-    # Comprobar si cambian las técnicas recomendadas[m
[31m-    cambio = "CAMBIA" if set(ganadoras_v) != set(ganadoras) else "igual"[m
[32m+[m[32m        # Comprobar si cambian las técnicas recomendadas[m
[32m+[m[32m        cambio = "CAMBIA" if set(ganadoras_v) != set(ganadoras) else "igual"[m
 [m
[31m-    print([m
[31m-        f"{clave} -> {variante[clave]}: "[m
[31m-        f"{ganadoras_v} [{cambio}]"[m
[31m-    )[m
[32m+[m[32m        print([m
[32m+[m[32m            f"{clave} -> {variante[clave]}: "[m
[32m+[m[32m            f"{ganadoras_v} [{cambio}]"[m
[32m+[m[32m        )[m
 [m
[31m-# Segundo caso: bot de atención al cliente[m
[32m+[m[32m    # Segundo caso: bot de atención al cliente[m
 [m
[31m-respuestas_caso1 = {[m
[31m-    "informacion_cambia_seguido": True,[m
[31m-    "problema_de_formato_o_tono": True,[m
[31m-    "dataset_grande_y_de_calidad": False,[m
[31m-    "presupuesto_limitado_o_iterar_rapido": True,[m
[31m-    "necesita_multiples_variantes": False,[m
[31m-}[m
[32m+[m[32m    respuestas_caso1 = {[m
[32m+[m[32m        "informacion_cambia_seguido": True,[m
[32m+[m[32m        "problema_de_formato_o_tono": True,[m
[32m+[m[32m        "dataset_grande_y_de_calidad": False,[m
[32m+[m[32m        "presupuesto_limitado_o_iterar_rapido": True,[m
[32m+[m[32m        "necesita_multiples_variantes": False,[m
[32m+[m[32m    }[m
 [m
[31m-puntos1, ganadoras1 = recomendar_estrategia(respuestas_caso1)[m
[32m+[m[32m    puntos1, ganadoras1 = recomendar_estrategia(respuestas_caso1)[m
 [m
[31m-print("\nSegundo caso:")[m
[31m-print("Puntajes:", puntos1)[m
[31m-print("Técnicas recomendadas:", ganadoras1)[m
[32m+[m[32m    print("\nSegundo caso:")[m
[32m+[m[32m    print("Puntajes:", puntos1)[m
[32m+[m[32m    print("Técnicas recomendadas:", ganadoras1)[m
 [m
