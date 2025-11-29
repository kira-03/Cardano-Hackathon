"""
Test PDF Generation
"""
import asyncio
from utils.pdf_generator import PDFGenerator

async def test_pdf():
    generator = PDFGenerator()
    
    # Sample analysis data
    sample_data = {
        "analysis_id": "test-12345678",
        "policy_id": "a3931691f5c4e65d01c429e473d0dd24c51afdb6daf88e632a6c1e51",
        "token_name": "SundaeSwap",
        "token_symbol": "SUNDAE",
        "timestamp": "2025-11-29T10:30:00Z",
        "metrics": {
            "total_supply": "2,000,000,000",
            "circulating_supply": "1,400,000,000",
            "holder_count": 45231,
            "top_10_concentration": 32.5,
            "top_50_concentration": 48.2,
            "liquidity_usd": 2450000,
            "volume_24h": 185000,
            "price_usd": 0.0125,
            "market_cap_usd": 17500000,
            "metadata_score": 0.92
        },
        "readiness_score": {
            "total_score": 78.5,
            "liquidity_score": 72,
            "holder_distribution_score": 85,
            "metadata_score": 95,
            "security_score": 80,
            "supply_stability_score": 75,
            "market_activity_score": 65,
            "grade": "B"
        },
        "recommendations": [
            {
                "category": "Liquidity",
                "priority": "high",
                "issue": "Liquidity below Tier 1 exchange requirements",
                "recommendation": "Add liquidity to major DEX pools to reach $5M+ TVL",
                "estimated_impact": "+15 points on liquidity score"
            },
            {
                "category": "Volume",
                "priority": "medium",
                "issue": "24h trading volume is below optimal levels",
                "recommendation": "Increase market making activities and trading incentives",
                "estimated_impact": "+10 points on market activity score"
            },
            {
                "category": "Holder Distribution",
                "priority": "low",
                "issue": "Top 10 wallet concentration slightly high",
                "recommendation": "Consider token distribution events to diversify holdings",
                "estimated_impact": "+5 points on holder distribution score"
            }
        ],
        "exchange_requirements": [
            {
                "exchange": "Binance",
                "requirement": "Minimum 10,000 holders",
                "current_status": "45,231 holders",
                "meets_requirement": True
            },
            {
                "exchange": "Binance",
                "requirement": "Minimum $5M liquidity",
                "current_status": "$2.45M liquidity",
                "meets_requirement": False
            },
            {
                "exchange": "Binance",
                "requirement": "Token registry metadata",
                "current_status": "Complete metadata",
                "meets_requirement": True
            },
            {
                "exchange": "KuCoin",
                "requirement": "Minimum 5,000 holders",
                "current_status": "45,231 holders",
                "meets_requirement": True
            },
            {
                "exchange": "KuCoin",
                "requirement": "Minimum $1M liquidity",
                "current_status": "$2.45M liquidity",
                "meets_requirement": True
            }
        ],
        "bridge_routes": [
            {
                "source_chain": "Cardano",
                "target_chain": "Ethereum",
                "bridge_name": "Wanchain",
                "estimated_fee": "$15-25",
                "estimated_time": "15-30 min",
                "trust_model": "hybrid",
                "slippage_estimate": "0.3%",
                "hops": 1,
                "recommendation_score": 85
            },
            {
                "source_chain": "Cardano",
                "target_chain": "BSC",
                "bridge_name": "Milkomeda",
                "estimated_fee": "$5-10",
                "estimated_time": "5-10 min",
                "trust_model": "trustless",
                "slippage_estimate": "0.2%",
                "hops": 1,
                "recommendation_score": 92
            }
        ],
        "recommended_chain": "BSC",
        "executive_summary": "SundaeSwap (SUNDAE) demonstrates strong fundamentals with 45,231 holders and robust metadata compliance. The token achieves a B grade (78.5/100) in listing readiness assessment. Primary improvement areas include liquidity enhancement to meet Tier 1 exchange requirements. The holder distribution is healthy with reasonable concentration levels. Cross-chain expansion via BSC through Milkomeda bridge offers the most efficient path for multi-chain presence.",
        "next_steps": [
            "[HIGH] Increase liquidity to $5M+ by adding to Minswap and SundaeSwap DEX pools",
            "[HIGH] Apply for Binance listing once liquidity threshold is met",
            "[MEDIUM] Implement market making strategy to boost 24h volume",
            "[MEDIUM] Explore BSC bridge for cross-chain expansion",
            "[LOW] Consider community distribution events to reduce top wallet concentration"
        ]
    }
    
    print("Generating PDF report...")
    pdf_path = await generator.generate_analysis_report("test-12345678", sample_data)
    
    if pdf_path:
        print(f"✅ PDF generated successfully: {pdf_path}")
        print(f"\nYou can open the PDF at: {pdf_path}")
    else:
        print("❌ Failed to generate PDF")

if __name__ == "__main__":
    asyncio.run(test_pdf())
