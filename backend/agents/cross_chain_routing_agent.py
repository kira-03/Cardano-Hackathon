"""
Cross-Chain Routing Agent - Analyzes bridge routes and recommends optimal expansion chain
"""
from typing import Dict, Any, List
from models.schemas import BridgeRoute

class CrossChainRoutingAgent:
    def __init__(self, cardano_service=None):
        self.name = "Cross-Chain Routing Agent"
        self.cardano_service = cardano_service
        
        # Bridge data based on real-world Cardano bridges
        self.bridge_data = {
            "Ethereum": [
                {
                    "bridge": "Wanchain",
                    "fee_base": 25,
                    "fee_percent": 0.1,
                    "time_min": 15,
                    "time_max": 30,
                    "trust_model": "hybrid",
                    "slippage": "0.5-1%",
                    "hops": 2,
                    "reliability_score": 85
                },
                {
                    "bridge": "Multichain",
                    "fee_base": 30,
                    "fee_percent": 0.15,
                    "time_min": 20,
                    "time_max": 45,
                    "trust_model": "custodial",
                    "slippage": "0.8-1.5%",
                    "hops": 1,
                    "reliability_score": 75
                },
                {
                    "bridge": "cBridge",
                    "fee_base": 20,
                    "fee_percent": 0.2,
                    "time_min": 10,
                    "time_max": 25,
                    "trust_model": "trustless",
                    "slippage": "0.3-0.8%",
                    "hops": 2,
                    "reliability_score": 90
                }
            ],
            "BSC": [
                {
                    "bridge": "Multichain",
                    "fee_base": 8,
                    "fee_percent": 0.1,
                    "time_min": 10,
                    "time_max": 20,
                    "trust_model": "custodial",
                    "slippage": "0.5-1%",
                    "hops": 1,
                    "reliability_score": 80
                },
                {
                    "bridge": "cBridge",
                    "fee_base": 5,
                    "fee_percent": 0.15,
                    "time_min": 8,
                    "time_max": 15,
                    "trust_model": "trustless",
                    "slippage": "0.3-0.7%",
                    "hops": 2,
                    "reliability_score": 88
                }
            ],
            "Polygon": [
                {
                    "bridge": "Multichain",
                    "fee_base": 4,
                    "fee_percent": 0.1,
                    "time_min": 10,
                    "time_max": 15,
                    "trust_model": "custodial",
                    "slippage": "0.4-0.8%",
                    "hops": 1,
                    "reliability_score": 82
                },
                {
                    "bridge": "cBridge",
                    "fee_base": 3,
                    "fee_percent": 0.12,
                    "time_min": 8,
                    "time_max": 12,
                    "trust_model": "trustless",
                    "slippage": "0.2-0.6%",
                    "hops": 2,
                    "reliability_score": 90
                }
            ],
            "Solana": [
                {
                    "bridge": "Wormhole",
                    "fee_base": 5,
                    "fee_percent": 0.1,
                    "time_min": 5,
                    "time_max": 15,
                    "trust_model": "trustless",
                    "slippage": "0.3-0.8%",
                    "hops": 2,
                    "reliability_score": 88
                },
                {
                    "bridge": "AllBridge",
                    "fee_base": 6,
                    "fee_percent": 0.15,
                    "time_min": 8,
                    "time_max": 18,
                    "trust_model": "hybrid",
                    "slippage": "0.5-1%",
                    "hops": 2,
                    "reliability_score": 82
                }
            ],
            "Avalanche": [
                {
                    "bridge": "Multichain",
                    "fee_base": 8,
                    "fee_percent": 0.1,
                    "time_min": 10,
                    "time_max": 20,
                    "trust_model": "custodial",
                    "slippage": "0.4-0.9%",
                    "hops": 1,
                    "reliability_score": 80
                },
                {
                    "bridge": "cBridge",
                    "fee_base": 6,
                    "fee_percent": 0.12,
                    "time_min": 8,
                    "time_max": 15,
                    "trust_model": "trustless",
                    "slippage": "0.3-0.7%",
                    "hops": 2,
                    "reliability_score": 87
                }
            ]
        }
        
        # Chain characteristics
        self.chain_info = {
            "Ethereum": {
                "liquidity_depth": 95,
                "dex_count": 50,
                "avg_gas_cost": 40,
                "user_base_score": 100,
                "cex_support": 100
            },
            "BSC": {
                "liquidity_depth": 85,
                "dex_count": 35,
                "avg_gas_cost": 3,
                "user_base_score": 90,
                "cex_support": 95
            },
            "Polygon": {
                "liquidity_depth": 75,
                "dex_count": 30,
                "avg_gas_cost": 1,
                "user_base_score": 85,
                "cex_support": 85
            },
            "Solana": {
                "liquidity_depth": 80,
                "dex_count": 25,
                "avg_gas_cost": 0.5,
                "user_base_score": 88,
                "cex_support": 90
            },
            "Avalanche": {
                "liquidity_depth": 70,
                "dex_count": 20,
                "avg_gas_cost": 2,
                "user_base_score": 80,
                "cex_support": 80
            }
        }
    
    async def find_routes(
        self,
        policy_id: str,
        target_chains: List[str]
    ) -> Dict[str, Any]:
        """Find and analyze bridge routes for a token"""
        # Get token liquidity - default to 10000 if not available
        token_liquidity = 10000
        if self.cardano_service:
            try:
                liquidity_data = await self.cardano_service.get_dex_liquidity(policy_id)
                token_liquidity = liquidity_data.get("total_liquidity_usd", 10000)
            except:
                pass
        
        return await self._analyze_routes(token_liquidity, target_chains)
    
    async def _analyze_routes(
        self,
        token_liquidity: float,
        target_chains: List[str]
    ) -> Dict[str, Any]:
        """Analyze bridge routes to target chains"""
        
        routes = []
        for chain in target_chains:
            if chain in self.bridge_data:
                chain_routes = self._analyze_chain_routes(
                    chain,
                    token_liquidity
                )
                routes.extend(chain_routes)
        
        # Rank chains
        chain_rankings = self._rank_chains(target_chains, token_liquidity)
        
        # Recommend best chain
        recommended_chain = chain_rankings[0]["chain"] if chain_rankings else None
        
        return {
            "routes": routes,
            "chain_rankings": chain_rankings,
            "recommended_chain": recommended_chain,
            "recommendation_reasoning": self._explain_recommendation(
                recommended_chain,
                chain_rankings
            )
        }
    
    def _analyze_chain_routes(
        self,
        chain: str,
        token_liquidity: float
    ) -> List[BridgeRoute]:
        """Analyze all bridge routes to a specific chain"""
        routes = []
        
        for bridge in self.bridge_data[chain]:
            # Estimate fees
            estimated_fee = self._estimate_fee(
                bridge,
                token_liquidity
            )
            
            # Estimate time
            time_estimate = f"{bridge['time_min']}-{bridge['time_max']} min"
            
            # Calculate recommendation score
            rec_score = self._calculate_route_score(bridge, chain)
            
            route = BridgeRoute(
                source_chain="Cardano",
                target_chain=chain,
                bridge_name=bridge["bridge"],
                estimated_fee=estimated_fee,
                estimated_time=time_estimate,
                trust_model=bridge["trust_model"],
                slippage_estimate=bridge["slippage"],
                hops=bridge["hops"],
                recommendation_score=rec_score
            )
            routes.append(route)
        
        return routes
    
    def _estimate_fee(
        self,
        bridge: Dict[str, Any],
        amount: float
    ) -> str:
        """Estimate bridge fee"""
        # For display, assume bridging $1000 worth
        test_amount = 1000
        fee = bridge["fee_base"] + (test_amount * bridge["fee_percent"] / 100)
        return f"${fee:.2f} (for $1000)"
    
    def _calculate_route_score(
        self,
        bridge: Dict[str, Any],
        chain: str
    ) -> float:
        """Calculate recommendation score for a route (0-100)"""
        # Factors: reliability, cost, speed, trust model
        reliability = bridge["reliability_score"]
        
        # Cost score (lower fee = higher score)
        cost_score = max(0, 100 - bridge["fee_base"] * 2)
        
        # Speed score (faster = higher score)
        avg_time = (bridge["time_min"] + bridge["time_max"]) / 2
        speed_score = max(0, 100 - avg_time * 2)
        
        # Trust model score
        trust_scores = {
            "trustless": 100,
            "hybrid": 80,
            "custodial": 60
        }
        trust_score = trust_scores.get(bridge["trust_model"], 70)
        
        # Weighted average
        score = (
            reliability * 0.35 +
            cost_score * 0.25 +
            speed_score * 0.20 +
            trust_score * 0.20
        )
        
        return round(score, 1)
    
    def _rank_chains(
        self,
        chains: List[str],
        token_liquidity: float
    ) -> List[Dict[str, Any]]:
        """Rank target chains by suitability"""
        rankings = []
        
        for chain in chains:
            if chain not in self.chain_info:
                continue
            
            info = self.chain_info[chain]
            
            # Calculate overall score
            # Factors: liquidity depth, user base, CEX support, costs
            score = (
                info["liquidity_depth"] * 0.30 +
                info["user_base_score"] * 0.25 +
                info["cex_support"] * 0.25 +
                (100 - info["avg_gas_cost"] * 2) * 0.20
            )
            
            # Adjust for token liquidity
            if token_liquidity < 50000:
                # Smaller projects prefer cheaper chains
                if info["avg_gas_cost"] < 5:
                    score += 10
            else:
                # Larger projects prefer higher liquidity chains
                if info["liquidity_depth"] > 80:
                    score += 10
            
            rankings.append({
                "chain": chain,
                "score": round(score, 1),
                "liquidity_depth": info["liquidity_depth"],
                "user_base": info["user_base_score"],
                "avg_gas_cost": f"${info['avg_gas_cost']}",
                "cex_support": info["cex_support"],
                "dex_count": info["dex_count"]
            })
        
        # Sort by score descending
        rankings.sort(key=lambda x: x["score"], reverse=True)
        return rankings
    
    def _explain_recommendation(
        self,
        recommended_chain: str,
        rankings: List[Dict[str, Any]]
    ) -> str:
        """Explain why a chain is recommended"""
        if not recommended_chain or not rankings:
            return "No recommendation available"
        
        top_chain = rankings[0]
        
        reasons = []
        
        if top_chain["liquidity_depth"] > 85:
            reasons.append("excellent liquidity depth")
        
        if top_chain["user_base"] > 85:
            reasons.append("large user base")
        
        if top_chain["cex_support"] > 85:
            reasons.append("strong CEX support")
        
        if float(top_chain["avg_gas_cost"].replace("$", "")) < 5:
            reasons.append("low transaction costs")
        
        if reasons:
            return f"{recommended_chain} recommended due to {', '.join(reasons)}."
        
        return f"{recommended_chain} offers the best overall balance for cross-chain expansion."
