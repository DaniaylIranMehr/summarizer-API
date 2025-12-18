import gradio as gr
import requests
import json

api_key = "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"

def summarize_text(text, api_key):
    if not api_key:
        return "Please enter the API key."
    if len(text.strip()) < 20:
        return "The text is too short. Please enter a longer text."
    
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content_type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {
                "role": "user",
                "content": f"Make a short and clean summary of the following text:\n\n{text}"
            }
        ],
        "extra_body": {"reasoning": {"enabled": True}}
    }


    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        return f"API Error: {response.status_code} - {response.text}"

    
    data = response.json()
    
    try:
        summary = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return "Invalid API response!"
    else:
        return summary
    
    


t = input("TEXT:\n")
result = summarize_text(t, api_key)

print("########################")

print(result)