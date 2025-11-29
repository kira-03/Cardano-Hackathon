# Cross-Chain Navigator Agent - Setup Script
# This script sets up both backend and frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cross-Chain Navigator Agent Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "[OK] $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "[OK] Node.js $nodeVersion found" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Setup backend
Set-Location backend

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "[WARNING] Please edit backend/.env and add your Blockfrost API key" -ForegroundColor Yellow
} else {
    Write-Host "[OK] .env file already exists" -ForegroundColor Green
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python scripts/init_db.py

Write-Host "[OK] Backend setup complete!" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Setup frontend
Set-Location frontend

# Install dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

# Create .env.local if it doesn't exist
if (-not (Test-Path .env.local)) {
    Write-Host "Creating .env.local file..." -ForegroundColor Yellow
    Copy-Item .env.local.example .env.local
    Write-Host "[OK] .env.local created" -ForegroundColor Green
} else {
    Write-Host "[OK] .env.local file already exists" -ForegroundColor Green
}

Write-Host "[OK] Frontend setup complete!" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit backend/.env and add your Blockfrost API key" -ForegroundColor White
Write-Host "   Get one at: https://blockfrost.io" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the backend (in one terminal):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python -m uvicorn main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start the frontend (in another terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Open http://localhost:3000 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see QUICKSTART.md" -ForegroundColor Cyan
Write-Host ""
