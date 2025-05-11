from youtube_transcript_api import YouTubeTranscriptApi
import re
from typing import Tuple


async def extract_content(content_type: str, content_id: str) -> Tuple[str, str]:
    if content_type == "youtube":
        video_id = extract_video_id(content_id)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
        content = extract_youtube_transcript(video_id)
        return video_id, content
    elif content_type == "text":
        return content_id[:50], content_id  # Use first 50 chars as identifier for text content
    else:
        raise ValueError(f"Unsupported content type: {content_type}")
    
def extract_youtube_transcript(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        raise ValueError(f"Could not retrieve transcript: {str(e)}")

def extract_video_id(url: str) -> str:
    # Extract video ID from various forms of YouTube URLs
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:\S*(?:(?:\/e(?:mbed))?\/|(?:v=)))?([^&?\/\s]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None