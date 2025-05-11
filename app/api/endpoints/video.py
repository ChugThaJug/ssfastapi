from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.video import Video
from app.schemas.video import VideoProcessRequest, VideoResponse, VideoUpdate
from app.services.transcript_processor import extract_video_id, get_raw_transcript, process_transcript
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/process_video/", response_model=VideoResponse)
async def process_video(video: VideoProcessRequest, db: Session = Depends(get_db)):
    logger.info(f"Received request to process video. Data: {video.dict()}")
    try:
        video_id = extract_video_id(video.youtube_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
        if db_video:
            logger.info(f"Video already exists: {video_id}")
            return VideoResponse.model_validate(db_video)

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

        logger.info(f"Successfully processed video: {video_id}")
        return VideoResponse.model_validate(db_video)

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@router.get("/video/{video_id}", response_model=VideoResponse)
def get_video(video_id: str, db: Session = Depends(get_db)):
    logger.info(f"Received request to get video: {video_id}")
    db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
    if db_video is None:
        logger.warning(f"Video not found: {video_id}")
        raise HTTPException(status_code=404, detail="Video not found")
    logger.info(f"Successfully retrieved video: {video_id}")
    return VideoResponse.model_validate(db_video)

@router.put("/video/{video_id}/summary", response_model=VideoResponse)
def update_video_summary(video_id: str, video_update: VideoUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update summary for video: {video_id}")
    db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
    if db_video is None:
        logger.warning(f"Video not found: {video_id}")
        raise HTTPException(status_code=404, detail="Video not found")
    
    db_video.summary = video_update.summary
    db.commit()
    db.refresh(db_video)
    
    logger.info(f"Successfully updated summary for video: {video_id}")
    return VideoResponse.model_validate(db_video)

@router.put("/video/{video_id}/transcript", response_model=VideoResponse)
def update_video_transcript(video_id: str, video_update: VideoUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update transcript for video: {video_id}")
    db_video = db.query(Video).filter(Video.youtube_id == video_id).first()
    if db_video is None:
        logger.warning(f"Video not found: {video_id}")
        raise HTTPException(status_code=404, detail="Video not found")
    
    db_video.paragraphs = video_update.transcript
    db.commit()
    db.refresh(db_video)
    
    logger.info(f"Successfully updated transcript for video: {video_id}")
    return VideoResponse.model_validate(db_video)