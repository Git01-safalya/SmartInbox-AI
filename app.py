
from email_reader import summarize_with_agent
import streamlit as st
from email_reader import fetch_emails
import subprocess

st.set_page_config(page_title="📬 SmartInbox AI", layout="wide")

# Run Granite through Ollama subprocess
def run_granite_prompt(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "granite3.2:8b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )
    output, error = process.communicate(input=prompt)
    return output.strip()

# Format the summarization prompt
def summarize_email(email_text):
    prompt = f"""
You are a helpful AI assistant that summarizes emails.
Return:
1. A 2-line summary.
2. Any action items (as bullet points).

Email:
\"\"\"
{email_text}
\"\"\"
"""
    return run_granite_prompt(prompt)

# Sidebar - Login Section
with st.sidebar:
    st.title("🔐 Gmail Access")
    email_user = st.text_input("Gmail Address", placeholder="you@gmail.com")
    email_pass = st.text_input("App Password", type="password", placeholder="Paste app password")

    st.markdown("---")
    st.markdown("ℹ️ You need an App Password for Gmail IMAP access. [How to get one?](https://myaccount.google.com/apppasswords)")

    fetch_button = st.button("📬 Fetch & Summarize Emails")

# Main title
st.title("📨 SmartInbox AI")
st.subheader("Summarize your Gmail inbox with IBM Granite – locally powered via Ollama 🧠")

# Fetch and display emails
if fetch_button and email_user and email_pass:
    with st.spinner("🔄 Connecting to Gmail..."):
        try:
            emails = fetch_emails(email_user, email_pass)
            st.success(f"✅ Fetched {len(emails)} recent emails.")
        except Exception as e:
            st.error(f"❌ Failed to fetch emails:\n{e}")
            st.stop()

    for idx, email_data in enumerate(emails):
        with st.expander(f"📩 {email_data['subject']}", expanded=False):
            st.markdown("**✉️ Original Email:**")
            st.code(email_data['body'], language="text")

            with st.spinner("🧠 Summarizing with Granite..."):
                summary = summarize_with_agent(email_data['body'])

            st.markdown("### 📝 Summary & Actions")
            st.success(summary)
            st.markdown("---")

elif fetch_button:
    st.warning("⚠️ Please enter your Gmail and app password.")
