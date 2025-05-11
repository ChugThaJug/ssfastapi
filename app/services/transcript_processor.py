# app/services/transcript_processor.py
import re
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from app.core.config import settings
from pydantic import AnyUrl
import os



from openai import OpenAI
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_video_id(url: AnyUrl) -> str:
    url_str = str(url)
    match = re.search(r"(?<=v=)[\w-]+|[\w-]+(?<=/v/)|(?<=youtu.be/)[\w-]+", url_str)
    return match.group(0) if match else None

def get_raw_transcript(video_id: str) -> List[Dict[str, str]]:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    return [{'start': s['start'], 'text': s['text']} for s in transcript]

def get_transcript_as_text(transcript: List[Dict[str, str]]) -> str:
    return ' '.join(s['text'] for s in transcript)

def process_transcript(transcript: List[Dict[str, str]], mode: str = "simple") -> List[Dict[str, str]]:
    full_text = get_transcript_as_text(transcript)
    
    if mode == "simple":
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
            {"role": "system", "content": "You are a helpful assistant that creates study guides."},
            {"role": "user", "content": f"Create a study guide based on the following text:\n\n{full_text}"}
            ],
            temperature=0.2
        )
        result = response.choices[0].message.content
        paragraphs = result.strip().split('\n\n')
    else:
        # Implement detailed processing mode here
        # This is a placeholder and should be replaced with actual implementation
        paragraphs = full_text.split('. ')

    return [{'paragraph_number': i, 'paragraph_text': p.strip()} for i, p in enumerate(paragraphs) if p.strip()]