from fastapi import APIRouter, UploadFile, HTTPException, File, Depends, Query
from fastapi.responses import JSONResponse
from typing import Dict, Optional, List
from bson import ObjectId
from datetime import datetime
from app.services.video_service import SyncLabsVideoService
from app.db.models import AudioToVideo, VideoUploadResponse, VideoProcessedResponse, JobStatusResponse
from app.db.database import database
from app.services.cloudinary import upload_file_to_cloudinary, get_cloudinary_video_url

router = APIRouter()

from app.core.config import Config
video_service = SyncLabsVideoService(api_key=Config.SYNCLABS_API_KEY)

@router.post("/upload-video/", response_model=VideoUploadResponse)
async def upload_video(user_id: str, video: UploadFile = File(...)):
    try:
        upload_result = await upload_file_to_cloudinary(video, folder="videos")
        
        video_id = str(ObjectId())
        video_record = {
            "user_id": user_id,
            "video_id": video_id,
            "public_id": upload_result['public_id'],
            "format": upload_result['format'],
            "resource_type": upload_result['resource_type'],
            "created_at": datetime.utcnow(),
        }
        await database.db.videos.insert_one(video_record)

        video_url = get_cloudinary_video_url(upload_result['public_id'], upload_result['resource_type'], upload_result['format'])

        return VideoUploadResponse(
            user_id=user_id,
            video_id=video_id,
            video_url=video_url,
            message="Video uploaded successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading video: {str(e)}")

@router.post("/sync-audio/", response_model=VideoProcessedResponse)
async def sync_audio(
    user_id: str,
    video_id: str,
    audio: UploadFile = File(...),
    max_credits: Optional[int] = None,
    model: str = "sync-1.6.0",
    synergize: bool = True,
    webhook_url: Optional[str] = None
):
    video_record = await database.db.videos.find_one({"user_id": user_id, "video_id": video_id})
    if not video_record:
        raise HTTPException(status_code=400, detail="No video found for this user and video ID")

    try:
        audio_upload_result = await upload_file_to_cloudinary(audio, folder="audios")

        video_url = get_cloudinary_video_url(
            video_record['public_id'], 
            video_record['resource_type'], 
            video_record['format'],
            transformations=[{"flags": "attachment"}]
        )
        audio_url = get_cloudinary_video_url(
            audio_upload_result['public_id'], 
            audio_upload_result['resource_type'], 
            audio_upload_result['format'],
            transformations=[{"flags": "attachment"}]
        )

        sync_result = video_service.sync_audio_with_video(
            audio_url=audio_url,
            video_url=video_url,
            max_credits=max_credits,
            model=model,
            synergize=synergize,
            webhook_url=webhook_url
        )

        sync_record = {
            "user_id": user_id,
            "video_id": video_id,
            "job_id": sync_result.get("id"),
            "status": sync_result.get("status", "processing"),
            "audio_public_id": audio_upload_result['public_id'],
            "sync_result": sync_result,  
            "created_at": datetime.utcnow(),
        }
        
        await database.db.audio_to_video.insert_one(sync_record)
        import json
        import os
        
        local_test_dir = "local_test_data"
        os.makedirs(local_test_dir, exist_ok=True)
        
        local_file_path = os.path.join(local_test_dir, f"sync_result_{user_id}_{video_id}.json")
        with open(local_file_path, "w") as f:
            json.dump(sync_record, f, default=str)

        return VideoProcessedResponse(
            user_id=user_id,
            video_id=video_id,
            sync_result=sync_result,
            message="Audio sync job submitted successfully and saved locally for testing"
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/job/{user_id}/{video_id}", response_model=JobStatusResponse)
async def get_job_status(user_id: str, video_id: str):
    sync_record = await database.db.audio_to_video.find_one({"user_id": user_id, "video_id": video_id})
    if not sync_record:
        raise HTTPException(status_code=404, detail="No sync record found for this user and video ID")
    
    job_id = sync_record.get("job_id")
    if not job_id:
        raise HTTPException(status_code=400, detail="No job ID found for this sync record")

    try:
        job_status = video_service.get_job_status(job_id)
        
        await database.db.audio_to_video.update_one(
            {"_id": sync_record["_id"]},
            {"$set": {"status": job_status.get("status"), "job_result": job_status}}
        )

        if job_status.get("status") == "completed":
            result_video_url = job_status.get("result", {}).get("url")
            if result_video_url:
                await database.db.audio_to_video.update_one(
                    {"_id": sync_record["_id"]},
                    {"$set": {"result_video_url": result_video_url}}
                )

        return JobStatusResponse(
            user_id=user_id,
            video_id=video_id,
            status=job_status.get("status"),
            result_video_url=job_status.get("result", {}).get("url"),
            job_result=job_status
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while checking job status: {str(e)}")