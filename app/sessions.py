sessions = {}

def get_session(session_id):
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "total_messages": 0,
            "scam_detected": False,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phoneNumbers": [],
                "phishingLinks": [],
                "suspiciousKeywords": []
            }
        }
    return sessions[session_id]
