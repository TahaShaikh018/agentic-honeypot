# app/scam_detector.py

SCAM_KEYWORDS = [
    "blocked", "verify", "urgent", "upi",
    "account", "suspend", "kyc",
    "otp", "click", "link", "bank"
]

def rule_based_detection(text: str) -> bool:
    text = text.lower()
    score = 0

    for word in SCAM_KEYWORDS:
        if word in text:
            score += 1

    # if 2 or more scam keywords → likely scam
    return score >= 2
