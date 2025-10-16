import os
import base64
import requests


class CelebrityDetector:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"

    def identify(self, image_bytes):
        """
        Identify the celebrity in the given image bytes using the Groq API.
        Args:
            image_bytes: The image in bytes format.
        Returns:
            The name of the identified celebrity or None if no celebrity is found.
        """
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        prompt = {
            "model": self.model,
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": """You are a celebrity recognition expert AI. 
Identify the person in the image. If known, respond in this format:

- **Full Name**:
- **Profession**:
- **Nationality**:
- **Famous For**:
- **Top Achievements**:

If unknown, return "Unknown".
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,    
            "max_tokens": 1024     
        }


        response = requests.post(self.api_url, headers=headers, json=prompt)
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            name = self.extract_name(message)
            return message, name
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None, None
        
    def extract_name(self, message):
        """
        Extract the celebrity's full name from the API response message.
        Args:
            message: The response message from the Groq API.
        Returns:
            The full name of the celebrity or None if not found.
        """
        for line in message.splitlines():
            if line.lower().startswith("- **full name**:"):
                return line.split(":")[1].strip()

        return "Unknown" 
