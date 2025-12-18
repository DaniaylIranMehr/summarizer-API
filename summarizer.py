import gradio as gr
import requests
import json


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
    
    
iface = gr.Interface(
    fn = summarize_text,
    inputs = [
        gr.Textbox(label="Input", lines=10, placeholder="Please enter your text."),
        gr.Textbox(label="API Key", type="password", placeholder="Openrouter's key.")
    ],
    outputs = gr.Textbox(label="Summary", lines=6),
    title = "Summarization with AI",
    description = "Enter text to summarize."
    )

iface.launch(share=False, analytics=False, allow_flagging=False)