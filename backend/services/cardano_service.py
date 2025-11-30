"""
Cardano Service - Interfaces with Blockfrost API for on-chain data
"""
import os
from typing import Dict, Any, List, Optional
from blockfrost import BlockFrostApi, ApiError, ApiUrls
from config import settings
import asyncio
import logging
import time
import requests

logger = logging.getLogger(__name__)

class CardanoService:
    def __init__(self):
        self.api_key = settings.blockfrost_api_key
        self.network = str(settings.blockfrost_network)
        
        # Initialize BlockFrost API with proper network URL and timeout
        network_lower = self.network.lower()
        if network_lower == "mainnet":
            base_url = ApiUrls.mainnet.value
        elif network_lower == "preprod":
            base_url = ApiUrls.preprod.value
        elif network_lower == "preview":
            base_url = ApiUrls.preview.value
        else:
            base_url = ApiUrls.testnet.value
        
        # Create API client and configure timeout on its internal session
        self.api = BlockFrostApi(
            project_id=self.api_key, 
            base_url=base_url
        )
        
        # Set no timeout on the BlockFrost API's internal session
        # The SDK uses requests.Session internally
        if hasattr(self.api, 'session'):
            # Monkey-patch the request method to remove timeout limits
            original_request = self.api.session.request
            def request_with_timeout(*args, **kwargs):
                kwargs.setdefault('timeout', None)  # No timeout, no retry
                return original_request(*args, **kwargs)
            self.api.session.request = request_with_timeout
            
            logger.info(f"✅ BlockFrost API session configured with no timeout")
    
    async def check_connection(self) -> bool:
        """Check if Blockfrost connection is working"""
        try:
            # Allow bypassing the health check for local development or when
            # a valid Blockfrost key is not available. Set environment
            # variable `SKIP_BLOCKFROST_CHECK=1` to skip the check.
            if str(getattr(settings, 'skip_blockfrost_check', False)).lower() in ('1', 'true', 'yes') or os.getenv('SKIP_BLOCKFROST_CHECK') in ('1', 'true', 'yes'):
                logger.warning("SKIP_BLOCKFROST_CHECK enabled - skipping BlockFrost health check")
                return False

            # Use sync method in async context
            health = await asyncio.to_thread(self.api.health)
            return health.is_healthy
        except Exception as e:
            # If Blockfrost returns HTTP 403 it usually means the project
            # key is invalid, disabled, or the request is forbidden by the
            # Blockfrost account configuration. Log a helpful hint.
            try:
                # ApiError from SDK exposes status_code and message
                if hasattr(e, 'status_code') and getattr(e, 'status_code') == 403:
                    logger.error("BlockFrost connection check failed: 403 Forbidden - check your BlockFrost API key, project status, and network (mainnet/preview).")
                    logger.error("Hint: set a valid key in backend/.env as BLOCKFROST_API_KEY or export environment variable BLOCKFROST_API_KEY.")
                else:
                    logger.error(f"BlockFrost connection check failed: {e}")
            except Exception:
                logger.error(f"BlockFrost connection check failed: {e}")
            return False
    
    async def get_token_info(self, policy_id: str) -> Dict[str, Any]:
        """Get basic token information"""
        try:
            logger.info(f"Fetching token info for policy: {policy_id[:16]}...")
            
            # Get assets for policy - direct call without timeout
            assets = await asyncio.to_thread(self.api.assets_policy, policy_id)
            logger.info(f"Found {len(assets)} assets for policy")
            
            if not assets:
                raise Exception("No assets found for policy ID")
            
            # Get first asset details - direct call without timeout
            asset_id = assets[0].asset
            logger.info(f"Fetching detailed info for asset: {asset_id[:16]}...")
            asset_info = await asyncio.to_thread(self.api.asset, asset_id)
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
        """Get token holder count and top holders - uses HTTP header for total count"""
        try:
            logger.info(f"Fetching holders for policy: {policy_id[:16]}...")
            
            # Get assets for policy
            assets = await asyncio.to_thread(self.api.assets_policy, policy_id)
            
            if not assets:
                logger.warning("No assets found, returning empty holder list")
                return []
            
            asset_id = assets[0].asset
            
            # Use direct HTTP call to get total count from response headers
            network_lower = self.network.lower()
            if network_lower == "mainnet":
                base_url = "https://cardano-mainnet.blockfrost.io/api/v0"
            elif network_lower == "preprod":
                base_url = "https://cardano-preprod.blockfrost.io/api/v0"
            elif network_lower == "preview":
                base_url = "https://cardano-preview.blockfrost.io/api/v0"
            else:
                base_url = "https://cardano-testnet.blockfrost.io/api/v0"
            
            url = f"{base_url}/assets/{asset_id}/addresses"
            headers = {"project_id": self.api_key}
            params = {"page": 1, "count": 100, "order": "desc"}
            
            # Make request to get total count from headers
            resp = await asyncio.to_thread(
                requests.get,
                url,
                headers=headers,
                params=params,
                timeout=None
            )
            
            resp.raise_for_status()
            
            # Parse response for top holders
            addresses_data = resp.json()
            holders = []
            for addr in addresses_data:
                holders.append({
                    "address": addr.get("address", "unknown"),
                    "quantity": int(addr.get("quantity", 0))
                })
            
            logger.info(f"✓ Fetched top {len(holders)} holders for analysis")

            # Calculate total holders
            total_holders = 0
            
            # If first page is not full, that's the total
            if len(addresses_data) < 100:
                total_holders = len(addresses_data)
                logger.info(f"✅ Total unique holders: {total_holders}")
            else:
                # Binary search for the last page
                logger.info("First page full, starting binary search for total count...")
                
                def check_page_sync(page_num):
                    try:
                        r = requests.get(
                            url, 
                            headers=headers, 
                            params={"page": page_num, "count": 100, "order": "desc"},
                            timeout=None
                        )
                        if r.status_code != 200:
                            return []
                        return r.json()
                    except:
                        return []

                # Find upper bound
                low = 1
                high = 1000
                while True:
                    logger.debug(f"Checking upper bound page {high}...")
                    data = await asyncio.to_thread(check_page_sync, high)
                    if not data:
                        break
                    low = high
                    high *= 10
                    if high > 10000000: # Safety break
                        break
                
                # Binary search
                final_page_data = []
                while low <= high:
                    mid = (low + high) // 2
                    if mid == low:
                        # Check high one last time
                        data = await asyncio.to_thread(check_page_sync, high)
                        if data:
                            low = high
                            final_page_data = data
                        else:
                            # If high is empty, low is the answer (we need to fetch low if we don't have it)
                            if not final_page_data:
                                final_page_data = await asyncio.to_thread(check_page_sync, low)
                        break
                    
                    logger.debug(f"Binary search checking page {mid}...")
                    data = await asyncio.to_thread(check_page_sync, mid)
                    
                    if data:
                        low = mid
                        final_page_data = data # Store data to avoid refetching
                    else:
                        high = mid - 1
                
                # Calculate total
                # low is the last page number
                # final_page_data is the content of that page
                count_on_last_page = len(final_page_data)
                total_holders = (low - 1) * 100 + count_on_last_page
                logger.info(f"✅ Total unique holders found via binary search: {total_holders} (Pages: {low})")

            # Add metadata entry with actual total count
            if total_holders > len(holders):
                holders.append({
                    "address": "__TOTAL_HOLDERS__",
                    "quantity": 0,
                    "total_count": total_holders
                })
            
            return holders
                
        except Exception as e:
            logger.error(f"Unexpected error fetching holders: {e}")
            return []  # Return empty on any error
    
    async def analyze_holder_distribution(self, holders: List[Dict[str, Any]], total_supply: int = 0) -> Dict[str, Any]:
        """Analyze holder concentration and distribution"""
        if not holders:
            return {
                "total_holders": 0,
                "top_10_concentration": 100.0,
                "top_50_concentration": 100.0,
                "gini_coefficient": 1.0
            }
        
        # Check if we have total count metadata
        total_count = len(holders)
        for h in holders:
            if h.get("address") == "__TOTAL_HOLDERS__":
                total_count = h.get("total_count", len(holders))
                holders = [x for x in holders if x.get("address") != "__TOTAL_HOLDERS__"]
                break
        
        # Use provided total supply or calculate from visible holders (fallback)
        if total_supply <= 0:
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
            "total_holders": total_count,  # Use actual total count from metadata
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
        Get market data from external sources.
        
        BlockFrost provides on-chain data only. For market data (price, volume, liquidity),
        we use CoinPaprika API (free, no API key required).
        
        Data sources:
        - On-chain data: BlockFrost API
        - Market data: CoinPaprika API (https://api.coinpaprika.com)
        """
        # First, get the token info to find the asset ID
        try:
            token_info = await self.get_token_info(policy_id)
            # Get the readable name from metadata, not the hex asset_name
            metadata = token_info.get("metadata", {})
            token_name = metadata.get("name") or metadata.get("ticker") or token_info.get("asset_name", "")
            
            # Search CoinPaprika for this token
            market_data = await self._get_coinpaprika_data(policy_id, token_name)
            
            if market_data:
                logger.info(f"✅ Market data retrieved from CoinPaprika for {token_name}")
                return market_data
            else:
                logger.info(f"⚠️ Token {token_name} not found on CoinPaprika, market data unavailable")
                return self._empty_market_data()
                
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return self._empty_market_data()
    
    async def _get_coinpaprika_data(self, policy_id: str, asset_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch market data from CoinPaprika API.
        CoinPaprika is free and doesn't require an API key.
        """
        try:
            # Build the full asset ID (policy_id + hex-encoded asset name)
            asset_name_hex = asset_name.encode().hex().upper() if asset_name else ""
            full_asset_id = f"{policy_id}{asset_name_hex}".lower()
            
            # Search for the token on CoinPaprika
            search_url = f"https://api.coinpaprika.com/v1/search?q={asset_name}&c=currencies"
            search_response = requests.get(search_url, timeout=10)
            
            if search_response.status_code != 200:
                logger.warning(f"CoinPaprika search failed: {search_response.status_code}")
                return None
            
            search_data = search_response.json()
            currencies = search_data.get("currencies", [])
            
            # Find matching Cardano token by contract address
            token_id = None
            for currency in currencies:
                contracts = currency.get("contract_address", [])
                for contract in contracts:
                    addr = contract.get("address", "").lower()
                    # Match by policy_id or full asset ID
                    if policy_id.lower() in addr or full_asset_id in addr:
                        token_id = currency.get("id")
                        logger.info(f"Found CoinPaprika match: {token_id}")
                        break
                if token_id:
                    break
            
            if not token_id:
                # Try matching by name for Cardano tokens (suffix -crd)
                for currency in currencies:
                    if currency.get("id", "").endswith("-crd") and currency.get("is_active"):
                        token_id = currency.get("id")
                        logger.info(f"Found CoinPaprika match by name: {token_id}")
                        break
            
            if not token_id:
                return None
            
            # Get ticker data for the token
            ticker_url = f"https://api.coinpaprika.com/v1/tickers/{token_id}"
            ticker_response = requests.get(ticker_url, timeout=10)
            
            if ticker_response.status_code != 200:
                logger.warning(f"CoinPaprika ticker failed: {ticker_response.status_code}")
                return None
            
            ticker_data = ticker_response.json()
            quotes = ticker_data.get("quotes", {}).get("USD", {})
            
            # Calculate estimated liquidity from market cap and volume
            market_cap = quotes.get("market_cap", 0) or 0
            volume_24h = quotes.get("volume_24h", 0) or 0
            price = quotes.get("price", 0) or 0
            
            # Estimate liquidity as ~10% of market cap (typical for active tokens)
            # This is an approximation - real liquidity requires DEX pool data
            estimated_liquidity = market_cap * 0.1 if market_cap > 0 else volume_24h * 2
            
            return {
                "total_liquidity_usd": estimated_liquidity,
                "volume_24h_usd": volume_24h,
                "price_usd": price,
                "market_cap_usd": market_cap,
                "price_change_24h": quotes.get("percent_change_24h", 0),
                "price_change_7d": quotes.get("percent_change_7d", 0),
                "data_source": "CoinPaprika API",
                "coinpaprika_id": token_id,
                "rank": ticker_data.get("rank", 0),
                "last_updated": ticker_data.get("last_updated", ""),
                "pools": []  # Pool-specific data would require DEX APIs
            }
            
        except requests.exceptions.Timeout:
            logger.warning("CoinPaprika API timeout")
            return None
        except Exception as e:
            logger.error(f"CoinPaprika API error: {e}")
            return None
    
    def _empty_market_data(self) -> Dict[str, Any]:
        """Return empty market data when external APIs fail"""
        return {
            "total_liquidity_usd": None,
            "volume_24h_usd": None,
            "price_usd": None,
            "market_cap_usd": None,
            "data_source": "Not available - token not found on exchanges",
            "note": "For unlisted tokens, market data is unavailable",
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
            # Get assets for policy - direct call
            assets = await asyncio.to_thread(self.api.assets_policy, policy_id)
            
            if not assets:
                return 50.0
            
            asset_id = assets[0].asset
            
            # Get asset info - direct call
            asset_info = await asyncio.to_thread(self.api.asset, asset_id)
            
            # Get asset history - direct call
            history = await asyncio.to_thread(self.api.asset_history, asset_id, count=100)
            
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
