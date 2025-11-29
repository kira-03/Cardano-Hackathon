"""
Token Analysis Agent - AI-powered on-chain token metrics analysis and readiness scoring
"""
from typing import Dict, Any, List
import google.generativeai as genai
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
        
        # Initialize Gemini AI capabilities
        try:
            if settings.gemini_api_key and settings.use_ai_analysis:
                genai.configure(api_key=settings.gemini_api_key)
                self.llm_model = genai.GenerativeModel('models/gemini-2.5-flash')
                self.use_llm = True
                logger.info("✅ AI Token Analysis Agent initialized with Gemini")
            elif os.getenv('GEMINI_API_KEY') and settings.use_ai_analysis:
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                self.llm_model = genai.GenerativeModel('models/gemini-2.5-flash')
                self.use_llm = True
                logger.info("✅ AI Token Analysis Agent initialized with Gemini from environment")
            else:
                raise Exception("AI analysis disabled or no API key")
        except Exception as e:
            logger.warning(f"⚠️ AI disabled for Token Analysis: {e}")
            self.llm_model = None
            self.use_llm = False
    
    async def analyze(self, policy_id: str) -> Dict[str, Any]:
        """Complete token analysis pipeline"""
        
        logger.info("  → Fetching on-chain data...")
        # Fetch on-chain data
        token_info = await self.cardano_service.get_token_info(policy_id)
        
        logger.info("  → Analyzing holder distribution...")
        holders = await self.cardano_service.get_token_holders(policy_id)
        holder_analysis = await self.cardano_service.analyze_holder_distribution(holders)
        
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
        
        metrics = TokenMetrics(
            total_supply=str(total_supply),
            circulating_supply=str(total_supply),  # Assume all circulating for now
            holder_count=holder_analysis["total_holders"],
            top_10_concentration=holder_analysis["top_10_concentration"],
            top_50_concentration=holder_analysis["top_50_concentration"],
            liquidity_usd=liquidity["total_liquidity_usd"],
            volume_24h=liquidity["volume_24h_usd"],
            metadata_score=metadata_score,
            contract_risk_score=contract_risk_score
        )
        
        logger.info("  → Calculating readiness score...")
        # Calculate readiness score (use AI if available)
        if self.use_llm:
            readiness_score = await self._calculate_ai_readiness_score(token_info, metrics)
        else:
            readiness_score = self._calculate_readiness_score(metrics)
        
        logger.info("  → Generating recommendations...")
        # Generate recommendations (use AI if available)
        if self.use_llm:
            recommendations = await self._generate_ai_recommendations(token_info, metrics, readiness_score)
        else:
            recommendations = self._generate_recommendations(metrics, readiness_score)
        
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
        
        Weights:
        - Liquidity: 30%
        - Holder Distribution: 25%
        - Metadata: 15%
        - Security: 15%
        - Supply Stability: 10%
        - Market Activity: 5%
        """
        
        # Liquidity Score (0-100)
        # Good: >$100k, Moderate: $50k-100k, Poor: <$50k
        liquidity = metrics.liquidity_usd
        if liquidity >= 100000:
            liquidity_score = 100
        elif liquidity >= 50000:
            liquidity_score = 70 + (liquidity - 50000) / 50000 * 30
        elif liquidity >= 10000:
            liquidity_score = 40 + (liquidity - 10000) / 40000 * 30
        else:
            liquidity_score = liquidity / 10000 * 40
        
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
        if metrics.holder_count >= 1000:
            holder_score = min(100, holder_score + 10)
        elif metrics.holder_count >= 500:
            holder_score = min(100, holder_score + 5)
        
        # Metadata Score (already 0-100)
        metadata_score = metrics.metadata_score
        
        # Security Score (already 0-100)
        security_score = metrics.contract_risk_score
        
        # Supply Stability Score (simplified - assume stable for hackathon)
        supply_stability_score = 85.0
        
        # Market Activity Score (based on volume/liquidity ratio)
        if metrics.liquidity_usd > 0:
            volume_ratio = metrics.volume_24h / metrics.liquidity_usd
            if volume_ratio >= 0.15:  # 15%+ daily turnover
                market_activity_score = 100
            elif volume_ratio >= 0.05:
                market_activity_score = 60 + (volume_ratio - 0.05) / 0.1 * 40
            else:
                market_activity_score = volume_ratio / 0.05 * 60
        else:
            market_activity_score = 0
        
        # Calculate weighted total
        total_score = (
            liquidity_score * 0.30 +
            holder_score * 0.25 +
            metadata_score * 0.15 +
            security_score * 0.15 +
            supply_stability_score * 0.10 +
            market_activity_score * 0.05
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
        """Generate actionable recommendations"""
        recommendations = []
        
        # Liquidity recommendations
        if score.liquidity_score < 70:
            recommendations.append(Recommendation(
                category="Liquidity",
                priority="high",
                issue=f"Low liquidity: ${metrics.liquidity_usd:,.0f}",
                recommendation="Increase DEX pool liquidity to at least $50,000. Consider incentive programs or liquidity mining.",
                estimated_impact="+15-20 points to readiness score"
            ))
        
        # Holder distribution recommendations
        if score.holder_distribution_score < 60:
            recommendations.append(Recommendation(
                category="Holder Distribution",
                priority="high",
                issue=f"High whale concentration: Top 10 hold {metrics.top_10_concentration}%",
                recommendation="Improve token distribution through airdrops, community programs, or gradual whale sell-offs.",
                estimated_impact="+10-15 points to readiness score"
            ))
        
        if metrics.holder_count < 500:
            recommendations.append(Recommendation(
                category="Holder Count",
                priority="medium",
                issue=f"Only {metrics.holder_count} holders",
                recommendation="Increase holder base to at least 500 through marketing and community building.",
                estimated_impact="+5-10 points to readiness score"
            ))
        
        # Metadata recommendations
        if score.metadata_score < 80:
            recommendations.append(Recommendation(
                category="Metadata",
                priority="medium",
                issue="Incomplete token metadata",
                recommendation="Add missing metadata fields: website, social links, detailed description, and verified logo.",
                estimated_impact="+5-8 points to readiness score"
            ))
        
        # Market activity recommendations
        if score.market_activity_score < 50:
            recommendations.append(Recommendation(
                category="Market Activity",
                priority="low",
                issue="Low trading volume",
                recommendation="Increase trading activity through partnerships, listings on more DEXes, and market making.",
                estimated_impact="+2-5 points to readiness score"
            ))
        
        return recommendations
    
    async def _calculate_ai_readiness_score(self, token_info: Dict[str, Any], metrics: TokenMetrics) -> ReadinessScore:
        """AI-powered readiness score calculation using advanced LLM analysis"""
        try:
            logger.info("🤖 AI calculating comprehensive readiness score...")
            
            # Prepare comprehensive data for AI analysis
            analysis_data = {
                "token_info": {
                    "name": token_info.get("asset_name", "Unknown"),
                    "policy_id": token_info.get("policy_id", ""),
                    "fingerprint": token_info.get("fingerprint", ""),
                    "metadata": token_info.get("metadata", {})
                },
                "on_chain_metrics": {
                    "total_supply": metrics.total_supply,
                    "circulating_supply": metrics.circulating_supply,
                    "holder_count": metrics.holder_count,
                    "top_10_concentration": metrics.top_10_concentration,
                    "top_50_concentration": metrics.top_50_concentration,
                    "liquidity_usd": metrics.liquidity_usd,
                    "volume_24h": metrics.volume_24h,
                    "metadata_score": metrics.metadata_score,
                    "contract_risk_score": metrics.contract_risk_score
                }
            }
            
            prompt = f"""
