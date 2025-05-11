from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentResponse
from app.services.content_extraction import extract_content
from app.services.content_processing import process_content
import time
import logging

router = APIRouter()

@router.post("/process_content/", response_model=ContentResponse)
async def process_content_endpoint(
    request: ContentCreate,
    db: Session = Depends(get_db)
):
    try:
        start_time = time.time()

        # Extract content
        try:
            content_id, raw_content = await extract_content(request.content_type, request.content_id)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))

        # Process content
        processed_content = await process_content(
            raw_content, 
            request.processing_type, 
            request.processing_mode
        )

        processing_time = time.time() - start_time

        # Check if content already exists
        existing_content = db.query(Content).filter(Content.content_id == content_id).first()

        if existing_content:
            # Update existing content
            existing_content.raw_content = str(raw_content)
            existing_content.processed_content = processed_content
            existing_content.processing_type = request.processing_type
            existing_content.processing_mode = request.processing_mode
            existing_content.processing_time = processing_time
            db.commit()
            db.refresh(existing_content)
            return ContentResponse.model_validate(existing_content)
        else:
            # Create new content
            db_content = Content(
                content_type=request.content_type,
                content_id=content_id,
                title=f"Content {content_id[:30]}...",  # TODO: Get actual content title
                raw_content=str(raw_content),
                processed_content=processed_content,
                processing_type=request.processing_type,
                processing_mode=request.processing_mode,
                processing_time=processing_time
            )
            db.add(db_content)
            db.commit()
            db.refresh(db_content)
            return ContentResponse.model_validate(db_content)

    except IntegrityError as e:
        db.rollback()
        print(f"Integrity Error: {str(e)}")
        raise HTTPException(status_code=409, detail="Content with this ID already exists")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error processing content: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")

@router.get("/content/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str, db: Session = Depends(get_db)):
    logging.info(f"Attempting to retrieve content with ID: {content_id}")
    db_content = db.query(Content).filter(Content.content_id == content_id).first()
    if db_content is None:
        logging.warning(f"Content with ID {content_id} not found in database")
        raise HTTPException(status_code=404, detail="Content not found")
    logging.info(f"Content found: {db_content}")
    return ContentResponse.model_validate(db_content)

# @router.put("/content/{content_id}", response_model=ContentResponse)
# async def update_content(
#     content_id: str, 
#     update_data: ContentUpdate,
#     db: Session = Depends(get_db)
# ):
#     db_content = db.query(Content).filter(Content.content_id == content_id).first()
#     if db_content is None:
#         raise HTTPException(status_code=404, detail="Content not found")
    
#     for key, value in update_data.dict(exclude_unset=True).items():
#         setattr(db_content, key, value)
    
#     db.commit()
#     db.refresh(db_content)
    
#     return ContentResponse.from_orm(db_content)