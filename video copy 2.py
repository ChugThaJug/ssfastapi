# app/api/endpoints/video.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.video import Video
from app.schemas.video import VideoCreate, VideoResponse, VideoUpdate
from app.services.transcript_processor import extract_video_id, get_raw_transcript, process_transcript
from pydantic import AnyUrl

router = APIRouter()

@router.post("/process_video/", response_model=VideoResponse)
async def process_video(video: VideoCreate, db: Session = Depends(get_db)):
    try:
        video_id = extract_video_id(video.youtube_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
        if db_video:
            return VideoResponse(
                id=db_video.id,
                youtube_id=db_video.youtube_id,
                title=db_video.title,
                paragraphs=db_video.paragraphs,
                processing_mode=db_video.processing_mode,
                summary=db_video.summary
            )

        transcript = get_raw_transcript(video_id)
        paragraphs = process_transcript(transcript, mode=video.processing_mode)
        paragraphs_text = "\n\n".join([p['paragraph_text'] for p in paragraphs])

        title = f"Video {video_id}"  # TODO: Get actual video title

        db_video = Video(
            youtube_id=video_id,
            title=title,
            transcript=str(transcript),
            paragraphs=paragraphs_text,
            processing_mode=video.processing_mode,
            summary=""  # Initialize with an empty summary
        )
        db.add(db_video)
        db.commit()
        db.refresh(db_video)

        return VideoResponse(
            id=db_video.id,
            youtube_id=db_video.youtube_id,
            title=db_video.title,
            paragraphs=db_video.paragraphs,
            processing_mode=db_video.processing_mode,
            summary=db_video.summary
        )
    except Exception as e:
        print(f"Error processing video: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
    
@router.get("/video/{video_id}", response_model=VideoResponse)
def get_video(video_id: str, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return VideoResponse(
        id=db_video.id,
        youtube_id=db_video.youtube_id,
        title=db_video.title,
        paragraphs=db_video.paragraphs,
        processing_mode=db_video.processing_mode,
        summary=db_video.summary
    )

@router.put("/video/{video_id}/summary", response_model=VideoResponse)
def update_video_summary(video_id: str, video_update: VideoUpdate, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    
    db_video.summary = video_update.summary
    db.commit()
    db.refresh(db_video)
    
    return VideoResponse(
        id=db_video.id,
        youtube_id=db_video.youtube_id,
        title=db_video.title,
        paragraphs=db_video.paragraphs,
        processing_mode=db_video.processing_mode,
        summary=db_video.summary
    )

@router.put("/video/{video_id}/transcript", response_model=VideoResponse)
def update_video_transcript(video_id: str, video_update: VideoUpdate, db: Session = Depends(get_db)):
    db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    
    db_video.paragraphs = video_update.transcript
    db.commit()
    db.refresh(db_video)
    
    return VideoResponse(
        id=db_video.id,
        youtube_id=db_video.youtube_id,
        title=db_video.title,
        paragraphs=db_video.paragraphs,
        processing_mode=db_video.processing_mode,
        summary=db_video.summary
    )