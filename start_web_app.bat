@echo off
echo ========================================
echo Starting Netflix Recommendation Bot
echo ========================================

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Launching Streamlit web interface...
echo Open your browser to the URL shown below.
echo.

python -m streamlit run streamlit_app.py

pause
