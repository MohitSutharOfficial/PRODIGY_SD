@echo off
:start
echo ===============================================
echo    Contact Management System Launcher
echo ===============================================
echo.
echo Choose your interface:
echo 1. GUI Version (Recommended)
echo 2. CLI Version 
echo 3. Run Tests and Demo
echo 4. Exit
echo.
set /p choice=Enter your choice (1-4): 

if "%choice%"=="1" (
    echo.
    echo Starting GUI Contact Manager...
    echo.
    py contact_manager.py
) else if "%choice%"=="2" (
    echo.
    echo Starting CLI Contact Manager...
    echo.
    py contact_manager_cli.py
) else if "%choice%"=="3" (
    echo.
    echo Running Tests and Demo...
    echo.
    py test_demo.py
) else if "%choice%"=="4" (
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
