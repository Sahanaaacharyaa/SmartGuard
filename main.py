from models.classifier import ai_guardrail
from utils.baseline import keyword_filter
from utils.category_classifier import classify_category


def analyze_prompt(prompt):
    """
    Runs both AI model and keyword filter
    """
    ai_verdict, score = ai_guardrail(prompt)
    keyword_verdict = keyword_filter(prompt)

    return {
        "prompt": prompt,
        "AI_verdict": ai_verdict,
        "AI_confidence": round(score, 3),
        "Keyword_verdict": keyword_verdict
    }


def final_guardrail(prompt,threshold):
    """
    Final decision logic (IMPROVED HYBRID SYSTEM)
    """

    result = analyze_prompt(prompt)

    ai_verdict = result["AI_verdict"]
    confidence = result["AI_confidence"]
    keyword_verdict = result["Keyword_verdict"]

   
    # Combine AI + keyword intelligently

    if ai_verdict == "UNSAFE" and confidence >= threshold:
        final = "UNSAFE"

    elif keyword_verdict == "UNSAFE" and confidence >= (threshold - 0.2):
        final = "UNSAFE"

    else:
        final = "SAFE"

    result["Final_verdict"] = final

    category = classify_category(prompt)
    result["category"] = category

    return result


if __name__ == "__main__":
    user_input = input("Enter prompt: ")
    output = final_guardrail(user_input)

    print(output)