#!/usr/bin/env pwsh
# Start backend server only

Write-Host ">>> Starting Backend Server..." -ForegroundColor Cyan

cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload

Write-Host ">>> Server stopped." -ForegroundColor Yellow
