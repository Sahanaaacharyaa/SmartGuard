from transformers import pipeline

# load model once (global)
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def ai_guardrail(prompt, threshold=0.6):
    
    result = classifier(prompt)[0]
    
    score = result["score"]
    label = result["label"]
    
    if label == "NEGATIVE" and score > threshold:
        return "UNSAFE", score
    else:
        return "SAFE", score