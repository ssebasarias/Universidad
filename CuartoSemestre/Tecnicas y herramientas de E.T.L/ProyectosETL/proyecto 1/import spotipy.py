import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Autenticación de la aplicación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="271281128da74d6695918702533b11dd",
                                               client_secret="853b86474eca4242b17dea8ad3e3d9e8",
                                               redirect_uri="http://localhost:3000",
                                               scope=["user-read-recently-played", "playlist-modify-public"]))

# Obtener las últimas canciones escuchadas
recent_tracks = sp.current_user_recently_played(limit=30)["items"]
track_uris = [track["track"]["uri"] for track in recent_tracks]

# Crear una nueva playlist y agregar canciones
playlist = sp.user_playlist_create(user=sp.current_user()["id"], name="Mis últimas canciones escuchadas")    
sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)  