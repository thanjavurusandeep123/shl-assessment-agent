OFF_TOPIC_KEYWORDS = [
    "legal advice",
    "politics",
    "medical",
    "ignore previous instructions",
    "system prompt",
    "hack"
]


def is_off_topic(text: str):
    lower = text.lower()

    for keyword in OFF_TOPIC_KEYWORDS:
        if keyword in lower:
            return True

    return False
