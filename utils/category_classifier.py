def classify_category(prompt):
    p = prompt.lower()

   
    if any(x in p for x in ["kill", "hurt", "bomb", "harm", "attack", "weapon", "fraud", "steal"]):
        return "harmful"

   
    elif any(x in p for x in [
        "dan", "bypass", "no restrictions", "ignore rules",
        "override", "jailbreak", "hack", "exploit", "malware"
    ]):
        return "jailbreak"

    elif any(x in p for x in [
        "summarize", "hidden", "inject", "secret",
        "confidential", "reveal", "system prompt"
    ]):
        return "prompt_injection"

   
    elif any(x in p for x in [
        "hate", "abuse", "racist", "insult"
    ]):
        return "toxic"

    return "general"