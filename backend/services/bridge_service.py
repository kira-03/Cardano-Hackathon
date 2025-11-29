"""
Bridge Service - Cross-chain bridge integrations (LiFi, Rango, Axelar)
"""
from typing import Dict, Any, List, Optional
import logging
import requests
import asyncio
import os

logger = logging.getLogger(__name__)


class BridgeService:
    """
    Service for simulating cross-chain bridge routes
    
    Integrations:
    - LiFi: Multi-chain bridge aggregator
    - Axelar: ITS (Interchain Token Service)
    """
    
    def __init__(self):
        # Official API endpoints
        self.lifi_base = "https://li.quest/v1"  # Correct quote endpoint
        self.axelar_base = "https://api.axelarscan.io"
    
    async def get_bridge_routes(
        self,
        source_chain: str,
        target_chains: List[str],
        token_policy_id: str
    ) -> Dict[str, Any]:
        """
        Get bridge routes from Cardano to target chains
        """
        logger.info(f"Fetching bridge routes: {source_chain} -> {target_chains}")
        
        results = {
            "source_chain": source_chain,
            "target_chains": target_chains,
            "routes": [],
            "providers": {}
        }
        
        # Check each target chain
        for target_chain in target_chains:
            if target_chain.lower() == "cardano":
                continue  # Skip same-chain
            
            # Try LiFi
            lifi_routes = await self._get_lifi_routes(source_chain, target_chain, token_policy_id)
            if lifi_routes:
                results["routes"].extend(lifi_routes)
                results["providers"]["lifi"] = {"status": "success", "routes": len(lifi_routes)}
            
            # Try Axelar
            axelar_routes = await self._get_axelar_routes(source_chain, target_chain, token_policy_id)
            if axelar_routes:
                results["routes"].extend(axelar_routes)
                results["providers"]["axelar"] = {"status": "success", "routes": len(axelar_routes)}
        
        # Sort routes by cost + time
        results["routes"].sort(key=lambda r: r.get("total_cost_usd", 999999))
        
        logger.info(f"✓ Found {len(results['routes'])} bridge routes")
        return results
    
    async def _get_lifi_routes(
        self,
        source_chain: str,
        target_chain: str,
        token_policy_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get routes from LiFi API
        Docs: https://li.fi/docs
        """
        try:
            logger.info(f"  → Querying LiFi for {source_chain} -> {target_chain}")
            
            # LiFi quote endpoint: https://li.quest/v1/quote
            # Docs: https://docs.li.fi
            quote_url = f"{self.lifi_base}/quote"
            headers = {
                "Accept": "application/json",
                "User-Agent": "EcosystemBridgeAssistant/1.0"
            }
            
            params = {
                "fromChain": source_chain,
                "toChain": target_chain,
                "fromToken": token_policy_id,
                "toToken": "0x0000000000000000000000000000000000000000",  # Native token
                "fromAmount": "1000000000",  # 1B units for estimation
                "fromAddress": "0x0000000000000000000000000000000000000000",  # Placeholder
                "toAddress": "0x0000000000000000000000000000000000000000"  # Placeholder
            }
            
            quote_response = await asyncio.to_thread(
                requests.get, quote_url, params=params, headers=headers, timeout=10
            )
            
            if quote_response.status_code == 404:
                logger.info("  ✓ LiFi: Cardano not yet supported")
                return []
            
            if quote_response.status_code != 200:
                logger.info(f"  ✓ LiFi: No routes available (status {quote_response.status_code})")
                return []
            
            quote = quote_response.json()
            
            # Parse route from quote response
            route = {
                "provider": "LiFi",
                "source_chain": source_chain,
                "target_chain": target_chain,
                "bridge_name": quote.get("tool", "Unknown"),
                "estimated_fee_usd": float(quote.get("estimate", {}).get("gasCosts", [{}])[0].get("amountUSD", 0)),
                "estimated_time_minutes": float(quote.get("estimate", {}).get("executionDuration", 0)) / 60,
                "trust_model": "aggregated",
                "hops": len(quote.get("includedSteps", [])),
                "security_score": self._calculate_security_score("lifi", quote)
            }
            
            logger.info(f"  ✓ LiFi: Found route via {route['bridge_name']}")
            return [route]
            
        except Exception as e:
            logger.info(f"  ✓ LiFi unavailable: {e}")
            return []
    
    async def _get_rango_routes(
        self,
        source_chain: str,
        target_chain: str,
        token_policy_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get routes from Rango API
        Docs: https://api-docs.rango.exchange/
        """
        try:
            logger.info(f"  → Querying Rango for {source_chain} -> {target_chain}")
            
            # Check if API key is available
            if not self.rango_api_key:
                logger.info("  ✓ Rango: API key not configured (set RANGO_API_KEY env var)")
                return []
            
            # Get metadata with API key (header: x-api-key per docs)
            # Docs: https://docs.rango.exchange
            meta_url = f"{self.rango_base}/basic/meta"
            headers = {
                "x-api-key": self.rango_api_key,
                "Accept": "application/json",
                "User-Agent": "EcosystemBridgeAssistant/1.0"
            }
            
            meta_response = await asyncio.to_thread(
                requests.get, meta_url, headers=headers, timeout=10
            )
            
            if meta_response.status_code == 401:
                logger.info("  ✓ Rango: Invalid API key (get key from https://rango.exchange)")
                return []
            
            if meta_response.status_code != 200:
                logger.info(f"  ✓ Rango API unavailable (status {meta_response.status_code})")
                return []
            
            meta = meta_response.json()
            blockchains = meta.get("blockchains", [])
            
            # Check Cardano support
            cardano_chain = next(
                (b for b in blockchains if "cardano" in b.get("name", "").lower() or b.get("name", "") == "ADA"),
                None
            )
            
            if not cardano_chain:
                logger.info("  ✓ Rango: Cardano not yet supported")
                return []
            
            # Get route quote
            route_url = f"{self.rango_base}/basic/quote"
            params = {
                "from": f"CARDANO.{token_policy_id}",
                "to": f"{target_chain.upper()}.NATIVE",
                "amount": "1000000000"
            }
            
            route_response = await asyncio.to_thread(
                requests.get, route_url, params=params, headers=headers, timeout=10
            )
            
            if route_response.status_code != 200:
                logger.info("  ✓ Rango: No routes available for this token")
                return []
            
            route_data = route_response.json()
            
            # Parse route from response
            route = {
                "provider": "Rango",
                "source_chain": source_chain,
                "target_chain": target_chain,
                "bridge_name": route_data.get("result", {}).get("swapper", {}).get("title", "Unknown"),
                "estimated_fee_usd": float(route_data.get("result", {}).get("fee", {}).get("totalFee", 0)),
                "estimated_time_minutes": float(route_data.get("result", {}).get("estimatedTimeInSeconds", 0)) / 60,
                "trust_model": "trustless",
                "hops": len(route_data.get("result", {}).get("path", [])),
                "security_score": self._calculate_security_score("rango", route_data)
            }
            
            logger.info(f"  ✓ Rango: Found route via {route['bridge_name']}")
            return [route]
            
        except Exception as e:
            logger.info(f"  ✓ Rango unavailable: {e}")
            return []
    
    async def _get_axelar_routes(
        self,
        source_chain: str,
        target_chain: str,
        token_policy_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get routes from Axelar ITS
        Docs: https://axelar.network/
        """
        try:
            logger.info(f"  → Querying Axelar for {source_chain} -> {target_chain}")
            
            # Axelar currently doesn't have direct Cardano support
            # This is a placeholder for future integration
            
            logger.info("  ✓ Axelar: Cardano integration pending")
            return []
            
        except Exception as e:
            logger.error(f"Axelar API error: {e}")
            return []
    
    def _calculate_security_score(self, provider: str, route_data: Dict[str, Any]) -> float:
        """
        Calculate security score for bridge route (0-100)
        """
        # Base scores by provider
        base_scores = {
            "lifi": 85,  # Aggregator with multiple bridges
            "rango": 80,  # Multi-bridge platform
            "axelar": 90  # Trusted validator network
        }
        
        score = base_scores.get(provider, 70)
        
        # Adjust based on hops (fewer is better)
        hops = route_data.get("hops", 1) if isinstance(route_data, dict) else 1
        if hops > 3:
            score -= 10
        elif hops > 1:
            score -= 5
        
        return max(0, min(100, score))
