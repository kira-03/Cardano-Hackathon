# EcosystemBridgeAssistant Agent

## Overview

The **EcosystemBridgeAssistant** is a comprehensive AI-powered agent designed to automate the entire exchange listing and cross-chain bridge integration process for Cardano tokens. It produces exchange-ready listing packages, liquidity action plans, market-maker RFPs, bridge feasibility reports, and governance proposal packages.

## Features

### 🔍 1. Automated Data Collection
- **Blockfrost Integration**: Fetches on-chain token data, holder distribution, and transfer volumes
- **DEX Analytics**: Queries Minswap, SundaeSwap, and MuesliSwap for liquidity and volume data
- **Off-chain Signals**: Gathers GitHub activity, social media metrics, and CoinGecko listings
- **30-Day Volume Calculation**: Analyzes transfer history for volume trends

### 🏦 2. Exchange Requirements Discovery
- **Automated Scraping**: Extracts listing requirements from exchange websites
- **Supported Exchanges**:
  - Binance (listing requirements and application process)
  - Coinbase (Asset Hub criteria)
  - Kraken (Get Listed program)
  - KuCoin (listing application)
  - Gate.io (listing request)
- **Form Schema Generation**: Creates fillable form templates with required fields

### 📊 3. Readiness Scoring Algorithm
- **Multi-Factor Analysis**: Evaluates tokens against exchange-specific criteria
- **Metrics Tracked**:
  - Top holder concentration (decentralization score)
  - Liquidity depth (USD value)
  - 30-day trading volume
  - Security audit status
  - Holder count and distribution
- **Exchange-Specific Thresholds**: Customized scoring for each exchange
- **Gap Analysis**: Identifies specific improvements needed for each exchange

### 📝 4. Proposal & Email Generation
- **Professional PDFs**: Creates comprehensive listing proposals with:
  - Executive summary
  - Token metrics and charts
  - Holder distribution analysis
  - Liquidity snapshots
  - Risk assessments
  - Roadmap and milestones
- **Exchange-Specific Emails**: Tailored email templates for each exchange
- **Form Auto-Fill**: Pre-populates application forms with project data
- **AI Enhancement**: Uses Google Gemini for compelling content generation

### 🌉 5. Bridge Simulation
- **LiFi Integration**: Queries bridge aggregator for cross-chain routes
- **Rango Support**: Alternative bridge route provider
- **Axelar ITS**: Interchain Token Service integration (pending Cardano support)
- **Route Optimization**: Ranks routes by cost, speed, and security
- **Cost Estimation**: Calculates bridge fees, gas costs, and slippage

### 💧 6. Liquidity Plan & Scripts
- **DEX Integration**: Generates liquidity provision scripts for:
  - Minswap (using Aggregator API)
  - SundaeSwap (using SDK)
  - MuesliSwap (using analytics API)
- **Transaction Building**: Creates unsigned transactions for dry-run testing
- **LP Strategy**: Recommends optimal liquidity distribution across DEXs
- **Incentive Programs**: Suggests liquidity mining campaigns

### 📊 7. Market Maker RFP
- **Professional RFP Document**: PDF with project metrics and requirements
- **MM Directory**: Curated list of market makers (Wintermute, GSR, Keyrock)
- **Requirements Specification**:
  - Minimum liquidity depth targets
  - Target spread percentages
  - Uptime requirements
  - Exchange coverage
- **Automated Outreach**: Email templates for market maker contact

### 🏛️ 8. Governance Package
- **Project Catalyst Proposals**: Draft proposals for Cardano governance
- **Structured Format**:
  - Problem statement
  - Solution description
  - Budget breakdown
  - Milestone timeline
  - Success metrics
- **IPFS Integration**: Optional upload for decentralized storage
- **Submission Instructions**: Step-by-step guide for Catalyst workspace

### 🔒 9. Execution Policy & Safety
- **Execution Modes**:
  - `preview`: Generate artifacts only (default)
  - `dryrun`: Build unsigned transactions
  - `submit`: Automated form submission (requires consent)
  - `live`: Broadcast transactions (requires consent + multisig)
- **Consent Flags**:
  - `allow_portal_login`: Enable automated portal access
  - `allow_email_send`: Enable automated email sending
  - `allow_tx_broadcast`: Enable transaction broadcasting
- **Safety Limits**:
  - Maximum auto-broadcast amount: $1,000 USD
  - High-risk concentration threshold: 40% top holder
  - Multisig approval required for large transactions
- **Audit Logging**: Immutable log of all actions and API calls

