"""
Liquidity Plan Agent - Generates actionable liquidity plans for Cardano tokens
"""
from typing import Dict, Any, List
from services.cardano_service import CardanoService
from services.dex_service import DEXService
import datetime
import logging

logger = logging.getLogger(__name__)


class LiquidityPlanAgent:
    def __init__(self, cardano_service: CardanoService, dex_service: DEXService = None):
        self.cardano_service = cardano_service
        # Default to a real DEXService if one wasn't provided
        self.dex_service = dex_service or DEXService()
        self.name = "Liquidity Plan Agent"

    async def generate_plan(self, policy_id: str, target_liquidity: float) -> Dict[str, Any]:
        """
        Generate a liquidity plan. This method is defensive: it supports older
        DEXService APIs as well as the consolidated `get_all_dex_data` and
        `generate_liquidity_plan` helpers. If market data is unavailable it
        returns a reasonable fallback plan instead of raising AttributeError.
        """
        try:
            # Prefer the consolidated DEX API if available
            current_liquidity = {"total_liquidity_usd": 0, "pools": []}
            if hasattr(self.dex_service, 'get_all_dex_data'):
                dex_data = await self.dex_service.get_all_dex_data(policy_id)
                current_liquidity = dex_data or current_liquidity
                pools = current_liquidity.get('pools', [])
            else:
                # Backwards compatible: try to call older methods if present
                pools = []
                if hasattr(self.dex_service, 'get_liquidity'):
                    try:
                        current_val = await self.dex_service.get_liquidity(policy_id)
                        # normalize to dict shape
                        current_liquidity = {"total_liquidity_usd": float(current_val or 0), "pools": []}
                    except Exception:
                        current_liquidity = {"total_liquidity_usd": 0, "pools": []}
                if hasattr(self.dex_service, 'get_pools'):
                    try:
                        pools = await self.dex_service.get_pools(policy_id)
                    except Exception:
                        pools = []

            ada_price = None
            try:
                ada_price = await self.cardano_service.get_ada_price()
            except Exception:
                ada_price = None

            current_total = float(current_liquidity.get('total_liquidity_usd') or 0)

            # If the DEXService provides a plan generator, prefer it
            if hasattr(self.dex_service, 'generate_liquidity_plan'):
                try:
                    plan = await self.dex_service.generate_liquidity_plan(policy_id, current_liquidity, target_liquidity)
                    # Enrich plan with ADA price if available
                    if ada_price is not None:
                        plan.setdefault('ada_price_usd', ada_price)
                    return plan
                except Exception as e:
                    logger.warning(f"DEXService.generate_liquidity_plan failed: {e}")

            # Fallback plan generation
            ada_to_add_usd = max(0.0, float(target_liquidity or 0.0) - current_total)
            ada_to_add = None
            if ada_price and ada_price > 0:
                ada_to_add = ada_to_add_usd / ada_price

            # Recommend optimal pool pair (highest volume or lowest fees)
            try:
                optimal_pool = max(pools, key=lambda p: p.get('volume', 0)) if pools else None
                pool_pair = optimal_pool.get('pair') if optimal_pool and isinstance(optimal_pool, dict) else 'ADA/UNKNOWN'
            except Exception:
                pool_pair = 'ADA/UNKNOWN'

            # Recommend liquidity split (e.g., 70/30)
            split = {'ADA': 0.7, 'Other': 0.3}

            # Sample transaction (unsigned)
            sample_tx = {
                'from': 'your_wallet_address',
                'to': 'liquidity_pool_address',
                'amount_ada': ada_to_add,
                'amount_usd': ada_to_add_usd,
                'pair': pool_pair
            }

            # Time-based liquidity schedule (e.g., DCA over 4 weeks)
            schedule = []
            weeks = 4
            weekly_usd = ada_to_add_usd / weeks if weeks and ada_to_add_usd else 0
            weekly_ada = (ada_to_add / weeks) if weeks and ada_to_add else None
            for i in range(weeks):
                schedule.append({
                    'week': i+1,
                    'date': (datetime.datetime.now() + datetime.timedelta(weeks=i)).strftime('%Y-%m-%d'),
                    'ada_amount': weekly_ada,
                    'usd_amount': weekly_usd
                })

            return {
                'current_liquidity_usd': current_total,
                'ada_price_usd': ada_price,
                'ada_to_add': ada_to_add,
                'ada_to_add_usd': ada_to_add_usd,
                'optimal_pool_pair': pool_pair,
                'liquidity_split': split,
                'sample_transaction': sample_tx,
                'liquidity_schedule': schedule
            }

        except Exception as e:
            logger.error(f"Error in LiquidityPlanAgent.generate_plan: {e}", exc_info=True)
            # Return a safe fallback instead of raising to avoid 500s
            return {
                'current_liquidity_usd': 0,
                'ada_price_usd': None,
                'ada_to_add': None,
                'ada_to_add_usd': max(0.0, float(target_liquidity or 0.0)),
                'optimal_pool_pair': 'ADA/UNKNOWN',
                'liquidity_split': {'ADA': 0.7, 'Other': 0.3},
                'sample_transaction': {},
                'liquidity_schedule': []
            }
