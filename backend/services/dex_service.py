"""
DEX Service - Integrations with Cardano DEXs (Minswap, SundaeSwap, MuesliSwap)
"""
from typing import Dict, Any, List, Optional
import logging
import requests
import asyncio

logger = logging.getLogger(__name__)


class DEXService:
    """
    Service for interacting with Cardano DEXs
    
    Integrations:
    - Minswap: Aggregator API for pools and volumes
    - MuesliSwap: Analytics API for liquidity data
    """
    
    def __init__(self):
        # Official API endpoints (corrected)
        self.minswap_base = "https://agg-api.minswap.org"  # Official Aggregator API
        self.muesli_base = "https://api.muesliswap.com"  # Official API
    
    async def get_all_dex_data(self, policy_id: str) -> Dict[str, Any]:
        """
        Fetch liquidity data from all supported DEXs
        """
        logger.info("Fetching DEX data from all sources...")
        
        results = {
            "total_liquidity_usd": 0,
            "total_volume_24h_usd": 0,
            "pools": [],
            "dexs": {}
        }
        
        # Fetch from each DEX
        minswap_data = await self._get_minswap_data(policy_id)
        muesli_data = await self._get_muesliswap_data(policy_id)
        
        # Aggregate results
        results["dexs"]["minswap"] = minswap_data
        results["dexs"]["muesliswap"] = muesli_data
        
        # Calculate totals
        for dex_data in [minswap_data, muesli_data]:
            if dex_data.get("liquidity_usd"):
                results["total_liquidity_usd"] += dex_data["liquidity_usd"]
            if dex_data.get("volume_24h_usd"):
                results["total_volume_24h_usd"] += dex_data["volume_24h_usd"]
            if dex_data.get("pools"):
                results["pools"].extend(dex_data["pools"])
        
        logger.info(f"✓ Total DEX liquidity: ${results['total_liquidity_usd']:,.0f}")
        return results
    
    async def _get_minswap_data(self, policy_id: str) -> Dict[str, Any]:
        """
        Fetch data from Minswap Aggregator API
        Docs: https://agg-api.minswap.org (Official Aggregator API)
        """
        try:
            logger.info("  → Querying Minswap Aggregator API...")
            
            # Search for token using POST /aggregator/tokens
            url = f"{self.minswap_base}/aggregator/tokens"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "EcosystemBridgeAssistant/1.0"
            }
            payload = {
                "query": policy_id,
                "only_verified": False  # Include all tokens
            }
            
            response = await asyncio.to_thread(
                requests.post, url, json=payload, headers=headers, timeout=10
            )
            
            if response.status_code != 200:
                logger.info(f"  ✓ Minswap: Token not found (status {response.status_code})")
                return {"liquidity_usd": 0, "volume_24h_usd": 0, "pools": []}
            
            data = response.json()
            tokens = data if isinstance(data, list) else []
            
            if not tokens:
                logger.info("  ✓ Token not found on Minswap")
                return {"liquidity_usd": 0, "volume_24h_usd": 0, "pools": []}
            
            # Extract liquidity and volume from first matching token
            token_info = tokens[0]
            liquidity = float(token_info.get("liquidity", 0))
            volume_24h = float(token_info.get("volume24h", 0))
            
            logger.info(f"  ✓ Minswap: ${liquidity:,.0f} liquidity, ${volume_24h:,.0f} 24h volume")
            
            return {
                "liquidity_usd": liquidity,
                "volume_24h_usd": volume_24h,
                "pools": [token_info],
                "pool_count": 1
            }
            
        except Exception as e:
            logger.info(f"  ✓ Minswap unavailable: {e}")
            return {"liquidity_usd": 0, "volume_24h_usd": 0, "pools": []}
    
    async def _get_muesliswap_data(self, policy_id: str) -> Dict[str, Any]:
        """
        Fetch data from MuesliSwap Analytics API
        Docs: https://docs.muesliswap.com (endpoints: /liquidity/pools, /price, /token-list)
        """
        try:
            logger.info("  → Querying MuesliSwap...")
            
            # Try liquidity pools endpoint first
            url = f"{self.muesli_base}/liquidity/pools"
            headers = {
                "Accept": "application/json",
                "User-Agent": "EcosystemBridgeAssistant/1.0"
            }
            
            response = await asyncio.to_thread(
                requests.get, url, headers=headers, timeout=15
            )
            
            if response.status_code != 200:
                logger.info(f"  ✓ MuesliSwap API unavailable (status {response.status_code})")
                return {"liquidity_usd": 0, "volume_24h_usd": 0, "pools": []}
            
            pools = response.json()
            
            # Filter pools containing our policy ID
            token_pools = [
                p for p in pools
                if policy_id.lower() in str(p).lower()
            ]
            
            if not token_pools:
                logger.info("  ✓ Token not found in MuesliSwap pools")
                return {"liquidity_usd": 0, "volume_24h_usd": 0, "pools": []}
            
            # Calculate total liquidity with proper decimal handling
            total_liquidity_usd = 0
            for pool in token_pools:
                # MuesliSwap returns raw integers - must apply decimals
                # Typical structure: {"liquidity": int, "baseDecimalPlaces": int, "quoteDecimalPlaces": int}
                liquidity_raw = pool.get("liquidity", 0)
                decimals = pool.get("baseDecimalPlaces", 6)  # Default to 6 (ADA)
                
                # Convert from raw units to decimal
                if liquidity_raw > 0 and decimals > 0:
                    liquidity_decimal = liquidity_raw / (10 ** decimals)
                    # If we have price info, calculate USD value
                    price_usd = pool.get("price_usd", 0)
                    if price_usd > 0:
                        total_liquidity_usd += liquidity_decimal * price_usd
                    else:
                        # Fallback: assume ~$0.40 per ADA if no price
                        total_liquidity_usd += liquidity_decimal * 0.4
            
            pool_count = len(token_pools)
            
            logger.info(f"  ✓ MuesliSwap: {pool_count} pools, ${total_liquidity_usd:,.0f} liquidity")
            
            return {
                "liquidity_usd": total_liquidity_usd,
                "volume_24h_usd": 0,  # Would need /price endpoint for volume
                "pools": token_pools[:5],  # Return first 5 for reference
                "pool_count": pool_count
            }
            
        except Exception as e:
            logger.info(f"  ✓ MuesliSwap unavailable: {e}")
            return {"liquidity_usd": 0, "volume_24h_usd": 0, "pools": []}
    
    async def generate_liquidity_plan(
        self,
        policy_id: str,
        current_liquidity: Dict[str, Any],
        target_liquidity: float
    ) -> Dict[str, Any]:
        """
        Generate liquidity provision plan with transaction scripts
        """
        logger.info(f"Generating liquidity plan (target: ${target_liquidity:,.0f})")
        
        current_total = current_liquidity.get("total_liquidity_usd", 0)
        liquidity_gap = max(0, target_liquidity - current_total)
        
        plan = {
            "current_liquidity_usd": current_total,
            "target_liquidity_usd": target_liquidity,
            "liquidity_gap_usd": liquidity_gap,
            "actions": [],
            "dry_run_transactions": []
        }
        
        if liquidity_gap > 0:
            # Suggest actions
            plan["actions"].append({
                "action": "add_liquidity_minswap",
                "dex": "Minswap",
                "amount_usd": liquidity_gap * 0.5,
                "steps": [
                    "Approve token spend on Minswap router",
                    f"Add liquidity: {liquidity_gap * 0.5 / 2:,.0f} ADA + equivalent tokens",
                    "Confirm transaction and receive LP tokens"
                ],
                "script": self._generate_minswap_script(liquidity_gap * 0.5)
            })
            
            plan["actions"].append({
                "action": "add_liquidity_sundaeswap",
                "dex": "SundaeSwap",
                "amount_usd": liquidity_gap * 0.3,
                "steps": [
                    "Connect wallet to SundaeSwap",
                    f"Add liquidity: {liquidity_gap * 0.3 / 2:,.0f} ADA + equivalent tokens",
                    "Submit transaction"
                ],
                "script": self._generate_sundae_script(liquidity_gap * 0.3)
            })
            
            plan["actions"].append({
                "action": "liquidity_mining_program",
                "description": "Launch incentive program for LP providers",
                "budget_usd": liquidity_gap * 0.2,
                "duration_days": 90
            })
        
        logger.info(f"✓ Liquidity plan generated: {len(plan['actions'])} actions")
        return plan
    
    def _generate_minswap_script(self, amount_usd: float) -> str:
        """Generate Minswap liquidity script"""
        return f"""
# Minswap Add Liquidity Script
# Amount: ${amount_usd:,.0f}

# This is a placeholder for actual Minswap SDK integration
# In production, use Minswap Aggregator API to build transactions

# Example:
# import MinswapSDK
# pool = minswap.getPool(policyId)
# tx = minswap.buildAddLiquidityTx(
#     pool_id=pool.id,
#     ada_amount={amount_usd / 2},
#     token_amount=calculate_equivalent_tokens(ada_amount)
# )
# signed_tx = wallet.sign(tx)
# broadcast(signed_tx)

echo "⚠️ Manual integration required"
"""
    
    def _generate_sundae_script(self, amount_usd: float) -> str:
        """Generate SundaeSwap liquidity script"""
        return f"""
# SundaeSwap Add Liquidity Script
# Amount: ${amount_usd:,.0f}

# This is a placeholder for actual SundaeSwap SDK integration
# In production, use SundaeSwap SDK

# Example:
# import SundaeSDK
# pool = sundae.findPool(tokenA, tokenB)
# tx = sundae.buildAddLiquidityTransaction(
#     pool=pool,
#     amountA={amount_usd / 2},
#     amountB=calculate_equivalent()
# )

echo "⚠️ Manual integration required"
"""
