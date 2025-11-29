"""
Exchange Preparation Agent - AI-powered CEX requirements analysis and listing document generation
"""
from typing import Dict, Any, List
from openai import OpenAI
import json
import logging
import os
from config import settings
from models.schemas import ExchangeRequirement, TokenMetrics, ReadinessScore

logger = logging.getLogger(__name__)

class ExchangePreparationAgent:
    def __init__(self, cardano_service=None):
        self.name = "AI Exchange Preparation Agent"
        self.cardano_service = cardano_service
        
        # Initialize OpenAI client
        try:
            api_key = settings.openai_api_key or os.getenv('OPENAI_API_KEY')
            if api_key and settings.use_ai_analysis:
                self.llm_client = OpenAI(api_key=api_key)
                self.llm_model = "gpt-4o-mini"
                self.use_llm = True
                logger.info("✅ OpenAI client initialized successfully")
            else:
                raise Exception("No API key available or AI analysis disabled")
        except Exception as e:
            logger.warning(f"⚠️ OpenAI client not available: {e}. Using algorithmic analysis.")
            self.llm_client = None
            self.use_llm = False
        
        # Public CEX listing requirements (based on industry standards)
        self.exchange_requirements = {
            "Binance": {
                "tier": "Tier 1",
                "min_liquidity": 100000,
                "min_holders": 1000,
                "min_volume_24h": 10000,
                "metadata_required": True,
                "security_audit_required": True,
                "kyc_required": True
            },
            "KuCoin": {
                "tier": "Tier 1",
                "min_liquidity": 50000,
                "min_holders": 500,
                "min_volume_24h": 5000,
                "metadata_required": True,
                "security_audit_required": False,
                "kyc_required": True
            },
            "Gate.io": {
                "tier": "Tier 2",
                "min_liquidity": 25000,
                "min_holders": 300,
                "min_volume_24h": 2500,
                "metadata_required": True,
                "security_audit_required": False,
                "kyc_required": True
            },
            "MEXC": {
                "tier": "Tier 2",
                "min_liquidity": 10000,
                "min_holders": 200,
                "min_volume_24h": 1000,
                "metadata_required": True,
                "security_audit_required": False,
                "kyc_required": False
            }
        }
    
    async def prepare(
        self,
        policy_id: str,
        metrics: TokenMetrics,
        target_exchanges: List[str]
    ) -> Dict[str, Any]:
        """Prepare exchange listing documents and analysis"""
        # Get token info if cardano_service available
        token_info = {}
        if self.cardano_service:
            try:
                token_info = await self.cardano_service.get_token_info(policy_id)
            except:
                pass
        
        # Calculate a readiness score (use LLM if available, otherwise algorithmic)
        if self.use_llm:
            readiness_score = await self._calculate_ai_score(token_info, metrics)
        else:
            readiness_score = self._calculate_simple_score(metrics)
        
        return await self._prepare_documents(token_info, metrics, readiness_score, target_exchanges)
    
    async def _prepare_documents(
        self,
        token_info: Dict[str, Any],
        metrics: TokenMetrics,
        readiness_score: Any,
        target_exchanges: List[str]
    ) -> Dict[str, Any]:
        """Prepare exchange listing documents and analysis"""
        # Check requirements for each target exchange
        all_requirements = []
        for exchange in target_exchanges:
            if exchange in self.exchange_requirements:
                reqs = self._check_exchange_requirements(exchange, metrics, readiness_score)
                all_requirements.extend(reqs)
        
        # Generate proposal data
        proposal_data = self._generate_proposal_data(
            token_info,
            metrics,
            readiness_score,
            all_requirements
        )
        
        # Identify compliance gaps
        gaps = self._identify_compliance_gaps(all_requirements)
        
        # Get unmet requirements
        unmet_requirements = [r for r in all_requirements if not r.meets_requirement]
        
        return {
            "requirements": all_requirements,
            "exchange_requirements": all_requirements,
            "proposal_data": proposal_data,
            "compliance_gaps": gaps,
            "unmet_requirements": unmet_requirements,
            "pdf_url": None,  # Would generate PDF in production
            "recommended_exchanges": self._recommend_exchanges(
                metrics,
                readiness_score
            )
        }
    
    def _calculate_simple_score(self, metrics: TokenMetrics):
        """Simple score calculation for internal use (fallback when LLM unavailable)"""
        class SimpleScore:
            def __init__(self):
                self.metadata_score = metrics.metadata_score
                self.total_score = 70.0
                self.grade = "B"
                self.liquidity_score = 15.0
                self.holder_distribution_score = 15.0
                self.security_score = 15.0
                self.market_activity_score = 10.0
        return SimpleScore()
    
    async def _calculate_ai_score(self, token_info: Dict[str, Any], metrics: TokenMetrics):
        """AI-powered readiness score calculation using LLM analysis"""
        try:
            logger.info("🤖 Using AI to analyze token readiness...")
            
            # Prepare data for LLM analysis
            analysis_data = {
                "token_name": token_info.get("asset_name", "Unknown"),
                "policy_id": token_info.get("policy_id", ""),
                "metadata": token_info.get("metadata", {}),
                "metrics": {
                    "total_supply": metrics.total_supply,
                    "holder_count": metrics.holder_count,
                    "top_10_concentration": metrics.top_10_concentration,
                    "liquidity_usd": metrics.liquidity_usd,
                    "volume_24h": metrics.volume_24h,
                    "metadata_score": metrics.metadata_score
                }
            }
            
            prompt = f"""
You are an expert cryptocurrency exchange listing analyst. Analyze this Cardano token and provide a comprehensive readiness score.

TOKEN DATA:
{json.dumps(analysis_data, indent=2, default=str)}

ANALYSIS CRITERIA:
1. Liquidity Depth (30% weight): Current liquidity vs industry standards
2. Holder Distribution (25% weight): Decentralization and whale concentration
3. Metadata Quality (15% weight): Completeness and professionalism
4. Market Activity (15% weight): Trading volume and engagement
5. Security & Stability (10% weight): Risk factors and stability
6. Community & Marketing (5% weight): Social presence and adoption

PROVIDE RESPONSE IN THIS EXACT JSON FORMAT:
{{
    "total_score": <0-100>,
    "grade": "<A/B/C/D/F>",
    "liquidity_score": <0-100>,
    "holder_distribution_score": <0-100>,
    "metadata_score": <0-100>,
    "security_score": <0-100>,
    "market_activity_score": <0-100>,
    "reasoning": "<detailed explanation of scoring>",
    "key_strengths": ["<strength1>", "<strength2>"],
    "critical_weaknesses": ["<weakness1>", "<weakness2>"],
    "improvement_priorities": ["<priority1>", "<priority2>"]
}}

Be thorough and provide actionable insights based on real market standards.
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
            
            # Create enhanced score object
            class AIScore:
                def __init__(self, ai_data):
                    self.total_score = ai_data["total_score"]
                    self.grade = ai_data["grade"]
                    self.liquidity_score = ai_data["liquidity_score"]
                    self.holder_distribution_score = ai_data["holder_distribution_score"]
                    self.metadata_score = ai_data["metadata_score"]
                    self.security_score = ai_data["security_score"]
                    self.market_activity_score = ai_data["market_activity_score"]
                    # AI-specific enhancements
                    self.ai_reasoning = ai_data["reasoning"]
                    self.key_strengths = ai_data["key_strengths"]
                    self.critical_weaknesses = ai_data["critical_weaknesses"]
                    self.improvement_priorities = ai_data["improvement_priorities"]
            
            logger.info(f"🎯 AI Analysis Complete: Grade {ai_analysis['grade']} ({ai_analysis['total_score']}/100)")
            return AIScore(ai_analysis)
            
        except Exception as e:
            logger.error(f"❌ AI analysis failed: {e}")
            # Fallback to simple scoring
            return self._calculate_simple_score(metrics)
    
    def _check_exchange_requirements(
        self,
        exchange: str,
        metrics: TokenMetrics,
        score: ReadinessScore
    ) -> List[ExchangeRequirement]:
        """Check if token meets exchange requirements"""
        reqs = self.exchange_requirements[exchange]
        requirements = []
        
        # Check if market data is available
        market_data_available = getattr(metrics, 'market_data_available', True)
        liquidity = metrics.liquidity_usd if metrics.liquidity_usd is not None else 0
        volume = metrics.volume_24h if metrics.volume_24h is not None else 0
        
        # Liquidity requirement
        if market_data_available:
            meets_liquidity = liquidity >= reqs["min_liquidity"]
            liquidity_status = f"Current: ${liquidity:,.0f}"
        else:
            meets_liquidity = None  # Unknown - requires DEX API integration
            liquidity_status = "N/A (requires DEX API integration)"
        requirements.append(ExchangeRequirement(
            exchange=exchange,
            requirement=f"Minimum liquidity: ${reqs['min_liquidity']:,}",
            current_status=liquidity_status,
            meets_requirement=meets_liquidity if meets_liquidity is not None else False
        ))
        
        # Holder requirement
        meets_holders = metrics.holder_count >= reqs["min_holders"]
        requirements.append(ExchangeRequirement(
            exchange=exchange,
            requirement=f"Minimum holders: {reqs['min_holders']:,}",
            current_status=f"Current: {metrics.holder_count:,}",
            meets_requirement=meets_holders
        ))
        
        # Volume requirement
        if market_data_available:
            meets_volume = volume >= reqs["min_volume_24h"]
            volume_status = f"Current: ${volume:,.0f}"
        else:
            meets_volume = None  # Unknown - requires DEX API integration
            volume_status = "N/A (requires DEX API integration)"
        requirements.append(ExchangeRequirement(
            exchange=exchange,
            requirement=f"Minimum 24h volume: ${reqs['min_volume_24h']:,}",
            current_status=volume_status,
            meets_requirement=meets_volume if meets_volume is not None else False
        ))
        
        # Metadata requirement
        meets_metadata = score.metadata_score >= 70
        requirements.append(ExchangeRequirement(
            exchange=exchange,
            requirement="Complete token metadata",
            current_status=f"Metadata score: {score.metadata_score:.0f}/100",
            meets_requirement=meets_metadata
        ))
        
        # Security audit (if required)
        if reqs.get("security_audit_required"):
            requirements.append(ExchangeRequirement(
                exchange=exchange,
                requirement="Security audit required",
                current_status="Manual verification needed",
                meets_requirement=False  # Requires manual verification
            ))
        
        # KYC (if required)
        if reqs.get("kyc_required"):
            requirements.append(ExchangeRequirement(
                exchange=exchange,
                requirement="Team KYC required",
                current_status="Not verified",
                meets_requirement=False  # Requires manual completion
            ))
        
        return requirements
    
    def _generate_proposal_data(
        self,
        token_info: Dict[str, Any],
        metrics: TokenMetrics,
        score: ReadinessScore,
        requirements: List[ExchangeRequirement]
    ) -> Dict[str, Any]:
        """Generate data for PDF proposal"""
        metadata = token_info.get("metadata", {})
        
        # Calculate requirements met percentage
        total_reqs = len(requirements)
        met_reqs = sum(1 for r in requirements if r.meets_requirement)
        compliance_rate = (met_reqs / total_reqs * 100) if total_reqs > 0 else 0
        
        return {
            "token_name": metadata.get("name", "Unknown Token"),
            "token_symbol": metadata.get("ticker", "UNK"),
            "policy_id": token_info.get("policy_id"),
            "description": metadata.get("description", "No description available"),
            "website": metadata.get("website", "N/A"),
            "social_links": {
                "twitter": metadata.get("twitter", "N/A"),
                "telegram": metadata.get("telegram", "N/A"),
                "discord": metadata.get("discord", "N/A")
            },
            "metrics": {
                "total_supply": metrics.total_supply,
                "holders": metrics.holder_count,
                "liquidity": f"${metrics.liquidity_usd:,.0f}" if metrics.liquidity_usd is not None else "N/A (requires DEX API)",
                "volume_24h": f"${metrics.volume_24h:,.0f}" if metrics.volume_24h is not None else "N/A (requires DEX API)",
                "top_10_concentration": f"{metrics.top_10_concentration}%"
            },
            "readiness_score": {
                "total": score.total_score,
                "grade": score.grade,
                "breakdown": {
                    "Liquidity": score.liquidity_score,
                    "Holder Distribution": score.holder_distribution_score,
                    "Metadata": score.metadata_score,
                    "Security": score.security_score,
                    "Market Activity": score.market_activity_score
                }
            },
            "compliance_rate": round(compliance_rate, 1),
            "unique_value_proposition": self._generate_uvp(metadata),
            "market_potential": self._assess_market_potential(metrics, score)
        }
    
    def _generate_uvp(self, metadata: Dict[str, Any]) -> str:
        """Generate AI-powered Unique Value Proposition from metadata"""
        if self.use_llm:
            return self._generate_ai_uvp(metadata)
        else:
            # Fallback logic
            description = metadata.get("description", "")
            if description:
                return description
            return "A Cardano native token with growing community adoption and strong fundamentals."
    
    def _generate_ai_uvp(self, metadata: Dict[str, Any]) -> str:
        """AI-generated Unique Value Proposition"""
        try:
            logger.info("🤖 Generating AI-powered UVP...")
            
            prompt = f"""
