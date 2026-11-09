import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials

# Authenticate using App Keys only (bypasses user login & 403 errors entirely)
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=st.secrets["SPOTIPY_CLIENT_ID"],
        client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    )
)
# Function to search Spotify for tracks without creating a user playlist
def search_tracks_from_gemini(songs):
    ui_tracks = []  # Stores song details, web links, and preview audio
    # Loop through each song provided by Gemini
    for song in songs:
        query = f"track:{song['title']} artist:{song['artist']}" if isinstance(song, dict) else str(song) #query: handles whether Gemini returns a dictionary:  {'title': ..., 'artist': ...})  formats cleanly.
        search_result = sp.search(q=query, limit=1, type='track') #sp.search(...): Asks Spotify for the top matching track for that query.

        # If Spotify found a match, save its details and audio preview
        if search_result['tracks']['items']: #if search_result makes sure spotify actually returned a song and converts to list of dictionaries 
            track = search_result['tracks']['items'][0]
            ui_tracks.append({
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "url": track['external_urls']['spotify'],
                "preview_url": track.get('preview_url')
            })
        return ui_tracks  # Returns the list of dicts to the Streamlit app

