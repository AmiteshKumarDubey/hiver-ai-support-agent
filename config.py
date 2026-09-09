import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Workspace Root & Data Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
GOLDEN_SET_DIR = DATA_DIR / "golden_set"
GOLDEN_SET_PATH = GOLDEN_SET_DIR / "golden_eval_set.json"
REPORT_DIR = BASE_DIR / "report"

# Target Brand Selection
TARGET_BRAND = "@AmazonHelp"
BRAND_NAME = "Amazon Customer Support"

# Intent Taxonomy for @AmazonHelp
INTENT_TAXONOMY = {
    "ORDER_TRACKING": "Inquiries regarding package delivery status, tracking numbers, shipping delays, and estimated arrival dates.",
    "REFUND_REQUEST": "Requests for refunds, return processing, money back, or resolution of double charges.",
    "DAMAGED_ITEM": "Reports of damaged, defective, broken, expired, or wrong items delivered.",
    "CANCELLATION": "Requests to cancel a pending order, modify order details, or halt item dispatch.",
    "ACCOUNT_SECURITY": "Issues related to account access, locked accounts, unauthorized charges, or hacked accounts.",
    "PRIME_BILLING": "Inquiries regarding Prime subscription charges, billing cycles, membership benefits, or cancellation.",
    "GENERAL_INQUIRY": "General customer service questions, app/website feedback, hours of operation, or seller policies."
}

# Policy-based Escalation Triggers (Keywords & Phrases demanding immediate human intervention)
ESCALATION_KEYWORDS = [
    "sue", "lawyer", "legal action", "attorney", "better business bureau", "bbb",
    "fraud", "scam", "stolen", "unauthorized charge", "police", "hacked",
    "threat", "physical damage", "hazard", "unsafe", "poisoned", "allergic reaction",
    "worst customer service", "never buying again", "disgusting", "lawsuit"
]

# Risk / Escalation Thresholds
ESCALATION_CONFIDENCE_THRESHOLD = float(os.getenv("ESCALATION_CONFIDENCE_THRESHOLD", "0.65"))

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
LLM_JUDGE_MODEL = os.getenv("LLM_JUDGE_MODEL", "gpt-4o-mini")

# System Tone and Constraints
SYSTEM_BRAND_PROMPT = """You are an official AI Customer Support Assistant for @AmazonHelp on Twitter.
Your job is to respond concisely, empathetically, and accurately to customer inquiries.

STRICT CONSTRAINTS:
1. ALWAYS maintain a polite, helpful, and professional brand voice.
2. NEVER fabricate tracking numbers, refund transaction IDs, or account specific details.
3. If specific account verification is needed, instruct the customer to reach out via Amazon Direct Message (DM) with their order number.
4. Keep replies under 280 characters whenever possible (Twitter format).
5. Ground your answers strictly in Amazon's official customer support policies.
"""
