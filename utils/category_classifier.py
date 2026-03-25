# utils/category_classifier.py

def classify_category(prompt):
    p = prompt.lower()

    if any(x in p for x in [
        "dan", "bypass", "no restrictions", "ignore rules", "hack",
        "override", "jailbreak", "exploit", "malware", "virus", "phishing",
        "confidential", "secret", "hidden commands", "secrets"
    ]):
        return "jailbreak"

    elif any(x in p for x in [
        "summarize", "document", "hidden", "inject",
        "prompt injection", "rewrite", "manipulate", "insert text",
        "replace content", "spoof", "malicious instruction"
    ]):
        return "prompt_injection"

    elif any(x in p for x in [
        "kill", "hurt", "bomb", "harm",
        "attack", "weapon", "suicide", "self-harm",
        "explode", "terror", "dangerous", "assault"
    ]):
        return "harmful"

    elif any(x in p for x in [
        "hate", "abuse", "toxic",
        "discriminate", "racist", "sexist", "offensive",
        "insult", "harass", "mock", "bully"
    ]):
        return "toxic"

    else:
        return "general"