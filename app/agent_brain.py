# app/agent_brain.py

from app.agent_memory import get_agent_state
from app.agent_strategy import choose_strategy
from app.llm_client import ask_llm

def honeypot_reply(session_id, profile, conversation):
    state = get_agent_state(session_id)
    strategy = choose_strategy(profile, state)

    prompt = f"""
You are a cybersecurity honeypot agent.

Your goal:
Extract phone numbers, UPI IDs, links, identities.

Conversation:
{conversation}

Current strategy: {strategy}

Respond as a human victim. Do NOT reveal you are AI.
Ask smart questions to extract more information.
"""

    reply = ask_llm(prompt)
    return reply
