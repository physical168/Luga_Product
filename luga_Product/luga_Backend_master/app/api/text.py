from fastapi import APIRouter, HTTPException
from typing import List
from app.db.models import TextCreate, TextResponse
from app.services.text_service import generate_response
from app.db.database import database
from pymongo import DESCENDING
from datetime import datetime

router = APIRouter()

@router.post("/generate", response_model=TextResponse)
async def create_prompt(prompt: TextCreate):
    try:
        # Gọi dịch vụ để tạo phản hồi từ prompt
        response_text = await generate_response(prompt.prompt)
        
        # Lưu trữ prompt và response vào cơ sở dữ liệu
        prompt_data = {
            "prompt": prompt.prompt,
            "response": response_text,
            "timestamp": datetime.utcnow()
        }
        await database.db.text.insert_one(prompt_data)

        return {"prompt": prompt.prompt, "response": response_text}
    
    except Exception as e:
        # Trả về lỗi nếu có
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[TextResponse])
async def get_history():
    try:
        # Lấy lịch sử các prompt từ cơ sở dữ liệu
        prompts = await database.db.text.find().sort("timestamp", DESCENDING).to_list(100)
        return [
            {"prompt": item["prompt"], "response": item["response"]}
            for item in prompts
        ]
    
    except Exception as e:
        # Trả về lỗi nếu có
        raise HTTPException(status_code=500, detail=str(e))
