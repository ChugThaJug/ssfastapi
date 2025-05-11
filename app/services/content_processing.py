# content processing 

from typing import List, Dict, Union
import os
from app.core.config import settings

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def process_content(content: Union[str, List[Dict[str, str]]], processing_type: str, processing_mode: str) -> str:
    if processing_mode == "detailed" and isinstance(content, str):
        # For detailed processing, we chunk the content first
        content = chunk_content(content)
    
    if isinstance(content, list):
        # For detailed processing, we process each chunk and then combine
        processed_chunks = [await process_chunk(chunk, processing_type) for chunk in content]
        return combine_chunks(processed_chunks, processing_type)
    else:
        # For simple processing, we process the entire content at once
        return await process_chunk(content, processing_type)

async def process_chunk(chunk: str, processing_type: str) -> str:
    prompt = generate_prompt(chunk, processing_type)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that processes content based on specific instructions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    result = response.choices[0].message.content
    return result

def generate_prompt(content: str, processing_type: str) -> str:
    prompts = {
        "summary": f"Summarize the following content:\n\n{content}",
        "transcript": f"Improve the readability of the following transcript:\n\n{content}",
        "study_guide": f"Create a study guide from the following content:\n\n{content}",
        "faq": f"Generate a list of FAQs based on the following content:\n\n{content}",
        "timeline": f"Create a timeline of events from the following content:\n\n{content}",
        "briefing": f"Create a briefing document from the following content:\n\n{content}"
    }
    return prompts.get(processing_type, f"Process the following content:\n\n{content}")

def combine_chunks(chunks: List[str], processing_type: str) -> str:
    if processing_type in ["summary", "transcript", "briefing"]:
        return " ".join(chunks)
    elif processing_type in ["study_guide", "faq", "timeline"]:
        return "\n\n".join(chunks)
    else:
        return "\n\n".join(chunks)

def chunk_content(content: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    chunks = []
    start = 0
    while start < len(content):
        end = start + chunk_size
        if end < len(content):
            # Try to find the end of a sentence within the last 200 characters of the chunk
            sentence_end = content.rfind('.', end - 200, end)
            if sentence_end != -1:
                end = sentence_end + 1
        chunk = content[start:end].strip()
        chunks.append(chunk)
        start = end - overlap
    return chunks