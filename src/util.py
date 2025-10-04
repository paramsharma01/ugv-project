import pandas as pd

def load_data(ratings_path, movies_path):
    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)
    return ratings, movies

def merge_datasets(ratings, movies):
    return pd.merge(ratings, movies, on='movieId')

def validate_movie_title(title, movies):
    matches = movies[movies['title'].str.lower() == title.lower()]
    return matches['title'].values[0] if not matches.empty else None

def suggest_titles(title_part, movies):
    pattern = title_part.lower()
    available_titles = movies[movies['title'].str.lower().str.contains(pattern)]['title'].head(5).tolist()
    return available_titles if available_titles else ["No similar titles found."]
