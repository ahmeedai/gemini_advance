import streamlit as st
import requests

st.set_page_config(page_title="Gemini Chatbot", layout="centered")

# Load API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

st.title("💬 Gemini Chatbot")
st.markdown("Ask anything and get smart responses from Gemini 2.0 Flash!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful but simple chatbot."}
    ]

# Display past messages
for msg in st.session_state.chat_history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input box for user message
user_input = st.chat_input("Type your message...")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare full history for Gemini
    data = {
        "contents": [
            {
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            } for msg in st.session_state.chat_history
        ]
    }

    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = f"⚠️ Error {response.status_code}: {response.text}"

    except Exception as e:
        reply = f"❌ Unexpected error: {e}"

    # Add bot reply to chat
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)