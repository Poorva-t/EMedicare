@echo off
echo ==========================================
echo Starting Healthcare MVP
echo ==========================================

echo [1] Checking and installing requirements...
pip install -r requirements.txt

echo [2] Seeding Database (if empty)...
python seed_data.py

echo [3] Setting Environment Variables...
:: ADD YOUR GROQ API KEY HERE:
set GROQ_API_KEY=YOUR_API_KEY

echo [4] Starting Main Backend (Port 8000)...
start cmd /k "python main.py"

echo ==========================================
echo MVP is running!
echo Access the UI at: http://localhost:8000
echo ==========================================
pause
