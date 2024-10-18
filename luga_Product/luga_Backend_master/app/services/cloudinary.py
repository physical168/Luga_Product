import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from cloudinary import CloudinaryVideo
from fastapi import UploadFile, HTTPException
from app.core.config import Config

cloudinary.config(
    cloud_name = Config.CLOUDINARY_CLOUD_NAME,
    api_key = Config.CLOUDINARY_API_KEY,
    api_secret = Config.CLOUDINARY_API_SECRET,
    secure = True
)

MAX_FILE_SIZE = 100 * 1024 * 1024  
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mp3', 'wav', 'webm','m4a'}

def is_file_allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def upload_file_to_cloudinary(file: UploadFile, folder: str) -> dict:
    try:
        if not is_file_allowed(file.filename):
            raise HTTPException(status_code=400, detail=f"File type not allowed. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}")
        
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB")

        upload_result = cloudinary.uploader.upload(
            file_content,
            folder=folder,
            resource_type="auto",
            public_id=file.filename.split('.')[0]  
        )

        return {
            "public_id": upload_result['public_id'],
            "format": upload_result['format'],
            "resource_type": upload_result['resource_type']
        }

    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading: {str(e)}")

def get_cloudinary_video_url(public_id: str, resource_type: str = "video", format: str = "mp4", transformations: list = None) -> str:
    if transformations is None:
        transformations = []
    
    video = CloudinaryVideo(public_id)
    url = video.build_url(secure=True, resource_type=resource_type, format=format, transformation=transformations)
    return url

def get_public_id_from_url(url: str) -> str:
    parts = url.split('/')
    return '/'.join(parts[-2:]).split('.')[0]