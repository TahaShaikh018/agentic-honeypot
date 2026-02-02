from fastapi import FastAPI, Depends
from app.auth import verify_api_key
from app.sessions import get_session
from app.agent_brain import honeypot_reply
from app.extractor import extract_intelligence
from app.scammer_profiles import get_profile, scammer_profiles
from app.threat_engine import get_threat_level
from app.scammer_graph import build_graph
from app.intel_analytics import global_stats, top_entities, scam_patterns

app = FastAPI(
    title="AGENTIC HONEYPOT — AI Scam Detection API",
    description="""
Agentic Honeypot for Scam Detection & Threat Intelligence.

Features:
- Scam intent detection
- Autonomous AI engagement
- Intelligence extraction
- Threat profiling
- GUVI final callback integration
""",
    version="1.0.0"
)

@app.post("/honeypot")
def honeypot_endpoint(payload: dict, api_key: str = Depends(verify_api_key)):
    session_id = payload.get("sessionId")
    message = payload.get("message")
    text = message.get("text", "")

    session = get_session(session_id)

    session["messages"].append(message)
    session["total_messages"] += 1

    # Extract Intelligence
    intelligence = extract_intelligence(text)
    for key in session["intelligence"]:
        session["intelligence"][key].extend(intelligence[key])
        session["intelligence"][key] = list(set(session["intelligence"][key]))

    # Update Scammer Profile
    profile = get_profile(session_id)

    text_lower = text.lower()
    if "otp" in text_lower:
        profile["behaviour"]["asks_for_otp"] = True
        profile["risk_score"] += 30
    if "bank" in text_lower or "rbi" in text_lower or "gov" in text_lower:
        profile["behaviour"]["impersonation"] = True
        profile["risk_score"] += 25
    if "urgent" in text_lower or "blocked" in text_lower or "10 minutes" in text_lower:
        profile["behaviour"]["uses_urgency"] = True
        profile["risk_score"] += 20
    if "upi" in text_lower:
        profile["behaviour"]["payment_request"] = True
        profile["risk_score"] += 25
    if "http" in text_lower or "www" in text_lower:
        profile["behaviour"]["phishing_link"] = True
        profile["risk_score"] += 25
    if "telegram" in text_lower or "whatsapp" in text_lower:
        profile["behaviour"]["off_platform_redirect"] = True
        profile["risk_score"] += 20
    if "0x" in text_lower:
        profile["behaviour"]["crypto_fraud"] = True
        profile["risk_score"] += 30
    
    profile["risk_score"] = min(profile["risk_score"], 100)
    profile["threat_level"] = get_threat_level(profile["risk_score"])

    # AUTOMATIC CALLBACK LOGIC
    if profile["risk_score"] >= 70:
        from app.guvi_callback import send_final_result_to_guvi
        send_final_result_to_guvi(session_id, session, profile)

    # add entities
    profile["entities"]["phones"] += intelligence["phoneNumbers"]
    profile["entities"]["upi"] += intelligence["upiIds"]
    profile["entities"]["links"] += intelligence["phishingLinks"]

    # Agent Brain Reply
    reply = honeypot_reply(session_id, profile, session["messages"])

    return {
        "status": "success",
        "scamDetected": session["scam_detected"],
        "reply": reply
    }

@app.get("/debug/{session_id}")
def debug_session(session_id: str):
    session = get_session(session_id)
    return session

@app.get("/scammer/{session_id}")
def get_scammer_profile(session_id: str):
    return scammer_profiles.get(session_id, {"error": "No such scammer"})

@app.get("/graph")
def get_graph():
    try:
        return build_graph()
    except Exception as e:
        return {"error": str(e)}

@app.get("/intel/stats")
def intel_stats():
    return global_stats()

@app.get("/intel/top-entities")
def intel_entities():
    return top_entities()

@app.get("/intel/patterns")
def intel_patterns():
    return scam_patterns()