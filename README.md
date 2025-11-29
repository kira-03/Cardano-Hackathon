# 🌉 EcosystemBridge Assistant

> AI-Powered Token Analysis & Exchange Listing Platform for Cardano

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Next.js](https://img.shields.io/badge/next.js-14.1.0-black)
![License](https://img.shields.io/badge/license-MIT-purple)

---

## 🚀 Overview

**EcosystemBridge Assistant** is a comprehensive platform that analyzes Cardano tokens and provides actionable insights for exchange listings and cross-chain expansion. Powered by AI, it delivers professional reports, personalized recommendations, and automated workflows.

### ✨ Key Features

- 🔍 **Deep Token Analysis** - On-chain metrics, holder distribution, liquidity analysis
- 🤖 **AI-Powered Insights** - Google Gemini-generated executive summaries and recommendations
- 📊 **Exchange Readiness Scoring** - Grade tokens A+ to F based on listing requirements
- 🌐 **Cross-Chain Routing** - Optimal bridge paths to Ethereum, BSC, Polygon, Solana
- 📧 **Email Reports** - Automatically send professional PDFs to stakeholders
- 📄 **PDF Generation** - Beautiful, branded reports with charts and metrics
- 🎯 **Exchange-Specific Prep** - Tailored requirements for Binance, Coinbase, Kraken, KuCoin, Gate.io
- 🔗 **Resource Links** - Verified links to DEXs, explorers, bridges (no 404s!)
- 🎨 **Animated UI** - Smooth framer-motion animations for delightful UX

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Features in Detail](#-features-in-detail)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🛠 Installation

### Prerequisites

- **Python 3.10+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **Git** - Version control

### Clone Repository

```bash
git clone https://github.com/your-org/cardano-hackathon.git
cd cardano-hackathon
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp ../.env.example .env

# Edit .env with your API keys
notepad .env  # Windows
nano .env     # Mac/Linux
```

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Development build
npm run dev
```

---

## ⚙️ Configuration

### Required API Keys

#### 1. Blockfrost API (Cardano On-Chain Data)
- Sign up: https://blockfrost.io
- Generate API key for **Mainnet**
- Add to `.env`: `BLOCKFROST_API_KEY=mainnetkxDq3x6Tn5SaDE7VVn1OgNdovwqrCZ70`

#### 2. Google Gemini API (AI Analysis)
- Sign up: https://makersuite.google.com/app/apikey
- Generate API key
- Add to `.env`: `GEMINI_API_KEY=AIzaSyC...`

#### 3. SMTP Email (Optional - for Email Reports)
See [EMAIL_SETUP_GUIDE.md](./EMAIL_SETUP_GUIDE.md) for detailed setup.

**Quick Gmail Setup:**
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SENDER_EMAIL=your-email@gmail.com
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Cardano
BLOCKFROST_API_KEY=mainnet...
BLOCKFROST_NETWORK=mainnet

# AI
GEMINI_API_KEY=AIzaSyC...
USE_AI_ANALYSIS=true

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME=EcosystemBridge Assistant
```

---

## 🏃 Running the Application

### Development Mode

#### Terminal 1 - Backend (Python)
```bash
cd backend
python main.py
```
Backend runs on: **http://localhost:8000**

#### Terminal 2 - Frontend (Next.js)
```bash
cd frontend
npm run dev
```
Frontend runs on: **http://localhost:3000**

### Production Mode

#### Backend (with Gunicorn)
```bash
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

#### Frontend (Build + Serve)
```bash
cd frontend
npm run build
npm start
```

---

## 🎯 Features in Detail

### 1. Token Analysis

**What it does:**
- Fetches on-chain data from Cardano blockchain
- Analyzes holder distribution (wallets, concentration)
- Calculates liquidity across DEXs (Minswap, MuesliSwap)
- Evaluates market metrics (volume, price, market cap)
- Generates readiness score (0-100) and grade (A+ to F)

**How to use:**
1. Enter Policy ID in the form
2. Select target exchanges (optional)
3. Select target chains for bridging (optional)
4. Click "Run Analysis"
5. Wait 30-60 seconds for AI processing

---

### 2. AI-Powered Insights

**Powered by Google Gemini 2.0 Flash**

**Features:**
- Executive summary of token status
- Personalized recommendations based on metrics
- Exchange-specific preparation steps
- Risk assessment and mitigation strategies
- Next steps prioritized by impact

**Example Output:**
```
This token shows strong fundamentals with 5,234 holders and 
$2.3M in liquidity. The holder distribution is well-balanced, 
indicating organic growth. Recommended next steps include 
listing on Tier 2 exchanges (KuCoin, Gate.io) before approaching 
Tier 1 platforms.
```

---

### 3. PDF Report Generation

**Professional reports include:**
- ✅ Cover page with token branding
- ✅ Executive summary (AI-generated)
- ✅ Score card with color-coded grade
- ✅ Token metrics table (holders, volume, liquidity)
- ✅ Exchange requirements breakdown
- ✅ Recommendations with resource links
- ✅ Cross-chain bridge routes with cost estimates
- ✅ Helpful resources section
- ✅ Professional footer with disclaimer

**File specs:**
- Format: PDF
- Size: 2-5 MB
- Pages: 5-10 depending on data
- Colors: Professional blue/purple gradient theme

---

### 4. Email Delivery System

**Features:**
- ✅ HTML email with branded template
- ✅ PDF attachment (analysis report)
- ✅ CC/BCC support for multiple recipients
- ✅ Retry logic (3 attempts with exponential backoff)
- ✅ Delivery logging and tracking
- ✅ Email validation
- ✅ Support for Gmail, Outlook, custom SMTP

**Email Template:**
```html
Subject: EcosystemBridge Analysis Report - [TOKEN_SYMBOL]

Hello,

Your token analysis report for [TOKEN_NAME] is ready!

📊 Readiness Score: 85/100 (Grade: B+)

The attached PDF contains:
✓ Executive Summary
✓ Token Metrics & Holder Analysis
✓ Exchange Requirements
✓ Recommendations & Next Steps

Best regards,
EcosystemBridge Team
```

---

### 5. Exchange Preparation

**Supported Exchanges:**
- 🟡 **Binance** - Tier 1, highest volume
- 🔵 **Coinbase** - US-compliant, institutional focus
- 🟣 **Kraken** - Security-focused, regulated
- 🟢 **KuCoin** - Altcoin-friendly, mid-tier
- 🔴 **Gate.io** - Wide token selection, easy listing

**Analysis includes:**
- Minimum requirements (liquidity, holders, volume)
- Your token's metrics vs requirements
- Readiness percentage for each exchange
- Preparation checklist
- Application links (verified - no 404s!)

---

### 6. Cross-Chain Routing

**Supported Bridges:**
- LiFi Protocol (multi-chain aggregator)
- Axelar Network (secure cross-chain communication)
- Multichain (any-to-any bridge)
- Celer cBridge (low-cost transfers)

**Routing analysis:**
- Optimal chains for expansion (Ethereum, BSC, Polygon, Solana, Avalanche)
- Cost estimates (gas fees)
- Time estimates (confirmation times)
- Liquidity requirements per chain
- Risk assessment per bridge

---

## 📡 API Documentation

### Core Endpoints

#### POST `/api/analyze`
Analyze a Cardano token and generate insights.

**Request:**
```json
{
  "policy_id": "e16c2dc8ae937e8d3790c7fd7168d7b994621ba14ca11415f39fed72",
  "target_exchanges": ["binance", "kucoin"],
  "target_chains": ["ethereum", "bsc"]
}
```

**Response:**
```json
{
  "analysis_id": "uuid-here",
  "token_name": "CardanoKitties",
  "token_symbol": "CKTT",
  "readiness_score": {
    "total_score": 85,
    "grade": "B+",
    "breakdown": { ... }
  },
  "metrics": { ... },
  "recommendations": [...],
  "exchange_requirements": { ... },
  "bridge_routes": [...],
  "pdf_path": "outputs/pdfs/analysis_uuid.pdf"
}
```

---

#### POST `/api/send-email`
Send analysis report via email.

**Request:**
```json
{
  "to_email": "stakeholder@example.com",
  "analysis_id": "uuid-from-analyze-endpoint",
  "cc": ["manager@example.com"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully to stakeholder@example.com",
  "timestamp": "2025-01-28T10:30:00Z",
  "recipient": "stakeholder@example.com"
}
```

---

#### GET `/api/download/pdf/{analysis_id}`
Download PDF report.

**Response:** PDF file (application/pdf)

---

#### GET `/api/analysis/{analysis_id}/status`
Get analysis metadata.

**Response:**
```json
{
  "analysis_id": "uuid",
  "token_name": "CardanoKitties",
  "token_symbol": "CKTT",
  "readiness_score": 85,
  "grade": "B+",
  "pdf_available": true,
  "timestamp": "2025-01-28T10:00:00Z"
}
```

---

### Utility Endpoints

- `GET /health` - Health check
- `GET /api/exchanges` - List supported exchanges
- `GET /api/chains` - List supported chains
- `GET /api/email-log` - View email delivery history

---

## 🏗 Architecture

### Backend Stack
- **FastAPI** - Modern Python web framework
- **Blockfrost** - Cardano blockchain API
- **Google Gemini** - AI analysis (LLM)
- **ReportLab** - PDF generation
- **SMTP/Email** - Email delivery
- **SQLite** - Session storage

### Frontend Stack
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Lucide React** - Icon library
- **Axios** - HTTP client

### Agent Architecture

```
EcosystemBridgeAssistant
├── Step 1: Token Discovery (Blockfrost API)
├── Step 2: Holder Analysis (On-chain data)
├── Step 3: Liquidity Analysis (DEX APIs)
├── Step 4: Market Metrics (CoinPaprika/CoinGecko)
├── Step 5: Exchange Requirements (Analysis)
├── Step 6: Bridge Routing (LiFi, Axelar)
├── Step 7: AI Insights (Gemini 2.0)
├── Step 8: PDF Generation (ReportLab)
└── Step 9: Recommendations (Prioritization)
```

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Run Link Validation
```bash
cd backend
python scripts/validate_links.py
```

**Expected output:**
```
✓ https://minswap.org
✓ https://muesliswap.com
✓ https://cardanoscan.io
...
🎉 All links validated successfully! (32/32)
```

### Manual API Testing

**Using cURL:**
```bash
# Health check
curl http://localhost:8000/health

# Analyze token
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"policy_id": "e16c2dc8..."}'

# Send email
curl -X POST http://localhost:8000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "test@example.com",
    "analysis_id": "uuid-here"
  }'
```

**Using Frontend:**
1. Open http://localhost:3000
2. Enter policy ID
3. Click "Run Analysis"
4. Click "View Report" (PDF preview)
5. Click "Email Report"

---

## 🚀 Deployment

### Backend (Railway / Heroku / DigitalOcean)

```bash
# Set environment variables
export BLOCKFROST_API_KEY=mainnet...
export GEMINI_API_KEY=AIzaSyC...
export SMTP_HOST=smtp.gmail.com
export SMTP_USER=noreply@yourdomain.com
export SMTP_PASSWORD=your-app-password

# Deploy
python main.py
```

### Frontend (Vercel / Netlify)

```bash
cd frontend
npm run build
npm start
```

**Environment Variables:**
- `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`

---

## 🐛 Troubleshooting

### Backend Issues

**"BlockfrostException: Invalid API key"**
- Check `.env` has correct `BLOCKFROST_API_KEY`
- Ensure key is for **mainnet** (not preprod/testnet)

**"SMTPAuthenticationError"**
- Gmail: Use **App Password**, not regular password
- Outlook: Enable "less secure apps"
- See [EMAIL_SETUP_GUIDE.md](./EMAIL_SETUP_GUIDE.md)

**"Module not found" errors**
```bash
cd backend
pip install -r requirements.txt
```

---

### Frontend Issues

**"Cannot connect to localhost:8000"**
- Ensure backend is running
- Check CORS settings in `backend/main.py`

**"npm install" fails**
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json
npm install
```

**Build errors**
```bash
npm run build -- --verbose
```

---

## 📚 Additional Resources

- [Email Setup Guide](./EMAIL_SETUP_GUIDE.md) - Detailed SMTP configuration
- [API Documentation](https://your-api-docs-url.com) - Full API reference
- [Cardano Developers](https://developers.cardano.org) - Blockchain resources
- [Blockfrost Docs](https://docs.blockfrost.io) - API documentation

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Cardano Foundation** - Blockchain infrastructure
- **Blockfrost** - API services
- **Google** - Gemini AI
- **Minswap** - DEX data
- **LiFi Protocol** - Cross-chain routing

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/your-org/cardano-hackathon/issues)
- **Email:** support@ecosystembridge.io
- **Discord:** [Join our community](https://discord.gg/ecosystembridge)

---

**Built with ❤️ for the Cardano Ecosystem**

