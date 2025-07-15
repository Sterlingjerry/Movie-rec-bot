# 🎬 Netflix Movie Recommendation Bot

A comprehensive Netflix movie and TV show recommendation system using machine learning and content-based filtering. This bot analyzes the Netflix dataset to provide personalized recommendations based on various criteria.

## 🌟 Features

- **Content-Based Recommendations**: Get recommendations based on movies/shows you already like
- **Description-Based Recommendations**: Describe what you want to watch in natural language (e.g., "funny romantic comedy", "dark sci-fi thriller")
- **Genre-Based Filtering**: Discover content by your favorite genres
- **Advanced Search**: Search by title, cast, director, or description
- **Interactive Web Interface**: Beautiful Streamlit web app
- **Command Line Interface**: Simple CLI for quick recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Internet connection (for downloading the dataset)

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

### Web Interface (Recommended)

Launch the Streamlit web app:
```bash
streamlit run streamlit_app.py
```

This will open a beautiful web interface in your browser with:
- Content-based recommendations
- Description-based recommendations 
- Genre browsing
- Advanced search functionality

### Command Line Interface

For a simple CLI experience:
```bash
python cli_app.py
```

### Python API

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

This project uses the "Netflix Movies and TV Shows" dataset from Kaggle by Shivam Bansal. The dataset contains:

- **8,800+** Netflix titles
- **Movies and TV Shows** from multiple countries
- **Detailed metadata** including cast, director, genres, ratings, and descriptions
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

## 📁 Project Structure

```
Netflix movie bot/
├── data_downloader.py      # Download Netflix dataset from Kaggle
├── recommendation_engine.py # Core recommendation algorithms
├── streamlit_app.py        # Web interface
├── cli_app.py             # Command line interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── netflix_titles.csv    # Downloaded dataset (created after first run)
```

## 🎨 Features in Detail

### Content-Based Recommendations
- Enter any movie or TV show title
- Get recommendations based on similar content
- Uses advanced NLP to analyze descriptions, cast, and genres

### Description-Based Recommendations
- Describe what you want to watch in natural language
- AI-powered understanding of your preferences
- Examples: "funny romantic comedy", "dark thriller with mystery", "heartwarming family drama"

### Genre Exploration
- Browse by popular genres (Action, Comedy, Drama, etc.)
- Filter by content type (Movies, TV Shows, or Both)
- Discover new content in your favorite categories

### Search Functionality
- Search across titles, descriptions, cast, and directors
- Flexible matching for easy discovery
- Ranked results based on relevance

## 🔧 Customization

You can easily customize the recommendation engine:

1. **Adjust similarity weights**: Modify the `combined_features` in `recommendation_engine.py`
2. **Add new features**: Include additional metadata like duration, country, etc.
3. **Change algorithms**: Experiment with different similarity metrics
4. **Modify UI**: Customize the Streamlit interface in `streamlit_app.py`

## 📈 Performance

- **Fast recommendations**: Optimized algorithms for quick results
- **Caching**: Streamlit caching for improved performance
- **Scalable**: Can handle large datasets efficiently
- **Memory efficient**: Smart data preprocessing and storage

## 🚀 Future Enhancements

Potential improvements:
- User rating system and collaborative filtering
- Machine learning models for better recommendations
- Integration with Netflix API for real-time data
- User profiles and personalized recommendations
- Export recommendations to various formats

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new recommendation algorithms
- Improving the user interface
- Adding more analytics features
- Optimizing performance
- Fixing bugs

## 📄 License

This project is for educational purposes. The Netflix dataset is sourced from Kaggle and subject to its terms of use.

## 🙏 Acknowledgments

- **Kaggle** for providing the Netflix dataset
- **Shivam Bansal** for creating and maintaining the dataset
- **Netflix** for the inspiration
- **Open source community** for the amazing libraries used

---

**Happy movie watching! 🍿**
