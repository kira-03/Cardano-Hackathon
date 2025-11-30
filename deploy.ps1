# Deployment Script for Render
# This script helps you prepare and push your code to GitHub for Render deployment

Write-Host "🚀 Cardano Cross-Chain Navigator - Render Deployment Helper" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "❌ Git repository not initialized!" -ForegroundColor Red
    Write-Host "Run: git init" -ForegroundColor Yellow
    exit 1
}

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Uncommitted changes detected:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    
    $commit = Read-Host "Do you want to commit these changes? (y/n)"
    if ($commit -eq "y") {
        $message = Read-Host "Enter commit message (or press Enter for default)"
        if ([string]::IsNullOrWhiteSpace($message)) {
            $message = "Ready for Render deployment - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        }
        
        git add .
        git commit -m $message
        Write-Host "✅ Changes committed!" -ForegroundColor Green
    }
}

# Check for remote
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    Write-Host "❌ No remote repository configured!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please add your GitHub repository:" -ForegroundColor Yellow
    Write-Host "git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Cyan
    exit 1
}

Write-Host "📡 Remote repository: $remote" -ForegroundColor Green
Write-Host ""

# Push to GitHub
$push = Read-Host "Push to GitHub? (y/n)"
if ($push -eq "y") {
    Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Cyan
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📋 Next Steps:" -ForegroundColor Cyan
        Write-Host "1. Go to https://dashboard.render.com" -ForegroundColor White
        Write-Host "2. Click 'New +' → 'Blueprint'" -ForegroundColor White
        Write-Host "3. Connect your GitHub repository" -ForegroundColor White
        Write-Host "4. Render will detect render.yaml automatically" -ForegroundColor White
        Write-Host "5. Add environment variables (see DEPLOY_RENDER.md)" -ForegroundColor White
        Write-Host ""
        Write-Host "📖 Full guide: DEPLOY_RENDER.md" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "❌ Push failed! Check the error above." -ForegroundColor Red
        Write-Host "You may need to pull first: git pull origin main" -ForegroundColor Yellow
    }
} else {
    Write-Host "⏸️  Deployment cancelled." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔑 Required Environment Variables for Render:" -ForegroundColor Cyan
Write-Host "Backend:" -ForegroundColor White
Write-Host "  - BLOCKFROST_API_KEY (required)" -ForegroundColor Yellow
Write-Host "  - BLOCKFROST_NETWORK (required)" -ForegroundColor Yellow
Write-Host "  - OPENAI_API_KEY (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "Frontend:" -ForegroundColor White
Write-Host "  - NEXT_PUBLIC_API_URL (set to backend URL after deployment)" -ForegroundColor Yellow
Write-Host ""
