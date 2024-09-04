import numpy as py
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

def format_df(movie_df):
    update_column(movie_df, 'genres', r'"name":\s*"([^"]+)"')
    update_column(movie_df, 'keywords', r'"name":\s*"([^"]+)"')
    update_column(movie_df, 'cast', r'"name":\s*"([^"]+)"', True)
    update_column(movie_df, 'crew', r'"job": "Director", "name":\s*"([^"]+)"')

    movie_df["overview"] = movie_df["overview"].apply(update_overview_col)
    movie_df["cast"] = movie_df["cast"].apply(remove_spaces)
    movie_df["crew"] = movie_df["crew"].apply(remove_spaces)
    movie_df["keywords"] = movie_df["keywords"].apply(remove_spaces)
    movie_df["tags"] = movie_df["overview"] + movie_df["genres"] + movie_df["keywords"] + movie_df["cast"] + movie_df["crew"]
    new_movie_df = movie_df[['movie_id', 'title', 'tags']]
    new_movie_df["tags"] = new_movie_df["tags"].apply(join_text)

    return new_movie_df

def update_overview_col(text):
    return text.split()

def remove_spaces(words):
    temp_list = []
    for i in words:
        temp_list.append(i.replace(" ", ""))
    return temp_list

def join_text(text):
    return " ".join(text).lower()

def load_dataset():
    movies = pd.read_csv("./assets/tmdb_5000_movies.csv")
    credits = pd.read_csv("./assets/tmdb_5000_credits.csv")

    movies_df = movies.merge(credits, on="title")

    subset_df = movies_df[['movie_id', 'overview', 'title', 'genres', 'keywords', 'cast', 'crew']]
    subset_df.dropna(inplace=True)

    return subset_df

def update_column(df, column, pattern, flag=False):
    if flag:
        for i in df.index:
            ith_row_of_col = df.at[i, column]
            df.at[i, column] = re.findall(pattern, ith_row_of_col)[:3]
    else:
        for i in df.index:
            ith_row_of_col = df.at[i, column]
            df.at[i, column] = re.findall(pattern, ith_row_of_col)
