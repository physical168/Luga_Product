import requests
from fastapi import HTTPException

class SyncLabsVideoService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # self.base_url = "https://api.synclabs.so"
        #v2 version
        self.base_url = "https://api.sync.so/v2/generate"
        
        

    def sync_audio_with_video(
        self,
        audio_url: str,
        video_url: str,
        max_credits: int = None,
        model: str = "sync-1.6.0",
        synergize: bool = True,
        webhook_url: str = None
    ):
        # endpoint = f"{self.base_url}/lipsync"
        endpoint = f"{self.base_url}"
        
        headers = {
            "accept": "application/json",
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "audioUrl": audio_url,
            "videoUrl": video_url,
            "synergize": synergize,
            "model": model
        }
        
        if max_credits is not None:
            payload["maxCredits"] = max_credits
        if webhook_url:
            payload["webhookUrl"] = webhook_url

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if e.response is not None:
                error_message = f"Error {e.response.status_code}: {e.response.text}"
            else:
                error_message = str(e)
            raise HTTPException(status_code=400, detail=error_message)

    def get_job_status(self, job_id: str):
        endpoint = f"{self.base_url}/lipsync/{job_id}"
        
        headers = {
            "x-api-key": self.api_key
        }

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")
            elif response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized. Check your API key")
            else:
                raise HTTPException(status_code=response.status_code, detail=str(http_err))
        except requests.RequestException as req_err:
            raise HTTPException(status_code=500, detail=str(req_err))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))