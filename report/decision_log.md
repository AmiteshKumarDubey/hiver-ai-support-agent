# Technical Decision Log: 15 Non-Obvious Engineering Decisions

This document details 15 non-obvious technical and architectural decisions made while building the `@AmazonHelp` AI Customer Support Agent and Evaluation Harness.

---

### 1. Choice of Brand (@AmazonHelp)
- **Decision**: Selected `@AmazonHelp` over telecommunications (@TMobile) or hardware (@AppleSupport).
- **Rationale**: E-commerce customer service presents the highest diversity of distinct transactional intents (shipping, refunds, damaged items, billing) and high-stakes safety risks (leaks, legal threats, compromised accounts).
- **Trade-off**: Higher dataset complexity and noisy multi-turn Twitter thread structures.

---

### 2. Taxonomy Scope (7 Mutually Exclusive Intents)
- **Decision**: Constrained taxonomy to 7 core intents rather than granular sub-intents (e.g., merging "damaged item" and "wrong item" into `DAMAGED_ITEM`).
- **Rationale**: High taxonomy granularity in zero-shot classification causes intent boundary blur and degrades LLM judge agreement.
- **Trade-off**: Requires secondary classification downstream if specific sub-routing is required.

---

### 3. Dual-Tier Safety & Risk Escalation Architecture
- **Decision**: Separated intent classification from escalation evaluation using an explicit multi-factor `EscalationEngine`.
- **Rationale**: Relying on an LLM to simultaneously generate text and decide escalation leads to safety bypasses on subtle adversarial prompts.
- **Trade-off**: Slight execution overhead due to double-pass policy checking.

---

### 4. Zero-Hallucination Policy Constraint in RAG Prompts
- **Decision**: Strictly prohibited the LLM from generating hypothetical tracking numbers (e.g., `TBA...`) or refund transaction IDs in tweet drafts.
- **Rationale**: Generating synthetic tracking IDs causes customer panic and support burden.
- **Trade-off**: Responses must consistently ask the user to Direct Message (DM) `@AmazonHelp` for order verification.

---

### 5. Multi-Rubric LLM-as-Judge Framework
- **Decision**: Evaluated reply quality across 4 independent 1-5 sub-scales (Tone, Factuality, Actionability, Safety) rather than a single holistic score.
- **Rationale**: Holistic LLM scores suffer from "positivity bias" where polite tone masks severe policy/safety failures.
- **Trade-off**: Increased LLM judge token cost and evaluation latency.

---

### 6. Escalation Safety Recall as a Core Headline Metric
- **Decision**: Introduced **Escalation Safety Recall** (recall specifically on true positive risk tickets) alongside standard F1-score.
- **Rationale**: In customer support, a False Negative (failing to escalate a legal/safety threat) is 100x more costly than a False Positive (over-escalating a routine query).
- **Trade-off**: System operates with a conservative bias towards human escalation on boundary cases.

---

### 7. Synthetic Golden Set Augmentation with Real Twitter Noise
- **Decision**: Constructed the 200-example Golden Evaluation Set with exact Kaggle `@AmazonHelp` noise patterns (typos, abbreviations, missing punctuation, hostile tone).
- **Rationale**: Evaluating purely on polished academic prompts inflates headline accuracy by 15-20%.
- **Trade-off**: Requires careful manual validation to prevent ground-truth label ambiguity.

---

### 8. Cohen’s Quadratic Weighted Kappa for Judge Agreement
- **Decision**: Used Quadratic Weighted Kappa rather than unweighted Kappa to evaluate Human-vs-Judge agreement.
- **Rationale**: Quadratic weighting penalizes extreme rating disagreements (e.g., Human 5 vs Judge 1) far more severely than minor variations (Human 5 vs Judge 4).
- **Trade-off**: Requires discrete score discretization across evaluation samples.

---

### 9. ROUGE-L and Semantic Cosine Dual Reply Metrics
- **Decision**: Evaluated draft replies using both n-gram overlap (ROUGE-L) and vector TF-IDF cosine similarity.
- **Rationale**: ROUGE-L captures exact policy keyword matching (e.g., "3-5 business days"), while semantic similarity captures tone paraphrasing.
- **Trade-off**: Metric disagreement on short (<20 word) Twitter support replies.

---

### 10. Hybrid Keyword + Embedding Intent Fallback
- **Decision**: Built a hybrid fallback mechanism that combines TF-IDF probability matrices with keyword rule scores when offline.
- **Rationale**: Ensures the evaluation harness runs 100% deterministically and offline without requiring cloud API keys.
- **Trade-off**: Requires maintaining keyword lists for cold-start initialization.

---

### 11. Strict Twitter 280-Character Boundary Guardrail
- **Decision**: Enforced hard character truncation and prompt constraints (<280 chars) on all drafted replies.
- **Rationale**: `@AmazonHelp` operates on Twitter/X where wordy multi-paragraph email templates are rejected by platform constraints.
- **Trade-off**: Requires concise phrasing and standard DM call-to-action phrasing.

---

### 12. Pre-computed Grounding Context Retrieval (RAG Indexing)
- **Decision**: Index historical `@AmazonHelp` tweet response pairs for RAG context insertion into the prompt.
- **Rationale**: Grounding LLM replies in actual brand historical resolutions prevents policy hallucination (e.g., promising free 1-day shipping on non-Prime accounts).
- **Trade-off**: RAG retrieval quality depends on initial vector index coverage.

---

### 13. Sub-2-Minute Benchmark Execution Pipeline
- **Decision**: Optimized the benchmark runner (`eval/run_eval.py`) to execute all 200 Golden Set evaluations across all 3 models in < 2 minutes.
- **Rationale**: Hiver assignment instructions mandate that reviewers must be able to reproduce headline results in < 15 minutes.
- **Trade-off**: Uses quick judge sampling (50 examples) for LLM rubric scoring during rapid test runs.

---

### 14. Explicit Reason Generation for Human Escalation
- **Decision**: Every escalated ticket must output an explicit, human-readable `escalation_reason` string (e.g., "Legal threat or attorney involvement").
- **Rationale**: Human support agents receiving escalated tickets need instant context to prioritize urgency queues.
- **Trade-off**: Requires structured metadata formatting in output payloads.

---

### 15. Standalone Interactive UI Demo (`app.py`)
- **Decision**: Developed a Streamlit web application providing real-time agent simulation, golden set browsing, and live metric calculation.
- **Rationale**: Technical reviewers can interactively stress-test edge cases and inspect RAG context in real-time.
- **Trade-off**: Adds Streamlit dependency to `requirements.txt`.
