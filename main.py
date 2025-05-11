from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import billing, auth, video
from app.database import engine
# from app.models import content as content_model
from app.models import video as video_model


# Create database tables
video_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(billing.router, prefix="/billing", tags=["billing"])
# app.include_router(content.router, prefix="/content", tags=["content"])
app.include_router(video.router, prefix="/video", tags=["video"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Content Processing API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)