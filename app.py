import streamlit as st
import matplotlib.pyplot as plt
from main import final_guardrail
from evaluation.evaluate import run_evaluation
from collections import Counter
import json
import time

st.set_page_config(page_title="🛡️ SmartGuard Dashboard", layout="wide")
st.title("🛡️ SmartGuard - LLM Firewall")

st.sidebar.header("⚙️ Settings")
threshold = st.sidebar.slider("Set Strictness Threshold", 0.1, 0.9, 0.7, 0.05)

tab_live, tab_metrics, tab_curve, tab_latency = st.tabs([
    "Live Prompt", 
    "Aggregate Metrics", 
    "Accuracy vs Threshold", 
    "Latency Test"
])


with tab_live:
    st.subheader("🔹 Live Prompt Analysis")
    user_input = st.text_area("Enter Prompt here:")

    if st.button("Analyze Prompt"):
        if not user_input.strip():
            st.warning("Please enter a prompt")
        else:
            result = final_guardrail(user_input, threshold)
            verdict = result["Final_verdict"]
            confidence = result["AI_confidence"]
            category = result["category"]

            if verdict == "SAFE":
                st.success("✅ SAFE")
            else:
                st.error("⚠️ UNSAFE")

            st.write(f"**Confidence:** {confidence}")
            st.write(f"**Category:** {category}")



with tab_metrics:
    st.subheader("🔹 Red-Team Evaluation Metrics")

    @st.cache_data
    def compute_metrics(thresh):
        tp, tn, fp, fn, acc = run_evaluation(thresh)

        # Per-category breakdown
        with open("data/redteam.json", "r") as f:
            data = json.load(f)

        category_counts = Counter()
        for item in data:
            result = final_guardrail(item["prompt"], thresh)
            if result["Final_verdict"] == "UNSAFE":
                category_counts[result["category"]] += 1

        return tp, tn, fp, fn, acc, category_counts

    if st.button("Compute Aggregate Metrics"):
        tp, tn, fp, fn, acc, category_counts = compute_metrics(threshold)

     
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Blocked (TP)", tp)
        col2.metric("Missed (FN)", fn)
        col3.metric("False Positives (FP)", fp)
        col4.metric("Accuracy", f"{round(acc*100,2)}%")

  
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        block_rate = recall  # same as recall

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Precision", f"{round(precision, 2)}")
        col6.metric("Recall (Block Rate)", f"{round(recall, 2)}")
        col7.metric("F1 Score", f"{round(f1, 2)}")
        col8.metric("False Positive Rate", f"{round(fpr, 2)}")

       
        st.info(f"""
 **Model Performance:**
- Block Rate: {round(block_rate*100,2)}%
- FPR: {round(fpr*100,2)}%
""")

        labels = ['TP', 'TN', 'FP', 'FN']
        values = [tp, tn, fp, fn]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_title("Confusion Matrix")
        st.pyplot(fig)

    
        st.subheader("🔹 Per-Category Unsafe Counts")

        categories = list(category_counts.keys())
        counts = list(category_counts.values())

        if categories:
            fig2, ax2 = plt.subplots()
            ax2.bar(categories, counts)
            ax2.set_ylabel("Count")
            ax2.set_title("Blocked Prompts per Category")
            st.pyplot(fig2)
        else:
            st.write("No unsafe prompts detected in any category at this threshold.")



with tab_curve:
    st.subheader("🔹 Accuracy vs Strictness (Recall & False Positive Rate)")

    @st.cache_data
    def compute_curve():
        thresholds = [round(x*0.1, 1) for x in range(1, 10)]
        recall_list, fpr_list, accuracy_list = [], [], []

        for t in thresholds:
            tp, tn, fp, fn, acc = run_evaluation(t)

            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

            recall_list.append(recall)
            fpr_list.append(fpr)
            accuracy_list.append(acc)

        return thresholds, recall_list, fpr_list, accuracy_list

    if st.button("Plot Accuracy Curve"):
        th, recall_values, fpr_values, acc_values = compute_curve()

        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(th, acc_values, marker='o', linestyle='-', label='Accuracy')
        ax.plot(th, recall_values, marker='x', linestyle='--', label='Recall')
        ax.plot(th, fpr_values, marker='s', linestyle='-.', label='False Positive Rate')

        ax.set_xlabel("Threshold")
        ax.set_ylabel("Rate / Accuracy")
        ax.set_title("Accuracy, Recall & FPR vs Threshold")
        ax.set_ylim(0, 1)
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)


with tab_latency:
    st.subheader("🔹 Latency Test on Red-Team Prompts")

    threshold_latency = st.slider("Set Threshold for Latency Test", 0.1, 0.9, 0.7, 0.05)

    if st.button("Run Latency Test"):
        with open("data/redteam.json", "r") as f:
            data = json.load(f)

        times = []
        progress = st.progress(0)
        total = len(data)

        for i, item in enumerate(data):
            start = time.time()
            final_guardrail(item["prompt"], threshold_latency)
            end = time.time()

            times.append(end - start)
            progress.progress((i+1)/total)

        times.sort()

        p95 = times[int(0.95 * len(times))]
        avg = sum(times) / len(times)

        st.success("Latency Test Completed!")
        st.write(f"**Average Latency:** {round(avg, 4)} sec per prompt")
        st.write(f"**P95 Latency:** {round(p95, 4)} sec per prompt")