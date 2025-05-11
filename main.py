from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import billing, auth, video
from app.database import engine
# from app.models import content as content_model
from app.models import video as video_model

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Try explicit imports instead of importing from a module
from app.api.endpoints.video import router as video_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.billing import router as billing_router


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

# Include routers with explicit variables
app.include_router(video_router, prefix="/video", tags=["video"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(billing_router, prefix="/billing", tags=["billing"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Content Processing API"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)