# app/agent_strategy.py

def choose_strategy(profile, state):
    risk = profile["risk_score"]
    behaviour = profile["behaviour"]

    if risk > 80:
        return "trap"
    elif behaviour["asks_for_otp"]:
        return "investigate"
    elif behaviour["uses_urgency"]:
        return "delay"
    else:
        return "passive"
