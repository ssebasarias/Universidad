# Importar librerías
import requests
import pandas as pd
import json

# Hacer petición GET a la url
url = "https://pokeapi.co/api/v2/pokemon/?limit=151"
response = requests.get(url)
data = response.json()

# Crear lista vacía
pokemons = []

# Iterar sobre los resultados
for result in data["results"]:
  pokemon_url = result["url"]
  pokemon_response = requests.get(pokemon_url)
  pokemon_data = pokemon_response.json()

  # Extraer los datos de interés
  name = result["name"]
  zone = pokemon_data["location_area_encounters"]
  abilities = [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
  photo = pokemon_data["sprites"]["front_default"]
  width = pokemon_data["weight"]
  height = pokemon_data["height"]

  # Crear diccionario con los datos
  pokemon_dict = {
    "name": name,
    "zone": zone,
    "photo": photo,
    "width": width,
    "height": height
  }

  # Añadir una variable "abilityX" por cada habilidad del Pokemon
  for i in range(len(abilities)):
    key = f"ability{i+1}"
    value = abilities[i]
    pokemon_dict[key] = value

  # Añadir diccionario a la lista
  pokemons.append(pokemon_dict)

# Crear dataframe de pandas
df = pd.DataFrame(pokemons)

# Escribir el dataframe en un archivo CSV, separando cada columna por comas y sin incluir índices
df.to_csv("pokemons.csv", index=False, sep=",")
