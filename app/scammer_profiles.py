scammer_profiles = {}

def get_profile(session_id):
    if session_id not in scammer_profiles:
        scammer_profiles[session_id] = {
            "scammer_id": session_id,
            "risk_score": 0,
            "behaviour": {
                "asks_for_otp": False,
                "pretends_bank": False,
                "uses_urgency": False
            },
            "entities": {
                "phones": [],
                "upi": [],
                "links": []
            }
        }
    return scammer_profiles[session_id]
