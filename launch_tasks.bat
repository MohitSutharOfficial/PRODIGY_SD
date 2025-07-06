@echo off
:start
echo ========================================================
echo     PRODIGY Software Development Internship
echo     Professional Programming Portfolio
echo ========================================================
echo.
echo Available Tasks:
echo 1. Temperature Converter        - Basic I/O and Math Functions
echo 2. Number Guessing Game        - Game Logic and Statistics  
echo 3. Contact Management System   - Data Structures and File I/O
echo 4. Sudoku Solver              - Advanced Algorithms and Recursion
echo 5. Web Scraping Tool          - Web APIs and Data Processing
echo 6. Exit Program
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo Starting Task 1: Temperature Converter...
    echo ==========================================
    cd Task_01_Temperature_Converter
    call run_converter.bat
    cd ..
) else if "%choice%"=="2" (
    echo.
    echo Starting Task 2: Number Guessing Game...
    echo ========================================
    cd Task_02_Guessing_Game
    call run_game.bat
    cd ..
) else if "%choice%"=="3" (
    echo.
    echo Starting Task 3: Contact Management System...
    echo =============================================
    cd Task_03_Contact_Management
    call run_contacts.bat
    cd ..
) else if "%choice%"=="4" (
    echo.
    echo Starting Task 4: Sudoku Solver...
    echo =================================
    cd Task_04_Sudoku_Solver
    call run_sudoku.bat
    cd ..
) else if "%choice%"=="5" (
    echo.
    echo Starting Task 5: Web Scraping Tool...
    echo =====================================
    cd Task_05_Web_Scraping
    call run_scraper.bat
    cd ..
) else if "%choice%"=="6" (
    echo.
    echo Thank you for exploring the PRODIGY Software Development Internship!
    echo All tasks completed successfully.
    echo.
    pause
    exit
) else (
    echo.
    echo Invalid choice. Please enter a number between 1-6.
    echo.
    pause
    goto :start
)

echo.
echo Returning to main menu...
echo.
pause
goto :start
