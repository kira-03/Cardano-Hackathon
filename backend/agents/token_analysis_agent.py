"""
Token Analysis Agent - AI-powered on-chain token metrics analysis and readiness scoring
"""
from typing import Dict, Any, List
from openai import OpenAI
import json
import logging
import os
from config import settings
from models.schemas import TokenMetrics, ReadinessScore, Recommendation
from services.cardano_service import CardanoService

logger = logging.getLogger(__name__)

class TokenAnalysisAgent:
    def __init__(self, cardano_service: CardanoService):
        self.cardano_service = cardano_service
        self.name = "AI Token Analysis Agent"
        
        # Initialize OpenAI capabilities
        try:
            api_key = settings.openai_api_key or os.getenv('OPENAI_API_KEY')
            if api_key and settings.use_ai_analysis:
                self.llm_client = OpenAI(api_key=api_key)
                self.llm_model = "gpt-4o-mini"
                self.use_llm = True
                logger.info("✅ AI Token Analysis Agent initialized with OpenAI")
            else:
                raise Exception("AI analysis disabled or no API key")
        except Exception as e:
            logger.warning(f"⚠️ AI disabled for Token Analysis: {e}")
            self.llm_client = None
            self.use_llm = False
    
    async def analyze(self, policy_id: str) -> Dict[str, Any]:
        """Complete token analysis pipeline"""
        
        logger.info("  → Fetching on-chain data...")
        # Fetch on-chain data
        token_info = await self.cardano_service.get_token_info(policy_id)
        
        logger.info("  → Analyzing holder distribution...")
        holders = await self.cardano_service.get_token_holders(policy_id)
        total_supply_raw = int(token_info.get("quantity", 0))
        holder_analysis = await self.cardano_service.analyze_holder_distribution(holders, total_supply_raw)
        
        logger.info("  → Estimating DEX liquidity...")
        liquidity = await self.cardano_service.get_dex_liquidity(policy_id)
        
        logger.info("  → Analyzing metadata quality...")
        metadata_score = await self.cardano_service.analyze_metadata_quality(
            token_info.get("metadata", {})
        )
        
        logger.info("  → Checking contract risk...")
        contract_risk_score = await self.cardano_service.analyze_contract_risk(policy_id)
        
        # Build metrics
        total_supply = int(token_info.get("quantity", 0))
        
        # Check if market data is available (from CoinPaprika or other APIs)
        market_data_available = liquidity.get("total_liquidity_usd") is not None
        data_source = liquidity.get("data_source", "BlockFrost (on-chain only)")
        
        # Build combined data source description
        if market_data_available:
            combined_source = f"BlockFrost (on-chain) + {data_source}"
        else:
            combined_source = "BlockFrost (on-chain only)"
        
        metrics = TokenMetrics(
            total_supply=str(total_supply),
            circulating_supply=str(total_supply),  # Assume all circulating for now
            holder_count=holder_analysis["total_holders"],
            top_10_concentration=holder_analysis["top_10_concentration"],
            top_50_concentration=holder_analysis["top_50_concentration"],
            liquidity_usd=liquidity.get("total_liquidity_usd"),  # From CoinPaprika if available
            volume_24h=liquidity.get("volume_24h_usd"),  # From CoinPaprika if available
            price_usd=liquidity.get("price_usd"),  # From CoinPaprika if available
            market_cap_usd=liquidity.get("market_cap_usd"),  # From CoinPaprika if available
            price_change_24h=liquidity.get("price_change_24h"),  # From CoinPaprika if available
            metadata_score=metadata_score,
            contract_risk_score=contract_risk_score,
            data_source=combined_source,
            market_data_available=market_data_available
        )
        
        logger.info("  → Calculating readiness score...")
        # Always use agentic AI (LLM) for readiness score and recommendations
        readiness_score = await self._calculate_ai_readiness_score(token_info, metrics)
        logger.info("  → Generating recommendations...")
        recommendations = await self._generate_ai_recommendations(token_info, metrics, readiness_score)
        
        logger.info(f"  ✓ Analysis complete: Score={readiness_score.total_score}, Grade={readiness_score.grade}")
        
        return {
            "token_info": token_info,
            "metrics": metrics,
            "readiness_score": readiness_score,
            "recommendations": recommendations
        }
    
    def _calculate_readiness_score(self, metrics: TokenMetrics) -> ReadinessScore:
        """
        Calculate listing readiness score (0-100)
        
        Note: When market data (liquidity, volume) is not available from DEX APIs,
        we score based only on on-chain metrics from BlockFrost.
        
        Weights when market data available:
        - Liquidity: 30%
        - Holder Distribution: 25%
        - Metadata: 15%
        - Security: 15%
        - Supply Stability: 10%
        - Market Activity: 5%
        
        Weights when market data NOT available:
        - Holder Distribution: 40%
        - Metadata: 25%
        - Security: 25%
        - Supply Stability: 10%
        """
        
        has_market_data = metrics.liquidity_usd is not None and metrics.volume_24h is not None
        
        # Liquidity Score (0-100) - Only if data available
        if has_market_data and metrics.liquidity_usd is not None:
            liquidity = metrics.liquidity_usd
            if liquidity >= 100000:
                liquidity_score = 100
            elif liquidity >= 50000:
                liquidity_score = 70 + (liquidity - 50000) / 50000 * 30
            elif liquidity >= 10000:
                liquidity_score = 40 + (liquidity - 10000) / 40000 * 30
            else:
                liquidity_score = liquidity / 10000 * 40
        else:
            liquidity_score = 0  # Unknown - not counted in score
        
        # Holder Distribution Score (0-100)
        # Lower concentration = better decentralization
        top_10 = metrics.top_10_concentration
        if top_10 <= 20:
            holder_score = 100
        elif top_10 <= 40:
            holder_score = 80 - (top_10 - 20) / 20 * 30
        elif top_10 <= 60:
            holder_score = 50 - (top_10 - 40) / 20 * 30
        else:
            holder_score = max(0, 20 - (top_10 - 60) / 40 * 20)
        
        # Bonus for holder count
        if metrics.holder_count >= 10000:
            holder_score = min(100, holder_score + 20)
        elif metrics.holder_count >= 1000:
            holder_score = min(100, holder_score + 10)
        elif metrics.holder_count >= 500:
            holder_score = min(100, holder_score + 5)
        
        # Metadata Score (already 0-100)
        metadata_score = metrics.metadata_score
        
        # Security Score (already 0-100)
        security_score = metrics.contract_risk_score
        
        # Supply Stability Score (simplified - assume stable for hackathon)
        supply_stability_score = 85.0
        
        # Market Activity Score - Only if data available
        if has_market_data and metrics.liquidity_usd and metrics.liquidity_usd > 0 and metrics.volume_24h is not None:
            volume_ratio = metrics.volume_24h / metrics.liquidity_usd
            if volume_ratio >= 0.15:  # 15%+ daily turnover
                market_activity_score = 100
            elif volume_ratio >= 0.05:
                market_activity_score = 60 + (volume_ratio - 0.05) / 0.1 * 40
            else:
                market_activity_score = volume_ratio / 0.05 * 60
        else:
            market_activity_score = 0  # Unknown - not counted
        
        # Calculate weighted total based on available data
        if has_market_data:
            # Full scoring with market data
            total_score = (
                liquidity_score * 0.30 +
                holder_score * 0.25 +
                metadata_score * 0.15 +
                security_score * 0.15 +
                supply_stability_score * 0.10 +
                market_activity_score * 0.05
            )
        else:
            # On-chain only scoring (no market data)
            total_score = (
                holder_score * 0.40 +
                metadata_score * 0.25 +
                security_score * 0.25 +
                supply_stability_score * 0.10
            )
        
        # Determine grade
        if total_score >= 85:
            grade = "A"
        elif total_score >= 70:
            grade = "B"
        elif total_score >= 55:
            grade = "C"
        elif total_score >= 40:
            grade = "D"
        else:
            grade = "F"
        
        return ReadinessScore(
            total_score=round(total_score, 1),
            liquidity_score=round(liquidity_score, 1),
            holder_distribution_score=round(holder_score, 1),
            metadata_score=round(metadata_score, 1),
            security_score=round(security_score, 1),
            supply_stability_score=round(supply_stability_score, 1),
            market_activity_score=round(market_activity_score, 1),
            grade=grade
        )
    
    def _generate_recommendations(
        self,
        metrics: TokenMetrics,
        score: ReadinessScore
    ) -> List[Recommendation]:
        """
        Generate recommendations by referencing exchange and chain requirements,
        matching them with actual token data, and producing dynamic, context-aware statements.
        """
        # Import ExchangePreparationAgent dynamically to avoid circular imports
        from agents.exchange_preparation_agent import ExchangePreparationAgent
        # Assume default exchanges and chains for now
        target_exchanges = ["Binance", "KuCoin", "Gate.io", "MEXC"]
        agent = ExchangePreparationAgent()
        # Use the requirement checker to get requirements for each exchange
        all_requirements = []
        for exchange in target_exchanges:
            if hasattr(agent, "_check_exchange_requirements"):
                reqs = agent._check_exchange_requirements(exchange, metrics, score)
                all_requirements.extend(reqs)

        # For each unmet requirement, generate a dynamic recommendation
        recommendations = []
        for req in all_requirements:
            if not req.meets_requirement:
                recommendations.append(Recommendation(
                    category="Exchange Requirement",
                    priority="high",
                    issue=f"{req.exchange}: {req.requirement}",
                    recommendation=f"{req.current_status}. Refer to {req.exchange} docs for details.",
                    estimated_impact="Required for listing approval"
                ))

        # Only return dynamic, requirements-driven recommendations
        return recommendations
    
    async def _calculate_ai_readiness_score(self, token_info: Dict[str, Any], metrics: TokenMetrics) -> ReadinessScore:
        """AI-powered readiness score calculation using advanced LLM analysis"""
        try:
            logger.info("🤖 AI calculating comprehensive readiness score...")
            
            # Prepare comprehensive data for AI analysis
            # Convert metrics to dict if it's a Pydantic model
            metrics_dict = metrics.dict() if hasattr(metrics, 'dict') else metrics
            
            analysis_data = {
                "token_info": {
                    "name": token_info.get("asset_name", "Unknown"),
                    "policy_id": token_info.get("policy_id", ""),
                    "fingerprint": token_info.get("fingerprint", ""),
                    "metadata": str(token_info.get("metadata", {}))  # Convert to string to avoid serialization issues
                },
                "on_chain_metrics": {
                    "total_supply": metrics_dict.get("total_supply") if isinstance(metrics_dict, dict) else metrics.total_supply,
                    "circulating_supply": metrics_dict.get("circulating_supply") if isinstance(metrics_dict, dict) else metrics.circulating_supply,
                    "holder_count": metrics_dict.get("holder_count") if isinstance(metrics_dict, dict) else metrics.holder_count,
                    "top_10_concentration": metrics_dict.get("top_10_concentration") if isinstance(metrics_dict, dict) else metrics.top_10_concentration,
                    "top_50_concentration": metrics_dict.get("top_50_concentration") if isinstance(metrics_dict, dict) else metrics.top_50_concentration,
                    "liquidity_usd": metrics_dict.get("liquidity_usd") if isinstance(metrics_dict, dict) else metrics.liquidity_usd,
                    "volume_24h": metrics_dict.get("volume_24h") if isinstance(metrics_dict, dict) else metrics.volume_24h,
                    "metadata_score": metrics_dict.get("metadata_score") if isinstance(metrics_dict, dict) else metrics.metadata_score,
                    "contract_risk_score": metrics_dict.get("contract_risk_score") if isinstance(metrics_dict, dict) else metrics.contract_risk_score
                }
            }
            
            prompt = f"""
You are an expert DeFi analyst specializing in token economics and exchange listings. Analyze this Cardano token comprehensively.

TOKEN DATA:
{json.dumps(analysis_data, indent=2, default=str)}

ANALYSIS FRAMEWORK:
1. LIQUIDITY ANALYSIS (30% weight):
   - Current liquidity depth vs industry benchmarks
   - Volume-to-liquidity ratio health
   - Market making potential
   
2. DECENTRALIZATION SCORE (25% weight):
   - Holder distribution patterns
   - Whale concentration risks  
   - Community engagement signals

3. METADATA & BRANDING (15% weight):
   - Professional presentation
   - Information completeness
   - Marketing readiness

4. SECURITY & STABILITY (15% weight):
   - Smart contract risk factors
   - Historical stability
   - Audit requirements

5. MARKET DYNAMICS (10% weight):
   - Trading activity patterns
   - Price stability indicators
   - Market maker presence

6. GROWTH POTENTIAL (5% weight):
   - Scalability indicators
   - Partnership potential
   - Ecosystem positioning

PROVIDE DETAILED ANALYSIS IN THIS JSON FORMAT:
{{
    "total_score": <0-100>,
    "grade": "<A/B/C/D/F>",
    "component_scores": {{
        "liquidity_score": <0-100>,
        "holder_distribution_score": <0-100>, 
        "metadata_score": <0-100>,
        "security_score": <0-100>,
        "supply_stability_score": <0-100>,
        "market_activity_score": <0-100>
    }},
    "detailed_analysis": {{
        "liquidity_assessment": "<detailed liquidity analysis>",
        "decentralization_review": "<holder distribution insights>",
        "metadata_evaluation": "<metadata completeness review>",
        "security_analysis": "<risk factor assessment>",
        "market_dynamics": "<trading pattern analysis>",
        "growth_outlook": "<potential and opportunities>"
    }},
    "critical_insights": [
        "<insight1>",
        "<insight2>", 
        "<insight3>"
    ],
    "exchange_readiness_factors": {{
        "immediate_strengths": ["<strength1>", "<strength2>"],
        "improvement_needed": ["<area1>", "<area2>"],
        "risk_factors": ["<risk1>", "<risk2>"]
    }}
}}

Be thorough and provide actionable insights for exchange listing preparation.
"""
            
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # Extract JSON from response text (handle markdown code blocks)
            response_text = response.choices[0].message.content.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            ai_analysis = json.loads(response_text)
            
            # Create enhanced ReadinessScore with AI insights
            scores = ai_analysis["component_scores"]
            readiness_score = ReadinessScore(
                total_score=round(ai_analysis["total_score"], 1),
                liquidity_score=round(scores["liquidity_score"], 1),
                holder_distribution_score=round(scores["holder_distribution_score"], 1),
                metadata_score=round(scores["metadata_score"], 1),
                security_score=round(scores["security_score"], 1),
                supply_stability_score=round(scores["supply_stability_score"], 1),
                market_activity_score=round(scores["market_activity_score"], 1),
                grade=ai_analysis["grade"]
            )
            
            # Add AI-specific insights as attributes
            readiness_score.ai_analysis = ai_analysis.get("detailed_analysis", {})
            readiness_score.critical_insights = ai_analysis.get("critical_insights", [])
            readiness_score.exchange_readiness_factors = ai_analysis.get("exchange_readiness_factors", {})
            
            logger.info(f"🎯 AI Readiness Analysis: Grade {readiness_score.grade} ({readiness_score.total_score}/100)")
            return readiness_score
            
        except Exception as e:
            logger.error(f"❌ AI readiness scoring failed: {e}")
            # Fallback to algorithmic scoring
            return self._calculate_readiness_score(metrics)
    
    async def _generate_ai_recommendations(
        self, 
        token_info: Dict[str, Any], 
        metrics: TokenMetrics, 
        score: ReadinessScore
    ) -> List[Recommendation]:
        """AI-powered recommendation generation"""
        try:
            logger.info("🤖 AI generating strategic recommendations...")
            
            # Get AI insights from score if available
            ai_insights = getattr(score, 'ai_analysis', {})
            readiness_factors = getattr(score, 'exchange_readiness_factors', {})
            
            prompt = f"""
Based on this token analysis, generate SHORT, CRISP, and ACTIONABLE recommendations for exchange listing.

TOKEN: {token_info.get("asset_name", "Unknown")} | GRADE: {score.grade} ({score.total_score}/100)

SCORES: Liquidity {score.liquidity_score} | Holders {score.holder_distribution_score} | Metadata {score.metadata_score} | Security {score.security_score}

METRICS: {metrics.holder_count} holders | {"$" + f"{metrics.liquidity_usd:,.0f}" if metrics.liquidity_usd is not None else "N/A"} liquidity | {metrics.top_10_concentration}% top 10 concentration

CRITICAL RULES:
1. Each recommendation must be MAX 120 characters (1-2 sentences)
2. Be SPECIFIC and ACTIONABLE (not generic advice)
3. Use imperative verbs (Audit, Deploy, Increase, Launch, etc.)
4. NO verbose explanations or background context
5. Generate 5 recommendations ONLY

JSON FORMAT:
{{
    "recommendations": [
        {{
            "category": "<Metadata|Security|Liquidity|Marketing|Compliance>",
            "priority": "<high|medium|low>", 
            "issue": "<10 words max>",
            "recommendation": "<MAX 120 chars - crisp action>",
            "estimated_impact": "<+X points or X% improvement>"
        }}
    ]
}}

EXAMPLES OF GOOD RECOMMENDATIONS (short & actionable):
- "Audit metadata completeness: add logo, whitepaper, social links, and tokenomics to all platforms"
- "Commission Tier-1 security audit (CertiK/Halborn) and publish full report within 30 days"
- "Deploy $50K liquidity to top DEXs with 2-3 month lock to stabilize trading pairs"
- "Launch community campaign: weekly AMAs, contests, and influencer partnerships for 60 days"
- "Register on CoinMarketCap and CoinGecko with verified profile and complete metadata"

BAD EXAMPLES (too verbose):
- "Conduct a comprehensive audit of all token metadata across blockchain explorers, official websites, and community platforms. Ensure consistency and completeness for: high-resolution logo and branding assets, detailed project description and use cases..."

Generate recommendations NOW:
"""
            
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            
            # Extract JSON from response text (handle markdown code blocks)
            response_text = response.choices[0].message.content.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            ai_recs = json.loads(response_text)
            
            # Convert to Recommendation objects
            recommendations = []
            for rec_data in ai_recs["recommendations"]:
                recommendation = Recommendation(
                    category=rec_data["category"],
                    priority=rec_data["priority"],
                    issue=rec_data["issue"], 
                    recommendation=rec_data["recommendation"],
                    estimated_impact=rec_data["estimated_impact"]
                )
                # Add AI-specific attributes
                recommendation.implementation_timeline = rec_data.get("implementation_timeline", "")
                recommendation.success_metrics = rec_data.get("success_metrics", "")
                recommendations.append(recommendation)
            
            logger.info(f"✅ AI generated {len(recommendations)} strategic recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ AI recommendation generation failed: {e}")
            # Fallback to algorithmic recommendations
            return self._generate_recommendations(metrics, score)
