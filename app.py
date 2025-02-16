import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd  # Ensure Pandas is imported

CLIENT_ID = "18a13ec4ce1d4e988463cc3736925837"
CLIENT_SECRET = "989d3b3d11c94b438fa9daaf20644d9a"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    if song not in music['song'].values:
        st.error(f"Error: '{song}' not found in the dataset.")
        return [], []

    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similar[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')

# ✅ Load `df.pkl`
file_path = "C:/Users/jueej/Downloads/df.pkl"

if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        music = pickle.load(f)
    
    X

# ✅ Load `similar.pkl`
file_path = "C:/Users/jueej/Downloads/similar.pkl"
if os.path.exists(file_path):
    with open(file_path, 'rb') as f:
        similar = pickle.load(f)
else:
    st.error("❌ ERROR: `similar.pkl` file not found.")
    st.stop()

# ✅ Dropdown for selecting a song
music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    if not recommended_music_names:  # If no recommendations are found
        st.error("❌ No recommendations found!")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for i in range(len(recommended_music_names)):
            with cols[i]:
                st.text(recommended_music_names[i])
                st.image(recommended_music_posters[i])
