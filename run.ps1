#!/usr/bin/env pwsh
# Quick start script for Cross-Chain Navigator Agent

Write-Host ">>> Starting Cross-Chain Navigator Agent..." -ForegroundColor Cyan
Write-Host ""

# Start backend server in new window
Write-Host ">>> Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$PSScriptRoot\backend'; .\venv\Scripts\Activate.ps1; python -m uvicorn main:app --reload"

# Wait for server
Write-Host ">>> Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

# Run test
Write-Host ""
Write-Host ">>> Running API Test..." -ForegroundColor Green
cd backend
.\venv\Scripts\Activate.ps1
python test_api.py

Write-Host ""
Write-Host ">>> Done! Server is running in separate window." -ForegroundColor Green
Write-Host "    API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "    Docs: http://localhost:8000/docs" -ForegroundColor Cyan
