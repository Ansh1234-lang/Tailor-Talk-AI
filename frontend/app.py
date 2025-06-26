# app.py

import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk AI", page_icon="🧵")
st.title("🤖 TailorTalk AI - Appointment Booking Assistant")

# Chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input from user
user_input = st.chat_input("Ask me to book or check calendar availability...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    try:
        res = requests.post("https://tailor-talk-ai.onrender.com/chat", json={"message": user_input})
        bot_reply = res.json().get("response", "Sorry, something went wrong.")
    except Exception as e:
        bot_reply = f"Error: {e}"

    # Show bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
# frontend/app.py

import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk AI", page_icon="🧵")
st.title("🧵 TailorTalk AI - Appointment Assistant")

# Session-based chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input field
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send message to FastAPI backend
    try:
        res = requests.post("https://tailor-talk-ai.onrender.com/chat", json={"message": user_input})
        bot_reply = res.json().get("response", "No response from backend.")
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    # Show bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
