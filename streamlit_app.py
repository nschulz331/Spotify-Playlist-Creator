import streamlit as st
from ai_service import generate_song_recommendations
from spotify_service import create_playlist
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Spotify Playlist Creator", layout="wide")
st.title("Spotify AI Playlist Creator")

# --- 1. SPOTIFY LOGIN UI ---
# --- 1. MASTER ACCOUNT BACKGROUND LOGIN ---
sp_oauth = SpotifyOAuth(
    client_id=st.secrets.get("SPOTIPY_CLIENT_ID"),
    client_secret=st.secrets.get("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8080", # Must match exactly, even though it's hidden now
    scope="playlist-modify-public playlist-modify-private"
)

# Fetch a fresh token using the master key in your secrets
token_info = sp_oauth.refresh_access_token(st.secrets.get("SPOTIPY_REFRESH_TOKEN"))

# Log in silently
sp = spotipy.Spotify(auth=token_info['access_token'])

# Optional: Show a quick success message at the top of your app so you know it worked
user_profile = sp.current_user()
st.success(f"Connected behind the scenes as: {user_profile['display_name']}")

# --- 2. MAIN APP UI ---
col1, col2 = st.columns(2)
with col1:
    track_count = st.slider("Number of Tracks", min_value=5, max_value=30, value=10)
with col2:
    mood = st.selectbox("Playlist Mood", ["Any", "Upbeat", "Chill", "Focus", "Party", "Workout", "Sad"])

prompt = st.text_input("What kind of playlist do you want?", placeholder="e.g., Late night study lo-fi, 2000s gym hits...")

if st.button("Create / Add Songs To Playlist", type="primary"):
    playlist_name = prompt if prompt.strip() else f"My {mood} Top Hits"
    
    with st.status("Building your playlist...", expanded=True) as status:
        try:
            st.write(f" Asking Gemini for {track_count} {mood.lower()} song recommendations...")
            songs = generate_song_recommendations(prompt, track_count, mood)
            
            if not songs:
                status.update(label="Failed to get AI recommendations.", state="error")
                st.stop()
            
            st.write(f" Found {len(songs)} songs! Connecting to Spotify...")
            
            st.write(" Creating playlist and adding tracks...")
            # Pass the authenticated 'sp' client directly to your function
            playlist_url = create_playlist(sp, playlist_name, songs)
            
            status.update(label="Playlist Complete!", state="complete", expanded=False)
            st.success(f" '{playlist_name}' created successfully with {len(songs)} tracks!")
            st.markdown(f"[Click here to open your new playlist on Spotify]({playlist_url})")
            
        except Exception as e:
            status.update(label="An error occurred!", state="error")
            st.error(f"Error details: {e}")