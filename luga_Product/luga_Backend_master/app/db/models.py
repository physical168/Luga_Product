from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, Dict, Any
from datetime import datetime

class Audio(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))  
    user_id: str
    voice_id: str
    audio_url: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class VoiceUploadResponse(BaseModel):
    user_id: str
    voice_id: str
    message: str

class DocumentResponse(BaseModel):
    user_id: str
    text: str

class VideoUploadResponse(BaseModel):
    user_id: str
    video_id: str
    message: str

class VideoProcessedResponse(BaseModel):
    user_id: str
    video_id: str
    sync_result: Dict[str, Any] = Field(..., description="Full response from SyncLabs API")
    message: str

class JobStatusResponse(BaseModel):
    user_id: str
    video_id: str
    status: str
    result_video_url: Optional[str] = None
    job_result: Dict[str, Any]
    
class AudioToVideo(BaseModel):
    user_id: str
    video_id: str
    audio_url: str
    video_url: str
    sync_result: Dict[str, Any] = Field(..., description="Full response from SyncLabs API")
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Text(BaseModel):
    prompt: str
    response: str
    timestamp: datetime = datetime.utcnow()

class TextCreate(BaseModel):
    prompt: str

class TextResponse(BaseModel):
    prompt: str
    response: str
