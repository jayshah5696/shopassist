from fastapi import FastAPI, Request
from pydantic import BaseModel
from llm import chat_llm, chat_llm_v2
import markdown
import json
import os
import dotenv
import requests
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
    return {"response": assistant_message}

@app.post("/chatbot_reset")
async def chatbot_reset(session_id: str):
    history_file = os.path.join(HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(history_file):
        os.remove(history_file)
    return {"status": "reset successful"}

@app.get("/chat_history/{session_id}")
async def get_chat_history(session_id: str):
    history_file = os.path.join(HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            chat_history = json.load(f)
        return {"history": chat_history}
    else:
        print('File does not exist')
        print(history_file)
    return {"history": []}

def get_wordware_search_assist_query(user_query):
    api_url = "https://app.wordware.ai/api/released-app/643105ed-de2a-467d-85f7-a8a83b9bf5e3/run"
    request_body = {
        "inputs": {"user_query": user_query},
        "version": "^1.0"
    }
    response = requests.post(api_url, json=request_body)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return {}
    
@app.post("/get_wordware_search_assist_results")
async def get_wordware_search_assist_results(request: ChatRequest):
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

    # get curl request to wordware
    # get response
    message = get_wordware_search_assist_query(user_message)
    assistant_message = message['outputs']['assistant_message']

    

    # Add assistant message to chat history
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Save updated chat history
    with open(history_file, "w") as f:
        json.dump(chat_history, f)

    # Convert assistant message to markdown
    return {"response": assistant_message}


@app.post("/chatbotv2")
async def chatbot_endpoint_v2(request: ChatRequest):
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
        # Get response from the LLM
    chat_response = chat_llm_v2(messages=chat_history, input=user_message)
    # Add user message to chat history
    
    # print(chat_response)
    assistant_message = chat_response[-1]["content"]
    # Add assistant message to chat history
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": assistant_message})

    # Save updated chat history
    with open(history_file, "w") as f:
        json.dump(chat_history, f)

    # Convert assistant message to markdown
    return {"response": assistant_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)