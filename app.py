import streamlit as st
import pickle
import pandas as pd
import requests

# 1. Load the serialized data
movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('models/similarity.pkl', 'rb'))

# 2. Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    # IMPORTANT: Replace 'YOUR_API_KEY' with your actual TMDB API Key!
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=66853f26f3456dd1506d5b853727378c&language=en-US"
    
    # Make the HTTP request to TMDB
    response = requests.get(url)
    data = response.json()
    
    # Extract the poster path and build the full image URL
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    
    # Fallback image if the API doesn't have a poster
    return "https://via.placeholder.com/500x750?text=No+Poster+Available" 

# 3. Updated recommendation function to return both names and posters
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        # We need the movie_id to pass into our fetch_poster function
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_movies_posters

# 4. Build the Streamlit UI with Columns
st.set_page_config(layout="wide") # Makes the app wider to fit 5 posters comfortably
st.title('🎬 Movie Recommender System')

def request_recommendation():
    st.session_state.recommend_requested = True


selected_movie_name = st.selectbox(
    'Search for a movie to get recommendations:',
    movies['title'].values,
    on_change=request_recommendation
)

recommend_clicked = st.button('Recommend')
recommend_clicked = recommend_clicked or st.session_state.pop(
    'recommend_requested', False
)

if recommend_clicked:
    with st.spinner('Fetching recommendations and posters...'):
        names, posters = recommend(selected_movie_name)
        
        st.subheader("You should also check out:")
        
        # Create 5 identical columns for the UI
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])