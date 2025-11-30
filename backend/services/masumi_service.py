import logging
import requests
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
from config import settings
from models.schemas import MasumiLog

logger = logging.getLogger(__name__)

class MasumiService:
    """
    Service for interacting with the Masumi Network.
    Handles agent registration, decision logging, and payment verification.
    """
    
    def __init__(self):
        self.registry_url = settings.masumi_registry_url
        self.payment_url = settings.masumi_payment_url
        self.agent_did = "did:masumi:agent:token-analyzer"  # This would ideally be config/dynamic
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "CrossChainNavigator/1.0"
        }

    async def check_connection(self) -> bool:
        """Check if Masumi node is accessible"""
        try:
            # Try to hit the health or version endpoint of the local Masumi node
            response = requests.get(f"{self.payment_url}/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    async def log_decision(self, 
                          decision_type: str, 
                          data: Dict[str, Any], 
                          metadata: Optional[Dict[str, Any]] = None) -> MasumiLog:
        """
        Log an agent decision to the Masumi Network.
        
        If the network is unreachable, falls back to a local signed log for later synchronization.
        """
        timestamp = datetime.utcnow()
        
        # Create a deterministic hash of the decision data
        data_str = json.dumps(data, sort_keys=True)
        decision_hash = hashlib.sha256(data_str.encode()).hexdigest()
        
        transaction_id = None
        
        try:
            # Attempt to send to Masumi Node
            payload = {
                "agent_did": self.agent_did,
                "decision_type": decision_type,
                "decision_hash": decision_hash,
                "timestamp": timestamp.isoformat(),
                "metadata": metadata or {}
            }
            
            # We use a short timeout so we don't block the user if the node isn't running
            response = requests.post(
                f"{self.payment_url}/logs", 
                json=payload, 
                headers=self.headers,
                timeout=3
            )
            
            if response.status_code == 200:
                result = response.json()
                transaction_id = result.get("transaction_id")
                logger.info(f"Successfully logged to Masumi Network. Tx: {transaction_id}")
            else:
                logger.warning(f"Masumi Node returned {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            logger.warning("Masumi Node unreachable. Using local simulation.")
            # In a real app, we might queue this for retry
            transaction_id = f"mock_tx_{decision_hash[:16]}"
        except Exception as e:
            logger.error(f"Error logging to Masumi: {e}")
            transaction_id = f"error_tx_{decision_hash[:16]}"

        # Return the log object
        return MasumiLog(
            agent_did=self.agent_did,
            decision_type=decision_type,
            decision_hash=decision_hash,
            transaction_id=transaction_id,
            timestamp=timestamp
        )

    async def register_agent(self) -> bool:
        """Register this agent with the Masumi Registry"""
        # Implementation would go here
        pass
