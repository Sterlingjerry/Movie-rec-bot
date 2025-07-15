@echo off
echo ========================================
echo Download Netflix Dataset
echo ========================================

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Downloading Netflix dataset from Kaggle...
echo This may take a few minutes...
echo.

python data_downloader.py

echo.
echo Download completed!
pause
