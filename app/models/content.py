# from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from app.database import Base


# class Content(Base):
#     __tablename__ = "contents"

#     id = Column(Integer, primary_key=True, index=True)
#     content_type = Column(String, index=True)
#     content_id = Column(String, unique=True, index=True)
#     title = Column(String, nullable=True)
#     raw_content = Column(String, nullable=True)
#     processed_content = Column(String, nullable=True)
#     processing_type = Column(String)
#     processing_mode = Column(String)
#     processing_time = Column(Float, nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())

#     __table_args__ = (UniqueConstraint('content_id', name='uq_content_id'),)

#     def __repr__(self):
#         return f"<Content(id={self.id}, content_id={self.content_id}, content_type={self.content_type})>"

# class ProcessingHistory(Base):
#     __tablename__ = "processing_history"

#     id = Column(Integer, primary_key=True, index=True)
#     content_id = Column(Integer, ForeignKey("contents.id"))
#     processing_type = Column(String)
#     processing_mode = Column(String)
#     processing_time = Column(Float)
#     processed_at = Column(DateTime(timezone=True), server_default=func.now())

#     # Relationship with Content
#     content = relationship("Content", back_populates="processing_history")