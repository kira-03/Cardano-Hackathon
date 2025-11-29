"""
Test AI Agent capabilities
"""
import asyncio
import logging
import os
from agents.exchange_preparation_agent import ExchangePreparationAgent
from models.schemas import TokenMetrics

# Set up logging
logging.basicConfig(level=logging.INFO)

async def test_ai_agent():
    """Test the AI-powered Exchange Preparation Agent"""
    
    print("🤖 Testing AI Exchange Preparation Agent")
    print("=" * 60)
    
    # Initialize agent
    agent = ExchangePreparationAgent()
    
    # Check if AI is available
    if agent.use_llm:
        print("✅ AI Mode: LLM-powered analysis ACTIVE")
    else:
        print("⚠️ Fallback Mode: Algorithmic analysis (no LLM)")
    
    # Create sample token metrics
    sample_metrics = TokenMetrics(
        total_supply="1000000000",
        circulating_supply="800000000",
        holder_count=450,
        top_10_concentration=35.5,
        top_50_concentration=62.1,
        liquidity_usd=25000.0,
        volume_24h=3500.0,
        metadata_score=75.0,
        contract_risk_score=85.0
    )
    
    # Sample token info
    sample_token_info = {
        "asset_name": "ADAHero",
        "policy_id": "a9fc2c980e6beed499b91089ca06ad433961a6238690219b8021fe43",
        "metadata": {
            "name": "ADAHero",
            "ticker": "HERO",
            "description": "A community-driven gaming token on Cardano focused on NFT-based RPG gameplay",
            "website": "https://adahero.io",
            "twitter": "@ADAHero_io"
        }
    }
    
    print(f"\n📊 Analyzing Sample Token: {sample_token_info['asset_name']}")
    print(f"Policy ID: {sample_token_info['policy_id'][:16]}...")
    print(f"Holders: {sample_metrics.holder_count}")
    print(f"Liquidity: ${sample_metrics.liquidity_usd:,.0f}")
    print(f"Volume 24h: ${sample_metrics.volume_24h:,.0f}")
    
    try:
        # Test AI scoring
        print("\n🧠 Testing AI Scoring...")
        if agent.use_llm:
            ai_score = await agent._calculate_ai_score(sample_token_info, sample_metrics)
            print(f"AI Score: {ai_score.total_score}/100 (Grade: {ai_score.grade})")
            
            if hasattr(ai_score, 'ai_reasoning'):
                print(f"AI Reasoning: {ai_score.ai_reasoning[:200]}...")
            
            if hasattr(ai_score, 'key_strengths'):
                print(f"Key Strengths: {ai_score.key_strengths}")
            
            if hasattr(ai_score, 'critical_weaknesses'):
                print(f"Weaknesses: {ai_score.critical_weaknesses}")
        else:
            simple_score = agent._calculate_simple_score(sample_metrics)
            print(f"Algorithmic Score: {simple_score.total_score}/100")
        
        # Test AI UVP generation
        print("\n✨ Testing AI UVP Generation...")
        uvp = agent._generate_uvp(sample_token_info["metadata"])
        print(f"Generated UVP: {uvp}")
        
        # Test AI market potential assessment
        print("\n📈 Testing AI Market Assessment...")
        if agent.use_llm:
            ai_score = await agent._calculate_ai_score(sample_token_info, sample_metrics)
            market_potential = agent._assess_market_potential(sample_metrics, ai_score)
        else:
            simple_score = agent._calculate_simple_score(sample_metrics)
            market_potential = agent._assess_market_potential(sample_metrics, simple_score)
        
        print(f"Market Potential: {market_potential}")
        
        # Test action suggestions
        print("\n🎯 Testing AI Action Suggestions...")
        test_requirements = [
            "Minimum liquidity: $50,000",
            "Minimum holders: 500",
            "Complete token metadata"
        ]
        
        for req in test_requirements:
            action = agent._suggest_action(req)
            print(f"• {req}")
            print(f"  → {action}")
        
        print("\n" + "=" * 60)
        print("🎉 AI Agent Test Complete!")
        
        if agent.use_llm:
            print("✅ Your agent is now AI-powered with LLM capabilities!")
            print("💡 Features enabled:")
            print("  - Intelligent token scoring")
            print("  - AI-generated value propositions") 
            print("  - Smart market assessments")
            print("  - Context-aware recommendations")
        else:
            print("⚠️ To enable AI features:")
            print("  1. Set OPENAI_API_KEY environment variable")
            print("  2. Or add openai_api_key to .env file")
            print("  3. Ensure use_ai_analysis=True in config")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ai_agent())