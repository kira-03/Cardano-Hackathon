"""
Cross-Chain Navigator Agent - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
import uuid
from typing import List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from config import settings
from models.schemas import (
    AnalysisRequest, 
    AnalysisResponse, 
    TokenMetrics,
    ReadinessScore,
    Recommendation,
    ExchangeRequirement,
    BridgeRoute,
    MasumiLog
)
from services.cardano_service import CardanoService
from agents.token_analysis_agent import TokenAnalysisAgent
from agents.exchange_preparation_agent import ExchangePreparationAgent
from agents.cross_chain_routing_agent import CrossChainRoutingAgent

# Initialize FastAPI app
app = FastAPI(
    title="Cross-Chain Navigator Agent",
    description="AI Agent for comprehensive Cardano token analysis and cross-chain expansion guidance",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting up with environment: {settings.environment}")
    logger.info(f"BlockFrost Network: {settings.blockfrost_network}")
    key = settings.blockfrost_api_key
    masked_key = f"{key[:8]}...{key[-4:]}" if key else "None"
    logger.info(f"BlockFrost API Key: {masked_key}")
    
    # Check connection on startup
    connected = await cardano_service.check_connection()
    logger.info(f"Initial BlockFrost Connection Check: {'✅ Success' if connected else '❌ Failed'}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services and agents
cardano_service = CardanoService()
token_agent = TokenAnalysisAgent(cardano_service)
exchange_agent = ExchangePreparationAgent(cardano_service)
routing_agent = CrossChainRoutingAgent(cardano_service)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "healthy",
        "name": "Cross-Chain Navigator Agent",
        "version": "1.0.0",
        "description": "AI-powered Cardano token analysis and cross-chain expansion platform",
        "features": [
            "On-chain token analysis",
            "Listing readiness scoring",
            "Exchange requirement mapping",
            "Cross-chain bridge routing",
            "PDF report generation",
            "Masumi on-chain logging"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check with connection status"""
    blockfrost_connected = await cardano_service.check_connection()
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "blockfrost": blockfrost_connected,
            "database": True,  # Simplified check
            "masumi": False  # Would check Masumi node in production
        },
        "network": settings.blockfrost_network
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_token(request: AnalysisRequest):
    """
    Complete token analysis pipeline
    
    Performs:
    1. On-chain metrics analysis
    2. Listing readiness scoring
    3. Exchange requirement checking
    4. Cross-chain routing recommendations
    5. PDF report generation
    6. Masumi on-chain logging
    """
    try:
        analysis_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        logger.info(f"=" * 80)
        logger.info(f"Starting Token Analysis - ID: {analysis_id}")
        logger.info(f"Policy ID: {request.policy_id}")
        logger.info(f"Target Exchanges: {request.target_exchanges}")
        logger.info(f"Target Chains: {request.target_chains}")
        logger.info(f"=" * 80)
        
        # Step 1: Token Analysis Agent
        logger.info("STEP 1: Running Token Analysis Agent...")
        token_analysis = await token_agent.analyze(request.policy_id)
        logger.info(f"✓ Token Analysis Complete - Grade: {token_analysis['readiness_score'].grade}")
        
        # Step 2: Exchange Preparation Agent
        logger.info("STEP 2: Running Exchange Preparation Agent...")
        exchange_prep = await exchange_agent.prepare(
            request.policy_id,
            token_analysis["metrics"],
            request.target_exchanges
        )
        logger.info(f"✓ Exchange Prep Complete - {len(exchange_prep['requirements'])} requirements checked")
        
        # Step 3: Cross-Chain Routing Agent
        logger.info("STEP 3: Running Cross-Chain Routing Agent...")
        routing = await routing_agent.find_routes(
            request.policy_id,
            request.target_chains
        )
        logger.info(f"✓ Routing Complete - Recommended chain: {routing['recommended_chain']}")
        
        # Step 4: Generate executive summary
        logger.info("STEP 4: Generating executive summary...")
        executive_summary = _generate_executive_summary(
            token_analysis,
            exchange_prep,
            routing
        )
        logger.info("✓ Executive summary generated")
        
        # Step 5: Generate next steps
        logger.info("STEP 5: Generating next steps...")
        next_steps = _generate_next_steps(
            token_analysis["recommendations"],
            exchange_prep["unmet_requirements"]
        )
        logger.info(f"✓ Generated {len(next_steps)} action items")
        
        # Step 6: Masumi logging (simplified for hackathon)
        logger.info("STEP 6: Creating Masumi logs...")
        masumi_logs = [
            MasumiLog(
                agent_did="did:masumi:agent:token-analyzer",
                decision_type="token_analysis",
                decision_hash=f"hash_{analysis_id[:8]}",
                transaction_id=None,
                timestamp=timestamp
            )
        ]
        
        # Build response
        response = AnalysisResponse(
            analysis_id=analysis_id,
            policy_id=request.policy_id,
            token_name=token_analysis["token_info"].get("asset_name", "Unknown"),
            token_symbol=token_analysis["token_info"].get("ticker", "???"),
            timestamp=timestamp,
            metrics=token_analysis["metrics"],
            readiness_score=token_analysis["readiness_score"],
            recommendations=token_analysis["recommendations"],
            exchange_requirements=exchange_prep["requirements"],
            proposal_pdf_url=exchange_prep.get("pdf_url"),
            bridge_routes=routing["routes"],
            recommended_chain=routing["recommended_chain"],
            masumi_logs=masumi_logs,
            executive_summary=executive_summary,
            next_steps=next_steps
        )
        
        logger.info(f"=" * 80)
        logger.info(f"✓ ANALYSIS COMPLETE - ID: {analysis_id}")
        logger.info(f"Token: {response.token_name} ({response.token_symbol})")
        logger.info(f"Overall Grade: {response.readiness_score.grade} ({response.readiness_score.total_score}/100)")
        logger.info(f"Recommendations: {len(response.recommendations)}")
        logger.info(f"Bridge Routes Found: {len(response.bridge_routes)}")
        logger.info(f"=" * 80)
        
        return response
        
    except Exception as e:
        logger.error(f"❌ ERROR during analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/token/{policy_id}/info")
