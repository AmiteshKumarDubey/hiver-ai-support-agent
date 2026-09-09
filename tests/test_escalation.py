import pytest
from src.escalation_engine import EscalationEngine

def test_escalation_legal_trigger():
    engine = EscalationEngine()
    should_escalate, reason = engine.evaluate("I am suing Amazon with my lawyer!", "GENERAL_INQUIRY", 0.95)
    assert should_escalate is True
    assert "Legal" in reason

def test_escalation_account_security():
    engine = EscalationEngine()
    should_escalate, reason = engine.evaluate("Someone hacked my account", "ACCOUNT_SECURITY", 0.95)
    assert should_escalate is True
    assert "security" in reason.lower()

def test_no_escalation_routine_inquiry():
    engine = EscalationEngine()
    should_escalate, reason = engine.evaluate("Where is my package tracking?", "ORDER_TRACKING", 0.95)
    assert should_escalate is False
    assert reason is None
