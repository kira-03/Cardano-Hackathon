# 🚀 Quick Start: Deploy to Render

This is a **quick reference guide** for deploying your Cardano Cross-Chain Navigator to Render. For detailed instructions, see [DEPLOY_RENDER.md](./DEPLOY_RENDER.md).

## ⚡ Quick Deploy (5 Steps)

### 1️⃣ Push to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

Or use the helper script:
```powershell
.\deploy.ps1
```

### 2️⃣ Create Render Services

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Select your GitHub repository
4. Render will detect `render.yaml` and create both services

### 3️⃣ Add Backend Environment Variables

In Render Dashboard → **Backend Service** → **Environment**:

```
BLOCKFROST_API_KEY=your_blockfrost_api_key_here
BLOCKFROST_NETWORK=mainnet
```

Optional:
```
OPENAI_API_KEY=your_openai_key_here
```

### 4️⃣ Add Frontend Environment Variable

In Render Dashboard → **Frontend Service** → **Environment**:

```
NEXT_PUBLIC_API_URL=https://cardano-hackathon-backend.onrender.com
```

⚠️ Replace `cardano-hackathon-backend` with your actual backend service name!

### 5️⃣ Deploy & Test

- Render will automatically build and deploy both services
- Wait 5-10 minutes for first deployment
- Test backend: `https://your-backend.onrender.com/health`
- Access frontend: `https://your-frontend.onrender.com`

## 🔑 Required API Keys

### Blockfrost API Key (Required)
1. Go to [blockfrost.io](https://blockfrost.io)
2. Sign up for free account
3. Create a new project (Mainnet or Testnet)
4. Copy your API key
5. Add to Render backend environment variables

### OpenAI API Key (Optional)
Only needed if you want AI-powered analysis features.

## 📁 Project Structure

```
Cardano-Hackathon/
├── backend/              # FastAPI backend
│   ├── Dockerfile       # Docker config for Render
│   ├── main.py          # Main API application
│   ├── requirements.txt # Python dependencies
│   └── .env.example     # Environment template
├── frontend/            # Next.js frontend
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   └── package.json    # Node dependencies
├── render.yaml         # Render deployment config
└── DEPLOY_RENDER.md   # Detailed deployment guide
```

## 🧪 Test Locally First

### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env  # Then edit .env with your keys
uvicorn main:app --host 0.0.0.0 --port 8000
```

Test: http://localhost:8000/health

### Frontend
```powershell
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

Test: http://localhost:3000

## 🐛 Common Issues

### Backend won't start
- ✅ Check `BLOCKFROST_API_KEY` is set
- ✅ Verify API key is for correct network (mainnet/testnet)
- ✅ Check Render logs for specific error

### Frontend can't connect to backend
- ✅ Verify `NEXT_PUBLIC_API_URL` is set correctly
- ✅ Ensure backend is deployed and healthy
- ✅ No trailing slash in URL
- ✅ Redeploy frontend after changing env vars

### Build fails
- ✅ Check Render build logs
- ✅ Verify all dependencies in requirements.txt/package.json
- ✅ Ensure Dockerfile has all system dependencies

## 📊 Monitor Your Deployment

- **Logs**: Render Dashboard → Service → Logs tab
- **Health**: Visit `/health` endpoint on backend
- **Metrics**: Render Dashboard → Service → Metrics tab

## 🆘 Need Help?

1. Check [DEPLOY_RENDER.md](./DEPLOY_RENDER.md) for detailed guide
2. Review Render logs for specific errors
3. Test locally to isolate issues
4. Check [Render documentation](https://render.com/docs)

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render services created from blueprint
- [ ] `BLOCKFROST_API_KEY` set in backend
- [ ] `BLOCKFROST_NETWORK` set in backend
- [ ] `NEXT_PUBLIC_API_URL` set in frontend
- [ ] Backend health check passes
- [ ] Frontend loads successfully
- [ ] Can analyze a token
- [ ] PDF download works

## 🎉 You're Live!

Once deployed, share your frontend URL:
`https://your-frontend-name.onrender.com`

---

**Note**: Render free tier spins down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.
