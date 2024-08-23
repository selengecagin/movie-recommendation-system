import streamlit as st
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Set up the Streamlit page
st.set_page_config(page_title="Movie Recommendation App", page_icon="🎬")
st.title("Movie Recommendation App")

# Set up the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is available
if not openai.api_key:
    st.error("OpenAI API key not found. Please add it to your .env file.")
    st.stop()

# Predefined list of movie genres
all_genres = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama",
    "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance",
    "Science Fiction", "Thriller", "War", "Western"
]

# Get movie genres from the user using checkboxes
st.subheader("Select your favorite movie genres:")
selected_genres = []
cols = st.columns(3)  # Create 3 columns for a more compact layout
for i, genre in enumerate(all_genres):
    with cols[i % 3]:  # Distribute genres across 3 columns
        if st.checkbox(genre):
            selected_genres.append(genre)

# Get the user's 3 favorite movies
st.subheader("Enter your 3 favorite movies:")
favorite_movies = []
for i in range(3):
    favorite_movies.append(st.text_input(f"Movie {i+1}:"))

if st.button("Get Recommendations"):
    if selected_genres and all(favorite_movies):
        # Prepare the ChatGPT prompt
        prompt = f"""
        User's favorite movie genres: {', '.join(selected_genres)}
        User's 3 favorite movies: {', '.join(favorite_movies)}

        Please provide 5 movie recommendations based on this information. Give your answer in a table format as follows:

        | Movie Title | Genre | Brief Summary |
        |-------------|-------|----------------|
        | ...         | ...   | ...            |
        """

        # Get recommendations using the ChatGPT API
        with st.spinner("Fetching recommendations..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a movie expert. You provide movie recommendations to users."},
                    {"role": "user", "content": prompt}
                ]
            )

        # Display the response
        st.subheader("Here are your movie recommendations:")
        st.markdown(response.choices[0].message.content)
    else:
        st.warning("Please select at least one genre and fill in all movie fields.")