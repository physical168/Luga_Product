from fastapi import FastAPI
from app.api import voice
from app.api import video
from app.api import text

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LuGaAI API"}

app.include_router(voice.router, prefix="/api/voice")
app.include_router(video.router, prefix="/api/video")
app.include_router(text.router, prefix="/api/text")
