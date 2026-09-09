import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd
import json
from src.agent import SupportAgent
from data.dataset_loader import load_golden_set
from eval.run_eval import run_evaluation_benchmark

st.set_page_config(
    page_title="@AmazonHelp AI Support Agent | Hiver Take-Home",
    page_icon="📦",
    layout="wide"
)

st.title("📦 @AmazonHelp AI Customer Support Agent")
st.caption("Production AI Support System with Intent Classification, Risk Escalation, RAG Reply Generation & Evaluation Harness")

# Sidebar navigation
st.sidebar.header("Navigation & Settings")
app_mode = st.sidebar.radio(
    "Choose Mode",
    ["🤖 Live Agent Simulator", "📊 Benchmark & Evaluation Harness", "📁 Golden Set Explorer"]
)

agent_mode = st.sidebar.selectbox(
    "Select System Model",
    ["proposed_agent", "simple_ml_baseline", "trivial_baseline"],
    format_func=lambda x: x.upper().replace("_", " ")
)

# Initialize Agent
agent = SupportAgent(mode=agent_mode)

if app_mode == "🤖 Live Agent Simulator":
    st.subheader("Interactive Support Agent Simulator")
    st.markdown("Enter a customer tweet to test classification, risk escalation, and grounded reply generation in real-time.")
    
    preset = st.selectbox(
        "Or choose a sample scenario preset:",
        [
            "Custom Input",
            "Where is my package? Order #114-8742910 was supposed to arrive yesterday!",
            "You charged me twice for order #112-998811! Refund me immediately or I am calling my bank!",
            "Opened my box today and the monitor screen is completely shattered! Bleach leaked everywhere!",
            "Someone hacked my account and bought $500 gift cards! Lock it right now!",
            "Your driver threw my box at my dog! I am suing Amazon with my lawyer!"
        ]
    )
    
    default_text = preset if preset != "Custom Input" else "@AmazonHelp My order #114-998877 is delayed and tracking hasn't updated!"
    user_input = st.text_area("Customer Tweet:", value=default_text, height=100)
    
    if st.button("🚀 Process Message", type="primary"):
        with st.spinner("Processing through AI pipeline..."):
            res = agent.process_message(user_input)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Predicted Intent", res["predicted_intent"])
            with col2:
                st.metric("Intent Confidence", f"{res['intent_confidence'] * 100:.1f}%")
            with col3:
                status = "🚨 ESCALATE TO HUMAN" if res["should_escalate"] else "✅ AUTO-HANDLE"
                st.metric("Escalation Decision", status)
                
            if res["should_escalate"]:
                st.error(f"**Escalation Reason**: {res['escalation_reason']}")
            else:
                st.success("Message safe for automated resolution.")
                
            st.subheader("Drafted @AmazonHelp Reply")
            st.info(res["draft_reply"])

elif app_mode == "📊 Benchmark & Evaluation Harness":
    st.subheader("Headline Evaluation Benchmark")
    st.markdown("Run the complete evaluation suite across all 3 model architectures on the 200-example Golden Evaluation Set.")
    
    if st.button("▶️ Run Evaluation Suite", type="primary"):
        with st.spinner("Evaluating all models on 200 Golden Set examples..."):
            benchmark_results = run_evaluation_benchmark(quick_judge_sample=20)
            
            rows = []
            for mode, data in benchmark_results.items():
                rows.append({
                    "Model Architecture": mode.upper(),
                    "Intent F1": data["intent_classification"]["f1"],
                    "Escalation F1": data["escalation_decision"]["f1"],
                    "Escalation Safety Recall": data["escalation_decision"]["escalation_safety_recall"],
                    "ROUGE-L": data["reply_quality"]["rouge_l"],
                    "Semantic Sim": data["reply_quality"]["semantic_similarity"],
                    "LLM Judge Score (1-5)": data["llm_judge_mean_score"],
                    "Human-Judge Kappa": data["human_judge_agreement"]["cohen_kappa_quadratic"]
                })
            
            df_res = pd.DataFrame(rows)
            st.dataframe(df_res, use_container_width=True)
            st.success("Evaluation benchmark complete!")

elif app_mode == "📁 Golden Set Explorer":
    st.subheader("200-Example Golden Evaluation Set")
    st.markdown("Browse and search through the hand-labelled dataset built for @AmazonHelp.")
    
    golden_data = load_golden_set()
    df_golden = pd.DataFrame(golden_data)
    
    search_query = st.text_input("Search customer messages or intents:", "")
    if search_query:
        df_golden = df_golden[
            df_golden["customer_message"].str.contains(search_query, case=False, na=False) |
            df_golden["gold_intent"].str.contains(search_query, case=False, na=False)
        ]
        
    st.dataframe(df_golden[["id", "gold_intent", "gold_should_escalate", "difficulty", "customer_message"]], use_container_width=True)
