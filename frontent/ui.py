import streamlit as st
import requests
import json
import os

HISTORY_DIR = "backend/history"

def send_message(session_id, message):
    url = "http://localhost:8000/chatbot"
    payload = {"session_id": session_id, "message": message}
    response = requests.post(url, json=payload)
    
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        try:
            return response.json()["response"]
        except json.JSONDecodeError:
            st.error("Error decoding JSON response")
            return None
    else:
        st.error(f"Error: {response.status_code}")
        return None

def reset_chat(session_id):
    url = "http://localhost:8000/chatbot_reset"
    payload = {"session_id": session_id}
    requests.post(url, json=payload)
    st.session_state["chat_history"] = []

def load_chat_history(session_id):
    history_file = os.path.join(HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []

def main():
    st.title("Simple Chatbot UI")

    # Session state to store chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Sidebar for session ID and chat history
    with st.sidebar:
        st.header("Session and Chat History")

        # Input for session ID
        session_id = st.text_input("Session ID", value="default_session")

        # Load chat history for the given session ID
        st.session_state["chat_history"] = load_chat_history(session_id)

        # Display chat history
        st.subheader("Chat History")
        for chat in st.session_state["chat_history"]:
            if chat["role"] == "user":
                st.text(f"User: {chat['content']}")
            else:
                st.text(f"Assistant: {chat['content']}")

        # Button to reset chat
        if st.button("Reset Chat"):
            reset_chat(session_id)

    # Main area for user message input
    user_message = st.text_input("Your Message")

    # Button to send message
    if st.button("Send"):
        if user_message:
            response = send_message(session_id, user_message)
            st.session_state["chat_history"].append({"role": "user", "content": user_message})
            st.session_state["chat_history"].append({"role": "assistant", "content": response})

    # Display chat history in a chatbot format
    st.subheader("Chatbot Conversation")
    for chat in st.session_state["chat_history"]:
        if chat["role"] == "user":
            st.markdown(f"**User:** {chat['content']}")
        else:
            st.markdown(f"**Assistant:** {chat['content']}")

if __name__ == "__main__":
    main()
