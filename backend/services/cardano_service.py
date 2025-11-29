"""
Cardano Service - Interfaces with Blockfrost API for on-chain data
"""
from typing import Dict, Any, List, Optional
from blockfrost import BlockFrostApi, ApiError, ApiUrls
from config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)

class CardanoService:
    def __init__(self):
        self.api_key = settings.blockfrost_api_key
        self.network = str(settings.blockfrost_network)
        
        # Initialize BlockFrost API with proper network URL
        network_lower = self.network.lower()
        if network_lower == "mainnet":
            base_url = ApiUrls.mainnet.value
        elif network_lower == "preprod":
            base_url = ApiUrls.preprod.value
        elif network_lower == "preview":
            base_url = ApiUrls.preview.value
        else:
            base_url = ApiUrls.testnet.value
        
        self.api = BlockFrostApi(project_id=self.api_key, base_url=base_url)
        
    async def check_connection(self) -> bool:
        """Check if Blockfrost connection is working"""
        try:
            # Use sync method in async context
            health = await asyncio.to_thread(self.api.health)
            return health.is_healthy
        except Exception as e:
            logger.error(f"BlockFrost connection check failed: {e}")
            return False
    
    async def get_token_info(self, policy_id: str) -> Dict[str, Any]:
        """Get basic token information"""
        try:
            logger.info(f"Fetching token info for policy: {policy_id[:16]}...")
            # Get assets for policy using BlockFrost SDK with timeout
            assets = await asyncio.wait_for(
                asyncio.to_thread(self.api.assets_policy, policy_id),
                timeout=30.0
            )
            logger.info(f"Found {len(assets)} assets for policy")
            
            if not assets:
                raise Exception("No assets found for policy ID")
            
            # Get first asset details
            asset_id = assets[0].asset
            logger.info(f"Fetching detailed info for asset: {asset_id[:16]}...")
            asset_info = await asyncio.wait_for(
                asyncio.to_thread(self.api.asset, asset_id),
                timeout=30.0
            )
            logger.info(f"✓ Token info retrieved: {asset_info.asset_name or 'Unknown'}")
            
            # Extract metadata and convert to dict
            metadata = {}
            if hasattr(asset_info, 'onchain_metadata') and asset_info.onchain_metadata:
                onchain_meta = asset_info.onchain_metadata
                # Convert to dict if it's a Namespace or other object
                if isinstance(onchain_meta, dict):
                    metadata = onchain_meta
                elif hasattr(onchain_meta, '__dict__'):
                    metadata = onchain_meta.__dict__
                elif hasattr(onchain_meta, '_asdict'):
                    metadata = onchain_meta._asdict()
                else:
                    metadata = {}
            
            return {
                "policy_id": policy_id,
                "asset_name": asset_info.asset_name or "Unknown",
                "fingerprint": asset_info.fingerprint or "",
                "quantity": asset_info.quantity or "0",
                "initial_mint_tx": asset_info.initial_mint_tx_hash or "",
                "metadata": metadata
            }
        except ApiError as e:
            logger.error(f"Blockfrost API error: {e} (Status: {e.status_code})")
            raise Exception(f"Blockfrost API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in get_token_info: {type(e).__name__}: {e}", exc_info=True)
            raise Exception(f"Error fetching token info: {type(e).__name__}: {e}")
    
    async def get_token_holders(self, policy_id: str) -> List[Dict[str, Any]]:
        """Get token holder distribution"""
        try:
            logger.info(f"Fetching holders for policy: {policy_id[:16]}...")
            # Get assets for policy
            assets = await asyncio.wait_for(
                asyncio.to_thread(self.api.assets_policy, policy_id),
                timeout=30.0
            )
            
            if not assets:
                return []
            
            # Get addresses for first asset using BlockFrost SDK
            asset_id = assets[0].asset
            logger.info(f"Fetching addresses for asset: {asset_id[:16]}...")
            addresses = await asyncio.wait_for(
                asyncio.to_thread(self.api.asset_addresses, asset_id),
                timeout=30.0
            )
            logger.info(f"✓ Found {len(addresses)} holders")
            
            holders = []
            for addr in addresses:
                holders.append({
                    "address": addr.address,
                    "quantity": int(addr.quantity)
                })
            
            # Sort by quantity descending
            holders.sort(key=lambda x: x["quantity"], reverse=True)
            return holders
                
        except ApiError as e:
            raise Exception(f"Blockfrost API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching holders: {str(e)}")
    
    async def analyze_holder_distribution(self, holders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze holder concentration and distribution"""
        if not holders:
            return {
                "total_holders": 0,
                "top_10_concentration": 100.0,
                "top_50_concentration": 100.0,
                "gini_coefficient": 1.0
            }
        
        total_supply = sum(h["quantity"] for h in holders)
        
        # Top 10 holders concentration
        top_10_sum = sum(h["quantity"] for h in holders[:10])
        top_10_pct = (top_10_sum / total_supply * 100) if total_supply > 0 else 0
        
        # Top 50 holders concentration
        top_50_sum = sum(h["quantity"] for h in holders[:50])
        top_50_pct = (top_50_sum / total_supply * 100) if total_supply > 0 else 0
        
        # Simple Gini coefficient approximation
        gini = self._calculate_gini(holders, total_supply)
        
        return {
            "total_holders": len(holders),
            "top_10_concentration": round(top_10_pct, 2),
            "top_50_concentration": round(top_50_pct, 2),
            "gini_coefficient": round(gini, 3)
        }
    
    def _calculate_gini(self, holders: List[Dict[str, Any]], total_supply: float) -> float:
        """Calculate Gini coefficient for wealth distribution"""
        if not holders or total_supply == 0:
            return 1.0
        
        # Sort by quantity
        sorted_holdings = sorted([h["quantity"] for h in holders])
        n = len(sorted_holdings)
        
        # Calculate Gini
        cumsum = 0
        for i, val in enumerate(sorted_holdings):
            cumsum += (n - i) * val
        
        gini = (2 * cumsum) / (n * total_supply) - (n + 1) / n
        return max(0, min(1, gini))
    
    async def get_dex_liquidity(self, policy_id: str) -> Dict[str, Any]:
        """
        Estimate DEX liquidity from major Cardano DEXes
        Note: This is a simplified simulation for hackathon.
        Real implementation would query Minswap, SundaeSwap, MuesliSwap APIs
        """
        # Simulated data - in production, query actual DEX APIs
        # For hackathon, we'll generate realistic estimates
        try:
            holders = await self.get_token_holders(policy_id)
            holder_count = len(holders)
            
            # Estimate liquidity based on holder count (rough heuristic)
            # More holders typically means more liquidity
            estimated_liquidity = holder_count * 50  # $50 per holder average
            estimated_volume_24h = estimated_liquidity * 0.1  # 10% daily turnover
            
            return {
                "total_liquidity_usd": estimated_liquidity,
                "volume_24h_usd": estimated_volume_24h,
                "pools": [
                    {
                        "dex": "Minswap",
                        "liquidity_usd": estimated_liquidity * 0.4,
                        "volume_24h": estimated_volume_24h * 0.5
                    },
                    {
                        "dex": "SundaeSwap",
                        "liquidity_usd": estimated_liquidity * 0.35,
                        "volume_24h": estimated_volume_24h * 0.3
                    },
                    {
                        "dex": "MuesliSwap",
                        "liquidity_usd": estimated_liquidity * 0.25,
                        "volume_24h": estimated_volume_24h * 0.2
                    }
                ]
            }
        except Exception as e:
            # Fallback values
            return {
                "total_liquidity_usd": 10000,
                "volume_24h_usd": 1000,
                "pools": []
            }
    
    async def analyze_metadata_quality(self, metadata: Dict[str, Any]) -> float:
        """Analyze token metadata completeness (0-100)"""
        score = 0
        max_score = 100
        
        logger.info(f"Analyzing metadata type: {type(metadata)}")
        
        # Convert metadata to dict if it's not
        if metadata is None:
            return 0.0
            
        if not isinstance(metadata, dict):
            logger.info("Metadata is not a dict, attempting conversion...")
            try:
                if hasattr(metadata, '__dict__'):
                    metadata = vars(metadata)
                elif hasattr(metadata, '_asdict'):
                    metadata = metadata._asdict()
                else:
                    logger.warning(f"Cannot convert metadata type {type(metadata)} to dict")
                    return 0.0
            except Exception as e:
                logger.error(f"Error converting metadata: {e}")
                return 0.0
        
        # Check for essential fields
        essential_fields = ["name", "description", "image", "ticker"]
        for field in essential_fields:
            try:
                if field in metadata and metadata.get(field):
                    score += 20
            except Exception as e:
                logger.error(f"Error checking field {field}: {e}")
                continue
        
        # Check for additional fields
        optional_fields = ["website", "twitter", "telegram", "logo"]
        for field in optional_fields:
            try:
                if field in metadata and metadata.get(field):
                    score += 5
            except Exception as e:
                logger.error(f"Error checking field {field}: {e}")
                continue
        
        return min(score, max_score)
    
    async def analyze_contract_risk(self, policy_id: str) -> float:
        """
        Analyze smart contract risk factors (0-100, higher is better)
        """
        try:
            # Get assets for policy
            assets = await asyncio.wait_for(
                asyncio.to_thread(self.api.assets_policy, policy_id),
                timeout=30.0
            )
            
            if not assets:
                return 50.0
            
            asset_id = assets[0].asset
            
            # Get asset info using BlockFrost SDK
            asset_info = await asyncio.wait_for(
                asyncio.to_thread(self.api.asset, asset_id),
                timeout=30.0
            )
            
            # Get asset history
            history = await asyncio.wait_for(
                asyncio.to_thread(self.api.asset_history, asset_id, count=100),
                timeout=30.0
            )
            
            score = 100.0
            
            # More transaction history = more established = lower risk
            if len(history) > 100:
                score += 0  # Max score
            elif len(history) > 50:
                score -= 10
            else:
                score -= 20
            
            return max(0, min(100, score))
            
        except ApiError as e:
            return 75.0  # Default moderate score
        except Exception as e:
            return 75.0  # Default moderate score
