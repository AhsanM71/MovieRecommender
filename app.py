import pickle
import streamlit as st
import requests

def fetch_poster(movie_ids):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=fea838e5c6daf4aa7bb1a2a9b90a99c2&language=en-US".format(movie_ids)
    data = requests.get(url)
    data = data.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

st.header("Movies Recommendtion System Using Machine Learning")
movies = pickle.load(open("artificats/movie_list.pkl", 'rb'))
similarity = pickle.load(open("artificats/similary_list.pkl", 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get a recommendation',
    movie_list
)

if st.button("Show Recommendation"):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])
    with col6:
        st.text(recommended_movies_name[5])
        st.image(recommended_movies_poster[5])
    with col7:
        st.text(recommended_movies_name[6])
        st.image(recommended_movies_poster[6])
    with col8:
        st.text(recommended_movies_name[7])
        st.image(recommended_movies_poster[7])
    with col9:
        st.text(recommended_movies_name[8])
        st.image(recommended_movies_poster[8])
    with col10:
        st.text(recommended_movies_name[9])
        st.image(recommended_movies_poster[9])

