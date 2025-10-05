def get_movie_recommendations(data, movie_title, min_ratings=3, top_n=5):
    import pandas as pd
    import numpy as np

    # --- Filter movies with enough ratings ---
    movie_counts = data.groupby('title')['rating'].count()
    popular_movies = movie_counts[movie_counts >= min_ratings].index
    filtered_data = data[data['title'].isin(popular_movies)]
    print(f"\n[INFO] Movies with ≥{min_ratings} ratings: {len(popular_movies)}")

    # --- Create user–movie matrix ---
    matrix = filtered_data.pivot_table(index='userId', columns='title', values='rating')
    print(f"[INFO] Matrix shape: {matrix.shape}")

    # --- Handle partial matches for movie title ---
    matches = [t for t in matrix.columns if movie_title.lower() in t.lower()]
    if not matches:
        return [f"No movie found similar to '{movie_title}'. Try entering full or partial name."]
    if len(matches) > 1:
        print("[INFO] Multiple matches found:", matches)
    movie_title = matches[0]
    print(f"[INFO] Using closest match: '{movie_title}'")

    # --- Remove movies with zero variance (all ratings same) ---
    before_cols = matrix.shape[1]
    matrix = matrix.loc[:, matrix.std(axis=0) > 0]
    after_cols = matrix.shape[1]
    print(f"[INFO] Removed {before_cols - after_cols} movies with no rating variability.")

    # --- Re-check target movie after filtering ---
    if movie_title not in matrix.columns:
        return [f"No variability in ratings for '{movie_title}'. Try another movie."]

    # --- Compute correlations ---
    target_ratings = matrix[movie_title]
    similar_movies = matrix.corrwith(target_ratings, drop=True)

    # --- Build correlation DataFrame ---
    corr_df = pd.DataFrame(similar_movies, columns=['correlation']).dropna()
    corr_df = corr_df[corr_df['correlation'] < 1.0]  # Exclude self
    corr_df = corr_df.sort_values('correlation', ascending=False)

    if corr_df.empty:
        return [f"No similar movies found for '{movie_title}'. Try a more popular movie."]

    print(f"[INFO] Found {len(corr_df)} correlated movies.")
    return corr_df.head(top_n).index.tolist()
