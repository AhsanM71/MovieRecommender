from LoadDataset import *
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def main():
    movie_df = load_dataset()

    new_movie_df = format_df(movie_df)
    new_movie_df['tags'] = new_movie_df['tags'].apply(stems)

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(new_movie_df['tags']).toarray()

    similary = cosine_similarity(vector)
    recommend("Avatar", new_movie_df, similary)

    pickle.dump(new_movie_df, open('./artificats/movie_list.pkl', 'wb'))
    pickle.dump(similary, open('./artificats/similary_list.pkl', 'wb'))

    # print(new_movie_df.iloc[0]['tags'])

def recommend(movie, new_movie_df, similary):
    index = new_movie_df[new_movie_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similary[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:10]:
        print(new_movie_df.iloc[i[0]].title)

def stems(text):
    temp_list = []
    for i in text.split():
        temp_list.append(PorterStemmer().stem(i))
    return " ".join(temp_list)

if __name__ == "__main__":
    main()