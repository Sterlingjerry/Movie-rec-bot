@echo off
echo ========================================
echo Netflix Movie Recommendation Bot Setup
echo ========================================

echo.
echo Creating virtual environment...
py -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing required Python packages...
echo.

python -m pip install --upgrade pip
python -m pip install kagglehub
python -m pip install pandas
python -m pip install numpy
python -m pip install scikit-learn
python -m pip install matplotlib
python -m pip install seaborn
python -m pip install nltk
python -m pip install wordcloud
python -m pip install streamlit
python -m pip install plotly

echo.
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"

echo.
echo ========================================
echo Installation complete!
echo ========================================

echo.
echo To run the recommendation bot:
echo 1. Web Interface: streamlit run streamlit_app.py
echo 2. Command Line: python cli_app.py
echo 3. Download dataset: python data_downloader.py

echo.
pause
