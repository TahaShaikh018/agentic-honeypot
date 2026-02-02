from app.llm_client import ask_llm

def scam_detection(text: str) -> bool:
    prompt = f"""
You are a strict scam detection system.

Classify the following message as either:
SCAM or NOT_SCAM

Message:
"{text}"

Rules:
- If it involves urgency, links, threats, verification, OTP, prizes, bank, account -> SCAM
- Answer with ONLY one word: SCAM or NOT_SCAM
"""

    result = ask_llm(prompt).strip().upper()
    return result.strip() == "SCAM"