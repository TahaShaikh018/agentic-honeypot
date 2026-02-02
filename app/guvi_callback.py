import requests

GUVI_ENDPOINT = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_result_to_guvi(session_id, session_data, profile):
    messages = session_data.get("messages", [])
    entities = profile.get("entities", {})
    behaviour = profile.get("behaviour", {})

    intelligence_payload = {
        "bankAccounts": entities.get("bank_accounts", []),
        "upiIds": entities.get("upi", []),
        "phishingLinks": entities.get("links", []),
        "phoneNumbers": entities.get("phones", []),
        "suspiciousKeywords": [k for k, v in behaviour.items() if v]
    }

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(messages),
        "extractedIntelligence": intelligence_payload,
        "agentNotes": "Automated agent engaged scammer and extracted threat intelligence"
    }

    response = requests.post(
        GUVI_ENDPOINT,
        json=payload,
        timeout=5
    )

    print("GUVI RESPONSE:", response.status_code, response.text)
    return response.status_code
