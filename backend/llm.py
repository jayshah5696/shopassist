from litellm import completion
from rich.pretty import pprint
import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Safely get the API key
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# print(api_key)

def completion_llm(text, model='groq/llama3-70b-8192t'):
    messages = [{ "content": text, "role": "user" }]
    response = completion(model=model, messages=messages)
    return response.choices[0].message.content

def chat_llm(input, model='groq/llama3-70b-8192'):
    messages = [{ "content": input, "role": "user" }]
    response = completion(model=model, messages=messages)
    # Append response as a new message with role 'assistant'
    messages.append({ "content": response.choices[0].message.content, "role": "assistant" })
    return messages


def chat_llm_v2_updated(messages, input, model='groq/llama3-70b-8192', system_prompt=None):
    # Check if system prompt already exists in the conversation
    if system_prompt and not any(msg.get("role") == "system" for msg in messages):
        messages.insert(0, {"content": system_prompt, "role": "system"})
    # Add new user message to the existing conversation
    messages.append({"content": input, "role": "user"})
    response = completion(model=model, messages=messages)
    # Append response as a new message with role 'assistant'
    print(response.choices[0].message.content)
    messages.append({"content": response.choices[0].message.content, "role": "assistant"})
    return messages