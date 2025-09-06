@echo off
echo Starting Zombie Strike...
python launch_game.py
if errorlevel 1 (
    echo.
    echo Failed to start the game.
    echo Please make sure you have Python 3.8 or later installed.
    echo You can download Python from https://www.python.org/downloads/
    echo.
    pause
)
pause
