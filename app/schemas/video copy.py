# app/schemas/video.py
from pydantic import BaseModel

class VideoCreate(BaseModel):
    youtube_url: str
    processing_mode: str

class VideoUpdate(BaseModel):
    summary: str | None = None
    transcript: str | None = None
    
class VideoResponse(BaseModel):
    id: int
    youtube_id: str
    title: str
    paragraphs: str
    processing_mode: str
    summary: str | None

    class Config:
        orm_mode = True