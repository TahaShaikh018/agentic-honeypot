# app/agent_memory.py

agent_memory = {}

def get_agent_state(session_id):
    if session_id not in agent_memory:
        agent_memory[session_id] = {
            "mode": "passive",
            "extracted": {
                "phones": set(),
                "upi": set(),
                "links": set()
            },
            "questions_asked": []
        }
    return agent_memory[session_id]
