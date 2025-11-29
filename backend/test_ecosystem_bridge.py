"""
Example usage of EcosystemBridgeAssistant Agent

This script demonstrates how to use the EcosystemBridgeAssistant to generate
comprehensive exchange listing packages, bridge routes, and liquidity plans.
"""
import asyncio
import logging
from pathlib import Path

from agents.ecosystem_bridge_agent import (
    EcosystemBridgeAgent,
    ProjectMetadata,
    ExecutionMode,
    ConsentFlags
)
from services.cardano_service import CardanoService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """
    Example usage of EcosystemBridgeAssistant
    """
    
    print("=" * 80)
    print("EcosystemBridgeAssistant - Exchange Listing Automation")
    print("=" * 80)
    print()
    
    # Example: Cardano policy ID (replace with actual)
    # Using a well-known Cardano token for demonstration
    policy_id = "279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f"  # SNEK token
    
    # Project metadata (fill in your project details)
    project_metadata = ProjectMetadata(
        name="SNEK",
        symbol="SNEK",
        website="https://snek.fun",
        whitepaper_url="https://snek.fun/whitepaper",
        github_url="https://github.com/snek",
        contact_email="team@snek.fun",
        legal_entity_info={
            "entity_name": "SNEK Foundation",
            "jurisdiction": "Switzerland",
            "registration_number": "CHE-123.456.789"
        }
    )
    
    # Target exchanges (you can customize this list)
    desired_exchanges = ["binance", "coinbase", "kraken", "kucoin", "gateio"]
    
    # Target chains for bridge analysis (currently Cardano-only)
    desired_target_chains = ["ethereum", "bsc", "polygon"]
    
    # Execution mode
    # - "preview": Only generate artifacts, no actual execution
    # - "dryrun": Build unsigned transactions
    # - "submit": Submit forms (requires consent)
    # - "live": Broadcast transactions (requires consent + multisig)
    execution_mode = ExecutionMode.PREVIEW
    
    # Consent flags (for non-preview modes)
    consent_flags = ConsentFlags(
        allow_portal_login=False,  # Set to True to allow automated portal login
        allow_email_send=False,     # Set to True to allow email sending
        allow_tx_broadcast=False    # Set to True to allow transaction broadcast
    )
    
    print(f"Policy ID: {policy_id}")
    print(f"Project: {project_metadata.name} ({project_metadata.symbol})")
    print(f"Execution Mode: {execution_mode}")
    print()
    
    # Initialize services
    print("Initializing services...")
    cardano_service = CardanoService()
    
    # Check connection
    connected = await cardano_service.check_connection()
    if not connected:
        print("❌ Failed to connect to Blockfrost API")
        print("Please check your BLOCKFROST_API_KEY in .env file")
        return
    
    print("✅ Connected to Blockfrost API")
    print()
    
    # Initialize EcosystemBridgeAssistant
    print("Initializing EcosystemBridgeAssistant...")
    agent = EcosystemBridgeAgent(cardano_service=cardano_service)
    print("✅ EcosystemBridgeAssistant initialized")
    print()
    
    # Process request
    print("=" * 80)
    print("Starting comprehensive ecosystem bridge analysis...")
    print("=" * 80)
    print()
    
    try:
        results = await agent.process_request(
            policy_id=policy_id,
            project_metadata=project_metadata,
            desired_exchanges=desired_exchanges,
            desired_target_chains=desired_target_chains,
            execution_mode=execution_mode,
            consent_flags=consent_flags
        )
        
        print()
        print("=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print()
        
        # Display results summary
        if results.get("errors"):
            print("⚠️ ERRORS:")
            for error in results["errors"]:
                print(f"  - {error}")
            print()
        
        if results.get("high_risk_flag"):
            print("⚠️ HIGH RISK TOKEN DETECTED")
            print("Manual approval required before proceeding with submissions")
            print()
        
        # Data Collection
        data_collection = results.get("data_collection", {})
        if data_collection:
            print("📊 DATA COLLECTION:")
            holder_dist = data_collection.get("holder_distribution", {})
            print(f"  • Holders: {holder_dist.get('total_holders', 0):,}")
            print(f"  • Top 10 concentration: {holder_dist.get('top_10_concentration', 0):.1f}%")
            
            dex_data = data_collection.get("dex_liquidity", {})
            liquidity = dex_data.get("total_liquidity_usd", 0)
            print(f"  • Total liquidity: ${liquidity:,.0f}")
            print()
        
        # Readiness Report
        readiness = results.get("readiness_report", {})
        if readiness:
            print("📈 READINESS SCORES:")
            exchange_scores = readiness.get("exchange_scores", {})
            for exchange, score_data in exchange_scores.items():
                score = score_data.get("score", 0)
                print(f"  • {exchange.capitalize()}: {score:.1f}/100")
            print()
        
        # Artifacts Generated
        artifacts = results.get("artifacts", {})
        if artifacts:
            print("📄 ARTIFACTS GENERATED:")
            for artifact_name, artifact_path in artifacts.items():
                if artifact_path:
                    print(f"  • {artifact_name}: {artifact_path}")
            print()
        
        # Proposals
        proposals = results.get("proposals", {})
        if proposals:
            print("📧 EXCHANGE EMAILS GENERATED:")
            emails = proposals.get("emails", {})
            for exchange, email_data in emails.items():
                print(f"  • {exchange.capitalize()}: {email_data.get('subject', 'N/A')}")
            print()
        
        # Bridge Routes
        bridge_sim = results.get("bridge_simulation", {})
        if bridge_sim:
            routes = bridge_sim.get("routes", [])
            print(f"🌉 BRIDGE ROUTES: {len(routes)} routes found")
            for i, route in enumerate(routes[:3], 1):
                source = route.get("source_chain", "")
                target = route.get("target_chain", "")
                bridge = route.get("bridge_name", "")
                print(f"  {i}. {source} → {target} via {bridge}")
            print()
        
        # Liquidity Plan
        liquidity_plan = results.get("liquidity_plan", {})
        if liquidity_plan:
            actions = liquidity_plan.get("actions", [])
            print(f"💧 LIQUIDITY PLAN: {len(actions)} actions recommended")
            for action in actions:
                action_name = action.get("action", "")
                amount = action.get("amount_usd", 0)
                print(f"  • {action_name}: ${amount:,.0f}")
            print()
        
        # Execution Results
        execution_results = results.get("execution_results", {})
        if execution_results:
            mode = execution_results.get("mode", "")
            print(f"⚡ EXECUTION: {mode}")
            message = execution_results.get("message", "")
            if message:
                print(f"  {message}")
            print()
        
        # Next Steps
        print("=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print()
        print("1. Review generated artifacts in the 'outputs/' directory")
        print("2. Check readiness scores and prioritize improvements")
        print("3. Review exchange-specific emails and forms")
        print("4. Implement recommended actions from liquidity plan")
        print("5. When ready, switch to 'submit' mode with appropriate consent flags")
        print()
        
        # Audit Log
        audit_log = results.get("audit_log", [])
        print(f"📋 Audit log: {len(audit_log)} events recorded")
        print()
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        print(f"\n❌ Analysis failed: {e}")
        print("\nPlease check the logs for details")
        return
    
    print("=" * 80)
    print("Analysis session complete!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
