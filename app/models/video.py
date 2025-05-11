from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    youtube_id = Column(String, unique=True, index=True)
    title = Column(String)
    transcript = Column(Text)
    paragraphs = Column(Text)
    processing_mode = Column(String)
    summary = Column(Text)

    def __repr__(self):
        return f"<Video(id={self.id}, youtube_id='{self.youtube_id}', title='{self.title}')>"