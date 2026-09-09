import pytest
from src.intent_classifier import KeywordIntentClassifier, TFIDFIntentClassifier, ProposedIntentClassifier

def test_keyword_classifier():
    clf = KeywordIntentClassifier()
    intent, conf = clf.predict("Where is my tracking package?")
    assert intent == "ORDER_TRACKING"
    assert conf > 0.5

def test_tfidf_classifier():
    clf = TFIDFIntentClassifier()
    intent, conf = clf.predict("I want a refund for double charge")
    assert intent == "REFUND_REQUEST"
    assert conf > 0.0

def test_proposed_classifier():
    clf = ProposedIntentClassifier()
    intent, conf = clf.predict("My item arrived damaged and shattered")
    assert intent == "DAMAGED_ITEM"
    assert conf >= 0.8
