# Golden Evaluation Set Methodology: @AmazonHelp Customer Support

## 1. Executive Summary
To rigorously evaluate the AI Support Agent for **@AmazonHelp**, we constructed a high-diversity **Golden Evaluation Set of 200 hand-curated customer support messages**. This dataset serves as the benchmark for testing Intent Classification, Risk Escalation, Reply Quality (ROUGE, BLEU, Semantic Similarity), and LLM-as-Judge agreement.

---

## 2. Sampling Strategy & Intent Breakdown
The golden set was sampled to reflect the real-world distribution of customer inquiries directed at `@AmazonHelp` on Twitter, with deliberate oversampling of edge cases and high-risk policy scenarios.

| Intent Category | Count | Distribution (%) | Primary Topic Focus |
| :--- | :---: | :---: | :--- |
| **`ORDER_TRACKING`** | 40 | 20.0% | Shipping delays, missing packages, courier updates, out-of-delivery status |
| **`REFUND_REQUEST`** | 35 | 17.5% | Return processing times, double charges, missing refunds, bank disputes |
| **`DAMAGED_ITEM`** | 35 | 17.5% | Broken screens, shattered items, wrong items received, hazardous leaks |
| **`CANCELLATION`** | 25 | 12.5% | Post-purchase cancellation, order modification, accidental purchases |
| **`ACCOUNT_SECURITY`** | 25 | 12.5% | Compromised accounts, unauthorized gift card purchases, 2FA issues |
| **`PRIME_BILLING`** | 20 | 10.0% | Subscription auto-renewal charges, Prime Student double billing |
| **`GENERAL_INQUIRY`** | 20 | 10.0% | Support hours, international shipping, legal/BBB complaints, feedback |
| **TOTAL** | **200** | **100.0%** | **Comprehensive @AmazonHelp Coverage** |

---

## 3. Difficulty & Risk Distribution
Inquiries were categorized across 4 difficulty tiers:
1. **Easy (45%)**: Standard customer queries with clear intent keywords and straightforward resolution.
2. **Medium (30%)**: Multi-sentence inquiries containing mild frustration or implicit intent hints.
3. **Hard (18%)**: Ambiguous or multi-intent messages requiring intent disambiguation and risk policy check.
4. **Adversarial (7%)**: Highly hostile messages, legal/lawyer threats, physical safety hazards, or account takeover alerts demanding immediate human escalation.

---

## 4. Labeling Schema & Ground Truth Guidelines
Each example in the golden set contains the following annotations:
- `customer_message`: Raw tweet string.
- `gold_intent`: One of the 7 predefined `@AmazonHelp` intents.
- `gold_should_escalate`: Boolean (`true`/`false`) indicating whether auto-handling is safe or human escalation is mandatory.
- `gold_escalation_reason`: Stated policy reason for escalation (e.g., "Legal threat or regulatory notice", "Physical safety hazard", "Security compromise").
- `gold_reference_reply`: High-quality human support agent reference reply adhering strictly to Amazon's Twitter support guidelines (concise, polite, requiring DM for account details).
- `human_annotations`: Numerical human expert ratings (1.0 to 5.0 scale) across Tone/Empathy, Factuality/Grounding, Safety, and Overall Quality for judge agreement testing.
