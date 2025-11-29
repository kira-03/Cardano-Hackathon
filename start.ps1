# Cross-Chain Navigator Agent - Startup Script
# Starts both backend and frontend in separate windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cross-Chain Navigator Agent" -ForegroundColor Cyan
Write-Host "Starting Backend and Frontend..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if setup has been run
if (-not (Test-Path "backend\venv")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first:" -ForegroundColor Yellow
    Write-Host "   .\setup.ps1" -ForegroundColor White
    exit 1
}

if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[ERROR] Node modules not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first:" -ForegroundColor Yellow
    Write-Host "   .\setup.ps1" -ForegroundColor White
    exit 1
}

# Check if .env exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "[ERROR] Backend .env file not found!" -ForegroundColor Red
    Write-Host "Please create backend\.env with your Blockfrost API key" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Setup verified" -ForegroundColor Green
Write-Host ""

# Start backend in new window
Write-Host "[STARTING] Backend (http://localhost:8000)..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\venv\Scripts\Activate.ps1; Write-Host 'Backend Starting...' -ForegroundColor Cyan; python -m uvicorn main:app --reload"

Start-Sleep -Seconds 2

# -----------------------------------------
# FRONTEND START DISABLED / COMMENTED OUT
# -----------------------------------------
# Write-Host "[STARTING] Frontend (http://localhost:3000)..." -ForegroundColor Yellow
# $frontendPath = Join-Path $PSScriptRoot "frontend"
# Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Frontend Starting...' -ForegroundColor Green; npm run dev"
# Start-Sleep -Seconds 2
# -----------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "[SUCCESS] Backend Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend was NOT started (commented out)." -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop: Close the PowerShell window or press Ctrl+C" -ForegroundColor Gray
Write-Host ""
