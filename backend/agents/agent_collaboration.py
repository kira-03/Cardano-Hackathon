"""
Agent Collaboration Logic - Enables event-driven communication between agents
"""
from typing import Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)

class AgentEventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def publish(self, event_type: str, data: Dict[str, Any]):
        for callback in self.listeners.get(event_type, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in event callback for {event_type}: {e}")

# Example usage:
# event_bus = AgentEventBus()
# event_bus.subscribe('listing_ready', liquidity_agent.handle_listing_ready)
# event_bus.publish('listing_ready', {...})