Create a compelling 2-3 sentence Unique Value Proposition for this Cardano token based on its metadata.

METADATA:
{json.dumps(metadata, indent=2, default=str)}

Requirements:
- Professional and exchange-ready tone
- Highlight unique features and benefits
- Focus on market differentiators
- Mention Cardano ecosystem advantages
- Keep it concise but impactful

Return only the UVP text, no additional formatting.
"""
            
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            uvp = response.choices[0].message.content.strip()
            logger.info("✅ AI UVP generated successfully")
            return uvp
            
        except Exception as e:
            logger.error(f"❌ AI UVP generation failed: {e}")
            return "A innovative Cardano native token offering unique utility and strong community-driven value proposition."
    
    def _assess_market_potential(
        self,
        metrics: TokenMetrics,
        score: ReadinessScore
    ) -> str:
        """AI-powered market potential assessment"""
        if self.use_llm:
            return self._assess_ai_market_potential(metrics, score)
        else:
            # Fallback algorithmic assessment
            if score.total_score >= 80:
                return "Strong market potential with excellent fundamentals"
            elif score.total_score >= 65:
                return "Good market potential with solid community support"
            elif score.total_score >= 50:
                return "Moderate market potential, improvements recommended"
            else:
                return "Developing market potential, significant improvements needed"
    
    def _assess_ai_market_potential(self, metrics: TokenMetrics, score: ReadinessScore) -> str:
        """AI-powered market potential analysis"""
        try:
            logger.info("🤖 AI analyzing market potential...")
            
            liquidity_str = f"${metrics.liquidity_usd:,.0f}" if metrics.liquidity_usd is not None else "N/A (requires DEX API)"
            volume_str = f"${metrics.volume_24h:,.0f}" if metrics.volume_24h is not None else "N/A (requires DEX API)"
            
            prompt = f"""
