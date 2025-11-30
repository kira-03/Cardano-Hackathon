# Deploying Cross-Chain Navigator to Render

This guide will help you deploy the full-stack Cardano Cross-Chain Navigator (FastAPI backend + Next.js frontend) to Render.

## 📋 Prerequisites

Before you begin, ensure you have:

1. ✅ A [Render account](https://render.com) (free tier works)
2. ✅ Your code pushed to a GitHub repository
3. ✅ A [Blockfrost API key](https://blockfrost.io) (required for Cardano blockchain access)
4. ✅ (Optional) An OpenAI API key for AI-powered analysis features

## 🚀 Deployment Steps

### Step 1: Push Your Code to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit your changes
git commit -m "Ready for Render deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to main branch
git push -u origin main
```

### Step 2: Connect Render to Your GitHub Repository

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select your repository
5. Render will automatically detect the `render.yaml` file

### Step 3: Configure Environment Variables

Render will create two services from the `render.yaml`:
- `cardano-hackathon-backend` (FastAPI)
- `cardano-hackathon-frontend` (Next.js)

#### Backend Environment Variables

In the Render Dashboard, go to **Backend Service** → **Environment** and add:

**Required:**
```
BLOCKFROST_API_KEY=your_actual_blockfrost_api_key
BLOCKFROST_NETWORK=mainnet
```

**Optional (but recommended):**
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./cardano_navigator.db
ENVIRONMENT=production
```

#### Frontend Environment Variables

In the Render Dashboard, go to **Frontend Service** → **Environment** and add:

**Required:**
```
NEXT_PUBLIC_API_URL=https://cardano-hackathon-backend.onrender.com
```

⚠️ **Important:** Replace `cardano-hackathon-backend` with your actual backend service name from Render.

### Step 4: Deploy

1. Click **"Apply"** or **"Create Services"** in Render
2. Render will start building both services:
   - **Backend**: Builds Docker image with all system dependencies
   - **Frontend**: Builds Next.js production bundle

3. Wait for both builds to complete (usually 5-10 minutes for first deployment)

### Step 5: Verify Deployment

Once deployed, you'll get two URLs:

**Backend URL:** `https://cardano-hackathon-backend.onrender.com`
- Test: Visit `https://cardano-hackathon-backend.onrender.com/health`
- Expected response: `{"status": "healthy", ...}`

**Frontend URL:** `https://cardano-hackathon-frontend.onrender.com`
- Visit this URL to access your application

### Step 6: Update Frontend API URL (If Needed)

If you didn't set `NEXT_PUBLIC_API_URL` in Step 3:

1. Go to **Frontend Service** → **Environment**
2. Add: `NEXT_PUBLIC_API_URL=https://YOUR-BACKEND-URL.onrender.com`
3. Click **"Save Changes"**
4. Render will automatically redeploy the frontend

## 🔧 Configuration Files

### render.yaml
Defines both services and their configurations. Already configured in your repository.

### backend/Dockerfile
Handles system dependencies (weasyprint, PDF generation libraries). Already created.

### backend/.env.example
Template for environment variables. Copy to `.env` for local development.

## 🧪 Local Testing Before Deployment

### Test Backend Locally

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Copy .env.example to .env and fill in your API keys
cp .env.example .env

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

Visit: `http://localhost:8000/health`

### Test Frontend Locally

```powershell
cd frontend
npm install

# Create .env.local with your backend URL
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev
```

Visit: `http://localhost:3000`

### Test Production Build Locally

```powershell
# Frontend
cd frontend
npm run build
npm run start

# Backend (already in production mode with uvicorn)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📊 Monitoring & Logs

### View Logs in Render

1. Go to your service in Render Dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs for errors or issues

### Health Checks

Both services have health checks configured:
- **Backend**: `/health` endpoint
- **Frontend**: Automatic Next.js health check

## 🐛 Troubleshooting

### Backend Build Fails

**Issue:** Python dependencies fail to install
**Solution:** 
- Check `backend/Dockerfile` has all system dependencies
- Verify `requirements.txt` is properly formatted
- Check Render build logs for specific error

**Issue:** Blockfrost connection fails
**Solution:**
- Verify `BLOCKFROST_API_KEY` is set correctly
- Check `BLOCKFROST_NETWORK` matches your API key (mainnet/testnet)
- Test your API key at https://blockfrost.io

### Frontend Build Fails

**Issue:** Build timeout or memory error
**Solution:**
- Render free tier has limited resources
- Try reducing dependencies if possible
- Check for circular dependencies

**Issue:** API calls fail (CORS errors)
**Solution:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Ensure backend CORS is configured (already done in `main.py`)
- Check browser console for exact error

### Frontend Can't Connect to Backend

**Issue:** 404 or connection refused
**Solution:**
1. Verify backend is deployed and healthy
2. Check `NEXT_PUBLIC_API_URL` in frontend environment variables
3. Ensure URL doesn't have trailing slash
4. Redeploy frontend after updating environment variables

### PDF Generation Fails

**Issue:** WeasyPrint errors
**Solution:**
- Dockerfile includes all required system libraries
- Check backend logs for specific error
- Verify `outputs` directory is writable

### Free Tier Limitations

**Issue:** Service spins down after inactivity
**Solution:**
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Consider upgrading to paid tier for always-on service

## 🔐 Security Best Practices

1. ✅ **Never commit API keys** to GitHub
2. ✅ Use Render's **Secret Files** for sensitive data
3. ✅ Set environment variables in Render Dashboard, not in code
4. ✅ Use `.gitignore` to exclude `.env` files
5. ✅ Rotate API keys periodically

## 📈 Performance Optimization

### Backend
- SQLite works for demo/hackathon
- For production, consider PostgreSQL (Render offers free tier)
- Enable caching for frequently accessed data

### Frontend
- Next.js automatically optimizes production builds
- Images are optimized with Next.js Image component
- Static pages are pre-rendered

## 🔄 Continuous Deployment

With `autoDeploy: true` in `render.yaml`:
- Every push to `main` branch triggers automatic deployment
- Both services rebuild and redeploy
- Zero-downtime deployment

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Blockfrost Docs**: https://docs.blockfrost.io
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

## ✅ Deployment Checklist

Before going live:

- [ ] Backend health check returns 200
- [ ] Frontend loads without errors
- [ ] Can submit token analysis request
- [ ] Results display correctly
- [ ] PDF download works
- [ ] All environment variables are set
- [ ] Logs show no critical errors
- [ ] CORS is working (no browser errors)

## 🎉 Success!

Your Cross-Chain Navigator is now live on Render! Share your frontend URL with users.

**Example URLs:**
- Frontend: `https://cardano-hackathon-frontend.onrender.com`
- Backend API: `https://cardano-hackathon-backend.onrender.com`
- Health Check: `https://cardano-hackathon-backend.onrender.com/health`

