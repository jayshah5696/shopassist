from fastapi import FastAPI, Request
from pydantic import BaseModel
from llm import chat_llm
import markdown
import json
import os
import dotenv

dotenv.load_dotenv('.env')

app = FastAPI()

# Directory to store chat history
HISTORY_DIR = "backend/history"
os.makedirs(HISTORY_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chatbot")
async def chatbot_endpoint(request: ChatRequest):
    print(request)
    session_id = request.session_id
    user_message = request.message

    # Load chat history if it exists
    history_file = os.path.join(HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            chat_history = json.load(f)
    else:
        chat_history = []

    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_message})

    # Get response from the LLM
    chat_response = chat_llm(user_message)
    assistant_message = chat_response[-1]["content"]

    # Add assistant message to chat history
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Save updated chat history
    with open(history_file, "w") as f:
        json.dump(chat_history, f)

    # Convert assistant message to markdown
    markdown_response = markdown.markdown(assistant_message)
    return {"response": markdown_response}

@app.post("/chatbot_reset")
async def chatbot_reset(session_id: str):
    history_file = os.path.join(HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(history_file):
        os.remove(history_file)
    return {"status": "reset successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



