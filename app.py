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
    for i in distances[1:11]:  # Fetching up to 10 movies
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

# Custom CSS to style the app with a vibrant theme
st.markdown("""
    <style>
    body {
        background-color: #f8f0f4;
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-family: 'Georgia', serif;
        font-size: 2.5em;
        color: #e94e77;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .movie-title {
        font-family: 'Verdana', sans-serif;
        font-size: 1.1em;
        color: #2c3e50;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .movie-poster {
        display: block;
        margin: 0 auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
    }
    .card {
        background-color: #fff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        width: 200px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">Movies Recommendation System Using Machine Learning</div>', unsafe_allow_html=True)

movies = pickle.load(open("artificats/movie_list.pkl", 'rb'))
similarity = pickle.load(open("artificats/similary_list.pkl", 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get a recommendation',
    movie_list
)

if st.button("Show Recommendation"):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    
    # Number of columns per row
    cols_per_row = 3
    
    # Create a grid-like structure
    num_movies = len(recommended_movies_name)
    num_rows = (num_movies + cols_per_row - 1) // cols_per_row  # Calculate number of rows needed
    
    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row):
            idx = row * cols_per_row + col
            if idx < num_movies:
                with cols[col]:
                    st.markdown(f'''
                    <div class="card">
                        <img class="movie-poster" src="{recommended_movies_poster[idx]}" width="150">
                        <div class="movie-title">{recommended_movies_name[idx]}</div>
                    </div>
                    ''', unsafe_allow_html=True)
