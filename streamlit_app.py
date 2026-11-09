import streamlit as st
from ai_service import generate_song_recommendations

# Import our new search function instead of the old create_playlist
from spotify_service import search_tracks_from_gemini

st.set_page_config(page_title="Spotify Playlist Creator", layout="wide")
st.title("Spotify AI Playlist Creator")


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
            
            st.write("Fetching track links and audio previews from Spotify...")
            ui_tracks = search_tracks_from_gemini(songs)
            
            status.update(label="Playlist Ready!", state="complete", expanded=False) #Closes the interactive loading spinner and updates the status header to "Playlist Ready!
            st.success(f"Generated {len(ui_tracks)} tracks for '{playlist_name}'!") #Displays a green notification banner stating how many songs were processed.
            
            for track in ui_tracks: #Loops through every track dictionary returned by your Spotify search.
                col_info, col_link = st.columns([3, 1])
                with col_info:
                    st.subheader(f"{track['name']} - {track['artist']}")
                    if track.get('preview_url'): #Checks if Spotify provides a 30 second audio preview link for this specific song.
                        st.audio(track['preview_url'])
                    else:
                        st.caption("No audio preview available for this track.")
                
                with col_link: #Switches context to the smaller right hand column in the row layout.
                    st.link_button("Listen on Spotify", track['url']) #renders a clickable button that opens track on Spotify.
                    st.divider()
                

        except Exception as e:
            status.update(label="An error occurred!", state="error")
            st.error(f"Error details: {e}")