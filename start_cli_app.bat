@echo off
echo ========================================
echo Netflix Recommendation Bot - CLI Mode
echo ========================================

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting command line interface...
echo.

python cli_app.py

pause
