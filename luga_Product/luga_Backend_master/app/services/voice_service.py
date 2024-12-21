import requests
from fastapi import HTTPException
from app.core.config import Config

class ElevenLabsService:
    BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"

    def __init__(self):
        self.api_key = Config.ELEVEN_LABS_API_KEY
        if not self.api_key:
            raise ValueError("Eleven Labs API key is missing. Please configure it correctly.")

    def text_to_speech(self, voice_id: str, text: str) -> str:
        url = f"{self.BASE_URL}/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from Eleven Labs API")
        
        return response.content