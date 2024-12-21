from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.voice_service import ElevenLabsService
from app.db.database import database
from app.db.models import Audio, VoiceUploadResponse, DocumentResponse
from bson import ObjectId
from io import StringIO
import docx
import PyPDF2

router = APIRouter()

async def get_eleven_labs_service():
    return ElevenLabsService()

@router.post("/text-to-speech/", response_model=Audio)
async def text_to_speech(user_id: str, voice_id: str, text: str, service: ElevenLabsService = Depends(get_eleven_labs_service)):
    """Generate speech from the provided text using the selected voice."""
    
    audio_content = service.text_to_speech(voice_id, text)
    
    audio_url = f"{user_id}_{voice_id}_{str(ObjectId())}.mp3"  

    with open(audio_url, 'wb') as f:
        f.write(audio_content)

    audio_record = Audio(user_id=user_id, voice_id=voice_id, audio_url=audio_url)
    await database.db.audio.insert_one(audio_record.dict())
    
    return audio_record

@router.post("/upload-voice/", response_model=VoiceUploadResponse)
async def upload_voice(user_id: str, file: UploadFile = File(None), voice_id: str = None, service: ElevenLabsService = Depends(get_eleven_labs_service)):
    """
    Upload a 2-minute voice file or select a voice from ElevenLabs.
    If a file is uploaded, it will be stored as the user's voice.
    If voice_id is provided, it will be set as the preselected voice.
    """
    if file:
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")
        
        file_location = f"voices/{user_id}_{str(ObjectId())}.mp3"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        voice_id = str(ObjectId())  

        await database.db.voice.insert_one({"user_id": user_id, "voice_id": voice_id, "file_location": file_location})

        return VoiceUploadResponse(user_id=user_id, voice_id=voice_id, message="Voice file uploaded successfully.")

    elif voice_id:
        if not service.validate_voice(voice_id):
            raise HTTPException(status_code=400, detail="Invalid voice ID.")
        
        await database.db.voice.update_one({"user_id": user_id}, {"$set": {"voice_id": voice_id}}, upsert=True)

        return VoiceUploadResponse(user_id=user_id, voice_id=voice_id, message="Preselected voice set successfully.")
    
    else:
        raise HTTPException(status_code=400, detail="Please either upload a voice file or provide a valid voice_id.")
    

@router.post("/upload-document/", response_model=DocumentResponse)
async def upload_document(user_id: str, file: UploadFile = File(...)):
    """
    Upload a document (.docx, .txt, or .pdf) and extract text from it.
    The extracted text can then be used for TTS.
    """
    if file.content_type == "text/plain":
        content = await file.read()
        text = content.decode('utf-8')

    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file.file)
        text = '\n'.join([para.text for para in doc.paragraphs])

    elif file.content_type == "application/pdf":
        reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF file.")

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .docx, .txt, or .pdf file.")

    return DocumentResponse(user_id=user_id, text=text)
