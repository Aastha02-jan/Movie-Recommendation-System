import pandas as pd
import streamlit as st
import pickle

def recommend(movie_name):

    movie_index = df[df['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(df.iloc[i[0]].title)
    return recommended_movies
  
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
df = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'Tell me your preferences?',
    df['title'].values
)
if st.button("Recommend"):
    recommendations = recommend(selected_movie_name)
    if recommendations:
        for movie in recommendations:
            st.write(movie)
    else:
        st.write("No recommendations available.")
