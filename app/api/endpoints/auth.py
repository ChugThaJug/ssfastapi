from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.config import settings
from app.api import deps
from app.models.user import User
from app.core.security import create_access_token
from app.core.oauth import get_oauth2_token, get_user_info
from datetime import datetime, timedelta
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/login/oauth/{provider}")
async def login_oauth(
    provider: str, 
    code: str = Query(..., description="Authorization code"),
    db: Session = Depends(deps.get_db)
):
    logger.info(f"Received OAuth login request for provider: {provider}")
    logger.info(f"Received code: {code}")
    
    if provider != "google":
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")
    
    try:
        # Exchange code for token
        token_data = get_oauth2_token(provider, code)
        
        # Get user info from Google
        user_info = get_user_info(provider, token_data["access_token"])
        
        # Find or create user in your database
        user = db.query(User).filter(User.email == user_info["email"]).first()
        if not user:
            user = User(email=user_info["email"], username=user_info.get("name"))
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token for your app
        access_token_expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "exp": access_token_expires}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during OAuth login: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))