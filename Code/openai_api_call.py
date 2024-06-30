import requests

def openai_api_call(prompt_text,openai_key):
    
    url = 'https://api.openai.com/v1/chat/completions'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {openai_key}"
    }
    
    payload = {
        'model': "gpt-3.5-turbo",
        'messages': [{
            'role': "user",
            'content': prompt_text
        }],
        'max_tokens': 1024
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()  # Decode the JSON response
    if 'choices' in response_json and len(response_json['choices']) > 0:
        text_response = response_json['choices'][0]['message']['content']
        return text_response
    else:
        return "No response found."

