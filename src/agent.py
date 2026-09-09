from typing import Dict, Any
from src.intent_classifier import KeywordIntentClassifier, TFIDFIntentClassifier, ProposedIntentClassifier
from src.reply_generator import TemplateReplyGenerator, RetrievalReplyGenerator, GroundedLLMReplyGenerator
from src.escalation_engine import EscalationEngine

class SupportAgent:
    """
    Unified @AmazonHelp Customer Support AI Agent pipeline.
    Coordinating Classification -> Escalation -> Reply Generation.
    """
    def __init__(self, mode: str = "proposed_agent"):
        self.mode = mode
        self.escalation_engine = EscalationEngine()
        
        if mode == "trivial_baseline":
            self.classifier = KeywordIntentClassifier()
            self.reply_gen = TemplateReplyGenerator()
        elif mode == "simple_ml_baseline":
            self.classifier = TFIDFIntentClassifier()
            self.reply_gen = RetrievalReplyGenerator()
        else:
            self.classifier = ProposedIntentClassifier()
            self.reply_gen = GroundedLLMReplyGenerator()

    def process_message(self, customer_message: str) -> Dict[str, Any]:
        """
        Process incoming tweet message through full pipeline.
        """
        # Step 1: Classify Intent
        intent, confidence = self.classifier.predict(customer_message)
        
        # Step 2: Evaluate Escalation Decision
        should_escalate, escalation_reason = self.escalation_engine.evaluate(
            customer_message, intent, confidence
        )
        
        # Step 3: Draft Reply
        if should_escalate:
            reply = f"We take this issue very seriously. This ticket has been escalated to an Amazon Senior Specialist ({escalation_reason}). Please send us a Direct Message (DM) with your email and order details to assist immediately."
        else:
            reply = self.reply_gen.generate(intent, customer_message)
            
        return {
            "mode": self.mode,
            "customer_message": customer_message,
            "predicted_intent": intent,
            "intent_confidence": round(confidence, 4),
            "should_escalate": should_escalate,
            "escalation_reason": escalation_reason,
            "draft_reply": reply
        }
