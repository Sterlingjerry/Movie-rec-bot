import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from recommendation_engine import NetflixRecommendationBot
from data_downloader import download_netflix_dataset
import os

# Page configuration
st.set_page_config(
    page_title="Netflix Movie Recommendation Bot",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #E50914;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #831010;
        margin-bottom: 1rem;
    }
    .recommendation-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #E50914;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #000000;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_recommendation_bot():
    """Load the recommendation bot with caching"""
    # Check if dataset exists locally
    if not os.path.exists("netflix_titles.csv"):
        with st.spinner("Downloading Netflix dataset... This may take a few minutes."):
            df, local_path = download_netflix_dataset()
            if df is None:
                st.error("Failed to download dataset. Please check your internet connection.")
                return None
    
    with st.spinner("Loading recommendation engine..."):
        bot = NetflixRecommendationBot()
        return bot

def display_recommendations(recommendations, title="Recommendations"):
    """Display recommendations in a nice format"""
    st.markdown(f"<h3 class='sub-header'>{title}</h3>", unsafe_allow_html=True)
    
    if isinstance(recommendations, str):
        st.warning(recommendations)
        return
    
    if recommendations.empty:
        st.info("No recommendations found.")
        return
    
    for idx, row in recommendations.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>{row['title']} ({row['type']})</h4>
                <p><strong>Release Year:</strong> {row['release_year']}</p>
                <p><strong>Rating:</strong> {row['rating']}</p>
                <p><strong>Genres:</strong> {row['listed_in']}</p>
                <p><strong>Description:</strong> {row['description'][:200]}{'...' if len(str(row['description'])) > 200 else ''}</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">🎬 Netflix Movie Recommendation Bot</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load the recommendation bot
    bot = load_recommendation_bot()
    
    if bot is None or bot.df is None:
        st.error("Failed to load the recommendation engine. Please try again.")
        return
    
    # Sidebar
    st.sidebar.title("🎯 Recommendation Options")
    
    # Get dataset statistics
    stats = bot.get_stats()
    
    # Display stats in sidebar
    st.sidebar.markdown("### 📊 Dataset Statistics")
    st.sidebar.metric("Total Titles", stats['total_titles'])
    st.sidebar.metric("Movies", stats['movies'])
    st.sidebar.metric("TV Shows", stats['tv_shows'])
    st.sidebar.metric("Unique Genres", stats['unique_genres'])
    st.sidebar.write(f"**Release Years:** {stats['release_year_range']}")
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Content-Based", "🎭 By Genre", "📝 By Description", "🔎 Search"])
    
    with tab1:
        st.markdown("### Content-Based Recommendations")
        st.write("Get recommendations based on a specific title you like.")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            title_input = st.text_input("Enter a movie/TV show title:", placeholder="e.g., Stranger Things, The Matrix")
        with col2:
            num_recs = st.selectbox("Number of recommendations:", [5, 10, 15, 20], index=1)
        
        if st.button("Get Content Recommendations", type="primary"):
            if title_input:
                recommendations = bot.get_content_recommendations(title_input, num_recs)
                display_recommendations(recommendations, f"Movies/Shows similar to '{title_input}'")
            else:
                st.warning("Please enter a title.")
    
    with tab2:
        st.markdown("### Recommendations by Genre")
        st.write("Discover content in your favorite genres.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            genre_input = st.selectbox("Select Genre:", [
                "Action", "Comedy", "Drama", "Horror", "Romance", "Thriller",
                "Documentary", "Crime", "Sci-Fi", "Fantasy", "Animation",
                "Family", "Mystery", "Adventure", "War", "History"
            ])
        with col2:
            content_type = st.selectbox("Content Type:", ["All", "Movie", "TV Show"])
        with col3:
            num_genre_recs = st.selectbox("Number of results:", [5, 10, 15, 20], index=1, key="genre_num")
        
        if st.button("Get Genre Recommendations", type="primary"):
            recommendations = bot.get_recommendations_by_genre(genre_input, content_type.lower(), num_genre_recs)
            display_recommendations(recommendations, f"Top {content_type} in {genre_input}")
    
    with tab3:
        st.markdown("### Recommendations by Description")
        st.write("Describe what you want to watch in natural language.")
        
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            description_input = st.text_area(
                "Describe what you want to watch:",
                placeholder="Examples:\n• 'funny romantic comedy with friends'\n• 'dark thriller with mystery and suspense'\n• 'action movie with superheroes and special effects'\n• 'heartwarming family drama about relationships'",
                height=100
            )
        with col2:
            desc_content_type = st.selectbox("Content Type:", ["All", "Movie", "TV Show"], key="desc_type")
        with col3:
            num_desc_recs = st.selectbox("Number of results:", [5, 10, 15, 20], index=1, key="desc_num")
        
        if st.button("Get Description-Based Recommendations", type="primary"):
            if description_input.strip():
                recommendations = bot.get_recommendations_by_description(description_input, desc_content_type.lower(), num_desc_recs)
                display_recommendations(recommendations, f"Recommendations for '{description_input[:50]}...'")
            else:
                st.warning("Please enter a description of what you'd like to watch.")
    
    with tab4:
        st.markdown("### Search Titles")
        st.write("Search for specific content by title, cast, director, or description.")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search for:", placeholder="e.g., Leonardo DiCaprio, zombies, comedy")
        with col2:
            num_search = st.selectbox("Number of results:", [5, 10, 15, 20], index=1, key="search_num")
        
        if st.button("Search", type="primary"):
            if search_query:
                results = bot.search_titles(search_query, num_search)
                display_recommendations(results, f"Search results for '{search_query}'")
            else:
                st.warning("Please enter a search query.")

if __name__ == "__main__":
    main()
