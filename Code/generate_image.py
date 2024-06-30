
import os
import re
from openai_dalle_call import openai_dalle_call
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the environment variables
openai_key = os.getenv('OPENAI_API_KEY')

def generate_image(dict_input):
    location = dict_input['location']
    country = dict_input['country']

    for i in range(1, 6):
        prompt_text = create_vacation_image_prompt(location, country, i)

        # Formatting the returned data for better usability
        formatted_location = re.sub(r"\\s+", "_", location)
        file_name = f"{formatted_location}_image_{i}"
        file_path = os.path.join('../trip-planner/public/images', f"{file_name}.png")

        # Check if the image already exists in the path
        if not os.path.exists(file_path):
            image_url = openai_dalle_call(prompt_text,openai_key)
            download_image(image_url, file_path, '../trip-planner/public/images')
        else:
            print(f"Image {file_name}.png already exists. Skipping download.")

def download_image(image_url, file_path, folder_path):
    if image_url:
        response = requests.get(image_url)
        if response.status_code == 200:

            # Save the image in the specified folder path
            os.makedirs(folder_path, exist_ok=True) # Ensure the directory exists

            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"Image successfully downloaded as {file_path}")
        else:
            print("Failed to download the image.")
    else:
        print("No URL provided for download.")

def create_vacation_image_prompt(location, country, i):
    prompts = [
        f"Transport yourself to the historic heart of {location}, {country}. Depict iconic landmarks, ancient ruins, or grand monuments that showcase the rich cultural heritage of this destination. Include details like intricate architectural elements, local artisans or performers, and visitors admiring the sites. Render this image with a sense of grandeur and timelessness, inviting the viewer to explore the storied past.",
        f"Visualize a day of leisure and relaxation in {location}, {country}'s idyllic coastal region. Render a scene of sun-drenched beaches with crystal-clear waters, swaying palm trees, and vibrant sunsets. Include details like beach umbrellas, people sunbathing or swimming, and local seafood cuisine. Evoke a sense of tranquility and tropical bliss in this image, inviting the viewer to unwind in paradise.",
        f"Imagine yourself exploring the stunning natural wonders of {location}, {country}. Depict majestic landscapes like towering mountains, cascading waterfalls, or lush rainforests. Incorporate elements of adventure, such as hikers on trails, kayakers navigating rivers, or wildlife in their natural habitats. Render this image with a sense of awe and grandeur, inviting the viewer to immerse themselves in the breathtaking scenery.",
        f"Envision a vibrant street scene in {location}, {country}. Capture the local architecture, colorful markets, and bustling daily life. Include details like ornate buildings, vendors selling traditional wares, and people engaged in cultural activities or cuisine. Render this image with vivid colors and intricate details to transport the viewer to the heart of this captivating destination."
    ]

    return prompts[i-1]

