"""
Continuous Monitoring Agent - Watches liquidity, holder concentration, exchange rules, and alerts for listing readiness
"""
import asyncio
from typing import Dict, Any, Callable
from services.cardano_service import CardanoService
from services.dex_service import DEXService
from services.exchange_service import ExchangeService
import logging

logger = logging.getLogger(__name__)

class MonitoringAgent:
    def __init__(self, cardano_service: CardanoService, dex_service: DEXService, exchange_service: ExchangeService, alert_callback: Callable[[Dict[str, Any]], None]):
        self.cardano_service = cardano_service
        self.dex_service = dex_service
        self.exchange_service = exchange_service
        self.alert_callback = alert_callback
        self.running = False

    async def start(self, policy_id: str, interval: int = 300):
        self.running = True
        while self.running:
            try:
                # Fetch latest metrics
                liquidity = await self.dex_service.get_liquidity(policy_id)
                holders = await self.cardano_service.get_token_holders(policy_id)
                holder_count = len(holders)
                concentration = await self.cardano_service.analyze_holder_distribution(holders, None)
                exchange_rules = await self.exchange_service.get_all_listing_requirements()

                # Check listing readiness
                alerts = []
                for ex, rules in exchange_rules.items():
                    if liquidity >= rules.get('min_liquidity', 0) and holder_count >= rules.get('min_holders', 0):
                        alerts.append({
                            'exchange': ex,
                            'ready': True,
                            'liquidity': liquidity,
                            'holders': holder_count
                        })
                # Alert if any exchange is ready
                if alerts:
                    self.alert_callback({'type': 'listing_ready', 'details': alerts})
                # Alert for low liquidity or high concentration
                if liquidity < min(r.get('min_liquidity', 0) for r in exchange_rules.values()):
                    self.alert_callback({'type': 'liquidity_low', 'liquidity': liquidity})
                if concentration.get('top_10_concentration', 100) > 40:
                    self.alert_callback({'type': 'concentration_high', 'concentration': concentration.get('top_10_concentration', 100)})
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
            await asyncio.sleep(interval)

    def stop(self):
        self.running = False
