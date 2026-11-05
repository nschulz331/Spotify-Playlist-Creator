import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

def get_spotify_client():
    # Set up Spotify OAuth credentials from secrets
    auth_manager = SpotifyOAuth(
        client_id=st.secrets.get("SPOTIPY_CLIENT_ID"),
        client_secret=st.secrets.get("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=st.secrets.get("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private",
        cache_path=".cache",
    )
    return spotipy.Spotify(auth_manager=auth_manager)

def create_playlist(sp, playlist_name, songs):
    # Create a private playlist directly on the current user's account
    playlist = sp.current_user_playlist_create(
        name=playlist_name, 
        public=False
    )

    track_uris = []
    for song in songs:
        results = sp.search(q=song, type="track", limit=1)
        tracks = results.get("tracks", {}).get("items", [])
        if tracks:
            track_uris.append(tracks[0]["uri"])

    if track_uris:
        sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)

    return playlist["external_urls"]["spotify"]