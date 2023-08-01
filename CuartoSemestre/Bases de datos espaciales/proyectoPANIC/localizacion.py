import googlemaps
from geopy.geocoders import Nominatim

# Inicializar el cliente de Google Maps
gmaps = googlemaps.Client(key='AIzaSyC8DY4m2uCQJ_5CG7tNSinSIr4MjZGBf7A')

# Obtener la ubicación actual del dispositivo
geolocator = Nominatim(user_agent="PANIC")
ubicacion_actual = geolocator.geocode("ubicación actual")

# Obtener la dirección de la ubicación actual
direccion = gmaps.reverse_geocode((ubicacion_actual.latitude, ubicacion_actual.longitude))[0]['formatted_address']

# Imprimir la dirección
print("La ubicación actual es:", direccion)
