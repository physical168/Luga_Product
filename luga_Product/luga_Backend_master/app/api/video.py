from fastapi import APIRouter, UploadFile, HTTPException, File, Depends, Query
from fastapi.responses import JSONResponse
from typing import Dict, Optional, List
from bson import ObjectId
from datetime import datetime
import logging
from app.services.video_service import SyncLabsVideoService
from app.db.models import AudioToVideo, VideoUploadResponse, VideoProcessedResponse, JobStatusResponse
from app.db.database import database
from app.services.cloudinary import upload_file_to_cloudinary, get_cloudinary_video_url

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

from app.core.config import Config
video_service = SyncLabsVideoService(api_key=Config.SYNCLABS_API_KEY)

@router.post("/upload-video/", response_model=VideoUploadResponse)
async def upload_video(user_id: str, video: UploadFile = File(...)):
    try:
        logger.info(f"Uploading video for user_id: {user_id}")
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

        video_url = get_cloudinary_video_url(
            upload_result['public_id'], 
            upload_result['resource_type'], 
            upload_result['format']
        )
        
        logger.info(f"Video uploaded successfully. video_id: {video_id}")
        return VideoUploadResponse(
            user_id=user_id,
            video_id=video_id,
            video_url=video_url,
            message="Video uploaded successfully"
        )
    except Exception as e:
        logger.error(f"Error uploading video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading video: {str(e)}")

@router.post("/sync-audio/", response_model=VideoProcessedResponse)
async def sync_audio(
    user_id: str,
    video_id: str,
    audio: UploadFile = File(...),
    model: str = "lipsync-1.7.1",
    output_format: str = "mp4",
    webhook_url: Optional[str] = None
):
    try:
        logger.info(f"Starting audio sync for user_id: {user_id}, video_id: {video_id}")
        
        video_record = await database.db.videos.find_one({"user_id": user_id, "video_id": video_id})
        if not video_record:
            logger.warning(f"Video not found. user_id: {user_id}, video_id: {video_id}")
            raise HTTPException(status_code=404, detail="Video not found for this user and video ID")

        # Upload audio and get URL
        audio_upload_result = await upload_file_to_cloudinary(audio, folder="audios")

        # Get video and audio URLs with attachment flag
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

        logger.info(f"URLs prepared - Video URL: {video_url}, Audio URL: {audio_url}")

        # Create sync job using service
        sync_payload = {
            "audio_url": audio_url,
            "video_url": video_url,
            "model": model,
            "output_format": output_format,
            "webhook_url": webhook_url
        }
        logger.info(f"Sending sync request with payload: {sync_payload}")

        sync_result = video_service.sync_audio_with_video(**sync_payload)
        logger.info(f"Sync job created. Result: {sync_result}")

        # Create database record
        sync_record = {
            "user_id": user_id,
            "video_id": video_id,
            "job_id": sync_result.get("id"),
            "status": sync_result.get("status", "PROCESSING"),  # Changed from PENDING
            "audio_public_id": audio_upload_result['public_id'],
            "sync_result": sync_result,
            "created_at": datetime.fromisoformat(sync_result["created_at"]),
            "updated_at": datetime.utcnow(),
            "video_url": video_url,
            "audio_url": audio_url
        }
        
        await database.db.audio_to_video.insert_one(sync_record)

        return VideoProcessedResponse(
            user_id=user_id,
            video_id=video_id,
            sync_result=sync_result,
            message="Audio sync job created successfully"
        )

    except HTTPException as e:
        logger.error(f"HTTP Exception in sync_audio: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error in sync_audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process audio sync request: {str(e)}")

@router.get("/job/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status_by_id(job_id: str):
    try:
        logger.info(f"Checking status for job_id: {job_id}")
        
        sync_record = await database.db.audio_to_video.find_one({"job_id": job_id})
        if not sync_record:
            logger.warning(f"No record found for job_id: {job_id}")
            raise HTTPException(status_code=404, detail=f"No record found for job ID: {job_id}")
        
        # Get the latest status from SyncLabs
        job_status = video_service.get_job_status(job_id)
        logger.info(f"Raw job status response: {job_status}")
        
        # Handle different job statuses
        status = job_status.get("status")
        
        if status == "error":
            logger.error(f"Job failed. job_id: {job_id}, error: {job_status.get('message')}")
            update_data = {
                "status": "FAILED",
                "error": job_status.get("message"),
                "updated_at": datetime.utcnow()
            }
            
        elif status == "completed":
            logger.info(f"Job completed successfully. job_id: {job_id}")
            result_video_url = job_status.get("result", {}).get("url")
            update_data = {
                "status": "COMPLETED",
                "result_video_url": result_video_url,
                "job_result": job_status,
                "updated_at": datetime.utcnow()
            }
            
        elif status == "not_found":
            if sync_record.get("status") == "PROCESSING":
                logger.info(f"Job still processing. job_id: {job_id}")
                return JobStatusResponse(
                    user_id=sync_record["user_id"],
                    video_id=sync_record["video_id"],
                    status="PROCESSING",
                    result_video_url=None,
                    job_result={
                        "status": "PROCESSING",
                        "message": "Job is being processed"
                    }
                )
            else:
                logger.warning(f"Job expired or deleted. job_id: {job_id}")
                update_data = {
                    "status": "EXPIRED",
                    "message": "Job expired or was deleted",
                    "updated_at": datetime.utcnow()
                }
        else:
            logger.info(f"Job in progress. job_id: {job_id}, status: {status}")
            update_data = {
                "status": status.upper(),
                "job_result": job_status,
                "updated_at": datetime.utcnow()
            }

        # Update database with new status
        await database.db.audio_to_video.update_one(
            {"job_id": job_id},
            {"$set": update_data}
        )

        return JobStatusResponse(
            user_id=sync_record["user_id"],
            video_id=sync_record["video_id"],
            status=update_data.get("status"),
            result_video_url=update_data.get("result_video_url"),
            job_result=job_status
        )

    except HTTPException as he:
        logger.error(f"HTTP Exception in get_job_status: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Error in get_job_status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check job status: {str(e)}"
        )

@router.get("/debug/job/{job_id}")
async def debug_job(job_id: str):
    """Debug endpoint to get all information about a job"""
    try:
        # Get database record
        sync_record = await database.db.audio_to_video.find_one({"job_id": job_id})
        if not sync_record:
            return {"error": "No database record found"}

        # Get current status from API
        api_status = video_service.get_job_status(job_id)

        return {
            "database_record": sync_record,
            "api_status": api_status,
            "video_url": sync_record.get("video_url"),
            "audio_url": sync_record.get("audio_url"),
            "created_at": sync_record.get("created_at"),
            "updated_at": sync_record.get("updated_at")
        }

    except Exception as e:
        return {"error": str(e)}