import re
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
from app.core.config import settings
from pydantic import AnyUrl
import os
from openai import OpenAI

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
        paragraphs = simple_process(full_text)
    else:
        paragraphs = detailed_process(full_text)

    return [{'paragraph_number': i, 'paragraph_text': p.strip(), 'start_time': get_start_time(transcript, p)} 
            for i, p in enumerate(paragraphs) if p.strip()]

def simple_process(full_text: str) -> List[str]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that splits text into coherent paragraphs."},
            {"role": "user", "content": f"Split the following text into coherent paragraphs:\n\n{full_text}\n\nReturn only the paragraphs, separated by two newlines."}
        ],
        temperature=0.2
    )
    result = response.choices[0].message.content
    return result.strip().split('\n\n')

def detailed_process(full_text: str) -> List[str]:
    chunk_size = 5000
    overlap = 200
    chunks = chunk_text(full_text, chunk_size, overlap)
    
    processed_chunks = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that improves text readability and structures it into paragraphs."},
                {"role": "user", "content": f"Improve the readability of the following text and structure it into paragraphs:\n\n{chunk}\n\nReturn only the improved and structured text."}
            ],
            temperature=0.2
        )
        processed_chunks.append(response.choices[0].message.content)
    
    return combine_processed_chunks(processed_chunks)

def chunk_text(text: str, chunk_size: int = 5000, overlap: int = 200) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            end = text.rfind(' ', end - overlap, end) + 1
        chunk = text[start:end].strip()
        chunks.append(chunk)
        start = end - overlap
    return chunks

def combine_processed_chunks(chunks: List[str]) -> List[str]:
    combined_text = ' '.join(chunks)
    return combined_text.split('\n\n')

def get_start_time(transcript: List[Dict[str, str]], paragraph: str) -> float:
    words = paragraph.split()
    for entry in transcript:
        if any(word in entry['text'] for word in words[:5]):
            return entry['start']
    return 0.0  # Default to 0 if no match found

# Additional functions for different processing types can be added here
def generate_summary(paragraphs: List[Dict[str, str]]) -> str:
    full_text = ' '.join(p['paragraph_text'] for p in paragraphs)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates concise summaries."},
            {"role": "user", "content": f"Generate a concise summary of the following text:\n\n{full_text}"}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def generate_study_guide(paragraphs: List[Dict[str, str]]) -> str:
    full_text = ' '.join(p['paragraph_text'] for p in paragraphs)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates study guides."},
            {"role": "user", "content": f"Create a study guide based on the following text:\n\n{full_text}"}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

# Add more functions for other processing types (FAQ, timeline, etc.) as needed