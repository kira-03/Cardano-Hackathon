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
    """Token on-chain metrics"""
    total_supply: str
    circulating_supply: str
    holder_count: int
    top_10_concentration: float
    top_50_concentration: float
    liquidity_usd: float
    volume_24h: float
    metadata_score: float
    contract_risk_score: float

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

class Recommendation(BaseModel):
    """Improvement recommendation"""
    category: str
    priority: str  # high, medium, low
    issue: str
    recommendation: str
    estimated_impact: str

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
