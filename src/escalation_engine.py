import re
from typing import Tuple, Optional
from config import ESCALATION_KEYWORDS, ESCALATION_CONFIDENCE_THRESHOLD

class EscalationEngine:
    """
    Multi-Factor Risk & Escalation Engine for @AmazonHelp AI Support Agent.
    Evaluates policy safety triggers, sentiment severity, intent ambiguity, and risk thresholds.
    """
    def __init__(self, confidence_threshold: float = ESCALATION_CONFIDENCE_THRESHOLD):
        self.confidence_threshold = confidence_threshold
        self.keywords = ESCALATION_KEYWORDS

    def evaluate(self, customer_message: str, intent: str, confidence: float) -> Tuple[bool, Optional[str]]:
        """
        Returns (should_escalate: bool, escalation_reason: str or None)
        """
        text_lower = customer_message.lower()

        # 1. Critical Legal & Regulatory Policy Triggers
        if any(kw in text_lower for kw in ["lawyer", "sue", "legal action", "attorney", "bbb", "better business bureau", "small claims", "police"]):
            return True, "Legal threat, law enforcement, or regulatory reporting notice."

        # 2. Account Security & Fraud Escalation
        if any(kw in text_lower for kw in ["hacked", "unauthorized", "stolen", "compromised", "fraud"]):
            return True, "Security risk, account takeover, or fraud attempt detected."

        if intent == "ACCOUNT_SECURITY":
            return True, "All account security and compromise issues require human agent verification."

        # 3. Physical Safety Hazards & Severe Damage
        if any(kw in text_lower for kw in ["bleach", "fire hazard", "glass shards", "poisoned", "injured", "hazard", "sliced", "burnt"]):
            return True, "Physical safety hazard or severe product liability issue."

        # 4. Severe Frustration & Manager Demands
        if any(kw in text_lower for kw in ["3rd time", "2 weeks", "lying", "disputing", "manager", "supervisor", "stealing", "twice", "demand"]):
            return True, "High customer frustration, repeated delay, or supervisor demand."

        # 5. Low Intent Confidence Escalation
        if confidence < self.confidence_threshold:
            return True, f"Intent classification confidence ({confidence:.2f}) below safety threshold ({self.confidence_threshold:.2f})."

        # Safe to auto-handle
        return False, None
