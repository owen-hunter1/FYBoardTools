@echo off
echo =========================
echo Setting up virtual environment...
echo =========================

if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate

echo.
echo Installing dependencies...
echo.

python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete.
echo To start the app, run:
echo.
echo     venv\Scripts\activate
echo     streamlit run app.py
echo.
pause