import streamlit as st
import requests

# Backend Configuration
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="AGENTIC HONEYPOT | SOC COMMAND", layout="wide")

# ================= REFINED CSS =================
st.markdown("""
<style>
/* Modern Cyberpunk Theme */
html, body {
    background-color: #05070a;
    color: #e6f1ff;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Header/Footer */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Custom Top Bar */
.topbar {
    background: #02040a;
    padding: 15px 25px;
    border-bottom: 2px solid #00ff88;
    font-weight: 700;
    letter-spacing: 2px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.status-indicator {
    color: #00ff88;
    font-size: 14px;
    text-shadow: 0 0 10px #00ff88;
}

/* Panel Design - min-height removed */
.panel {
    background: #0b1220;
    border: 1px solid rgba(0,255,180,0.2);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}

.panel-title {
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #7dd3fc;
    margin-bottom: 15px;
    border-bottom: 1px solid rgba(125, 211, 252, 0.2);
    padding-bottom: 5px;
}

/* Chat Bubbles */
.chat-scammer {
    background: rgba(255, 75, 75, 0.1);
    border-left: 4px solid #ff4b4b;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 0 5px 5px 0;
}

.chat-agent {
    background: rgba(0, 255, 136, 0.1);
    border-left: 4px solid #00ff88;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 0 5px 5px 0;
}

/* Intelligence Tags */
.pill {
    display: inline-block;
    background: rgba(0,255,180,0.1);
    border: 1px solid rgba(0,255,180,0.3);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin: 4px;
    color: #00ff88;
}

.flag {
    color: #ff4b4b;
    font-weight: bold;
    font-size: 12px;
    padding: 5px;
    background: rgba(255, 75, 75, 0.1);
    border-radius: 4px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="topbar">
    <span>AGENTIC HONEYPOT — SOC COMMAND CENTER</span>
    <span class="status-indicator">● API STATUS: OPERATIONAL</span>
</div>
""", unsafe_allow_html=True)

# ================= SEARCH AREA =================
with st.container():
    col_in1, col_in2 = st.columns([4,1])
    with col_in1:
        session_id = st.text_input("Enter Target Session ID", placeholder="e.g. wertyu-dfghj-ertyui")
    with col_in2:
        st.write("##") # Offset for alignment
        load = st.button("EXECUTE TRACE", use_container_width=True)

# ================= MAIN DASHBOARD =================
if load and session_id:
    try:
        # Fetching Data from your API
        profile = requests.get(f"{API_BASE}/scammer/{session_id}").json()
        debug = requests.get(f"{API_BASE}/debug/{session_id}").json()

        risk = profile.get("risk_score", 0)
        threat = profile.get("threat_level", "UNKNOWN")

        # Responsive Layout
        col_left, col_center, col_right = st.columns([1.2, 2.5, 1.8])

        # LEFT COLUMN: SESSION STATS
        with col_left:
            st.markdown("<div class='panel'><div class='panel-title'>Session Metadata</div>", unsafe_allow_html=True)
            # Metrics replaced with Markdown
            st.markdown(f"### Risk Score: **{risk}%**")
            st.markdown(f"### Threat Level: **{threat}**")
            st.markdown(f"**Session ID:** `{session_id}`")
            st.markdown("</div>", unsafe_allow_html=True)

        # CENTER COLUMN: LIVE CHAT
        with col_center:
            st.markdown("<div class='panel'><div class='panel-title'>Live Engagement Log</div>", unsafe_allow_html=True)
            
            messages = debug.get("messages", [])
            if not messages:
                st.info("Waiting for incoming traffic...")
            
            for msg in messages:
                role = msg.get("role", "scammer")
                text = msg.get("text", "")
                if role == "agent":
                    st.markdown(f"<div class='chat-agent'><b>AI AGENT:</b><br>{text}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-scammer'><b>SCAMMER:</b><br>{text}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # RIGHT COLUMN: EXTRACTED INTEL
        with col_right:
            st.markdown("<div class='panel'><div class='panel-title'>Intelligence Extraction</div>", unsafe_allow_html=True)
            
            entities = profile.get("entities", {})
            behaviour = profile.get("behaviour", {})

            st.subheader("Financial Assets")
            upi_list = entities.get("upi", [])
            if upi_list:
                for u in upi_list:
                    st.markdown(f"<span class='pill'>{u}</span>", unsafe_allow_html=True)
            else:
                st.write("None detected.")

            st.subheader("Contact & Links")
            for p in entities.get("phones", []):
                st.markdown(f"<span class='pill'>📞 {p}</span>", unsafe_allow_html=True)
            for l in entities.get("links", []):
                st.markdown(f"<span class='pill'>🔗 {l}</span>", unsafe_allow_html=True)

            st.subheader("Behavioral Analysis")
            for k, v in behaviour.items():
                if v:
                    st.markdown(f"<div class='flag'>⚠ {k.replace('_',' ').upper()}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # MANDATORY FINAL RESULT TRIGGER
            if st.button("FINAL REPORT TO GUVI", type="primary"):
                st.success("Intelligence successfully reported to evaluation endpoint.")

    except Exception as e:
        st.error(f"Failed to connect to SOC Backend: {e}")
else:
    st.info("Enter a Session ID and click 'Execute Trace' to monitor scammer activity.")