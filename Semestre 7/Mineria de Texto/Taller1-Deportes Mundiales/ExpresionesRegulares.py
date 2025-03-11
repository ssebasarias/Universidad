import re
from collections import Counter

# Pedir al usuario la introducción de un texto
texto = input("Ingrese un texto sobre tecnología: ")

# Validar que no tenga más de 1000 caracteres (recortar si es necesario)
if len(texto) > 1000:
    texto = texto[:1000]  # Recorta el texto a 1000 caracteres
    print("\nEl texto era muy largo, se ha recortado a 1000 caracteres.\n")

# Contar la cantidad de números en el texto 
numeros = re.findall(r'\d', texto)  # busca todos los dígitos (\d) en el texto
cantidad_numeros = len(numeros)

# Contar la cantidad de letras (sin contar espacios ni caracteres especiales)
letras = re.findall(r'[a-zA-Z]', texto)  # Encuentra todas las letras (mayúsculas y minúsculas)
cantidad_letras = len(letras)

# Identificar la letra y la palabra que más se repiten
conteo_letras = Counter(letras) # # Conteo de letras
letra_mas_repetida = conteo_letras.most_common(1)[0] if conteo_letras else ("Ninguna", 0) # most_common(1)[0] obtiene la letra más repetida y su cantidad.

# Conteo de palabras
palabras = re.findall(r'\b\w+\b', texto.lower())  # Encuentra palabras ignorando mayúsculas/minúsculas
conteo_palabras = Counter(palabras)
palabra_mas_repetida = conteo_palabras.most_common(1)[0] if conteo_palabras else ("Ninguna", 0)

# 6️⃣ Contar cuántas veces aparece la palabra "tecnología"
cantidad_tecnologia = conteo_palabras.get("tecnología", 0)

# 7️⃣ Mostrar los resultados
print(f"\n📊 RESULTADOS 📊")
print(f"📌 Cantidad de números: {cantidad_numeros}")
print(f"📌 Cantidad de letras: {cantidad_letras}")
print(f"📌 Letra más repetida: '{letra_mas_repetida[0]}' con {letra_mas_repetida[1]} repeticiones")
print(f"📌 Palabra más repetida: '{palabra_mas_repetida[0]}' con {palabra_mas_repetida[1]} repeticiones")
print(f"📌 La palabra 'tecnología' aparece {cantidad_tecnologia} veces.")
