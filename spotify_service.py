import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler

sp_oauth = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope="playlist-modify-public playlist-modify-private",
    cache_handler=MemoryCacheHandler()
)
def create_playlist(sp, playlist_name, songs):
    # 1. Get your personal Spotify user ID
    user_id = sp.current_user()['id']
    
    # 2. Create a brand new, empty playlist on your profile
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist['id']
    
    # 3. Search Spotify for each song Gemini generated
    track_uris = []
    for song in songs:
        # We search by both track name and artist to ensure we get the right version
        query = f"track:{song['title']} artist:{song['artist']}"
        search_result = sp.search(q=query, type='track', limit=1)
        
        # If Spotify successfully finds a match, grab its unique URI code
        if search_result['tracks']['items']:
            track_uri = search_result['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
            
    # 4. Push all the found songs into the playlist in one batch
    if track_uris:
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
        
    # 5. Return the web link so Streamlit can make it clickable
    return playlist['external_urls']['spotify']
