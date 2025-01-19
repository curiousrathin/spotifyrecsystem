import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

class SpotifyRecommender:
    def __init__(self):
        """Initialize the recommender system with data loading and preprocessing."""
        try:
            # Load datasets with forced string types
            self.df = pd.read_csv('largeds_cleaned.csv', dtype=str)
            self.df_frontend = pd.read_csv('frontds_cleaned.csv', dtype=str)
            
            # Convert numeric columns after loading
            numeric_columns = [
                'streams', 'bpm', 'danceability_%', 'valence_%', 'energy_%',
                'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'
            ]
            
            # Convert numeric columns and scale them
            for col in numeric_columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                self.df_frontend[col] = pd.to_numeric(self.df_frontend[col], errors='coerce')
            
            # Scale numeric features
            self.scaler = MinMaxScaler()
            self.df[numeric_columns] = self.scaler.fit_transform(self.df[numeric_columns])
            self.df_frontend[numeric_columns] = self.scaler.transform(self.df_frontend[numeric_columns])
            
        except Exception as e:
            raise Exception(f"Error initializing recommender: {str(e)}")

    def get_recommendations(self, song_name, artist_name, n_recommendations=10):
        """Get song recommendations based on input song and artist."""
        try:
            # Find the song in the frontend dataset
            mask = (
                (self.df_frontend['track_name'].str.lower() == song_name.lower()) & 
                (self.df_frontend['artist(s)_name'].str.lower() == artist_name.lower())
            )
            
            if not mask.any():
                return "Song not found in the dataset."
            
            # Get the song features
            song_features = self.df_frontend[mask].iloc[0]
            
            # Calculate similarity scores
            feature_columns = [
                'bpm', 'danceability_%', 'valence_%', 'energy_%',
                'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%'
            ]
            
            # Reshape song features for similarity calculation
            song_features_array = song_features[feature_columns].values.reshape(1, -1)
            
            # Calculate similarity with all songs in the large dataset
            similarity_scores = cosine_similarity(
                song_features_array,
                self.df[feature_columns]
            )
            
            # Get indices of most similar songs
            similar_indices = similarity_scores[0].argsort()[::-1][1:n_recommendations+1]
            
            # Get the recommended songs
            recommendations = self.df.iloc[similar_indices]
            
            return recommendations[['track_name', 'artist(s)_name']]
            
        except Exception as e:
            raise Exception(f"Error getting recommendations: {str(e)}")

    def get_available_songs(self):
        """Return a list of all available songs in the frontend dataset."""
        try:
            return self.df_frontend[['track_name', 'artist(s)_name']].values.tolist()
        except Exception as e:
            raise Exception(f"Error getting available songs: {str(e)}")