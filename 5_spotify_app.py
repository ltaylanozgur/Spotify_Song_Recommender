import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
st.set_page_config(page_title="Song Recommendation", layout="wide")
import streamlit.components.v1 as components
import pickle
import random
from random import randint

title = "Song Recommender"
st.title(title)
st.write("Hello Music Lovers! Here is a perfect place for you to listen to your favorite songs through the song recommender system.")
st.markdown("##")
    
st.markdown(
    """
    <style>
    div[class*="stTextInput"] label {
      font-size: 20px;
    }
    text{
      font-size: 200% !important;
      text-align: center !important;
    }
    input {
        font-size: 2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
image = Image.open('images/image1.PNG')
st.image(image)
    
secrets_file = open("secrets.txt","r")
string = secrets_file.read()
string.split('\n')

secrets_dict={}
for line in string.split('\n'):
    if len(line) > 0:
        secrets_dict[line.split(':')[0]]=line.split(':')[1].strip()

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets_dict['cid'],
                                                               client_secret=secrets_dict['csecret']))

def import_file(doc):
    return pickle.load(open(doc, 'rb'))
    
transformer = import_file('/Users/ozguryildirim/IH-Labs/Spotify_Song_Recommender/transformer.sav')
kmeans = import_file('/Users/ozguryildirim/IH-Labs/Spotify_Song_Recommender/kmeans.sav')
playlist_df_all = import_file('/Users/ozguryildirim/IH-Labs/Spotify_Song_Recommender/playlist_df_all.p')
songs_df = pd.read_csv("songs_df_uri.csv")

def song_uri(song_name):
    try:
        querry = 'track:'+str(song_name)
        track = sp.search(q=song_name, limit=1)
        return track['tracks']['items'][0]['uri'].split('spotify:track:')[1]                 
    except:
        return 'Null'
    
def collect_song_features(uri):  
    playlist_features_list = ["danceability","energy","key","loudness","mode", "speechiness","acousticness",
                              "instrumentalness","liveness","valence","tempo","duration_ms","time_signature"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)      
    audio_features = sp.audio_features(uri)[0]
    playlist_df.loc[len(playlist_df)] = [audio_features[feature] for feature in playlist_features_list]        
    return playlist_df

uri = ''

state = True

if True:
    song_name = st.text_input("Please enter your favorite song 👇", key = '<txt>')    
    
    if song_name != '':
        exist=False
        
        for i in ['artist', 'song']:
            if len(songs_df[songs_df[i].str.contains(song_name, case = False, regex = False)]) != 0:
                exist = True
        if exist == True:
            index = random.randint(0,len(songs_df))
            st.write('### Our song recommendation is: ')
            uri = songs_df['uri'].values[index]                    
        else:
            try:
                df = collect_song_features(song_uri(song_name))
                cluster = kmeans.predict(pd.DataFrame(transformer.transform(df), columns=df.columns))
                choose_song = playlist_df_all[playlist_df_all['k_cluster'] == cluster[0]]
                st.write('### Recommendation from Spotify database: ')
                index = random.randint(0,len(choose_song))
                uri = choose_song['track_id'].values[index]
            except:
                st.write('Please enter a valid song name')              
                    
if uri != '':
            
    html_string = """<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/"""+uri+"""#42?utm_source=generator&theme=0" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
    
    components.html(html_string,height=600)
