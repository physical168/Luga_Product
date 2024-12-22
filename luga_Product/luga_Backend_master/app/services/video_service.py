import requests
from fastapi import HTTPException
from datetime import datetime

class SyncLabsVideoService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sync.so/v2"

    def sync_audio_with_video(
        self,
        audio_url: str,
        video_url: str,
        model: str = "lipsync-1.7.1",
        output_format: str = "mp4",
        webhook_url: str = None,
        retries: int = 3
    ):
        """
        Create a new lip sync job
        """
        endpoint = f"{self.base_url}/generate"
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "input": [
                {
                    "type": "video",
                    "url": video_url
                },
                {
                    "type": "audio", 
                    "url": audio_url
                }
            ],
            "options": {
                "output_format": output_format
            }
        }
        
        if webhook_url:
            payload["webhookUrl"] = webhook_url

        for attempt in range(retries):
            try:
                response = requests.post(endpoint, json=payload, headers=headers)
                if response.status_code == 429:  # Rate limit
                    if attempt < retries - 1:
                        continue
                response.raise_for_status()
                response_data = response.json()
                return {
                    **response_data,
                    "created_at": datetime.utcnow().isoformat()
                }
            except requests.RequestException as e:
                if attempt < retries - 1:
                    continue
                if e.response is not None:
                    error_message = f"Error {e.response.status_code}: {e.response.text}"
                else:
                    error_message = str(e)
                raise HTTPException(status_code=400, detail=error_message)

    def get_job_status(self, job_id: str, retries: int = 3):
        """
        Check job status
        """
        endpoint = f"{self.base_url}/jobs/{job_id}"
        
        headers = {
            "x-api-key": self.api_key,
            "accept": "application/json"
        }

        for attempt in range(retries):
            try:
                response = requests.get(endpoint, headers=headers)
                
                if response.status_code == 404:
                    return {
                        "status": "not_found",
                        "message": f"Job {job_id} not found or has been deleted"
                    }
                elif response.status_code == 401:
                    return {
                        "status": "error",
                        "message": "Invalid or expired API key"
                    }
                elif response.status_code == 429:  # Rate limit
                    if attempt < retries - 1:
                        continue
                
                response.raise_for_status()
                return response.json()
                
            except requests.RequestException as e:
                if attempt < retries - 1:
                    continue
                return {
                    "status": "error",
                    "message": str(e)
                }