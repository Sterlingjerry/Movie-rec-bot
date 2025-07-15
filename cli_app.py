#!/usr/bin/env python3
"""
Netflix Movie Recommendation Bot - Command Line Interface
"""

import os
from recommendation_engine import NetflixRecommendationBot
from data_downloader import download_netflix_dataset

class NetflixBotCLI:
    def __init__(self):
        self.bot = None
        self.setup_bot()
    
    def setup_bot(self):
        """Setup the recommendation bot"""
        print("🎬 Netflix Movie Recommendation Bot")
        print("=" * 40)
        
        # Check if dataset exists
        if not os.path.exists("netflix_titles.csv"):
            print("Dataset not found locally. Downloading...")
            df, local_path = download_netflix_dataset()
            if df is None:
                print("❌ Failed to download dataset. Please check your internet connection.")
                return
        
        # Initialize bot
        print("Loading recommendation engine...")
        self.bot = NetflixRecommendationBot()
        
        if self.bot.df is not None:
            print("✅ Recommendation bot loaded successfully!")
            stats = self.bot.get_stats()
            print(f"📊 Dataset contains {stats['total_titles']} titles ({stats['movies']} movies, {stats['tv_shows']} TV shows)")
        else:
            print("❌ Failed to load recommendation bot.")
    
    def display_recommendations(self, recommendations, title="Recommendations"):
        """Display recommendations in CLI format"""
        print(f"\n{title}")
        print("-" * len(title))
        
        if isinstance(recommendations, str):
            print(f"⚠️  {recommendations}")
            return
        
        if recommendations.empty:
            print("No recommendations found.")
            return
        
        for idx, (_, row) in enumerate(recommendations.iterrows(), 1):
            print(f"\n{idx}. {row['title']} ({row['type']}, {row['release_year']})")
            print(f"   Rating: {row['rating']}")
            print(f"   Genres: {row['listed_in']}")
            description = str(row['description'])[:150] + "..." if len(str(row['description'])) > 150 else str(row['description'])
            print(f"   Description: {description}")
    
    def content_based_recommendations(self):
        """Get content-based recommendations"""
        title = input("\nEnter a movie/TV show title: ").strip()
        if not title:
            print("❌ Please enter a valid title.")
            return
        
        try:
            num_recs = int(input("Number of recommendations (default 10): ") or "10")
        except ValueError:
            num_recs = 10
        
        recommendations = self.bot.get_content_recommendations(title, num_recs)
        self.display_recommendations(recommendations, f"Movies/Shows similar to '{title}'")
    
    def description_based_recommendations(self):
        """Get description-based recommendations"""
        description = input("\nDescribe what you want to watch (e.g., 'funny romantic comedy', 'dark sci-fi thriller'): ").strip()
        if not description:
            print("❌ Please enter a valid description.")
            return
        
        content_type = input("Content type (movie/tv show/all, default: all): ").strip().lower() or "all"
        
        try:
            num_recs = int(input("Number of recommendations (default 10): ") or "10")
        except ValueError:
            num_recs = 10
        
        recommendations = self.bot.get_recommendations_by_description(description, content_type, num_recs)
        self.display_recommendations(recommendations, f"Recommendations for '{description}'")
    
    def genre_based_recommendations(self):
        """Get genre-based recommendations"""
        print("\nAvailable genres: Action, Comedy, Drama, Horror, Romance, Thriller, Documentary, Crime, Sci-Fi, Fantasy, Animation, Family, Mystery, Adventure, War, History")
        genre = input("Enter a genre: ").strip()
        if not genre:
            print("❌ Please enter a valid genre.")
            return
        
        content_type = input("Content type (movie/tv show/all, default: all): ").strip().lower() or "all"
        
        try:
            num_recs = int(input("Number of recommendations (default 10): ") or "10")
        except ValueError:
            num_recs = 10
        
        recommendations = self.bot.get_recommendations_by_genre(genre, content_type, num_recs)
        self.display_recommendations(recommendations, f"Top {content_type} in {genre}")
    
    def search_titles(self):
        """Search for titles"""
        query = input("\nEnter search query (title, cast, director, description): ").strip()
        if not query:
            print("❌ Please enter a valid search query.")
            return
        
        try:
            num_results = int(input("Number of results (default 10): ") or "10")
        except ValueError:
            num_results = 10
        
        results = self.bot.search_titles(query, num_results)
        self.display_recommendations(results, f"Search results for '{query}'")
    
    def show_stats(self):
        """Show dataset statistics"""
        stats = self.bot.get_stats()
        print("\n📊 Dataset Statistics")
        print("=" * 20)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    def run(self):
        """Run the CLI interface"""
        if self.bot is None or self.bot.df is None:
            print("❌ Bot not initialized. Exiting.")
            return
        
        while True:
            print("\n" + "=" * 50)
            print("🎬 NETFLIX RECOMMENDATION BOT")
            print("=" * 50)
            print("1. Content-based recommendations")
            print("2. Genre-based recommendations")
            print("3. Description-based recommendations")
            print("4. Search titles")
            print("5. Dataset statistics")
            print("6. Exit")
            
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == '1':
                self.content_based_recommendations()
            elif choice == '2':
                self.genre_based_recommendations()
            elif choice == '3':
                self.description_based_recommendations()
            elif choice == '4':
                self.search_titles()
            elif choice == '5':
                self.show_stats()
            elif choice == '6':
                print("👋 Thank you for using Netflix Recommendation Bot!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    cli = NetflixBotCLI()
    cli.run()
