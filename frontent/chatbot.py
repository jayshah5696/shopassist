import requests
import json
import os
import gradio as gr
import uuid

HISTORY_DIR = "backend/history"

def send_message(session_id, message):
    url = "http://localhost:8000/chatbot"
    payload = {"session_id": session_id, "message": message}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        try:
            return {"role": "assistant", "content": response.json()["response"]}
        except json.JSONDecodeError:
            return {"role": "assistant", "content": "Error decoding JSON response"}
    else:
        return {"role": "assistant", "content": f"Error: {response.status_code}"}

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

def chatbot(message, history, session_id=str(uuid.uuid4())):
    chat_history = load_chat_history(session_id)
    
    if message:
        response = send_message(session_id, message)
        chat_history.append({"role": "user", "content": message})
        chat_history.append(response)
    
    return response['content']

iface = gr.ChatInterface(
    fn=chatbot,
    additional_inputs=[
        gr.Textbox(label="Session ID", value=str(uuid.uuid4()), interactive=False)
    ],
    title="Chatbot Interface",
    description="A simple chatbot interface using Gradio's ChatInterface API.",
    theme="compact",
    avatar_images=(None, "https://em-content.zobj.net/source/twitter/53/robot-face_1f916.png")
)

iface.launch(share=True)