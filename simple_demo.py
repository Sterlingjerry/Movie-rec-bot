"""
Simple Netflix Recommendation Bot Demo
This version works with basic Python libraries for testing purposes.
"""

import csv
import re
from collections import Counter
import json

class SimpleNetflixBot:
    def __init__(self, csv_file='netflix_titles.csv'):
        self.movies = []
        self.load_data(csv_file)
    
    def load_data(self, csv_file):
        """Load Netflix data from CSV file"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.movies = list(reader)
            print(f"Loaded {len(self.movies)} titles")
        except FileNotFoundError:
            print(f"File {csv_file} not found. Creating sample data...")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample Netflix data for demonstration"""
        self.movies = [
            {
                'title': 'Stranger Things',
                'type': 'TV Show',
                'release_year': '2016',
                'rating': 'TV-14',
                'listed_in': 'Horror, Drama, Sci-Fi',
                'description': 'A group of kids discover supernatural forces in their small town.',
                'cast': 'Millie Bobby Brown, Finn Wolfhard, Gaten Matarazzo',
                'director': 'The Duffer Brothers'
            },
            {
                'title': 'The Matrix',
                'type': 'Movie', 
                'release_year': '1999',
                'rating': 'R',
                'listed_in': 'Action, Sci-Fi',
                'description': 'A hacker learns about the true nature of his reality.',
                'cast': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss',
                'director': 'The Wachowski Brothers'
            },
            {
                'title': 'Friends',
                'type': 'TV Show',
                'release_year': '1994', 
                'rating': 'TV-14',
                'listed_in': 'Comedy, Romance',
                'description': 'Six friends navigate life and love in New York City.',
                'cast': 'Jennifer Aniston, Courteney Cox, Lisa Kudrow',
                'director': 'Various'
            },
            {
                'title': 'Inception',
                'type': 'Movie',
                'release_year': '2010',
                'rating': 'PG-13', 
                'listed_in': 'Action, Sci-Fi, Thriller',
                'description': 'A thief enters dreams to steal secrets.',
                'cast': 'Leonardo DiCaprio, Marion Cotillard, Tom Hardy',
                'director': 'Christopher Nolan'
            },
            {
                'title': 'The Office',
                'type': 'TV Show',
                'release_year': '2005',
                'rating': 'TV-14',
                'listed_in': 'Comedy',
                'description': 'Mockumentary about office workers.',
                'cast': 'Steve Carell, John Krasinski, Jenna Fischer',
                'director': 'Various'
            }
        ]
        print(f"Created {len(self.movies)} sample titles for demonstration")
    
    def simple_similarity(self, title1, title2):
        """Calculate simple similarity between two titles"""
        movie1 = next((m for m in self.movies if m['title'].lower() == title1.lower()), None)
        movie2 = next((m for m in self.movies if m['title'].lower() == title2.lower()), None)
        
        if not movie1 or not movie2:
            return 0
        
        score = 0
        
        # Genre similarity
        genres1 = set(genre.strip().lower() for genre in movie1['listed_in'].split(','))
        genres2 = set(genre.strip().lower() for genre in movie2['listed_in'].split(','))
        genre_overlap = len(genres1.intersection(genres2))
        score += genre_overlap * 2
        
        # Type similarity
        if movie1['type'] == movie2['type']:
            score += 1
        
        # Rating similarity
        if movie1['rating'] == movie2['rating']:
            score += 0.5
        
        return score
    
    def get_recommendations(self, title, num_recommendations=5):
        """Get recommendations based on a title"""
        title_lower = title.lower()
        
        # Find the input movie
        input_movie = None
        for movie in self.movies:
            if title_lower in movie['title'].lower():
                input_movie = movie
                break
        
        if not input_movie:
            return f"Movie '{title}' not found. Available titles: {[m['title'] for m in self.movies[:5]]}"
        
        # Calculate similarities
        similarities = []
        for movie in self.movies:
            if movie['title'] != input_movie['title']:
                sim_score = self.simple_similarity(input_movie['title'], movie['title'])
                similarities.append((movie, sim_score))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top recommendations
        recommendations = []
        for movie, score in similarities[:num_recommendations]:
            recommendations.append({
                'title': movie['title'],
                'type': movie['type'],
                'year': movie['release_year'],
                'genres': movie['listed_in'],
                'similarity_score': score
            })
        
        return recommendations
    
    def get_by_genre(self, genre, content_type='all', num_results=5):
        """Get titles by genre"""
        results = []
        genre_lower = genre.lower()
        
        for movie in self.movies:
            # Check genre match
            movie_genres = [g.strip().lower() for g in movie['listed_in'].split(',')]
            if genre_lower in movie_genres:
                # Check content type
                if content_type == 'all' or movie['type'].lower() == content_type.lower():
                    results.append({
                        'title': movie['title'],
                        'type': movie['type'],
                        'year': movie['release_year'],
                        'genres': movie['listed_in'],
                        'description': movie['description'][:100] + '...'
                    })
        
        return results[:num_results]
    
    def search(self, query, num_results=5):
        """Search for titles"""
        results = []
        query_lower = query.lower()
        
        for movie in self.movies:
            # Search in multiple fields
            searchable_text = ' '.join([
                movie['title'],
                movie['description'],
                movie['cast'],
                movie['director'],
                movie['listed_in']
            ]).lower()
            
            if query_lower in searchable_text:
                results.append({
                    'title': movie['title'],
                    'type': movie['type'],
                    'year': movie['release_year'],
                    'genres': movie['listed_in'],
                    'description': movie['description'][:100] + '...'
                })
        
        return results[:num_results]
    
    def get_by_description(self, description, content_type='all', num_results=5):
        """Get titles by description using simple keyword matching"""
        results = []
        desc_words = set(description.lower().split())
        
        for movie in self.movies:
            # Check content type
            if content_type != 'all' and movie['type'].lower() != content_type.lower():
                continue
            
            # Create searchable text
            searchable_text = ' '.join([
                movie['title'],
                movie['description'],
                movie['cast'],
                movie['director'],
                movie['listed_in']
            ]).lower()
            
            # Count matching words
            search_words = set(searchable_text.split())
            matches = len(desc_words.intersection(search_words))
            
            if matches > 0:
                results.append({
                    'title': movie['title'],
                    'type': movie['type'],
                    'year': movie['release_year'],
                    'genres': movie['listed_in'],
                    'description': movie['description'][:100] + '...',
                    'match_score': matches
                })
        
        # Sort by match score
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return results[:num_results]
    
    def get_stats(self):
        """Get basic statistics"""
        total = len(self.movies)
        movies = len([m for m in self.movies if m['type'] == 'Movie'])
        tv_shows = len([m for m in self.movies if m['type'] == 'TV Show'])
        
        all_genres = []
        for movie in self.movies:
            genres = [g.strip() for g in movie['listed_in'].split(',')]
            all_genres.extend(genres)
        
        unique_genres = len(set(all_genres))
        
        return {
            'total_titles': total,
            'movies': movies,
            'tv_shows': tv_shows,
            'unique_genres': unique_genres
        }

