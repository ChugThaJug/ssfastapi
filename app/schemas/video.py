from pydantic import BaseModel, AnyUrl, ConfigDict
from typing import Optional

class VideoBase(BaseModel):
    youtube_id: str
    title: str
    paragraphs: str
    processing_mode: str
    summary: str

class VideoProcessRequest(BaseModel):
    youtube_url: AnyUrl
    processing_mode: str

class VideoCreate(VideoBase):
    youtube_url: AnyUrl

class VideoResponse(VideoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class VideoUpdate(BaseModel):
    summary: Optional[str] = None
    transcript: Optional[str] = None

class VideoInDB(VideoBase):
    id: int
    transcript: str

    model_config = ConfigDict(from_attributes=True)