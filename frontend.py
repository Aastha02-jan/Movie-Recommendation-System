import pandas as pd
import streamlit as st
import pickle
import requests

# TMDb API Key
TMDB_API_KEY = "5fd8bd128c81a8bade382df0f226bf66"  # Replace with your TMDb API key

# Function to fetch movie details (poster, IMDb rating, genre, and release year) using TMDb API
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            # Extract required details
            poster_path = f"https://image.tmdb.org/t/p/original{data.get('poster_path', '')}"
            imdb_rating = round(data.get('vote_average', 0), 2)  # IMDb rating rounded to 2 decimal places
            genres = ", ".join([genre['name'] for genre in data.get('genres', [])])  # Genres as a comma-separated string
            
            # Extract release year from release_date
            release_date = data.get('release_date', 'N/A')
            release_year = pd.to_datetime(release_date).year if release_date != 'N/A' else "N/A"
            
            return poster_path, imdb_rating, genres, release_year
            
        else:
            return (
                "https://via.placeholder.com/300x450?text=No+Poster+Available",  # Poster fallback
                "N/A",  # IMDb rating fallback
                "N/A",  # Genre fallback
                "N/A"   # Release year fallback
            )
    except Exception as e:
        print(f"Error fetching details for movie ID {movie_id}: {e}")
        return (
            "https://via.placeholder.com/300x450?text=No+Poster+Available",  # Poster fallback
            "N/A",  # IMDb rating fallback
            "N/A",  # Genre fallback
            "N/A"   # Release year fallback
        )

# Function to fetch streaming links using TMDb's /watch/providers endpoint
def fetch_streaming_links(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={TMDB_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", {}).get("IN", {})  # Get results for India (locale: IN)
            
            if results and "link" in results:
                tmdb_watch_link = results["link"]  # Link to TMDb's /watch page for the movie
                return [f"[View Streaming Options]({tmdb_watch_link})"]
            else:
                return ["No streaming platforms found"]
        else:
            return [f"Error fetching streaming links (HTTP {response.status_code})"]
    except Exception as e:
        print(f"Error fetching streaming links: {e}")
        return [f"Error: {str(e)}"]

# Function to recommend movies and fetch their details (poster, IMDb rating, genre, release year, and streaming links)
def recommend(movie_name):
    movie_index = df[df['title'] == movie_name].index[0]  # Get the index of the selected movie
    distances = similarity[movie_index]  # Get similarity scores for the selected movie
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  # Sort and get top 5 similar movies

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_genres = []
    recommended_release_years = []
    recommended_streaming_links = []  # List to store streaming links
    
    for i in movie_list:
        movie_id = df.iloc[i[0]].movie_id  # Assuming 'movie_id' column contains TMDb IDs
        
        title = df.iloc[i[0]].title
        poster, imdb_rating, genres, release_year = fetch_movie_details(movie_id)  # Fetch all details
        
        streaming_links = fetch_streaming_links(movie_id)  # Fetch streaming links
        
        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_ratings.append(imdb_rating)
        recommended_genres.append(genres)
        recommended_release_years.append(release_year)
        recommended_streaming_links.append(streaming_links)

    return recommended_movies, recommended_posters, recommended_ratings, recommended_genres, recommended_release_years, recommended_streaming_links

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
similarity = pickle.load(open('similarity.pkl', 'rb'))
df = pd.DataFrame(movies_dict)


# Streamlit app title with styled class
st.markdown('<div class="title">Movie Recommendation System</div>', unsafe_allow_html=True)

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations',
    options=["Select a movie"] + list(df['title'].values),
)

if selected_movie_name != "Select a movie" and st.button("Recommend"):
    recommendations, posters, ratings, genres, release_years, streaming_links_list = recommend(selected_movie_name)
    
    if recommendations:
        st.write("Recommended Movies:")
        
        cols = st.columns(len(recommendations)) 
        
        for col, title, poster, rating, genre, release_year, streaming_links in zip(cols, recommendations, posters, ratings, genres, release_years, streaming_links_list):
            with col:
                st.image(poster)  # Display poster
                
                st.markdown(f"**{title} ({release_year})**")
                st.markdown(f"⭐ IMDb Rating: {rating}/10")
                st.markdown(f"🎭 Genre: {genre}")
                
                for link in streaming_links:
                    st.markdown(link)  # Display clickable OTT links
                
    else:
        st.write("No recommendations available.")