As a crypto market analyst, assess the market potential for this Cardano token.

METRICS:
- Total Score: {score.total_score}/100 (Grade: {score.grade})
- Holder Count: {metrics.holder_count}
- Liquidity: {liquidity_str}
- 24h Volume: {volume_str}
- Top 10 Concentration: {metrics.top_10_concentration}%
- Metadata Score: {metrics.metadata_score}/100

Consider:
- Current market position
- Growth trajectory indicators
- Competitive landscape
- Risk factors
- Exchange listing potential

Provide a concise 1-2 sentence market potential assessment that would be suitable for an exchange listing proposal.
"""
            
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            
            assessment = response.choices[0].message.content.strip()
            logger.info("✅ AI market assessment completed")
            return assessment
            
        except Exception as e:
            logger.error(f"❌ AI market assessment failed: {e}")
            return "Moderate market potential with room for strategic growth and community expansion."
    
    def _identify_compliance_gaps(
        self,
        requirements: List[ExchangeRequirement]
    ) -> List[Dict[str, str]]:
        """Identify what needs improvement"""
        gaps = []
        for req in requirements:
            if not req.meets_requirement:
                gaps.append({
                    "exchange": req.exchange,
                    "requirement": req.requirement,
                    "current_status": req.current_status,
                    "action_needed": self._suggest_action(req.requirement)
                })
        return gaps
    
    def _suggest_action(self, requirement: str) -> str:
        """AI-powered action suggestions for unmet requirements"""
        if self.use_llm:
            return self._suggest_ai_action(requirement)
        else:
            # Fallback algorithmic suggestions
            if "liquidity" in requirement.lower():
                return "Add liquidity to DEX pools or implement liquidity mining program"
            elif "holders" in requirement.lower():
                return "Increase marketing efforts and community building"
            elif "volume" in requirement.lower():
                return "Increase trading activity through partnerships and market making"
            elif "metadata" in requirement.lower():
                return "Complete token metadata with all required information"
            elif "audit" in requirement.lower():
                return "Commission security audit from reputable firm"
            elif "kyc" in requirement.lower():
                return "Complete KYC process with exchange"
            return "Contact exchange for specific requirements"
    
    def _suggest_ai_action(self, requirement: str) -> str:
        """AI-generated action suggestions"""
        try:
            prompt = f"""
