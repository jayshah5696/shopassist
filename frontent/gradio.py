import gradio as gr
import requests
import json
import os

HISTORY_DIR = "backend/history"

def send_message(session_id, message):
    url = "http://localhost:8000/chatbot"
    payload = {"session_id": session_id, "message": message}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        try:
            return response.json()["response"]
        except json.JSONDecodeError:
            return "Error decoding JSON response"
    else:
        return f"Error: {response.status_code}"

def reset_chat(session_id):
    url = "http://localhost:8000/chatbot_reset"
    payload = {"session_id": session_id}
    requests.post(url, json=payload)
    return []

def load_chat_history(session_id):
    history_file = os.path.join(HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []

def chatbot_interface(session_id, user_message, chat_history):
    if user_message:
        response = send_message(session_id, user_message)
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": response})
    return chat_history, chat_history

def reset_interface(session_id):
    return reset_chat(session_id), []

def main():
    with gr.Blocks() as demo:
        session_id = gr.Textbox(label="Session ID", value="default_session")
        chat_history = gr.State([])

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Chat History")
                chat_display = gr.Chatbot()

            with gr.Column():
                user_message = gr.Textbox(label="Your Message")
                send_button = gr.Button("Send")
                reset_button = gr.Button("Reset Chat")

        send_button.click(chatbot_interface, [session_id, user_message, chat_history], [chat_display, chat_history])
        reset_button.click(reset_interface, [session_id], [chat_display, chat_history])

    demo.launch()

if __name__ == "__main__":
    main()