## Architecture

```
backend/
├── agents/
│   └── ecosystem_bridge_agent.py    # Main agent orchestration
├── services/
│   ├── cardano_service.py            # Blockfrost integration
│   ├── dex_service.py                # DEX APIs (Minswap, Sundae, Muesli)
│   ├── bridge_service.py             # Bridge aggregators (LiFi, Rango)
│   └── exchange_service.py           # Exchange requirements scraping
└── utils/
    ├── pdf_generator.py              # Professional PDF generation
    └── email_generator.py            # Exchange-specific emails
```

## Installation

### Prerequisites
- Python 3.10+
- Blockfrost API key (get from https://blockfrost.io)
- Google Gemini API key (optional, for AI features)

### Setup

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   Create a `.env` file in the `backend` directory:
   ```env
   BLOCKFROST_API_KEY=your_mainnet_key_here
   BLOCKFROST_NETWORK=mainnet
   GEMINI_API_KEY=your_gemini_key_here
   USE_AI_ANALYSIS=true
   ```

3. **Test the installation**:
   ```bash
   python test_ecosystem_bridge.py
   ```

## Usage

### Basic Example

```python
import asyncio
from agents.ecosystem_bridge_agent import (
    EcosystemBridgeAgent,
    ProjectMetadata,
    ExecutionMode,
    ConsentFlags
)
from services.cardano_service import CardanoService

async def main():
    # Initialize services
    cardano_service = CardanoService()
    agent = EcosystemBridgeAgent(cardano_service=cardano_service)
    
    # Define project metadata
    project_metadata = ProjectMetadata(
        name="YourToken",
        symbol="TKN",
        website="https://yourtoken.io",
        whitepaper_url="https://yourtoken.io/whitepaper.pdf",
        github_url="https://github.com/yourtoken",
        contact_email="team@yourtoken.io"
    )
    
    # Process request
    results = await agent.process_request(
        policy_id="your_policy_id_here",
        project_metadata=project_metadata,
        desired_exchanges=["binance", "kraken", "kucoin"],
        desired_target_chains=["ethereum", "bsc"],
        execution_mode=ExecutionMode.PREVIEW,
        consent_flags=ConsentFlags()
    )
    
    # Review results
    print(f"Readiness scores: {results['readiness_report']}")
    print(f"Artifacts: {results['artifacts']}")

asyncio.run(main())
```

### Execution Modes

#### Preview Mode (Default)
```python
execution_mode = ExecutionMode.PREVIEW
consent_flags = ConsentFlags()
```
- ✅ Generates all artifacts (PDFs, JSONs, scripts)
- ❌ No emails sent
- ❌ No forms submitted
- ❌ No transactions broadcast

#### Dry Run Mode
```python
execution_mode = ExecutionMode.DRYRUN
consent_flags = ConsentFlags()
```
- ✅ Generates artifacts
- ✅ Builds unsigned transactions
- ✅ Shows transaction payloads
- ❌ No broadcasting

#### Submit Mode
```python
execution_mode = ExecutionMode.SUBMIT
consent_flags = ConsentFlags(allow_portal_login=True)
```
- ✅ Generates artifacts
- ✅ Automated form submission (Playwright)
- ⚠️ Requires CAPTCHA handling
- ❌ No transaction broadcasting

#### Live Mode
```python
execution_mode = ExecutionMode.LIVE
consent_flags = ConsentFlags(
    allow_portal_login=True,
    allow_email_send=True,
    allow_tx_broadcast=True
)
```
- ✅ Full automation
- ⚠️ Requires multisig approval for large amounts
- ⚠️ High-risk tokens blocked

## Output Files

All artifacts are saved to `outputs/` directory:

```
outputs/
├── readiness_report.json           # Readiness scores per exchange
├── proposal.pdf                    # Comprehensive listing proposal
├── exchange_form_binance.json      # Pre-filled Binance form
├── exchange_form_coinbase.json     # Pre-filled Coinbase form
├── email_binance.json              # Binance email content
├── email_coinbase.json             # Coinbase email content
├── bridge_simulation.json          # Bridge routes and costs
├── liquidity_plan.json             # LP actions and scripts
├── mm_rfp.pdf                      # Market maker RFP
└── governance_proposal.json        # Catalyst proposal
```

## API Integrations

### Blockfrost API
- **Endpoint**: `https://cardano-mainnet.blockfrost.io/api/v0`
- **Used For**: Token info, holders, transaction history
- **Docs**: https://docs.blockfrost.io

### Minswap Aggregator API
- **Endpoint**: `https://api-mainnet-prod.minswap.org`
- **Used For**: Pool reserves, 24h volumes
- **Docs**: https://docs.minswap.org/developer/aggregator-api

### SundaeSwap
- **SDK**: `sundae-sdk`
- **Used For**: Pool queries, swap simulation
- **Docs**: https://github.com/SundaeSwap-finance/sundae-sdk

### MuesliSwap Analytics
- **Endpoint**: `https://api.muesliswap.com`
- **Used For**: Liquidity data, ticker info
- **Docs**: https://api.muesliswap.com/docs

### LiFi API
- **Endpoint**: `https://li.fi/api/v1`
- **Used For**: Cross-chain bridge routes
- **Docs**: https://li.fi/docs

### Rango API
- **Endpoint**: `https://api.rango.exchange`
- **Used For**: Alternative bridge routes
- **Docs**: https://api-docs.rango.exchange

## Exchange Requirements

### Binance
- **Minimum Liquidity**: $50,000
- **30-Day Volume**: $20,000+
- **Top Holder Concentration**: <30%
- **Audit Required**: Yes
- **Application**: https://www.binance.com/en/support/faq/detail/053e4bdc48364343b863d1833618d8ba

### Coinbase
- **Minimum Liquidity**: $100,000
- **30-Day Volume**: $50,000+
- **Top Holder Concentration**: <25%
- **Audit Required**: Yes
- **Application**: https://www.coinbase.com/exchange/asset-listings

### Kraken
- **Minimum Liquidity**: $75,000
- **30-Day Volume**: $30,000+
- **Top Holder Concentration**: <30%
- **Audit Required**: Yes
- **Application**: https://www.kraken.com/get-listed

### KuCoin
- **Minimum Liquidity**: $25,000
- **30-Day Volume**: $10,000+
- **Top Holder Concentration**: <35%
- **Audit Required**: No
- **Application**: https://www.kucoin.com/support/list-on-kucoin

### Gate.io
- **Minimum Liquidity**: $20,000
- **30-Day Volume**: $8,000+
- **Top Holder Concentration**: <40%
- **Audit Required**: No
- **Application**: https://www.gate.io/trade/listing

## Safety & Security

### High-Risk Detection
Tokens are flagged as high-risk if:
- Top holder concentration > 40%
- No security audit present (for tier-1 exchanges)
- Unusual transaction patterns

High-risk tokens require manual approval before submission mode.

### Transaction Limits
- Automatic broadcast limit: $1,000 USD
- Above limit requires multisig confirmation
- All transactions logged to immutable audit trail

### Privacy
- No private keys handled by agent
- Unsigned transactions generated for user signing
- API keys stored securely in environment variables

## Troubleshooting

### Blockfrost Connection Issues
```
Error: Failed to connect to Blockfrost API
Solution: Check BLOCKFROST_API_KEY in .env file
```

### DEX Data Unavailable
```
Warning: No DEX data available for token
Solution: Token may not be listed on DEXs yet. Continue with on-chain data only.
```

### Exchange Scraping Errors
```
Error: Failed to fetch exchange requirements
Solution: Exchange website structure may have changed. Uses fallback requirements.
```

### Bridge Route Not Found
```
Info: Cardano not yet supported by bridge aggregator
Solution: Manual bridge integration may be required. Monitor LiFi and Rango updates.
```

## Roadmap

### Planned Features
- [ ] Playwright integration for automated form submission
- [ ] Wallet integration for transaction signing
- [ ] IPFS upload for governance packages
- [ ] Enhanced AI analysis with GPT-4
- [ ] Real-time price feed integration
- [ ] Multi-language proposal generation
- [ ] Community voting simulation
- [ ] Regulatory compliance checks

### Bridge Support
- [ ] LiFi Cardano support (pending)
- [ ] Rango Cardano integration (pending)
- [ ] Axelar ITS for Cardano (in development)
- [ ] Wormhole bridge simulation
- [ ] Multichain bridge comparison

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- GitHub Issues: https://github.com/yourrepo/issues
- Email: support@yourproject.io
- Discord: https://discord.gg/yourproject

## Acknowledgments

- **Blockfrost**: On-chain data provider
- **Minswap, SundaeSwap, MuesliSwap**: DEX integrations
- **LiFi & Rango**: Bridge aggregation
- **Google Gemini**: AI-powered analysis
- **Cardano Community**: Testing and feedback

---

Built with ❤️ for the Cardano ecosystem
