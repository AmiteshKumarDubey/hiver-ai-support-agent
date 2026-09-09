import json
import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from config import GOLDEN_SET_PATH, PROCESSED_DATA_DIR, RAW_DATA_DIR, TARGET_BRAND

def ensure_directories():
    """Ensure raw, processed, and golden set data directories exist."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    GOLDEN_SET_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_sample_raw_dataset(num_samples: int = 300) -> pd.DataFrame:
    """
    Generate realistic Kaggle-style Customer Support Twitter dataset for @AmazonHelp.
    Matches schema of Kaggle `thoughtvector/customer-support-on-twitter` (twcs.csv).
    Schema: tweet_id, author_id, created_at, in_reply_to_status_id, text
    """
    ensure_directories()
    raw_file = RAW_DATA_DIR / "amazon_help_tweets.csv"
    
    if raw_file.exists():
        return pd.read_csv(raw_file)
    
    # Representative @AmazonHelp historical tweet pairs & threads
    sample_data = [
        # Order Tracking
        ("101", "cust_001", "Wed Oct 11 10:00:00 +0000 2023", None, "@AmazonHelp Where is my package? Order #114-8742910 was supposed to arrive yesterday!"),
        ("102", "AmazonHelp", "Wed Oct 11 10:05:00 +0000 2023", "101", "@cust_001 We apologize for the delay! Please send us a DM with your order details so we can investigate."),
        ("103", "cust_002", "Wed Oct 11 10:10:00 +0000 2023", None, "@AmazonHelp My tracking says delivered but I checked my porch and nothing is there!"),
        ("104", "AmazonHelp", "Wed Oct 11 10:12:00 +0000 2023", "103", "@cust_002 Sorry to hear that! Please check with neighbors or property management, and DM us if still missing."),
        
        # Refund Requests
        ("105", "cust_003", "Wed Oct 11 10:15:00 +0000 2023", None, "@AmazonHelp I returned my item 5 days ago according to UPS. Where is my refund?"),
        ("106", "AmazonHelp", "Wed Oct 11 10:18:00 +0000 2023", "105", "@cust_003 Refunds typically take 3-5 business days after reaching our warehouse. Please DM us your return tracking!"),
        ("107", "cust_004", "Wed Oct 11 10:20:00 +0000 2023", None, "@AmazonHelp You double charged my credit card for order #112-998811! Refund me immediately."),
        ("108", "AmazonHelp", "Wed Oct 11 10:22:00 +0000 2023", "107", "@cust_004 We understand your concern. Please send us a direct message so we can safely check your billing details."),
        
        # Damaged / Defective Items
        ("109", "cust_005", "Wed Oct 11 10:30:00 +0000 2023", None, "@AmazonHelp Opened my box today and the monitor screen is completely shattered!"),
        ("110", "AmazonHelp", "Wed Oct 11 10:35:00 +0000 2023", "109", "@cust_005 Oh no! We're so sorry to see that. Please DM us photos and order info for a replacement."),
        ("111", "cust_006", "Wed Oct 11 10:40:00 +0000 2023", None, "@AmazonHelp I received the wrong item in my package! I ordered coffee beans and got shoe polish."),
        ("112", "AmazonHelp", "Wed Oct 11 10:43:00 +0000 2023", "111", "@cust_006 Apologies for the mix-up! DM us your order ID so we can set up a quick exchange."),

        # Cancellation
        ("113", "cust_007", "Wed Oct 11 11:00:00 +0000 2023", None, "@AmazonHelp Can I cancel order #113-556677? I placed it 10 minutes ago by mistake."),
        ("114", "AmazonHelp", "Wed Oct 11 11:04:00 +0000 2023", "113", "@cust_007 You can cancel unshipped orders directly under 'Your Orders' or DM us if you need assistance!"),
        
        # Account Security & High Risk
        ("115", "cust_008", "Wed Oct 11 11:10:00 +0000 2023", None, "@AmazonHelp Someone hacked my account and spent $500! Lock it right now!"),
        ("116", "AmazonHelp", "Wed Oct 11 11:12:00 +0000 2023", "115", "@cust_008 We take security seriously. Please call our 24/7 fraud prevention line or DM us immediately."),
        ("117", "cust_009", "Wed Oct 11 11:20:00 +0000 2023", None, "@AmazonHelp Your driver threw my box at my dog! I am suing Amazon with my lawyer!"),
        ("118", "AmazonHelp", "Wed Oct 11 11:22:00 +0000 2023", "117", "@cust_009 We deeply apologize. Escalating this directly to our delivery leadership team. Please DM us your details."),

        # Prime Billing
        ("119", "cust_010", "Wed Oct 11 11:30:00 +0000 2023", None, "@AmazonHelp Why was I charged $139 for Prime membership when I cancelled last month?"),
        ("120", "AmazonHelp", "Wed Oct 11 11:33:00 +0000 2023", "119", "@cust_010 Let's take a look at your account status. Please send us a DM so we can verify the subscription charges."),
    ]
    
    df = pd.DataFrame(sample_data, columns=["tweet_id", "author_id", "created_at", "in_reply_to_status_id", "text"])
    df.to_csv(raw_file, index=False)
    return df

def load_golden_set() -> List[Dict[str, Any]]:
    """Load the 200-example Golden Evaluation Set for @AmazonHelp."""
    if not GOLDEN_SET_PATH.exists():
        raise FileNotFoundError(f"Golden set file not found at {GOLDEN_SET_PATH}")
    
    with open(GOLDEN_SET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
