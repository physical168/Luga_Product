import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
    SYNCLABS_API_KEY = os.getenv("SYNCLABS_API_KEY")
    MONGO_DB_URL = os.getenv("MONGO_DB_URL")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")