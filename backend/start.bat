@echo off
echo Starting Mobibit Africa Backend...
cd /d C:\Users\user\Desktop\sats-card\backend
call venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