def demo():
    """Run a simple demo of the recommendation bot"""
    print("🎬 Simple Netflix Recommendation Bot Demo")
    print("=" * 50)
    
    bot = SimpleNetflixBot()
    
    # Show stats
    stats = bot.get_stats()
    print(f"\n📊 Dataset: {stats['total_titles']} titles ({stats['movies']} movies, {stats['tv_shows']} TV shows)")
    print(f"Genres: {stats['unique_genres']}")
    
    # Demo recommendations
    print(f"\n🎯 Recommendations based on 'Stranger Things':")
    recs = bot.get_recommendations('Stranger Things', 3)
    if isinstance(recs, list):
        for i, rec in enumerate(recs, 1):
            print(f"{i}. {rec['title']} ({rec['type']}, {rec['year']}) - Score: {rec['similarity_score']}")
    else:
        print(recs)
    
    # Demo genre search
    print(f"\n🎭 Comedy titles:")
    comedies = bot.get_by_genre('Comedy', 'all', 3)
    for i, movie in enumerate(comedies, 1):
        print(f"{i}. {movie['title']} ({movie['type']}, {movie['year']})")
    
    # Demo search
    print(f"\n🔍 Search results for 'sci-fi':")
    search_results = bot.search('sci-fi', 3)
    for i, result in enumerate(search_results, 1):
        print(f"{i}. {result['title']} ({result['type']}, {result['year']})")
    
    # Demo description-based search
    print(f"\n📖 Search results for description 'dreams':")
    desc_results = bot.get_by_description('dreams', 'all', 3)
    for i, result in enumerate(desc_results, 1):
        print(f"{i}. {result['title']} ({result['type']}, {result['year']}) - Matches: {result['match_score']}")
    
    print(f"\n✅ Demo completed! For the full experience, install the required packages and run:")
    print("   - streamlit run streamlit_app.py (web interface)")
    print("   - python cli_app.py (command line)")

if __name__ == "__main__":
    demo()
