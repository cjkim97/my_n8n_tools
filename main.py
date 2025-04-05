from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import asyncio
import uvicorn

# src 폴더의 크롤링 함수 임포트
from src.crawl_today_luck import crawl_luck

app = FastAPI()

class LuckRequest(BaseModel):
    gender: Literal["남성", "여성"]
    birth_type: Literal["양력", "음력 평달", "음력 윤달"]
    birth_time_code: Literal["0", "1", "2", "3", "4", "5","6", "7", "8", "9", "10", "11", "12"]
    birth_year: str
    birth_month: str
    birth_day: str

@app.post("/today-luck")
async def get_today_luck(req: LuckRequest):
    try:
        result = await crawl_luck(
            gender=req.gender,
            birth_type=req.birth_type,
            birth_time_code=req.birth_time_code,
            birth_year=req.birth_year,
            birth_month=req.birth_month,
            birth_day=req.birth_day
        )
        return {
            "status": "success",
            "output": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # 로컬테스트용
