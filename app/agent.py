from app.llm_client import ask_llm

def generate_agent_reply(text: str, is_scam: bool):
    if is_scam:
        prompt = f"""
You are pretending to be a normal human.
You received this suspicious message:

"{text}"

Your goals:
- Act innocent and unaware
- Do NOT accuse or mention scam
- Ask curious questions
- Sound realistic and casual
- Keep the sender talking

Reply in one short human-like message.
"""
    else:
        prompt = f"""
You are a friendly college student chatting normally.

Message:
"{text}"

Reply casually like a real human.
"""

    return ask_llm(prompt)
