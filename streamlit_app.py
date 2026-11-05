import streamlit as st
from ai_service import generate_song_recommendations
from spotify_service import create_playlist, get_spotify_client

st.set_page_config(page_title="Spotify Playlist Creator", layout="wide")
st.title(" Spotify AI Playlist Creator")

prompt = st.text_input("What kind of playlist do you want?", placeholder="e.g., Late night study lo-fi, 2000s gym hits...")

if st.button("Create / Add Songs To Playlist", type="primary"):
    if not st.secrets.get("SPOTIPY_CLIENT_ID"):
        st.error("Please configure your Spotify Credentials inside your Streamlit secrets file.")
    else:
        playlist_name = prompt if prompt.strip() else "My Daily Top Hits"
        
        # st.status creates a dropdown menu showing exactly what step the code is on
        with st.status("Building your playlist...", expanded=True) as status:
            try:
                st.write(" Asking Gemini for song recommendations...")
                songs = generate_song_recommendations(prompt)
                
                if not songs:
                    # Stops the app from continuing if the AI failed to return songs
                    status.update(label="Failed to get AI recommendations.", state="error")
                    st.stop()
                
                st.write(f" Found {len(songs)} songs! Connecting to Spotify...")
                sp = get_spotify_client()
                
                st.write(" Creating playlist and adding tracks...")
                playlist_url = create_playlist(sp, playlist_name, songs)
                
                # If everything succeeds, close the status box and show the success link
                status.update(label="Playlist Complete!", state="complete", expanded=False)
                st.success(f" '{playlist_name}' created successfully with {len(songs)} tracks!")
                st.markdown(f"[ Click here to open your new playlist on Spotify]({playlist_url})")
                
            
            except Exception as e:
                # If ANY step fails, it stops the spinner and prints the exact error in red
                status.update(label="An error occurred!", state="error")
                st.error(f"Error details: {e}")


