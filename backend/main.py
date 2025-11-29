"""
Cross-Chain Navigator Agent - Main FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
import uuid
import os
from typing import List, Dict
import logging

# Configure logging with more detailed output
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for maximum visibility
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
    ]
)
# Set specific loggers to DEBUG
logging.getLogger('services.cardano_service').setLevel(logging.DEBUG)
logging.getLogger('agents.token_analysis_agent').setLevel(logging.DEBUG)
logging.getLogger('agents.exchange_preparation_agent').setLevel(logging.DEBUG)
logging.getLogger('agents.cross_chain_routing_agent').setLevel(logging.DEBUG)
logging.getLogger('blockfrost').setLevel(logging.DEBUG)
logging.getLogger('uvicorn').setLevel(logging.INFO)

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
from utils.pdf_generator import PDFGenerator
from utils.docx_generator import ListingProposalGenerator
from services.email_service import EmailService

# Initialize FastAPI app
app = FastAPI(
    title="Cross-Chain Navigator Agent",
    description="AI Agent for comprehensive Cardano token analysis and cross-chain expansion guidance",
    version="1.0.0"
)

# Store analysis results for PDF generation
analysis_cache: Dict[str, dict] = {}

# Initialize email service
email_service = EmailService()

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
pdf_generator = PDFGenerator()
proposal_generator = ListingProposalGenerator()

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
        
        # Generate Word document for listing proposal
        logger.info("STEP 2.5: Generating exchange listing proposal document...")
        proposal_docx_path = proposal_generator.generate_proposal(
            analysis_id,
            exchange_prep["proposal_data"]
        )
        if proposal_docx_path:
            logger.info(f"✓ Listing proposal generated: {proposal_docx_path}")
            exchange_prep["proposal_docx_url"] = proposal_docx_path
        else:
            logger.warning("⚠ Failed to generate listing proposal document")
        
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
        # Extract token symbol from metadata, or use asset_name as fallback
        metadata = token_analysis["token_info"].get("metadata", {})
        token_symbol = metadata.get("ticker") or metadata.get("symbol") or token_analysis["token_info"].get("asset_name", "TOKEN")
        token_name = metadata.get("name") or token_analysis["token_info"].get("asset_name", "Unknown")
        
        response = AnalysisResponse(
            analysis_id=analysis_id,
            policy_id=request.policy_id,
            token_name=token_name,
            token_symbol=token_symbol,
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
        
        # Generate PDF immediately after analysis
        pdf_path = await pdf_generator.generate_analysis_report(analysis_id, {
            "analysis_id": analysis_id,
            "policy_id": request.policy_id,
            "token_name": response.token_name,
            "token_symbol": response.token_symbol,
            "timestamp": timestamp.isoformat(),
            "metrics": response.metrics.dict() if hasattr(response.metrics, 'dict') else response.metrics,
            "readiness_score": response.readiness_score.dict() if hasattr(response.readiness_score, 'dict') else response.readiness_score,
            "recommendations": [r.dict() if hasattr(r, 'dict') else r for r in response.recommendations],
            "exchange_requirements": [r.dict() if hasattr(r, 'dict') else r for r in response.exchange_requirements],
            "bridge_routes": [r.dict() if hasattr(r, 'dict') else r for r in response.bridge_routes],
            "recommended_chain": response.recommended_chain,
            "executive_summary": response.executive_summary,
            "next_steps": response.next_steps
        })
        
        logger.info(f"✓ PDF generated: {pdf_path}")
        
        # Cache the analysis for PDF generation
        analysis_cache[analysis_id] = {
            "analysis_id": analysis_id,
            "policy_id": request.policy_id,
            "token_name": response.token_name,
            "token_symbol": response.token_symbol,
            "timestamp": timestamp.isoformat(),
            "metrics": response.metrics.dict() if hasattr(response.metrics, 'dict') else response.metrics,
            "readiness_score": response.readiness_score.dict() if hasattr(response.readiness_score, 'dict') else response.readiness_score,
            "recommendations": [r.dict() if hasattr(r, 'dict') else r for r in response.recommendations],
            "exchange_requirements": [r.dict() if hasattr(r, 'dict') else r for r in response.exchange_requirements],
            "bridge_routes": [r.dict() if hasattr(r, 'dict') else r for r in response.bridge_routes],
            "recommended_chain": response.recommended_chain,
            "executive_summary": response.executive_summary,
            "next_steps": response.next_steps,
            "pdf_path": pdf_path
        }
        
        return response
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ ERROR during analysis: {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/token/{policy_id}/info")
async def get_token_info(policy_id: str):
    """Get basic token information"""
    try:
        info = await cardano_service.get_token_info(policy_id)
        return info
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/analysis/{analysis_id}/pdf")
async def get_analysis_pdf(analysis_id: str):
    """Generate and download PDF report for an analysis"""
    try:
        # Check if analysis exists in cache
        if analysis_id not in analysis_cache:
            raise HTTPException(status_code=404, detail="Analysis not found. Please run the analysis first.")
        
        analysis_data = analysis_cache[analysis_id]
        
        # Generate PDF
        pdf_path = await pdf_generator.generate_analysis_report(analysis_id, analysis_data)
        
        if not pdf_path:
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            filename=f"token_analysis_{analysis_id[:8]}.pdf",
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/pdf")
async def export_analysis_to_pdf(analysis_data: dict):
    """Generate PDF from provided analysis data"""
    try:
        analysis_id = analysis_data.get('analysis_id', str(uuid.uuid4()))
        
        # Generate PDF
        pdf_path = await pdf_generator.generate_analysis_report(analysis_id, analysis_data)
        
        if not pdf_path:
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            filename=f"token_analysis_{analysis_id[:8]}.pdf",
            media_type="application/pdf"
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

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
    
    # Handle case when market data is not available from BlockFrost
    if hasattr(metrics, 'market_data_available') and not metrics.market_data_available:
        summary += "Liquidity: N/A (requires DEX API integration). "
    else:
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
    """Generate prioritized next steps - concise and actionable"""
    steps = []
    
    # High priority recommendations
    high_priority = [r for r in recommendations if r.priority == "high"]
    for rec in high_priority[:2]:  # Top 2
        steps.append(f"[HIGH] {rec.recommendation.strip()}")
    
    # Critical exchange requirements
    for req in unmet_requirements[:2]:  # Top 2
        steps.append(f"[EXCHANGE] {req.requirement.strip()}")
    
    # Medium priority recommendations
    medium_priority = [r for r in recommendations if r.priority == "medium"]
    for rec in medium_priority[:2]:  # Top 2
        steps.append(f"[MEDIUM] {rec.recommendation.strip()}")
    
    if not steps:
        steps.append("Continue monitoring metrics and market conditions")
    
    return steps[:5]  # Max 5 steps

# ============================================================================
# EMAIL ENDPOINTS
# ============================================================================

from pydantic import BaseModel, EmailStr

class SendEmailRequest(BaseModel):
    """Request model for sending email"""
    to_email: EmailStr
    analysis_id: str
    cc: List[EmailStr] = []

class SendEmailResponse(BaseModel):
    """Response model for email sending"""
    success: bool
    message: str
    timestamp: str = None
    recipient: str = None

@app.post("/api/send-email", response_model=SendEmailResponse)
async def send_analysis_email(request: SendEmailRequest):
    """
    Send analysis report via email with PDF attachment
    
    Features:
    - Professional HTML email formatting
    - Automatic PDF attachment
    - CC/BCC support
    - Retry logic on failure
    - Delivery logging
    """
    try:
        # Retrieve analysis from cache
        if request.analysis_id not in analysis_cache:
            raise HTTPException(
                status_code=404,
                detail=f"Analysis {request.analysis_id} not found. Please run analysis first."
            )
        
        analysis_data = analysis_cache[request.analysis_id]
        
        # Get PDF path
        pdf_path = analysis_data.get("pdf_path")
        if not pdf_path or not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=404,
                detail="PDF report not found. Please regenerate the analysis."
            )
        
        # Send email
        result = await email_service.send_analysis_report(
            to_email=request.to_email,
            token_name=analysis_data.get("token_name", "Unknown"),
            token_symbol=analysis_data.get("token_symbol", "???"),
            pdf_path=pdf_path,
            readiness_score=analysis_data.get("readiness_score", {}).get("total_score", 0),
            grade=analysis_data.get("readiness_score", {}).get("grade", "N/A"),
            cc=request.cc if request.cc else None
        )
        
        if not result.get("success"):
            # Check if mock mode
            if result.get("mock"):
                logger.warning("Email service in mock mode - returning success for demo")
                return SendEmailResponse(
                    success=True,
                    message="✅ Email would be sent (demo mode - configure SMTP for real sending)",
                    timestamp=datetime.utcnow().isoformat(),
                    recipient=request.to_email
                )
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Failed to send email")
            )
        
        return SendEmailResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in send_analysis_email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/email-log")
async def get_email_log(limit: int = 50):
    """
    Get recent email delivery log
    
    Returns history of email sending attempts with status
    """
    try:
        return {
            "log": email_service.get_delivery_log(limit=limit),
            "total": len(email_service.delivery_log)
        }
    except Exception as e:
        logger.error(f"Error retrieving email log: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PDF DOWNLOAD ENDPOINT (Enhanced)
# ============================================================================

@app.get("/api/download/pdf/{analysis_id}")
async def download_pdf(analysis_id: str):
    """
    Download PDF report with security token validation
    
    Features:
    - Secure file serving
    - Proper MIME types
    - Content-Disposition headers for download
    """
    try:
        # Check cache
        if analysis_id not in analysis_cache:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found. PDF may have expired."
            )
        
        analysis_data = analysis_cache[analysis_id]
        pdf_path = analysis_data.get("pdf_path")
        
        if not pdf_path or not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=404,
                detail="PDF file not found"
            )
        
        # Secure filename
        token_symbol = analysis_data.get("token_symbol", "TOKEN")
        filename = f"{token_symbol}_Analysis_{analysis_id[:8]}.pdf"
        
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=filename,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Cache-Control": "no-cache, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading PDF: {e}")
        raise HTTPException(status_code=500, detail="Failed to download PDF")

# ============================================================================
# ANALYSIS STATUS ENDPOINT
# ============================================================================

@app.get("/api/analysis/{analysis_id}/status")
async def get_analysis_status(analysis_id: str):
    """
    Get analysis status and metadata
    
    Returns analysis information without full data payload
    """
    try:
        if analysis_id not in analysis_cache:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis_data = analysis_cache[analysis_id]
        
        return {
            "analysis_id": analysis_id,
            "token_name": analysis_data.get("token_name"),
            "token_symbol": analysis_data.get("token_symbol"),
            "policy_id": analysis_data.get("policy_id"),
            "readiness_score": analysis_data.get("readiness_score", {}).get("total_score"),
            "grade": analysis_data.get("readiness_score", {}).get("grade"),
            "pdf_available": bool(analysis_data.get("pdf_path") and os.path.exists(analysis_data.get("pdf_path", ""))),
            "timestamp": analysis_data.get("timestamp"),
            "target_exchanges": analysis_data.get("target_exchanges"),
            "target_chains": analysis_data.get("target_chains")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import os
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
