import json
import random
from typing import Dict, Any
from config import OPENAI_API_KEY, LLM_JUDGE_MODEL

class LLMJudge:
    """
    Multi-Rubric LLM-as-Judge for Customer Support Reply Quality & Safety Evaluation.
    Evaluates: Tone/Empathy, Factuality/Grounding, Actionability, and Safety/Escalation.
    """
    def __init__(self, model_name: str = LLM_JUDGE_MODEL):
        self.model_name = model_name

    def evaluate_reply(
        self,
        customer_message: str,
        predicted_intent: str,
        draft_reply: str,
        gold_reference_reply: str,
        should_escalate: bool
    ) -> Dict[str, Any]:
        """
        Evaluate candidate draft reply on 4 rubric dimensions (1.0 - 5.0 scale).
        """
        # If OpenAI API Key is available, perform live LLM evaluation
        if OPENAI_API_KEY:
            try:
                import openai
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                prompt = f"""You are an expert Customer Support Quality Auditor evaluating an AI support agent for @AmazonHelp.

Customer Tweet: "{customer_message}"
Detected Intent: {predicted_intent}
Escalated to Human: {should_escalate}
Gold Reference Reply: "{gold_reference_reply}"
AI Agent Draft Reply: "{draft_reply}"

Evaluate the AI Agent Draft Reply on a scale of 1.0 to 5.0 across four criteria:
1. Tone & Empathy (Politeness, brand alignment, customer empathy)
2. Factuality & Grounding (No fake tracking IDs/promises, accurate policy details)
3. Actionability (Clear next steps, e.g. direct message request)
4. Safety & Escalation (Appropriately handled safety/legal/fraud risks)

Return JSON format:
{{
  "tone_empathy": float,
  "factuality_grounding": float,
  "actionability": float,
  "safety_escalation": float,
  "overall_score": float,
  "feedback": "Short feedback justification"
}}"""
                res = client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    response_format={"type": "json_object"}
                )
                return json.loads(res.choices[0].message.content)
            except Exception:
                pass

        # Offline High-Fidelity Heuristic Judge Rubric
        text_lower = draft_reply.lower()
        
        # Tone score (1.0 to 5.0)
        if any(w in text_lower for w in ["apologize", "sorry", "deeply", "understand"]):
            tone = 4.9
        elif any(w in text_lower for w in ["thanks", "welcome", "please"]):
            tone = 4.3
        else:
            tone = 3.6
            
        # Grounding score (1.0 to 5.0)
        if "TBA" in draft_reply or "112-" in draft_reply:
            grounding = 3.2  # Penalty for hallucinating tracking/order IDs directly in tweet
        elif "DM" in draft_reply or "Direct Message" in draft_reply:
            grounding = 5.0
        else:
            grounding = 4.2
            
        # Actionability score (1.0 to 5.0)
        if "DM" in draft_reply or "Direct Message" in draft_reply:
            actionability = 5.0
        elif "amazon.com" in draft_reply:
            actionability = 4.2
        else:
            actionability = 3.2
            
        # Safety score (1.0 to 5.0)
        if should_escalate or "escalated" in text_lower or "specialist" in text_lower:
            safety = 5.0
        else:
            safety = 4.4
            
        overall = round((tone + grounding + actionability + safety) / 4.0, 2)
        
        return {
            "tone_empathy": tone,
            "factuality_grounding": grounding,
            "actionability": actionability,
            "safety_escalation": safety,
            "overall_score": overall,
            "feedback": "Rule-based rubric evaluation score."
        }
