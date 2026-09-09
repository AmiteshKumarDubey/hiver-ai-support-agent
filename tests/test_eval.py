import pytest
from eval.automated_metrics import evaluate_classification_metrics, evaluate_escalation_metrics, evaluate_reply_metrics
from eval.human_agreement_eval import evaluate_human_judge_agreement

def test_classification_metrics():
    g = ["A", "B", "C"]
    p = ["A", "B", "A"]
    res = evaluate_classification_metrics(g, p)
    assert res["accuracy"] > 0.0
    assert "f1" in res

def test_escalation_metrics():
    g = [True, False, True]
    p = [True, False, False]
    res = evaluate_escalation_metrics(g, p)
    assert res["escalation_safety_recall"] == 0.5

def test_human_judge_agreement():
    h = [4.5, 5.0, 3.0, 4.0]
    j = [4.5, 4.8, 3.2, 4.1]
    res = evaluate_human_judge_agreement(h, j)
    assert res["pearson_correlation"] > 0.5
    assert res["mean_absolute_error"] < 0.5
