def get_movie_recommendations(data, movie_title, min_ratings=5, top_n=5):
    import pandas as pd
    import numpy as np

    # Filter movies with enough ratings
    movie_counts = data.groupby('title')['rating'].count()
    popular_movies = movie_counts[movie_counts >= min_ratings].index
    filtered_data = data[data['title'].isin(popular_movies)]

    # Create user-movie matrix
    matrix = filtered_data.pivot_table(index='userId', columns='title', values='rating')

    if movie_title not in matrix.columns:
        return ["Movie not found or has insufficient ratings."]

    # Remove movies with zero variance (all same ratings)
    matrix = matrix.loc[:, matrix.std(axis=0) > 0]

    if movie_title not in matrix.columns:
        return ["No variability in ratings for this movie."]

    # Compute correlation only if matrix is valid
    target_ratings = matrix[movie_title]
    similar_movies = matrix.corrwith(target_ratings, drop=True)

    # Convert to DataFrame and sort
    corr_df = pd.DataFrame(similar_movies, columns=['correlation']).dropna()
    corr_df = corr_df[corr_df['correlation'] < 1.0]  # Exclude self
    corr_df = corr_df.sort_values('correlation', ascending=False)

    return corr_df.head(top_n).index.tolist()
