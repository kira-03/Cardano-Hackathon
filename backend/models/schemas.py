from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalysisRequest(BaseModel):
    """Request model for token analysis"""
    policy_id: str = Field(..., description="Cardano token policy ID")
    target_exchanges: Optional[List[str]] = Field(
        default=["Binance", "KuCoin", "Gate.io"],
        description="Target exchanges for listing"
    )
    target_chains: Optional[List[str]] = Field(
        default=["Ethereum", "BSC", "Polygon"],
        description="Target chains for cross-chain expansion"
    )

class TokenMetrics(BaseModel):
    """Token on-chain and market metrics"""
    total_supply: str
    circulating_supply: str
    holder_count: int
    top_10_concentration: float
    top_50_concentration: float
    # Market data from CoinPaprika API (free, no API key)
    liquidity_usd: Optional[float] = None  # Estimated from market cap
    volume_24h: Optional[float] = None  # 24h trading volume
    price_usd: Optional[float] = None  # Current price
    market_cap_usd: Optional[float] = None  # Market capitalization
    price_change_24h: Optional[float] = None  # 24h price change %
    # Scores
    metadata_score: float
    contract_risk_score: float
    # Data source info
    data_source: str = "BlockFrost (on-chain only)"
    market_data_available: bool = False  # True if CoinPaprika data available

class ReadinessScore(BaseModel):
    """Listing readiness score breakdown"""
    total_score: float = Field(..., ge=0, le=100)
    liquidity_score: float
    holder_distribution_score: float
    metadata_score: float
    security_score: float
    supply_stability_score: float
    market_activity_score: float
    grade: str  # A, B, C, D, F
    # AI Insights
    ai_analysis: Optional[Dict[str, str]] = None
    critical_insights: Optional[List[str]] = None
    exchange_readiness_factors: Optional[Dict[str, List[str]]] = None

class Recommendation(BaseModel):
    """Improvement recommendation"""
    category: str
    priority: str  # high, medium, low
    issue: str
    recommendation: str
    estimated_impact: str
    implementation_timeline: Optional[str] = None
    success_metrics: Optional[str] = None

class ExchangeRequirement(BaseModel):
    """Exchange listing requirement"""
    exchange: str
    requirement: str
    current_status: str
    meets_requirement: bool

class BridgeRoute(BaseModel):
    """Cross-chain bridge route information"""
    source_chain: str
    target_chain: str
    bridge_name: str
    estimated_fee: str
    estimated_time: str
    trust_model: str  # custodial, trustless, hybrid
    slippage_estimate: str
    hops: int
    recommendation_score: float

class MasumiLog(BaseModel):
    """Masumi on-chain logging record"""
    agent_did: str
    decision_type: str
    decision_hash: str
    transaction_id: Optional[str]
    timestamp: datetime

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    analysis_id: str
    policy_id: str
    token_name: str
    token_symbol: str
    timestamp: datetime
    
    # Token Analysis
    metrics: TokenMetrics
    readiness_score: ReadinessScore
    recommendations: List[Recommendation]
    
    # Exchange Preparation
    exchange_requirements: List[ExchangeRequirement]
    proposal_pdf_url: Optional[str]
    
    # Cross-Chain Routing
    bridge_routes: List[BridgeRoute]
    recommended_chain: str
    
    # Masumi Logging
    masumi_logs: List[MasumiLog]
    
    # Summary
    executive_summary: str
    next_steps: List[str]
