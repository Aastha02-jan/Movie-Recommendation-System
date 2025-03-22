import pandas as pd
import streamlit as st
import pickle
import requests
import time

# Function to fetch movie details (poster, IMDb rating, genre, and release year) using TMDb API
def fetch_movie_details(movie_id):
    api_key = "5fd8bd128c81a8bade382df0f226bf66"  # Your TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Extract required details
                poster_path = f"https://image.tmdb.org/t/p/original{data.get('poster_path', '')}"
                imdb_rating = data.get('vote_average', 'N/A')  # IMDb rating
                genres = ", ".join([genre['name'] for genre in data.get('genres', [])])  # Genres as a comma-separated string
                
                # Extract release year from release_date
                release_date = data.get('release_date', 'N/A')
                release_year = pd.to_datetime(release_date).year if release_date != 'N/A' else "N/A"
                
                return poster_path, imdb_rating, genres, release_year
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching details for movie ID {movie_id}: {e}")
            time.sleep(1)  # Wait for 1 second before retrying
    
    # Fallback values in case of failure
    return (
        "https://via.placeholder.com/300x450?text=No+Poster+Available",  # Poster fallback
        "N/A",  # IMDb rating fallback
        "N/A",  # Genre fallback
        "N/A"   # Release year fallback
    )

# Function to recommend movies and fetch their details (poster, IMDb rating, genre, and release year)
def recommend(movie_name):
    movie_index = df[df['title'] == movie_name].index[0]  # Get the index of the selected movie
    distances = similarity[movie_index]  # Get similarity scores for the selected movie
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Sort and get top 5 similar movies

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_genres = []
    recommended_release_years = []
    
    for i in movie_list:
        movie_id = df.iloc[i[0]].movie_id  # Assuming 'movie_id' column contains TMDb IDs
        
        title = df.iloc[i[0]].title
        poster, imdb_rating, genres, release_year = fetch_movie_details(movie_id)  # Fetch all details
        
        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_ratings.append(imdb_rating)
        recommended_genres.append(genres)
        recommended_release_years.append(release_year)

    return recommended_movies, recommended_posters, recommended_ratings, recommended_genres, recommended_release_years

# Function to set background image and style title for better contrast
def set_background_and_style():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-image: url("https://media.licdn.com/dms/image/v2/D5612AQGy6sM0SJAdxg/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1693150322893?e=2147483647&v=beta&t=2_aostRG53XjmjiS9FSI9Jcfn73tsoq3uFate9rV0XE");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .title {
            font-size: 3em;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); /* Add shadow for better contrast */
            text-align: center;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background and title styling
set_background_and_style()

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
df = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title with styled class
st.markdown('<div class="title">Movie Recommendation System</div>', unsafe_allow_html=True)

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Tell me your preferences?',
    df['title'].values
)

# Button to trigger recommendations
if st.button("Recommend"):
    recommendations, posters, ratings, genres, release_years = recommend(selected_movie_name)
    
    if recommendations:
        st.write("Recommended Movies:")
        
        # Display movies and posters side by side in a single row with additional details
        cols = st.columns(len(recommendations))  # Create one column per recommendation
        
        for col, title, poster, rating, genre, release_year in zip(cols, recommendations, posters, ratings, genres, release_years):
            with col:
                st.image(poster, use_container_width=True)  # Display poster in the column
                
                # Display title with release year in brackets and IMDb rating below it
                st.markdown(f"**{title} ({release_year})**")  
                st.markdown(f"⭐ IMDb Rating: {rating}/10")
                st.markdown(f"🎭 Genre: {genre}")
                
    else:
        st.write("No recommendations available.")
