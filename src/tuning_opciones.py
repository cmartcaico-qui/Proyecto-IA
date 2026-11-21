
from google.genai import types

# Mostrar los modos de personalización disponibles
print("Modos de tuning disponibles:")

for modo in types.TuningMode:
    print(" ", modo)

# Mostrar los tamaños de adapter disponibles
print("\nTamaños de adapter disponibles (solo PEFT):")

for tamanio in types.AdapterSize:
    print(" ", tamanio)

# Explorar los parámetros de configuración del entrenamiento
print("\nParámetros de entrenamiento:")

for campo in ["epoch_count", "learning_rate_multiplier", "batch_size"]:
    try:
        descripcion = types.CreateTuningJobConfig.model_fields[campo].description
        print(campo, "->", descripcion)
    except KeyError:
        print(campo, "-> este campo no existe en tu versión del SDK")
