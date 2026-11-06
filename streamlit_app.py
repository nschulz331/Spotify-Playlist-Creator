import streamlit as st
from ai_service import generate_song_recommendations
from spotify_service import create_playlist
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Spotify Playlist Creator", layout="wide")
st.title("Spotify AI Playlist Creator")

# --- 1. SPOTIFY LOGIN UI ---
sp_oauth = SpotifyOAuth(
    client_id=st.secrets.get("SPOTIPY_CLIENT_ID"),
    client_secret=st.secrets.get("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=st.secrets.get("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public",
    open_browser=False # Critical: Prevents terminal freezes
)

token_info = sp_oauth.get_cached_token()

if not token_info:
    st.warning(" You need to connect your Spotify account first.")
    auth_url = sp_oauth.get_authorize_url()
    st.markdown(f"[** Click here to log in to Spotify**]({auth_url})")
    
    redirect_response = st.text_input("Paste the entire 'localhost' URL here after logging in:")
    
    if redirect_response:
        code = sp_oauth.parse_response_code(redirect_response)
        token_info = sp_oauth.get_access_token(code)
        st.success("Successfully connected! Refreshing...")
        st.rerun()
        
    st.stop() # Stops the rest of the page from loading until logged in

# If authenticated, create the client
sp = spotipy.Spotify(auth=token_info['access_token'])

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