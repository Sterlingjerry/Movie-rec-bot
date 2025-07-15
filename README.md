# Movie Recommendation Bot

A comprehensive Netflix movie and TV show recommendation system using machine learning and content-based filtering. This bot analyzes the Netflix dataset gotten from kaggle to provide personalized recommendations based on various criteria.

## Features

- **Content-Based Recommendations**: Get recommendations based on movies/shows 
- **Description-Based Recommendations**: Describe what you want to watch (e.g., "funny romantic comedy", "dark sci-fi thriller")
- **Genre-Based Filtering**: Discover content by your favorite genres
- **Advanced Search**: Search by title, cast, director, or description
- **Interactive Web Interface**: Streamlit web app
-

### Prerequisites

- Python 3.8 or higher

### Installation

1. **Clone or download the project files**

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Netflix dataset** (first time only):
   ```bash
   python data_downloader.py
   ```

## 🎯 Usage


Launch the Streamlit web app:
```bash
streamlit run streamlit_app.py
```

### Command Line Interface

For a simple CLI experience:
```bash
python cli_app.py
```

Python API

Use the recommendation engine directly in your code:

```python
from recommendation_engine import NetflixRecommendationBot

# Initialize the bot
bot = NetflixRecommendationBot()

# Get content-based recommendations
recommendations = bot.get_content_recommendations("Stranger Things", 10)
print(recommendations)

# Get description-based recommendations
description_recs = bot.get_recommendations_by_description("funny romantic comedy", "movie", 5)
print(description_recs)

# Get genre-based recommendations
action_movies = bot.get_recommendations_by_genre("Action", "movie", 5)
print(action_movies)

# Search for titles
results = bot.search_titles("Leonardo DiCaprio", 5)
print(results)
```

## 📊 Dataset

This project uses the "Netflix Movies and TV Shows" dataset from Kaggle. The dataset contains:

- **8,800+** Netflix titles
- **Movies and TV Shows** from multiple countries
- **Detailed data** including cast, director, genres, ratings, and descriptions
- **Release years** spanning several decades

## 🛠️ Technical Details

### Recommendation Engine

The system uses multiple recommendation strategies:

1. **Content-Based Filtering**:
   - TF-IDF vectorization of combined features (genres, description, cast, director)
   - Cosine similarity for finding similar content
   - Natural language processing with NLTK

2. **Genre-Based Filtering**:
   - Direct genre matching and filtering
   - Content type filtering (Movies vs TV Shows)

3. **Description-Based Filtering**:
   - Natural language processing of user descriptions
   - TF-IDF similarity matching with content descriptions

### Technologies Used

- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms (TF-IDF, cosine similarity)
- **NLTK**: Natural language processing
- **Streamlit**: Web interface
- **Plotly**: Interactive visualizations
- **KaggleHub**: Dataset downloading

## 🚀 Future Enhancements

Potential improvements:
- User rating system and collaborative filtering
- Removing Bugs
- Machine learning models for better recommendations
- Integration with Netflix API for real-time data
- User profiles and personalized recommendations
- Export recommendations to various formats


## NOTE
This program is still under development so there might still be quite a few bugs.
