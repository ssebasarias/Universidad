try:
    # Solicitar al usuario los números
    numerosLista = input("Ingrese una lista de números del 1 al 100 separados por comas: ")

    # Convertir la entrada en una lista de números enteros
    numeros = [int(numero.strip()) for numero in numerosLista.split(",")]

    # Validar que los números estén en el rango 1-100
    for num in numeros:
        if num < 1 or num > 100:
            raise ValueError("Todos los números deben estar entre 1 y 100.")

    # Diccionario para clasificar los precios
    diccionario = {}

    for numero in numeros:
        if numero < 10:
            diccionario[numero] = "Es un precio muy bajo."
        elif 10 <= numero <= 50:
            diccionario[numero] = "Es un precio medio."
        else:
            diccionario[numero] = "Es un precio regular."

    # Imprimir clasificación de precios
    print("\nClasificación de precios:")
    for key, value in diccionario.items():
        print(f"Precio {key}: {value}")

    # Obtener el menor y mayor precio ingresado
    precio_minimo = min(numeros)
    precio_maximo = max(numeros)

    print(f"\nEl precio más bajo ingresado es: {precio_minimo}")
    print(f"El precio más alto ingresado es: {precio_maximo}")

# Manejar errores
except ValueError as ve:
    print(f"Error de valor: {ve}")
except Exception as e:
    print(f"Ocurrió un error: {e}")
