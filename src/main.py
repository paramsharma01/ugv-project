import pandas as pd
from recommender import get_movie_recommendations

def main():
    # Load ratings and movies CSV files
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    df = pd.merge(ratings, movies, on="movieId")

    # User input
    movie_title = input("Enter a movie you like: ").strip()
    recommendations = get_movie_recommendations(df, movie_title)
    print(f"\nRecommended for you if you like '{movie_title}':")
    for movie in recommendations:
        print(movie)

if __name__ == "__main__":
    main()
