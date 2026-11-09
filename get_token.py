import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tomllib

with open(".streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

sp_oauth = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri="http://127.0.0.1:8080",
    scope="playlist-modify-public playlist-modify-private",
    show_dialog=True  # Forces the permissions screen to appear
)

print("\nAuthorization URL:\n", sp_oauth.get_authorize_url())


response_url = input("\nPaste the full redirected URL here: ")
code = sp_oauth.parse_response_code(response_url)
token_info = sp_oauth.get_access_token(code)
print("\nYOUR REFRESH TOKEN:\n", token_info["refresh_token"])