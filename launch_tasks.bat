@echo off
echo PRODIGY Software Development Internship
echo =======================================
echo.
echo Available Tasks:
echo 1. Task 1: Temperature Converter
echo 2. Task 2: Number Guessing Game
echo 3. Task 3: [Next Task - Not Started]
echo 4. Task 4: [Next Task - Not Started]
echo 5. Task 5: [Next Task - Not Started]
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo Starting Task 1: Temperature Converter...
    cd Task_01_Temperature_Converter
    call run_converter.bat
    cd ..
) else if "%choice%"=="2" (
    echo Starting Task 2: Number Guessing Game...
    cd Task_02_Guessing_Game
    call run_game.bat
    cd ..
) else if "%choice%"=="3" (
    echo Task 3 is not yet available.
    echo Please wait for the next assignment.
    pause
) else if "%choice%"=="4" (
    echo Task 4 is not yet available.
    echo Please wait for the next assignment.
    pause
) else if "%choice%"=="5" (
    echo Task 5 is not yet available.
    echo Please wait for the next assignment.
    pause
) else if "%choice%"=="6" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Please run the script again.
    pause
)

pause
