@echo off
REM WatchShop - Quick Start Script (Windows)
REM Hướng dẫn chạy website nhanh nhất

title WatchShop - Quick Start
color 0A
cls

echo.
echo ========================================
echo   WATCHSHOP - BAN DONG HO CHINH HANG
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python from python.org
    pause
    exit /b 1
)

REM Check if venv exists
if exist venv (
    echo.
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo.
    echo Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
)

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo.
echo Creating database...
python manage.py migrate

REM Load seed data
echo.
echo Loading sample data...
python manage.py seed_data

REM Ask about admin creation
echo.
set /p create_admin="Do you want to create a superuser admin account? (y/n): "
if /i "%create_admin%"=="y" (
    python manage.py createsuperuser
)

REM Start server
echo.
echo ========================================
echo   STARTING DEVELOPMENT SERVER
echo ========================================
echo.
echo Website: http://127.0.0.1:8000/
echo Admin Panel: http://127.0.0.1:8000/admin/
echo Products: http://127.0.0.1:8000/products/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause
