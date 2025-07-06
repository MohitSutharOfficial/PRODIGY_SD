@echo off
echo Number Guessing Game
echo ====================
echo.
echo Choose a version to run:
echo 1. GUI Version (Recommended)
echo 2. Command Line Version
echo 3. Test and Demo Script
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting GUI version...
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" guessing_game.py
    if errorlevel 1 (
        echo Error: Python not found or script failed to run
        echo Please make sure Python is installed and in your PATH
        pause
    )
) else if "%choice%"=="2" (
    echo Starting CLI version...
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" guessing_game_cli.py
    if errorlevel 1 (
        echo Error: Python not found or script failed to run
        echo Please make sure Python is installed and in your PATH
        pause
    )
) else if "%choice%"=="3" (
    echo Starting test and demo script...
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" test_demo.py
    if errorlevel 1 (
        echo Error: Python not found or script failed to run
        echo Please make sure Python is installed and in your PATH
        pause
    )
) else if "%choice%"=="4" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Please run the script again.
    pause
)

pause
