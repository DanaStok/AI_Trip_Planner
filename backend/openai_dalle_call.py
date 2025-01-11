import requests

def openai_dalle_call(prompt_text, openai_key):
    url = 'https://api.openai.com/v1/images/generations'
    
    # Insert your actual API token here
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {openai_key}"
    }
    
    payload = {
        'model': "dall-e-2",
        'prompt': prompt_text,
        'n': 1,  # Number of images to generate
        'size': '1024x1024'  # Image size
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()  # Decode the JSON response
    print(response_json)
    
    if response.status_code == 200 and 'data' in response_json and len(response_json['data']) > 0:
        image_url = response_json['data'][0]['url']  # Access the URL of the generated image
        return image_url
    else:
        print("No image found or an error occurred.")
        return None

