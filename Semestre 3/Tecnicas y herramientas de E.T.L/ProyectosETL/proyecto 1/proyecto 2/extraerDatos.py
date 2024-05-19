import csv
import requests

# Configura tu api_key obtenida al registrarte en OpenWeatherMap
api_key = "5a938992046e6dbf5b30536e68d78446"

# Define una lista de ciudades utilizando la API Cities500
api_url = f"https://api.cities500.com/v1/cities?min_population=500000&key={api_key}"
response = requests.get(api_url)

if response.status_code == 200:
    cities_data = response.json()["data"]
    cities = [{"id": city["city_id"], "name": city["city"]} for city in cities_data]
    # La lista de ciudades se encuentra ahora en la variable 'cities'
else:
    print("Error al obtener los datos de la API Cities500")

# Abre un archivo CSV para escribir los datos
with open("datos_clima.csv", mode="w", newline="") as csv_file:
    fieldnames = ["Ciudad", "Temperatura Actual (ºC)", "Descripción del Clima"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Escribe la cabecera del archivo CSV
    writer.writeheader()

    # Extrae los datos de cada ciudad y escribe una fila en el archivo CSV para cada una
    for city in cities:
        try:
            # Hacer una solicitud GET a la API de OpenWeatherMap para obtener los datos de la ciudad actual
            url = f"http://api.openweathermap.org/data/2.5/weather?id={city['id']}&units=metric&appid={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Extraer los datos necesarios de la ciudad actual
            city_name = city["name"]
            current_temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]

            # Escribir una fila en el archivo CSV para la ciudad actual
            writer.writerow({"Ciudad": city_name, "Temperatura Actual (ºC)": current_temp, "Descripción del Clima": weather_desc})
        except requests.exceptions.HTTPError:
            print(f"Error al obtener los datos de la ciudad {city['name']}")

print("Los datos han sido guardados en el archivo datos_clima.csv.")
