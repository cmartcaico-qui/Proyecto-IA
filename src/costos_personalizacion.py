#Costo de etiquetar datos

def estimar_costo_de_etiquetar(num_ejemplos, minutos_por_ejemplo, costo_por_hora):
    horas = (num_ejemplos * minutos_por_ejemplo) / 60
    costo = horas * costo_por_hora
    return horas, costo


# Ejemplo 1: dataset de 8 ejemplos
horas, costo = estimar_costo_de_etiquetar(8, 5, 25)
print(f"{horas:.2f} horas, aprox ${costo:.2f}")

# Ejemplo 2: dataset de 200 ejemplos
horas2, costo2 = estimar_costo_de_etiquetar(200, 5, 25)
print(f"{horas2:.2f} horas, aprox ${costo2:.2f}")

print(f"Factor de crecimiento en horas: {horas2 / horas:.1f}x")


# Ejercicio: dataset de 500 ejemplos

# Etiquetado inicial: 500 ejemplos, 4 minutos cada uno
horas_base, costo_base = estimar_costo_de_etiquetar(500, 4, 20)

# Segunda revisión: 20% de los ejemplos, 2 minutos cada uno
horas_rev, costo_rev = estimar_costo_de_etiquetar(500 * 0.20, 2, 20)

# Calcular los totales
total_horas = horas_base + horas_rev
total_costo = costo_base + costo_rev
jornadas = total_horas / 8

print(f"\nEtiquetado base: {horas_base:.2f} horas, aprox ${costo_base:.2f}")
print(f"Segunda revisión: {horas_rev:.2f} horas, aprox ${costo_rev:.2f}")
print(f"Total: {total_horas:.2f} horas, aprox ${total_costo:.2f}")
print(f"Jornadas de 8 horas: {jornadas:.1f}")
