import streamlit as st
from google import genai

MODEL = "gemini-2.5-flash"

PROMPT = """You are a friendly scam-detection assistant helping everyday people,
especially seniors and their families. Read the message below and respond in
plain, simple English (no jargon).

Use exactly this format:

VERDICT: Safe, Suspicious, or Scam
WHY: 2 short sentences explaining the main warning signs (or why it looks fine)
WHAT TO DO: 1-2 clear steps (e.g. don't click the link, call the company using
the number on their official website, block the sender)

Rules:
- Never claim 100% certainty. If unsure, say "Suspicious" and explain.
- Look for urgency, threats, requests for money/gift cards/codes/passwords,
  unknown links, wrong sender details, and too-good-to-be-true offers.
- Never tell the person to reply to the message or click anything in it.

MESSAGE TO CHECK:
"""

st.set_page_config(page_title="Is This a Scam?", page_icon="🛡️")
st.title("🛡️ Is This a Scam?")
st.write("Paste a text, email, or link below and get a plain-English second opinion.")

message = st.text_area("Paste the message here", height=200)

if st.button("Check it"):
    if not message.strip():
        st.warning("Please paste a message first.")
    else:
        with st.spinner("Checking..."):
            try:
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                response = client.models.generate_content(
                    model=MODEL, contents=PROMPT + message
                )
                st.markdown(response.text)
            except Exception as e:
                st.error("Something went wrong. Please try again in a moment.")
                st.caption(str(e))

st.caption("This is a second opinion, not a guarantee. When in doubt, don't click, and call the company directly.")