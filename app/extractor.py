import re

def extract_intelligence(text: str):
    bank_accounts = re.findall(r"\b\d{9,18}\b", text)
    upi_ids = re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text)
    phone_numbers = re.findall(r"\+?\d{10,13}", text)
    phishing_links = re.findall(r"https?://\S+|www\.\S+", text)

    suspicious_keywords = []
    keywords = ["urgent", "verify", "account", "blocked", "otp", "bank", "prize"]
    for word in keywords:
        if word in text.lower():
            suspicious_keywords.append(word)

    return {
        "bankAccounts": list(set(bank_accounts)),
        "upiIds": list(set(upi_ids)),
        "phoneNumbers": list(set(phone_numbers)),
        "phishingLinks": list(set(phishing_links)),
        "suspiciousKeywords": list(set(suspicious_keywords))
    }
