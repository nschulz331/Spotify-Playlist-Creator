import json
from google import genai
import streamlit as st

def generate_song_recommendations(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    search_topic = prompt if prompt.strip() else "the current top hit songs in Canada"

    full_prompt = f"""
The user wants a playlist for: "{search_topic}".
Provide a list of 10 tracks that fit this vibe perfectly.
do not have the same song twice
Output your response ONLY as a JSON array of 10 objects:
[
  {{"title": "Song Title", "artist": "Artist Name"}}
]
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=full_prompt,
        config={"response_mime_type": "application/json"}
    )

    try:
        songs_list = json.loads(response.text)
        return songs_list
    except Exception as e:
        st.error(f"Failed to parse song JSON: {e}")
        return [
            {"title": "Blinding Lights", "artist": "The Weeknd"},
            {"title": "Stay", "artist": "Justin Bieber"}
        ]