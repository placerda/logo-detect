import os
import base64
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI API credentials
api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
deployment_id = os.getenv('AZURE_OPENAI_DEPLOYMENT_ID')
api_version = '2023-10-01-preview'  # Update this to the correct API version

# Headers for the API request
headers = {
    'api-key': api_key,
    'Content-Type': 'application/json',
}

# Output file to store results
output_dir = 'output'
output_file = os.path.join(output_dir, 'logos_output_gpt4o.txt')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Clear the output file if it exists
with open(output_file, 'w') as f_out:
    pass

# Directory containing the PNG files
SLIDES_DIR = 'slides'

# Check if the slides directory exists
if not os.path.isdir(SLIDES_DIR):
    print(f"Error: The directory '{SLIDES_DIR}' does not exist. Please create it and add PNG files to process.")
    exit(1)

# Sort and process each PNG file in the directory
for filename in sorted(os.listdir(SLIDES_DIR)):
    if filename.lower().endswith('.png'):
        filepath = os.path.join(SLIDES_DIR, filename)

        # Read and base64-encode the image
        with open(filepath, 'rb') as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')

        # Prepare the API request URL
        url = f"{endpoint}/openai/deployments/{deployment_id}/chat/completions?api-version={api_version}"

        # Messages to send to the GPT-4 model
        messages = [
            {"role": "system", "content": "You are an assistant that detect company logos in slides."},
            {"role": "user", "content": [
                {
                    "type": "text", 
                    "text": (
                        "The following image is a slide. "
                        "Give me a list of logos that are present in the slide. "
                        "Generate the list as a string list, for example: [Microsoft,NVIDIA,IBM]."
                        "In case there are no logos just generate an empty list: []." 
                        "Do not write anything else besides the list content in the response."                                                  
                    )
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }            
            ]}
        ]

        # Payload for the API request
        payload = {
            'messages': messages
        }

        # Send the request to the Azure OpenAI API
        response = requests.post(url, headers=headers, json=payload)

        # Handle the API response
        if response.status_code == 200:
            response_data = response.json()
            assistant_reply = response_data['choices'][0]['message']['content']

            # Write the filename and the assistant's reply to the output file
            with open(output_file, 'a') as f_out:
                f_out.write(f"{filename}: {assistant_reply}\n")
        else:
            print(f"Error processing {filename}: {response.status_code} - {response.text}")
