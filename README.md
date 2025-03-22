# Movie-Recommendation-System
This repository contains a Movie Recommendation System built using Python, Pandas, Scikit-learn, and NLTK for the backend, and HTML, CSS, and JavaScript for the frontend. The system recommends movies based on their similarity to a given movie, using features like genres, keywords, cast, and crew. 

Key Features:

Backend:
1.Preprocesses movie data (genres, keywords, cast, crew).
2.Uses stemming and vectorization to analyze text data.
3.Computes cosine similarity to find similar movies.

Frontend:
1.Built entirely with Streamlit, eliminating the need for separate HTML/CSS/JavaScript.
2.Users can enter a movie title and get recommendations instantly.

Integration:
Streamlit seamlessly integrates the backend and frontend, making it easy to deploy and use.

How It Works:
User Input: Enter a movie title in the Streamlit interface.

Backend Processing:
1.Finds similar movies using cosine similarity.
2.Returns a list of recommendations.

Frontend Display: Displays the recommended movies dynamically in the Streamlit app.

Technologies Used:
Backend: Python, Pandas, Scikit-learn, NLTK.

Frontend: Streamlit.

Dataset: TMDB 5000 Movies Dataset.
TMDB 5000 Credits Dataset.

Install dependencies:
pip install pandas numpy scikit-learn nltk streamlit

Run the Streamlit app:
streamlit run app.py

Example:
Input: "Avatar"
Output:
Jupiter Ascending
The Martian
The Amazing Spider-Man
Spectre
2012
