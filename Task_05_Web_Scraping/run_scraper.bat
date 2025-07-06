@echo off
:start
echo ===============================================
echo        Web Scraping Tool Launcher
echo ===============================================
echo.
echo Choose your interface:
echo 1. GUI Version (Recommended)
echo 2. CLI Version 
echo 3. Run Tests and Demo
echo 4. Install Dependencies
echo 5. Exit
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" (
    echo.
    echo Starting GUI Web Scraper...
    echo.
    py web_scraper.py
) else if "%choice%"=="2" (
    echo.
    echo Starting CLI Web Scraper...
    echo.
    py web_scraper_cli.py
) else if "%choice%"=="3" (
    echo.
    echo Running Tests and Demo...
    echo.
    py test_demo.py
) else if "%choice%"=="4" (
    echo.
    echo Installing Dependencies...
    echo.
    py -m pip install -r requirements.txt
    echo.
    echo Dependencies installation completed!
) else if "%choice%"=="5" (
    echo.
    echo Goodbye!
    exit /b 0
) else (
    echo.
    echo Invalid choice. Please run the script again.
    echo.
)

echo.
echo Press any key to return to the main menu...
pause > nul
goto start
