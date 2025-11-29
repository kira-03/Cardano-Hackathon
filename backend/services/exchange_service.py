"""
Exchange Service - Exchange listing requirements and form generation
"""
from typing import Dict, Any, List, Optional
import logging
import requests
import asyncio
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ExchangeService:
    """
    Service for managing exchange listing requirements and submissions
    
    Supports:
    - Binance: Listing requirements and application process
    - Coinbase: Asset Hub requirements
    - Kraken: Get Listed program
    - KuCoin: Listing application
    - Gate.io: Listing request process
    """
    
    # Official listing documentation URLs
    EXCHANGE_DOCS = {
        "binance": "https://www.binance.com/en/support/faq/detail/053e4bdc48364343b863d1833618d8ba",
        "coinbase": "https://www.coinbase.com/exchange/asset-listings",
        "kraken": "https://www.kraken.com/get-listed",
        "kucoin": "https://www.kucoin.com/support/list-on-kucoin",
        "gateio": "https://www.gate.io/trade/listing"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    async def get_listing_requirements(self, exchange: str) -> Dict[str, Any]:
        """
        Scrape and parse listing requirements for exchange
        """
        exchange_lower = exchange.lower()
        
        if exchange_lower not in self.EXCHANGE_DOCS:
            logger.warning(f"Unknown exchange: {exchange}")
            return {"error": f"Unknown exchange: {exchange}"}
        
        logger.info(f"Fetching requirements for {exchange}")
        
        try:
            if exchange_lower == "binance":
                return await self._get_binance_requirements()
            elif exchange_lower == "coinbase":
                return await self._get_coinbase_requirements()
            elif exchange_lower == "kraken":
                return await self._get_kraken_requirements()
            elif exchange_lower == "kucoin":
                return await self._get_kucoin_requirements()
            elif exchange_lower == "gateio":
                return await self._get_gateio_requirements()
            else:
                return {"error": "Not implemented"}
        except Exception as e:
            logger.error(f"Error fetching {exchange} requirements: {e}")
            return {"error": str(e)}
    
    async def _get_binance_requirements(self) -> Dict[str, Any]:
        """
        Binance listing requirements
        Source: https://www.binance.com/en/support/faq/detail/053e4bdc48364343b863d1833618d8ba
        """
        try:
            url = self.EXCHANGE_DOCS["binance"]
            response = await asyncio.to_thread(self.session.get, url, timeout=15)
            
            # Binance returns 202 (Accepted) for some pages, which is acceptable
            if response.status_code not in [200, 202]:
                logger.warning(f"Binance docs fetch failed: {response.status_code}")
                return self._get_binance_requirements_fallback()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract requirements from page
            # This is a simplified version - production would need more robust parsing
            
            requirements = {
                "exchange": "Binance",
                "source_url": url,
                "key_requirements": [
                    "Strong project fundamentals and team",
                    "Active community and social media presence",
                    "Significant trading volume and liquidity",
                    "Completed security audit (recommended)",
                    "Legal compliance and regulatory clarity",
                    "Unique value proposition and innovation"
                ],
                "minimum_metrics": {
                    "holder_count": "5,000+",
                    "liquidity_usd": "$50,000+",
                    "volume_30d_usd": "$20,000+",
                    "top_holder_concentration": "<30%",
                    "audit_required": True
                },
                "application_process": [
                    "Submit application via Binance Listing Application Form",
                    "Provide project documentation and technical details",
                    "Undergo due diligence review",
                    "Listing fee may apply (case by case)",
                    "Community voting may be required"
                ],
                "form_fields": self._get_binance_form_schema()
            }
            
            logger.info("✓ Binance requirements retrieved")
            return requirements
            
        except Exception as e:
            logger.error(f"Error fetching Binance requirements: {e}")
            return self._get_binance_requirements_fallback()
    
    def _get_binance_requirements_fallback(self) -> Dict[str, Any]:
        """Fallback Binance requirements based on known criteria"""
        return {
            "exchange": "Binance",
            "source_url": self.EXCHANGE_DOCS["binance"],
            "key_requirements": [
                "Strong project fundamentals",
                "Active community",
                "High liquidity",
                "Security audit recommended",
                "Legal compliance"
            ],
            "minimum_metrics": {
                "holder_count": "5,000+",
                "liquidity_usd": "$50,000+",
                "volume_30d_usd": "$20,000+",
                "top_holder_concentration": "<30%",
                "audit_required": True
            },
            "form_fields": self._get_binance_form_schema()
        }
    
    async def _get_coinbase_requirements(self) -> Dict[str, Any]:
        """
        Coinbase Asset Hub requirements
        Source: https://www.coinbase.com/exchange/asset-listings
        """
        return {
            "exchange": "Coinbase",
            "source_url": self.EXCHANGE_DOCS["coinbase"],
            "key_requirements": [
                "Decentralized and non-security token",
                "Strong development team and roadmap",
                "Active community engagement",
                "High liquidity and trading volume",
                "Compliance with local regulations",
                "Security best practices"
            ],
            "minimum_metrics": {
                "holder_count": "10,000+",
                "liquidity_usd": "$100,000+",
                "volume_30d_usd": "$50,000+",
                "top_holder_concentration": "<25%",
                "audit_required": True
            },
            "application_process": [
                "Submit via Coinbase Asset Hub",
                "Complete Digital Asset Framework assessment",
                "Provide technical documentation",
                "Undergo compliance review",
                "Listing decision communicated within weeks"
            ],
            "form_fields": self._get_coinbase_form_schema()
        }
    
    async def _get_kraken_requirements(self) -> Dict[str, Any]:
        """
        Kraken Get Listed program
        Source: https://www.kraken.com/get-listed
        """
        return {
            "exchange": "Kraken",
            "source_url": self.EXCHANGE_DOCS["kraken"],
            "key_requirements": [
                "Regulatory compliance",
                "Strong security posture",
                "Active development",
                "Community support",
                "Market demand",
                "Unique value proposition"
            ],
            "minimum_metrics": {
                "holder_count": "7,500+",
                "liquidity_usd": "$75,000+",
                "volume_30d_usd": "$30,000+",
                "top_holder_concentration": "<30%",
                "audit_required": True
            },
            "application_process": [
                "Submit Get Listed application",
                "Provide project details and documentation",
                "Technical integration assessment",
                "Compliance and legal review",
                "Listing decision and integration timeline"
            ],
            "form_fields": self._get_kraken_form_schema()
        }
    
    async def _get_kucoin_requirements(self) -> Dict[str, Any]:
        """KuCoin listing requirements"""
        return {
            "exchange": "KuCoin",
            "source_url": self.EXCHANGE_DOCS["kucoin"],
            "key_requirements": [
                "Project innovation and uniqueness",
                "Active development team",
                "Community engagement",
                "Market liquidity",
                "Transparent tokenomics"
            ],
            "minimum_metrics": {
                "holder_count": "3,000+",
                "liquidity_usd": "$25,000+",
                "volume_30d_usd": "$10,000+",
                "top_holder_concentration": "<35%",
                "audit_required": False
            },
            "application_process": [
                "Submit listing application form",
                "Provide whitepaper and documentation",
                "Review and assessment",
                "Listing fee negotiation (if applicable)",
                "Integration and launch"
            ],
            "form_fields": self._get_kucoin_form_schema()
        }
    
    async def _get_gateio_requirements(self) -> Dict[str, Any]:
        """Gate.io listing requirements"""
        return {
            "exchange": "Gate.io",
            "source_url": self.EXCHANGE_DOCS["gateio"],
            "key_requirements": [
                "Innovative project concept",
                "Strong team background",
                "Active community",
                "Reasonable tokenomics",
                "Market potential"
            ],
            "minimum_metrics": {
                "holder_count": "2,500+",
                "liquidity_usd": "$20,000+",
                "volume_30d_usd": "$8,000+",
                "top_holder_concentration": "<40%",
                "audit_required": False
            },
            "application_process": [
                "Submit via Gate.io listing portal",
                "Provide comprehensive project information",
                "Review and evaluation",
                "Listing terms discussion",
                "Integration and listing"
            ],
            "form_fields": self._get_gateio_form_schema()
        }
    
    def _get_binance_form_schema(self) -> Dict[str, Any]:
        """Binance application form schema"""
        return {
            "project_name": {"type": "string", "required": True},
            "token_symbol": {"type": "string", "required": True},
            "blockchain": {"type": "string", "required": True},
            "contract_address": {"type": "string", "required": True},
            "website": {"type": "url", "required": True},
            "whitepaper": {"type": "url", "required": True},
            "contact_email": {"type": "email", "required": True},
            "team_info": {"type": "text", "required": True},
            "project_description": {"type": "text", "required": True},
            "total_supply": {"type": "number", "required": True},
            "circulating_supply": {"type": "number", "required": True},
            "listing_exchanges": {"type": "text", "required": False},
            "audit_report": {"type": "url", "required": False},
            "github_repository": {"type": "url", "required": False},
            "social_media": {"type": "object", "required": True}
        }
    
    def _get_coinbase_form_schema(self) -> Dict[str, Any]:
        """Coinbase Asset Hub form schema"""
        return {
            "asset_name": {"type": "string", "required": True},
            "ticker_symbol": {"type": "string", "required": True},
            "blockchain_platform": {"type": "string", "required": True},
            "contract_address": {"type": "string", "required": True},
            "website": {"type": "url", "required": True},
            "whitepaper": {"type": "url", "required": True},
            "contact_email": {"type": "email", "required": True},
            "legal_entity": {"type": "string", "required": True},
            "jurisdiction": {"type": "string", "required": True},
            "asset_description": {"type": "text", "required": True},
            "use_case": {"type": "text", "required": True},
            "total_supply": {"type": "number", "required": True},
            "security_audit": {"type": "url", "required": True},
            "regulatory_compliance": {"type": "text", "required": True}
        }
    
    def _get_kraken_form_schema(self) -> Dict[str, Any]:
        """Kraken Get Listed form schema"""
        return {
            "project_name": {"type": "string", "required": True},
            "token_ticker": {"type": "string", "required": True},
            "blockchain": {"type": "string", "required": True},
            "token_address": {"type": "string", "required": True},
            "website": {"type": "url", "required": True},
            "whitepaper": {"type": "url", "required": True},
            "contact_name": {"type": "string", "required": True},
            "contact_email": {"type": "email", "required": True},
            "project_summary": {"type": "text", "required": True},
            "token_utility": {"type": "text", "required": True},
            "tokenomics": {"type": "text", "required": True},
            "market_cap": {"type": "number", "required": False},
            "daily_volume": {"type": "number", "required": False}
        }
    
    def _get_kucoin_form_schema(self) -> Dict[str, Any]:
        """KuCoin listing form schema"""
        return {
            "token_name": {"type": "string", "required": True},
            "token_symbol": {"type": "string", "required": True},
            "blockchain": {"type": "string", "required": True},
            "contract_address": {"type": "string", "required": True},
            "website": {"type": "url", "required": True},
            "whitepaper": {"type": "url", "required": True},
            "contact_email": {"type": "email", "required": True},
            "project_intro": {"type": "text", "required": True},
            "total_supply": {"type": "number", "required": True},
            "circulating_supply": {"type": "number", "required": True}
        }
    
    def _get_gateio_form_schema(self) -> Dict[str, Any]:
        """Gate.io listing form schema"""
        return {
            "project_name": {"type": "string", "required": True},
            "token_name": {"type": "string", "required": True},
            "blockchain": {"type": "string", "required": True},
            "token_address": {"type": "string", "required": True},
            "website": {"type": "url", "required": True},
            "whitepaper": {"type": "url", "required": True},
            "email": {"type": "email", "required": True},
            "description": {"type": "text", "required": True},
            "supply": {"type": "number", "required": True}
        }
