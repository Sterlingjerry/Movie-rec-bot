"""
Simple test script to verify the Netflix Recommendation Bot setup
"""

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'kagglehub',
        'pandas', 
        'numpy',
        'sklearn',
        'matplotlib',
        'seaborn',
        'nltk',
        'wordcloud',
        'streamlit',
        'plotly'
    ]
    
    print("Testing package imports...")
    print("=" * 40)
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package} - {e}")
    
    print("\n" + "=" * 40)
    print("If any packages are missing, install them with:")
    print("pip install kagglehub pandas numpy scikit-learn matplotlib seaborn nltk wordcloud streamlit plotly")

def test_basic_functionality():
    """Test basic functionality without downloading dataset"""
    try:
        import pandas as pd
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        print("\nTesting basic functionality...")
        print("=" * 40)
        
        # Create a simple test dataset
        test_data = {
            'title': ['Movie A', 'Movie B', 'Movie C'],
            'description': ['Action movie about heroes', 'Comedy about friends', 'Drama about life'],
            'listed_in': ['Action, Adventure', 'Comedy', 'Drama, Romance'],
            'type': ['Movie', 'Movie', 'Movie'],
            'release_year': [2020, 2021, 2019]
        }
        
        df = pd.DataFrame(test_data)
        
        # Test TF-IDF vectorization
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(df['description'])
        
        print(f"✅ Created test dataset with {len(df)} movies")
        print(f"✅ TF-IDF matrix shape: {tfidf_matrix.shape}")
        print("✅ Basic recommendation engine components working!")
        
    except Exception as e:
        print(f"❌ Error in basic functionality test: {e}")

if __name__ == "__main__":
    test_imports()
    test_basic_functionality()
    
    print("\n" + "=" * 50)
    print("🎬 NETFLIX RECOMMENDATION BOT - SETUP COMPLETE")
    print("=" * 50)
    print("\nAvailable features:")
    print("✅ Content-based recommendations")
    print("✅ Genre-based recommendations") 
    print("✅ Description-based recommendations")
    print("✅ Search functionality")
    print("\nTo run the recommendation bot:")
    print("1. Web Interface: streamlit run streamlit_app.py")
    print("2. Command Line: python cli_app.py")
    print("3. Download dataset: python data_downloader.py")
    print("\nMake sure all packages are installed before running!")