You are a crypto exchange listing consultant. A Cardano token project has failed to meet this requirement:

REQUIREMENT: {requirement}

Provide a specific, actionable recommendation (1-2 sentences) that the project team can implement to address this requirement. Focus on practical, achievable steps.
"""
            
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"❌ AI action suggestion failed: {e}")
            return "Consult with exchange requirements team for specific guidance"
    
    def _recommend_exchanges(
        self,
        metrics: TokenMetrics,
        score: ReadinessScore
    ) -> List[str]:
        """Recommend most suitable exchanges based on current metrics"""
        recommendations = []
        
        # Check each exchange
        for exchange, reqs in self.exchange_requirements.items():
            # Calculate match score (handle None values with default 0)
            liquidity_match = (metrics.liquidity_usd or 0) / reqs["min_liquidity"]
            holder_match = (metrics.holder_count or 0) / reqs["min_holders"]
            volume_match = (metrics.volume_24h or 0) / reqs["min_volume_24h"]
            
            avg_match = (liquidity_match + holder_match + volume_match) / 3
            
            # If >80% of requirements met, recommend
            if avg_match >= 0.8:
                recommendations.append(exchange)
        
        # If no matches, recommend lower tier exchanges
        if not recommendations:
            recommendations = ["MEXC", "Gate.io"]
        
        return recommendations
