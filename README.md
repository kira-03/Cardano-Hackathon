# EcosystemBridge Assistant

AI-powered token analysis for Cardano exchange listings and cross-chain expansion.

---

## What It Does

Analyzes Cardano tokens and tells you exactly what's needed for exchange listings. Get AI-generated insights, professional PDF reports, and actionable recommendations in minutes.

**Key Features:**
- On-chain analysis with holder distribution and liquidity metrics
- AI-powered readiness scoring (A+ to F)
- Exchange-specific requirements for Binance, Coinbase, Kraken, KuCoin, Gate.io
- Cross-chain routing for Ethereum, BSC, Polygon, Solana
- Professional PDF reports with email delivery

---

## Quick Setup

**Requirements:** Python 3.10+, Node.js 18+

```bash
# Clone and setup backend
git clone https://github.com/your-org/cardano-hackathon.git
cd cardano-hackathon/backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
```

**Configure API Keys** (create `backend/.env`):
```bash
BLOCKFROST_API_KEY=mainnet_your_key_here
OPENAI_API_KEY=sk-your_key_here
BLOCKFROST_NETWORK=mainnet

# Optional - for email reports
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Get API Keys:**
- Blockfrost: https://blockfrost.io
- OpenAI: https://platform.openai.com/api-keys

**Run It:**
```bash
# Terminal 1 - Backend
cd backend && python main.py

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

Visit http://localhost:3000

---

## How to Use

1. Enter your Cardano token's policy ID
2. Select target exchanges (optional)
3. Choose blockchain networks for expansion (optional)
4. Click "Run Analysis"
5. Review the readiness score and recommendations
6. Download PDF report or email to stakeholders

**API Example:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "policy_id": "e16c2dc8ae937e8d3790c7fd7168d7b994621ba14ca11415f39fed72",
    "target_exchanges": ["binance", "kucoin"]
  }'
```

---

## What You Get

**Analysis Report:**
- Executive summary with AI insights
- Holder distribution and concentration metrics
- Liquidity analysis across DEXs
- Exchange readiness breakdown
- Step-by-step preparation guides
- Cross-chain bridge routes with cost estimates

**Readiness Score:**
Grades your token A+ to F based on exchange requirements. Shows exactly what's missing and how to fix it.

---

## Tech Stack

**Backend:** FastAPI, Blockfrost API, OpenAI GPT-4, ReportLab  
**Frontend:** Next.js 14, TypeScript, Tailwind CSS

---

## Deployment

**Backend:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

**Frontend:**
```bash
npm run build && npm start
```

Set `NEXT_PUBLIC_API_URL` to your backend URL.

---

## Common Issues

**"Invalid API key"** - Check your .env file has the correct mainnet key from Blockfrost

**"SMTP authentication failed"** - Gmail users need an App Password, not your regular password

**Can't connect to backend** - Make sure the backend is running on port 8000

---

## Contributing

Fork the repo, make your changes, submit a PR. Keep it clean and well-documented.

---

## License

MIT License - see LICENSE file for details.

---

## Support

Issues: https://github.com/your-org/cardano-hackathon/issues  
Email: support@ecosystembridge.io

Built for the Cardano community.
