import streamlit as st
from chatbot import get_answer  # 👈 import the function from chatbot.py

# Page config
st.set_page_config(
    page_title="Lumi - Your Mental Health Friend 💖",
    page_icon="🌸",
    layout="centered",
)

# Custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background-color: #ffe6f0;
        }
        .user-bubble {
            background-color: #ffccd5;
            color: black;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px;
            max-width: 70%;
            float: right;
            clear: both;
        }
        .bot-bubble {
            background-color: #ffffff;
            color: black;
            padding: 10px 15px;
            border-radius: 20px;
            margin: 5px;
            max-width: 70%;
            float: left;
            clear: both;
            border: 1px solid #ff99bb;
        }
        h1 {
            color: #cc3366;
            text-align: center;
            font-family: 'Trebuchet MS', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🌸 Lumi - Your Mental Health Friend 💖</h1>", unsafe_allow_html=True)

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.chat_input("Type your message here...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call backend (chatbot.py) to get Lumi's reply
    bot_reply = get_answer(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# Show chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
