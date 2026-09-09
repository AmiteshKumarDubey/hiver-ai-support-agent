import math
from collections import Counter
from typing import List, Dict, Any
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_n_gram_overlap(reference: str, candidate: str, n: int = 1) -> float:
    """Helper to compute n-gram overlap (ROUGE / BLEU proxy)."""
    ref_words = reference.lower().split()
    cand_words = candidate.lower().split()
    
    if len(cand_words) == 0 or len(ref_words) == 0:
        return 0.0
        
    ref_ngrams = [tuple(ref_words[i:i+n]) for i in range(len(ref_words)-n+1)]
    cand_ngrams = [tuple(cand_words[i:i+n]) for i in range(len(cand_words)-n+1)]
    
    if not ref_ngrams or not cand_ngrams:
        return 0.0
        
    ref_counts = Counter(ref_ngrams)
    cand_counts = Counter(cand_ngrams)
    
    overlap = sum((ref_counts & cand_counts).values())
    precision = overlap / len(cand_ngrams)
    recall = overlap / len(ref_ngrams)
    
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def calculate_lcs_rouge(reference: str, candidate: str) -> float:
    """Compute Longest Common Subsequence ROUGE-L score."""
    ref = reference.lower().split()
    cand = candidate.lower().split()
    m, n = len(ref), len(cand)
    if m == 0 or n == 0:
        return 0.0
        
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if ref[i] == cand[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
                
    lcs_len = dp[m][n]
    rec = lcs_len / m
    prec = lcs_len / n
    if rec + prec == 0:
        return 0.0
    return (2 * prec * rec) / (prec + rec)

def compute_semantic_similarity(references: List[str], candidates: List[str]) -> List[float]:
    """Compute cosine semantic similarity using TF-IDF word representations."""
    sims = []
    vectorizer = TfidfVectorizer()
    for ref, cand in zip(references, candidates):
        try:
            tfidf = vectorizer.fit_transform([ref, cand])
            sim = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
        except Exception:
            sim = 0.5
        sims.append(sim)
    return sims

def evaluate_classification_metrics(gold_labels: List[str], pred_labels: List[str]) -> Dict[str, float]:
    """Compute Accuracy, Precision, Recall, F1 for Intent Classification."""
    acc = accuracy_score(gold_labels, pred_labels)
    p, r, f1, _ = precision_recall_fscore_support(gold_labels, pred_labels, average="weighted", zero_division=0)
    return {
        "accuracy": round(float(acc), 4),
        "precision": round(float(p), 4),
        "recall": round(float(r), 4),
        "f1": round(float(f1), 4)
    }

def evaluate_escalation_metrics(gold_escalates: List[bool], pred_escalates: List[bool]) -> Dict[str, float]:
    """
    Compute Escalation Precision, Recall, F1, and Escalation Safety Recall.
    Escalation Safety Recall measures how effectively critical/risky tickets are caught.
    """
    acc = accuracy_score(gold_escalates, pred_escalates)
    p, r, f1, _ = precision_recall_fscore_support(gold_escalates, pred_escalates, average="binary", zero_division=0)
    
    # Escalation Safety Recall (Recall on true positives)
    tp = sum(1 for g, p in zip(gold_escalates, pred_escalates) if g and p)
    fn = sum(1 for g, p in zip(gold_escalates, pred_escalates) if g and not p)
    safety_recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0

    return {
        "accuracy": round(float(acc), 4),
        "precision": round(float(p), 4),
        "recall": round(float(r), 4),
        "f1": round(float(f1), 4),
        "escalation_safety_recall": round(float(safety_recall), 4)
    }

def evaluate_reply_metrics(gold_replies: List[str], draft_replies: List[str]) -> Dict[str, float]:
    """Compute ROUGE-1, ROUGE-2, ROUGE-L, and Semantic Similarity."""
    rouge1_list = [calculate_n_gram_overlap(g, d, n=1) for g, d in zip(gold_replies, draft_replies)]
    rouge2_list = [calculate_n_gram_overlap(g, d, n=2) for g, d in zip(gold_replies, draft_replies)]
    rougel_list = [calculate_lcs_rouge(g, d) for g, d in zip(gold_replies, draft_replies)]
    sem_sims = compute_semantic_similarity(gold_replies, draft_replies)

    return {
        "rouge1": round(sum(rouge1_list) / len(rouge1_list), 4),
        "rouge2": round(sum(rouge2_list) / len(rouge2_list), 4),
        "rouge_l": round(sum(rougel_list) / len(rougel_list), 4),
        "semantic_similarity": round(sum(sem_sims) / len(sem_sims), 4)
    }
