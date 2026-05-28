import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

# OMDb API Key
API_KEY = "52fc3a00"


# Fetch poster from OMDb
def fetch_poster(movie_name):

    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    data = requests.get(url).json()

    if data['Response'] == 'True':

        poster = data.get('Poster')

        if poster != "N/A":
            return poster

    return "https://via.placeholder.com/300x450.png?text=No+Image"


# Recommendation function
def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_name = movies.iloc[i[0]].title

        recommended_movie_names.append(movie_name)

        recommended_movie_posters.append(fetch_poster(movie_name))

    return recommended_movie_names, recommended_movie_posters


# Streamlit title
st.title('Movie Recommendation System')


# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

movies = pd.DataFrame.from_dict(movies_dict)


# Load compressed similarity file
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


# Movie list
movie_list = movies['title'].values


# Select movie
selected_movie = st.selectbox(
    "Select a movie:",
    movie_list
)


# Recommend movies
if st.button("Recommend Movie"):

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], use_container_width=True)

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], use_container_width=True)

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], use_container_width=True)

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], use_container_width=True)

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], use_container_width=True)