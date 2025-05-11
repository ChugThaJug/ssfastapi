# from pydantic import BaseModel, ConfigDict
# from typing import Optional, List
# from datetime import datetime

# class ContentBase(BaseModel):
#     content_type: str
#     content_id: str
#     processing_type: str
#     processing_mode: str

# class ContentCreate(ContentBase):
#     title: Optional[str] = None

# class ContentUpdate(BaseModel):
#     title: Optional[str] = None
#     processed_content: Optional[str] = None
#     processing_type: Optional[str] = None
#     processing_mode: Optional[str] = None

# class ContentInDB(ContentBase):
#     id: int
#     title: Optional[str] = None
#     raw_content: Optional[str] = None
#     processed_content: Optional[str] = None
#     processing_time: Optional[float] = None
#     created_at: Optional[datetime] = None
#     updated_at: Optional[datetime] = None

#     model_config = ConfigDict(from_attributes=True)

# class ContentResponse(BaseModel):
#     id: int
#     content_type: str
#     content_id: str
#     title: Optional[str] = None
#     processed_content: Optional[str] = None
#     processing_type: str
#     processing_mode: str
#     processing_time: Optional[float] = None

#     model_config = ConfigDict(from_attributes=True)

# class ProcessingHistoryBase(BaseModel):
#     processing_type: str
#     processing_mode: str
#     processing_time: float

# class ProcessingHistoryCreate(ProcessingHistoryBase):
#     content_id: int

# class ProcessingHistoryInDB(ProcessingHistoryBase):
#     id: int
#     content_id: int
#     processed_at: datetime

#     model_config = ConfigDict(from_attributes=True)

# class ProcessingHistoryResponse(ProcessingHistoryInDB):
#     pass

# class ContentWithHistory(ContentResponse):
#     processing_history: List[ProcessingHistoryResponse] = []

# class ContentListItem(BaseModel):
#     id: int
#     content_type: str
#     content_id: str
#     title: Optional[str] = None
#     processing_type: str
#     processing_mode: str
#     created_at: Optional[datetime] = None

#     model_config = ConfigDict(from_attributes=True)

# class PaginatedContentList(BaseModel):
#     items: List[ContentListItem]
#     total: int
#     page: int
#     size: int
#     pages: int