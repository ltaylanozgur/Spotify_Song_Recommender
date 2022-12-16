# Spotify song recommender

<img src="images/image1.png"/>

L.T. Ozgur Yildirim

### Index:

* [Purpose of the study](#section1)
* [Materials and Methods](#section2)
* [License](#section3)

<a id='section1'></a>
### Purpose of the study

The ultimate goal of this  project is to improve the recommendations of artists. The jupyter notebook and pyton are used. The song recommendation system is also created using streamlit.

<a id='section2'></a>
### Files

#### 1_Web_Scraping
The songs are firstly scraped from https://playback.fm/charts/top-100-songs/2015, https://playback.fm/charts/top-100-songs/2016, and https://www.popvortex.com/music/charts/top-100-songs.php websites. Songs_df.csv is the final collection of the songs in this step.

#### 2_API wrappers - SPOTIFY
The playlists in Spotify are scraped using Spotify API. More than 10000 songs are collected to perform clustering. playlist_df_all.csv is the final collection of the songs in this step.

#### 3_Song_uri
The uri of all the songs in the Songs_df database is added.

#### 4_Unsupervised_Learning_Intro 
The collected songs are clustered using KMeans clustering model. Clustering the songs allows the recommendation system to limit the scope of the recommendations to only songs that belong to the same cluster - songs with similar audio features. The audio features are collected from Spotify API. After that, the Spotify audio features of the submitted song are sent to the clustering model, which should return a cluster number. The song uri is collected from the song name. Then, the song features are collected from song uri. Finally, the song recommendation system is created.

#### 5_spotify_app.py
The song recommendation application is created using streamlit and python.

<a id='section3'></a>
### License
This is an educational project; therefore, all materials are free to be used.
