#!/usr/bin/env pwsh
# Run API tests

Write-Host ">>> Running API Tests..." -ForegroundColor Cyan

cd backend
.\venv\Scripts\Activate.ps1
python test_api.py

Write-Host ">>> Tests completed." -ForegroundColor Green
