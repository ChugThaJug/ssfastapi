# # app/api/endpoints/video.py
# from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.video import Video
# from app.schemas.video import VideoCreate, VideoResponse, VideoUpdate
# # from app.services.content_processor import (
# #     extract_video_id, get_raw_transcript, process_content,
# #     extract_pdf_content, chunk_content
# # )

# from app.services.content_extraction import extract_content, extract_pdf_content, extract_youtube_transcript

# from typing import List, Dict, Union
# import time

# router = APIRouter()

# @router.post("/process_content/", response_model=VideoResponse)
# async def process_content_endpoint(
#     request: VideoCreate,
#     db: Session = Depends(get_db),
#     file: UploadFile = File(None)
# ):
#     try:
#         start_time = time.time()

#         # Extract and process content based on content_type
#         if request.content_type == "youtube":
#             content_id = extract_video_id(request.content_id)
#             if not content_id:
#                 raise HTTPException(status_code=400, detail="Invalid YouTube URL")
#             raw_content = get_raw_transcript(content_id)
#         elif request.content_type == "pdf":
#             if not file:
#                 raise HTTPException(status_code=400, detail="PDF file is required")
#             content_id = file.filename
#             raw_content = extract_pdf_content(file)
#         elif request.content_type == "text":
#             content_id = request.content_id[:50]  # Use first 50 chars as identifier
#             raw_content = request.content_id
#         else:
#             raise HTTPException(status_code=400, detail="Invalid content type")

#         # Check if content has already been processed
#         db_video = db.query(Video).filter(Video.content_id == content_id).first()
#         if db_video:
#             return VideoResponse(
#                 id=db_video.id,
#                 content_type=db_video.content_type,
#                 content_id=db_video.content_id,
#                 title=db_video.title,
#                 processed_content=db_video.processed_content,
#                 processing_type=db_video.processing_type,
#                 processing_mode=db_video.processing_mode,
#                 processing_time=db_video.processing_time
#             )

#         # Process content
#         if request.processing_mode == "simple":
#             processed_content = process_content(raw_content, request.processing_type)
#         elif request.processing_mode == "detailed":
#             chunks = chunk_content(raw_content)
#             processed_content = process_content(chunks, request.processing_type)
#         else:
#             raise HTTPException(status_code=400, detail="Invalid processing mode")

#         processing_time = time.time() - start_time

#         # Save to database
#         db_video = Video(
#             content_type=request.content_type,
#             content_id=content_id,
#             title=f"Content {content_id}",  # TODO: Get actual content title
#             raw_content=raw_content,
#             processed_content=processed_content,
#             processing_type=request.processing_type,
#             processing_mode=request.processing_mode,
#             processing_time=processing_time
#         )
#         db.add(db_video)
#         db.commit()
#         db.refresh(db_video)

#         return VideoResponse(
#             id=db_video.id,
#             content_type=db_video.content_type,
#             content_id=db_video.content_id,
#             title=db_video.title,
#             processed_content=db_video.processed_content,
#             processing_type=db_video.processing_type,
#             processing_mode=db_video.processing_mode,
#             processing_time=db_video.processing_time
#         )
#     except Exception as e:
#         print(f"Error processing content: {str(e)}")  # Log the error
#         raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")

# @router.get("/content/{content_id}", response_model=VideoResponse)
# def get_content(content_id: str, db: Session = Depends(get_db)):
#     db_video = db.query(Video).filter(Video.content_id == content_id).first()
#     if db_video is None:
#         raise HTTPException(status_code=404, detail="Content not found")
#     return VideoResponse(
#         id=db_video.id,
#         content_type=db_video.content_type,
#         content_id=db_video.content_id,
#         title=db_video.title,
#         processed_content=db_video.processed_content,
#         processing_type=db_video.processing_type,
#         processing_mode=db_video.processing_mode,
#         processing_time=db_video.processing_time
#     )

# @router.put("/content/{content_id}", response_model=VideoResponse)
# def update_content(content_id: str, video_update: VideoUpdate, db: Session = Depends(get_db)):
#     db_video = db.query(Video).filter(Video.content_id == content_id).first()
#     if db_video is None:
#         raise HTTPException(status_code=404, detail="Content not found")
    
#     for key, value in video_update.dict(exclude_unset=True).items():
#         setattr(db_video, key, value)
    
#     db.commit()
#     db.refresh(db_video)
    
#     return VideoResponse(
#         id=db_video.id,
#         content_type=db_video.content_type,
#         content_id=db_video.content_id,
#         title=db_video.title,
#         processed_content=db_video.processed_content,
#         processing_type=db_video.processing_type,
#         processing_mode=db_video.processing_mode,
#         processing_time=db_video.processing_time
#     )