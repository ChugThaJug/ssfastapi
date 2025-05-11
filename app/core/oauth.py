import requests
from app.core.config import settings

def get_oauth2_token(provider: str, code: str):
    if provider == "google":
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json()
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def get_user_info(provider: str, access_token: str):
    if provider == "google":
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()
    else:
        raise ValueError(f"Unsupported provider: {provider}")