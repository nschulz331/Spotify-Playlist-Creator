import json
import time
from google import genai
import streamlit as st

def get_custom_fallbacks(prompt):
    """Returns a hardcoded list of songs based on the requested vibe."""
    prompt_lower = prompt.lower()
    
    if "edm" in prompt_lower or "house" in prompt_lower:
        return [
            {"title": "Strobe", "artist": "deadmau5"},
            {"title": "Clarity", "artist": "Zedd"},
            {"title": "Animals", "artist": "Martin Garrix"},
            {"title": "Wake Me Up", "artist": "Avicii"}
        ]
    elif "rap" in prompt_lower or "hip hop" in prompt_lower:
        return [
            {"title": "HUMBLE.", "artist": "Kendrick Lamar"},
            {"title": "God's Plan", "artist": "Drake"},
            {"title": "SICKO MODE", "artist": "Travis Scott"},
            {"title": "Not Like Us", "artist": "Kendrick Lamar"}
        ]
    else:
        # Generic hits fallback for anything else
        return [
            {"title": "Blinding Lights", "artist": "The Weeknd"},
            {"title": "As It Was", "artist": "Harry Styles"},
            {"title": "Cruel Summer", "artist": "Taylor Swift"},
            {"title": "Stay", "artist": "Justin Bieber"}
        ]

def generate_song_recommendations(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    search_topic = prompt if prompt.strip() else "the current top hit songs in Canada"

    full_prompt = f"""
The user wants a playlist for: "{search_topic}".
Provide a list of 10 tracks that fit this vibe perfectly.
CRITICAL INSTRUCTIONS:
- Return ONLY unique tracks (no duplicate artist/title pairs).
- Ensure songs strictly match the requested genre/vibe.
Output your response ONLY as a JSON array of 10 objects:
[
  {{"title": "Song Title", "artist": "Artist Name"}}
]
"""
    # 1. Try Primary Model
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=full_prompt,
            config={"response_mime_type": "application/json"}
        )
    except Exception as e1:
        st.warning("Servers are busy. Waiting a few seconds...")
        time.sleep(15) 
        
        # 2. Try Fallback Model
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=full_prompt,
                config={"response_mime_type": "application/json"}
            )
        except Exception as e2:
            st.error("AI is currently overloaded. Loading a curated backup playlist instead!")
            # 3. Ultimate Fallback: The custom queue
            return get_custom_fallbacks(prompt)

    # Parse the JSON
    try:
        return json.loads(response.text)
    except Exception:
        return get_custom_fallbacks(prompt)