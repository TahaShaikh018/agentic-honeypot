# app/intel_analytics.py

from app.sessions import sessions
from app.scammer_profiles import scammer_profiles

def global_stats():
    total_sessions = len(sessions)
    total_messages = sum(s["total_messages"] for s in sessions.values())
    total_scammers = len(scammer_profiles)

    high_risk = 0
    critical = 0

    for p in scammer_profiles.values():
        if p["risk_score"] >= 60:
            high_risk += 1
        if p.get("threat_level") == "CRITICAL":
            critical += 1

    return {
        "total_scammers": total_scammers,
        "total_sessions": total_sessions,
        "total_messages": total_messages,
        "high_risk_scammers": high_risk,
        "critical_threats": critical
    }


def top_entities():
    phones = {}
    upi = {}
    links = {}

    for p in scammer_profiles.values():
        for ph in p["entities"]["phones"]:
            phones[ph] = phones.get(ph, 0) + 1
        for u in p["entities"]["upi"]:
            upi[u] = upi.get(u, 0) + 1
        for l in p["entities"]["links"]:
            links[l] = links.get(l, 0) + 1

    return {
        "top_phones": sorted(phones, key=phones.get, reverse=True),
        "top_upi": sorted(upi, key=upi.get, reverse=True),
        "top_links": sorted(links, key=links.get, reverse=True)
    }


def scam_patterns():
    patterns = {
        "asks_for_otp": 0,
        "pretends_bank": 0,
        "uses_urgency": 0
    }

    for p in scammer_profiles.values():
        for k in patterns:
            if p["behaviour"][k]:
                patterns[k] += 1

    return patterns
