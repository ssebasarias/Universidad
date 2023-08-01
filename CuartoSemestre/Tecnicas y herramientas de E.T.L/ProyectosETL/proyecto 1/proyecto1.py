import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Autenticación de la aplicación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="271281128da74d6695918702533b11dd",
                                               client_secret="853b86474eca4242b17dea8ad3e3d9e8",
                                               redirect_uri="http://localhost:3000",
                                               scope=["user-read-recently-played"]))

# Obtener las últimas canciones escuchadas
recent_tracks = sp.current_user_recently_played(limit=50)["items"]

# Crear una lista de diccionarios con detalles de canciones
song_details = []
for track in recent_tracks:
    song_info = {}
    song_info["titulo_cancion"] = track["track"]["name"]
    song_info["genero"] = track["track"]["album"].get("genres", [""])[0]
    duration_ms = track["track"]["duration_ms"]
    song_info["duracion"] = f"{int(duration_ms/60000)}:{int((duration_ms/1000)%60):02d}"
    song_details.append(song_info)

# Escribir detalles de canciones en archivo CSV
with open("detalles_canciones.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["titulo_cancion", "genero", "duracion"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for song in song_details:
        writer.writerow(song)
