from transformers import pipeline

# Load model once
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# ✅ 1. Benign query filter (reduces false positives)
SAFE_PREFIXES = [
    "what is", "explain", "define", "how does", "how do",
    "give tips", "write", "benefits of", "examples of"
]

def is_obviously_safe(prompt):
    prompt = prompt.lower().strip()
    return any(prompt.startswith(p) for p in SAFE_PREFIXES)


def ai_guardrail(prompt, threshold=0.9):
    """
    Improved AI guardrail with:
    - benign filtering
    - higher threshold
    """

    # ✅ Step 1: Allow clearly safe queries
    if is_obviously_safe(prompt):
        return "SAFE", 1.0

    # ✅ Step 2: Run model
    result = classifier(prompt)[0]

    score = result["score"]
    label = result["label"]

    # ✅ Step 3: Strict unsafe condition
    if label == "NEGATIVE" and score > threshold:
        return "UNSAFE", score

    # ✅ Step 4: Default safe
    return "SAFE", score