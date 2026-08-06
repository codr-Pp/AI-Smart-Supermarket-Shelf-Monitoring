@echo off
title Campa Vision AI Server

cd /d "%~dp0"

if exist .venv\Scripts\activate (
    echo Activating virtual environment...
    call .venv\Scripts\activate
)

echo Starting Flask server...
python run.py

pause
