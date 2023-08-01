import requests

# Hacemos una petición GET a la API
response = requests.get('http://127.0.0.1:5000/books')

# Imprimimos la respuesta de la API
print(response.json())
