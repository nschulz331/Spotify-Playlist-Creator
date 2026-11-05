import json
from google import genai
import streamlit as st

def generate_song_recommendations(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # If the user didn't enter anything, provide a default topic
    search_topic = prompt if prompt.strip() else "the current top hit songs in Canada"
    
    full_prompt = f"""
    The user wants a playlist for: "{search_topic}".
    Provide a list of 10 tracks that fit this vibe perfectly.
    
    CRITICAL INSTRUCTIONS:
    1. Output your response ONLY as a JSON array of objects.
    2. Do not include any intro, outro, or conversational text.
    3. Each object in the array must look exactly like this:
    {{
        "title": "Song Title",
        "artist": "Artist Name"
    }}
    
    Wrap your final response in a triple backtick json code block exactly like this:
    ```json
    [
      {{"title": "Song 1", "artist": "Artist 1"}},
      {{"title": "Song 2", "artist": "Artist 2"}}
    ]
    ```
    """
    
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=full_prompt
    )
    
    raw_response = response.text
    
    # Isolate the JSON string using your financial app splitting trick
    if "```json" in raw_response:
        parts = raw_response.split("```json")
        if len(parts) > 1:
            json_part = parts[1].split("```")[0].strip()  #  ADD [1] AND [0]
        else:
            json_part = raw_response.strip()
    else:
        json_part = raw_response.strip()
        
    try:
        # Convert the string block into a real executable Python list of dictionaries
        songs_list = json.loads(json_part)
        return songs_list
    except Exception as e:
        st.error(f"Failed to parse song JSON: {e}")
        # Safe fallback so your app does not completely crash if the model drops character strings
        return [
            {"title": "Blinding Lights", "artist": "The Weeknd"},
            {"title": "Stay", "artist": "Justin Bieber"}
        ]

