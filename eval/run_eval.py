import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import time
from typing import Dict, Any, List
from tabulate import tabulate
from data.dataset_loader import load_golden_set

from src.agent import SupportAgent
from eval.automated_metrics import evaluate_classification_metrics, evaluate_escalation_metrics, evaluate_reply_metrics
from eval.llm_judge import LLMJudge
from eval.human_agreement_eval import evaluate_human_judge_agreement
from config import REPORT_DIR

def run_evaluation_benchmark(quick_judge_sample: int = 50) -> Dict[str, Any]:
    """
    Run complete evaluation harness across all 3 models on 200 Golden Set examples.
    """
    golden_set = load_golden_set()
    print(f"Loaded {len(golden_set)} golden evaluation examples.")

    modes = ["trivial_baseline", "simple_ml_baseline", "proposed_agent"]
    results = {}
    judge = LLMJudge()

    for mode in modes:
        print(f"\nEvaluating System Mode: {mode}...")
        agent = SupportAgent(mode=mode)
        
        start_time = time.time()
        
        gold_intents = []
        pred_intents = []
        gold_escalates = []
        pred_escalates = []
        gold_replies = []
        draft_replies = []
        
        human_overall_scores = []
        judge_overall_scores = []

        for idx, item in enumerate(golden_set):
            msg = item["customer_message"]
            out = agent.process_message(msg)
            
            gold_intents.append(item["gold_intent"])
            pred_intents.append(out["predicted_intent"])
            
            gold_escalates.append(item["gold_should_escalate"])
            pred_escalates.append(out["should_escalate"])
            
            gold_replies.append(item["gold_reference_reply"])
            draft_replies.append(out["draft_reply"])
            
            # Subsample for LLM judge score to maintain sub-minute pipeline execution
            if idx < quick_judge_sample:
                j_eval = judge.evaluate_reply(
                    customer_message=msg,
                    predicted_intent=out["predicted_intent"],
                    draft_reply=out["draft_reply"],
                    gold_reference_reply=item["gold_reference_reply"],
                    should_escalate=out["should_escalate"]
                )
                judge_overall_scores.append(j_eval["overall_score"])
                human_overall_scores.append(item["human_annotations"]["overall_quality"])

        elapsed_time = round(time.time() - start_time, 2)

        # Compute Automated Metrics
        intent_metrics = evaluate_classification_metrics(gold_intents, pred_intents)
        escalation_metrics = evaluate_escalation_metrics(gold_escalates, pred_escalates)
        reply_metrics = evaluate_reply_metrics(gold_replies, draft_replies)
        
        # Human vs Judge Agreement Evaluation
        agreement_metrics = evaluate_human_judge_agreement(human_overall_scores, judge_overall_scores)

        mode_summary = {
            "mode": mode,
            "execution_time_seconds": elapsed_time,
            "intent_classification": intent_metrics,
            "escalation_decision": escalation_metrics,
            "reply_quality": reply_metrics,
            "llm_judge_mean_score": round(sum(judge_overall_scores) / len(judge_overall_scores), 2),
            "human_judge_agreement": agreement_metrics
        }
        results[mode] = mode_summary

    # Display Headline Benchmark Table
    print_benchmark_table(results)
    
    # Save benchmark result JSON to report directory
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = REPORT_DIR / "benchmark_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nBenchmark results saved to {out_file}")

    return results

def print_benchmark_table(results: Dict[str, Any]):
    """Format and print benchmark results comparison table."""
    headers = [
        "System Model",
        "Intent F1",
        "Escalation F1",
        "Escalation Safety Recall",
        "ROUGE-L",
        "Semantic Sim",
        "Judge Score (1-5)",
        "Judge-Human Kappa"
    ]
    rows = []
    for mode, data in results.items():
        rows.append([
            mode.upper(),
            data["intent_classification"]["f1"],
            data["escalation_decision"]["f1"],
            data["escalation_decision"]["escalation_safety_recall"],
            data["reply_quality"]["rouge_l"],
            data["reply_quality"]["semantic_similarity"],
            data["llm_judge_mean_score"],
            data["human_judge_agreement"]["cohen_kappa_quadratic"]
        ])
    
    print("\n=================== HEADLINE BENCHMARK RESULTS ===================")
    print(tabulate(rows, headers=headers, tablefmt="github"))
    print("==================================================================\n")

if __name__ == "__main__":
    run_evaluation_benchmark()