async def get_token_info(policy_id: str):
    """Get basic token information"""
    try:
        info = await cardano_service.get_token_info(policy_id)
        return info
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/token/{policy_id}/holders")
async def get_token_holders(policy_id: str):
    """Get token holder distribution"""
    try:
        holders = await cardano_service.get_token_holders(policy_id)
        analysis = await cardano_service.analyze_holder_distribution(holders)
        return {
            "holders": holders[:50],  # Return top 50
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/exchanges")
async def get_supported_exchanges():
    """Get list of supported exchanges"""
    return {
        "exchanges": [
            {"name": "Binance", "tier": "Tier 1"},
            {"name": "Coinbase", "tier": "Tier 1"},
            {"name": "KuCoin", "tier": "Tier 2"},
            {"name": "Gate.io", "tier": "Tier 2"},
            {"name": "Huobi", "tier": "Tier 2"},
            {"name": "Bybit", "tier": "Tier 2"},
            {"name": "MEXC", "tier": "Tier 3"},
            {"name": "BitMart", "tier": "Tier 3"}
        ]
    }

@app.get("/api/chains")
async def get_supported_chains():
    """Get list of supported target chains"""
    return {
        "chains": [
            {"name": "Ethereum", "type": "EVM"},
            {"name": "BSC", "type": "EVM"},
            {"name": "Polygon", "type": "EVM"},
            {"name": "Avalanche", "type": "EVM"},
            {"name": "Arbitrum", "type": "EVM"},
            {"name": "Optimism", "type": "EVM"},
            {"name": "Solana", "type": "Non-EVM"},
            {"name": "Polkadot", "type": "Non-EVM"}
        ]
    }

def _generate_executive_summary(
    token_analysis: dict,
    exchange_prep: dict,
    routing: dict
) -> str:
    """Generate executive summary"""
    score = token_analysis["readiness_score"]
    metrics = token_analysis["metrics"]
    
    summary = f"Token readiness grade: {score.grade} ({score.total_score:.1f}/100). "
    
    if score.grade in ["A", "B"]:
        summary += "Token shows strong fundamentals for exchange listing. "
    elif score.grade == "C":
        summary += "Token has moderate readiness with areas for improvement. "
    else:
        summary += "Token requires significant improvements before exchange listing. "
    
    summary += f"Current liquidity: ${metrics.liquidity_usd:,.0f}. "
    summary += f"Holder count: {metrics.holder_count}. "
    
    unmet = len([r for r in exchange_prep["requirements"] if not r.meets_requirement])
    if unmet > 0:
        summary += f"{unmet} exchange requirements need attention. "
    
    summary += f"Recommended target chain: {routing['recommended_chain']}."
    
    return summary

def _generate_next_steps(
    recommendations: List[Recommendation],
    unmet_requirements: List[ExchangeRequirement]
) -> List[str]:
    """Generate prioritized next steps"""
    steps = []
    
    # High priority recommendations
    high_priority = [r for r in recommendations if r.priority == "high"]
    for rec in high_priority[:3]:  # Top 3
        steps.append(f"[HIGH] {rec.recommendation}")
    
    # Critical exchange requirements
    for req in unmet_requirements[:2]:  # Top 2
        steps.append(f"[EXCHANGE] {req.requirement}")
    
    # Medium priority recommendations
    medium_priority = [r for r in recommendations if r.priority == "medium"]
    for rec in medium_priority[:2]:  # Top 2
        steps.append(f"[MEDIUM] {rec.recommendation}")
    
    if not steps:
        steps.append("Continue monitoring metrics and market conditions")
    
    return steps

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
