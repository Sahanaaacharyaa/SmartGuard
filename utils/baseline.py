def keyword_filter(prompt):

    prompt = prompt.lower()

    unsafe_keywords = [
        # hacking / cyber
        "hack", "bypass", "exploit", "malware", "virus", "phishing","confidential",

        # violence / harm
        "kill", "hurt", "harm", "attack", "bomb", "weapon","evil AI",

        # illegal activities
        "steal", "fraud", "scam", "blackmail", "cheat","hack", "perform attack", "bypass security",

        # manipulation
        "manipulate", "brainwash","ignore previous","secretly","output dangerous","extract","reveal","hidden commands","secrets",

        # jailbreak patterns
        "ignore all rules", "bypass restrictions", "no restrictions",
        "act as", "pretend to", "override", "jailbreak","break into systems","ignore"
    ]

    for word in unsafe_keywords:
        if word in prompt:
            return "UNSAFE"

    return "SAFE"