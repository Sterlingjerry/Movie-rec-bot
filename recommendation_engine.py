import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings('ignore')

class NetflixRecommendationBot:
    def __init__(self, csv_path='netflix_titles.csv'):
        """Initialize the recommendation bot with Netflix data"""
        self.df = None
        self.tfidf_matrix = None
        self.feature_matrix = None
        self.vectorizer = None
        self.scaler = StandardScaler()
        
        # Download NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
        except:
            pass
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Load and preprocess data
        self.load_data(csv_path)
        if self.df is not None:
            self.preprocess_data()
            self.create_feature_matrix()
    
    def load_data(self, csv_path):
        """Load the Netflix dataset"""
        try:
            self.df = pd.read_csv(csv_path)
            print(f"Loaded {len(self.df)} titles from Netflix dataset")
            print(f"Columns: {self.df.columns.tolist()}")
        except FileNotFoundError:
            print(f"File {csv_path} not found. Please run data_downloader.py first.")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def clean_text(self, text):
        """Clean and preprocess text data"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def preprocess_data(self):
        """Preprocess the Netflix data"""
        # Fill missing values
        self.df['description'] = self.df['description'].fillna('')
        self.df['cast'] = self.df['cast'].fillna('')
        self.df['director'] = self.df['director'].fillna('')
        self.df['listed_in'] = self.df['listed_in'].fillna('')
        self.df['country'] = self.df['country'].fillna('')
        
        # Create combined text features
        self.df['genres_clean'] = self.df['listed_in'].apply(self.clean_text)
        self.df['description_clean'] = self.df['description'].apply(self.clean_text)
        self.df['cast_clean'] = self.df['cast'].apply(self.clean_text)
        self.df['director_clean'] = self.df['director'].apply(self.clean_text)
        
        # Combine all text features
        self.df['combined_features'] = (
            self.df['genres_clean'] + ' ' +
            self.df['description_clean'] + ' ' +
            self.df['cast_clean'] + ' ' +
            self.df['director_clean']
        )
        
        # Extract release year
        if 'release_year' in self.df.columns:
            self.df['release_year'] = pd.to_numeric(self.df['release_year'], errors='coerce')
        
        print("Data preprocessing completed!")
    
    def create_feature_matrix(self):
        """Create TF-IDF feature matrix"""
        # Create TF-IDF matrix
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
        print(f"Created TF-IDF matrix with shape: {self.tfidf_matrix.shape}")
    
    def get_content_recommendations(self, title, n_recommendations=10):
        """Get content-based recommendations"""
        # Find the movie/show
        idx = self.df[self.df['title'].str.contains(title, case=False, na=False)].index
        
        if len(idx) == 0:
            return f"Title '{title}' not found in the dataset."
        
        # Use the first match
        idx = idx[0]
        
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
        
        # Get similarity scores
        sim_scores = list(enumerate(cosine_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top recommendations (excluding the input title)
        sim_scores = sim_scores[1:n_recommendations+1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return recommendations
        recommendations = self.df.iloc[movie_indices][['title', 'type', 'release_year', 'rating', 'listed_in', 'description']]
        
        return recommendations
    
    def get_recommendations_by_genre(self, genre, content_type='all', n_recommendations=10):
        """Get recommendations by genre"""
        # Filter by content type
        if content_type.lower() == 'movie':
            filtered_df = self.df[self.df['type'] == 'Movie']
        elif content_type.lower() == 'tv show':
            filtered_df = self.df[self.df['type'] == 'TV Show']
        else:
            filtered_df = self.df
        
        # Filter by genre
        genre_mask = filtered_df['listed_in'].str.contains(genre, case=False, na=False)
        genre_titles = filtered_df[genre_mask]
        
        if len(genre_titles) == 0:
            return f"No {content_type} found for genre '{genre}'"
        
        # Sort by release year (most recent first)
        if 'release_year' in genre_titles.columns:
            genre_titles = genre_titles.sort_values('release_year', ascending=False)
        
        return genre_titles.head(n_recommendations)[['title', 'type', 'release_year', 'rating', 'listed_in', 'description']]
    
    def get_popular_titles(self, content_type='all', n_recommendations=10):
        """Get popular titles (most recent releases)"""
        # Filter by content type
        if content_type.lower() == 'movie':
            filtered_df = self.df[self.df['type'] == 'Movie']
        elif content_type.lower() == 'tv show':
            filtered_df = self.df[self.df['type'] == 'TV Show']
        else:
            filtered_df = self.df
        
        # Sort by release year
        if 'release_year' in filtered_df.columns:
            popular_titles = filtered_df.sort_values('release_year', ascending=False)
        else:
            popular_titles = filtered_df
        
        return popular_titles.head(n_recommendations)[['title', 'type', 'release_year', 'rating', 'listed_in', 'description']]
    
    def search_titles(self, query, n_results=10):
        """Search for titles containing the query"""
        # Search in title, description, cast, and director
        mask = (
            self.df['title'].str.contains(query, case=False, na=False) |
            self.df['description'].str.contains(query, case=False, na=False) |
            self.df['cast'].str.contains(query, case=False, na=False) |
            self.df['director'].str.contains(query, case=False, na=False)
        )
        
        results = self.df[mask]
        
        if len(results) == 0:
            return f"No results found for '{query}'"
        
        return results.head(n_results)[['title', 'type', 'release_year', 'rating', 'listed_in', 'description']]
    
    def get_stats(self):
        """Get dataset statistics"""
        stats = {
            'total_titles': len(self.df),
            'movies': len(self.df[self.df['type'] == 'Movie']),
            'tv_shows': len(self.df[self.df['type'] == 'TV Show']),
            'unique_genres': len(set([genre.strip() for genres in self.df['listed_in'].dropna() 
                                    for genre in genres.split(',')])),
            'release_year_range': f"{self.df['release_year'].min():.0f} - {self.df['release_year'].max():.0f}"
        }
        return stats
    
    def get_recommendations_by_description(self, description, content_type='all', n_recommendations=10):
        """Get recommendations based on user description using TF-IDF similarity"""
        # Filter by content type
        if content_type.lower() == 'movie':
            filtered_df = self.df[self.df['type'] == 'Movie']
        elif content_type.lower() == 'tv show':
            filtered_df = self.df[self.df['type'] == 'TV Show']
        else:
            filtered_df = self.df
        
        if len(filtered_df) == 0:
            return f"No {content_type} found"
        
        # Clean the input description
        clean_description = self.clean_text(description)
        
        # Create TF-IDF matrix for filtered data
        filtered_indices = filtered_df.index
        filtered_tfidf = self.tfidf_matrix[filtered_indices]
        
        # Transform the input description
        description_vector = self.vectorizer.transform([clean_description])
        
        # Calculate cosine similarity
        cosine_sim = cosine_similarity(description_vector, filtered_tfidf).flatten()
        
        # Get similarity scores
        sim_scores = list(enumerate(cosine_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top recommendations
        top_indices = [filtered_indices[i] for i, score in sim_scores[:n_recommendations] if score > 0]
        
        if not top_indices:
            return f"No matches found for description: '{description}'"
        
        # Return recommendations
        recommendations = self.df.iloc[top_indices][['title', 'type', 'release_year', 'rating', 'listed_in', 'description']]
        
        return recommendations

# Example usage
if __name__ == "__main__":
    # Initialize the recommendation bot
    bot = NetflixRecommendationBot()
    
    if bot.df is not None:
        # Get some statistics
        stats = bot.get_stats()
        print("\nDataset Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # Example recommendations
        print("\n" + "="*50)
        print("EXAMPLE RECOMMENDATIONS")
        print("="*50)
        
        # Content-based recommendations
        print("\nContent-based recommendations for 'Stranger Things':")
        recommendations = bot.get_content_recommendations('Stranger Things', 5)
        if isinstance(recommendations, pd.DataFrame):
            for idx, row in recommendations.iterrows():
                print(f"- {row['title']} ({row['type']}, {row['release_year']})")
        else:
            print(recommendations)
        
        # Genre-based recommendations
        print("\nTop Action Movies:")
        action_movies = bot.get_recommendations_by_genre('Action', 'movie', 5)
        if isinstance(action_movies, pd.DataFrame):
            for idx, row in action_movies.iterrows():
                print(f"- {row['title']} ({row['release_year']})")
        else:
            print(action_movies)
        
        # Description-based recommendations
        print("\nRecommendations based on description 'funny romantic comedy with friends':")
        desc_recs = bot.get_recommendations_by_description('funny romantic comedy with friends', 'all', 5)
        if isinstance(desc_recs, pd.DataFrame):
            for idx, row in desc_recs.iterrows():
                print(f"- {row['title']} ({row['type']}, {row['release_year']})")
        else:
            print(desc_recs)
