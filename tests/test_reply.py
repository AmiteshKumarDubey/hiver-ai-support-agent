import pytest
from src.reply_generator import TemplateReplyGenerator, RetrievalReplyGenerator, GroundedLLMReplyGenerator

def test_template_reply_generator():
    gen = TemplateReplyGenerator()
    reply = gen.generate("ORDER_TRACKING", "Where is my order?")
    assert "Your Orders" in reply

def test_retrieval_reply_generator():
    gen = RetrievalReplyGenerator()
    reply = gen.generate("REFUND_REQUEST", "I returned my item 3 days ago")
    assert "refund" in reply.lower() or "dm" in reply.lower()

def test_grounded_llm_reply_generator():
    gen = GroundedLLMReplyGenerator()
    reply = gen.generate("DAMAGED_ITEM", "My screen is shattered")
    assert len(reply) > 10