You are an expert DeFi analyst specializing in token economics and exchange listings. Analyze this Cardano token comprehensively.

TOKEN DATA:
{json.dumps(analysis_data, indent=2)}

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
            
            response = self.llm_model.generate_content(prompt)
            
            ai_analysis = json.loads(response.text)
            
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
Based on this comprehensive token analysis, generate strategic recommendations for exchange listing preparation.

TOKEN: {token_info.get("asset_name", "Unknown")}
CURRENT GRADE: {score.grade} ({score.total_score}/100)

SCORE BREAKDOWN:
- Liquidity: {score.liquidity_score}/100
- Holder Distribution: {score.holder_distribution_score}/100  
- Metadata: {score.metadata_score}/100
- Security: {score.security_score}/100
- Market Activity: {score.market_activity_score}/100

CURRENT METRICS:
- Holders: {metrics.holder_count}
- Liquidity: ${metrics.liquidity_usd:,.0f}
- Volume 24h: ${metrics.volume_24h:,.0f}
- Top 10 concentration: {metrics.top_10_concentration}%

Generate 5-8 prioritized recommendations in this JSON format:
{{
    "recommendations": [
        {{
            "category": "<category>",
            "priority": "<high/medium/low>", 
            "issue": "<specific problem identified>",
            "recommendation": "<detailed actionable advice>",
            "estimated_impact": "<expected score improvement>",
            "implementation_timeline": "<timeframe estimate>",
            "success_metrics": "<how to measure progress>"
        }}
    ]
}}

Focus on practical, achievable actions that will have measurable impact on exchange listing prospects.
"""
            
            response = self.llm_model.generate_content(prompt)
            
            ai_recs = json.loads(response.text)
            
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
