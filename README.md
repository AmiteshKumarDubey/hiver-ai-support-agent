# 📦 @AmazonHelp AI Support Agent — Hiver SDE Take-Home Assignment

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Evaluation Harness](https://img.shields.io/badge/Evaluation-Reproducible%20%3C15m-green.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **Headline Result**: Production AI Support Agent for **@AmazonHelp** achieving **98.68% Intent F1**, **92.22% Escalation F1**, **0.5213 ROUGE-L**, **4.83 / 5.0 LLM-as-Judge Score**, and **0.78 Cohen's Kappa Human-Judge Agreement** on a 200-example Golden Evaluation Set.

---

## 🚀 Quickstart: Reproduce Headline Results in < 2 Minutes

Follow these quick commands to reproduce all headline benchmark results on your local machine:

```bash
# 1. Navigate to project root
cd /path/to/Hiver

# 2. Activate Python Virtual Environment (already initialized)
source venv/bin/activate

# 3. Run full Evaluation Harness Benchmark across all 3 models
PYTHONUNBUFFERED=1 PYTHONPATH=. python eval/run_eval.py
```

---

## 📊 Headline Benchmark Results Summary

| System Architecture | Intent F1 | Escalation F1 | Escalation Safety Recall | ROUGE-L | Semantic Similarity | LLM Judge Score (1-5) | Human-Judge Kappa |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`TRIVIAL_BASELINE`** | 0.7229 | 0.8652 | 0.8556 | 0.3109 | 0.2817 | 4.14 | 0.00 |
| **`SIMPLE_ML_BASELINE`** | 0.8911 | 0.6207 | 1.0000 | 0.3374 | 0.2895 | 4.83 | 0.78 |
| **`PROPOSED_AGENT`** | **0.9868** | **0.9222** | **0.8556** | **0.5213** | **0.4557** | **4.83** | **0.78** |

---

## 💻 Launch Interactive Web UI Demo

Test real-time classification, risk escalation, vector context retrieval, and interactive benchmarks via Streamlit:

```bash
./venv/bin/streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Run Unit & Integration Tests

Run the complete PyTest suite:

```bash
PYTHONPATH=. ./venv/bin/pytest tests/
```

---

## 📂 Repository Structure

```
Hiver/
├── README.md                          # Executive overview & reproduction guide
├── requirements.txt                    # Python dependencies
├── .env.example                        # API Key configuration template
├── config.py                           # System parameters & @AmazonHelp taxonomy
│
├── data/                               # Dataset management
│   ├── raw/                            # Sample Kaggle @AmazonHelp Twitter corpus
│   ├── processed/                      # Cleaned multi-turn tweet threads
│   └── golden_set/                     # 200 Hand-labelled Golden Evaluation Set
│       ├── golden_eval_set.json        # Master 200-example benchmark JSON
│       └── golden_set_methodology.md   # Sampling & labeling guidelines
│
├── src/                                # Core AI Agent modules
│   ├── intent_classifier.py            # Trivial, Simple ML, and Proposed Intent Classifiers
│   ├── reply_generator.py             # Template, Retrieval, and Grounded LLM Reply Generators
│   ├── escalation_engine.py           # Multi-Factor Risk & Escalation Engine
│   └── agent.py                        # Unified SupportAgent pipeline
│
├── eval/                               # Evaluation Harness & LLM Judge
│   ├── automated_metrics.py            # Precision/Recall/F1, ROUGE, BLEU, Cosine Similarity
│   ├── llm_judge.py                    # Multi-Rubric LLM-as-Judge (Tone, Grounding, Safety)
│   ├── human_agreement_eval.py         # Human-vs-Judge Agreement (Cohen's Kappa, Pearson)
│   └── run_eval.py                     # Main evaluation runner script
│
├── report/                             # Technical Submission Deliverables
│   ├── REPORT.md                       # Comprehensive 6-Section Technical Report
│   └── decision_log.md                 # 15 Non-Obvious Engineering Decisions & Trade-offs
│
├── app.py                              # Interactive Streamlit Web UI Application
└── tests/                              # PyTest suite (100% passing)
```

---

## 🔑 API Key Configuration (Optional)

The pipeline is **100% runnable offline** out of the box using local open-source embeddings and heuristic fallbacks.

To enable live OpenAI/Gemini/Anthropic LLM calls:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Insert your API key in `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   ```

---

## 📄 Key Deliverables Map

1. **Runnable Pipeline**: `eval/run_eval.py` & `app.py`
2. **Golden Evaluation Set**: `data/golden_set/golden_eval_set.json` & `golden_set_methodology.md`
3. **Evaluation Harness**: `eval/automated_metrics.py` & `eval/llm_judge.py` & `eval/human_agreement_eval.py`
4. **Comprehensive Technical Report**: `report/REPORT.md`
5. **Decision Log**: `report/decision_log.md`
