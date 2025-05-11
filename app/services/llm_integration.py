from app.core.config import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

async def process_with_llm(content: str, processing_type: str):
    prompt = generate_prompt(content, processing_type)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000
    )
    return response.choices[0].text.strip()

def generate_prompt(content: str, processing_type: str):
    prompts = {
        "summary": f"Summarize the following content:\n\n{content}\n\nSummary:",
        "transcript": f"Improve the readability of the following transcript:\n\n{content}\n\nImproved transcript:",
        "guide": f"Create a step-by-step guide based on the following content:\n\n{content}\n\nGuide:",
        "faq": f"Generate a list of FAQs based on the following content:\n\n{content}\n\nFAQs:",
        "study_guide": f"Create a study guide from the following content:\n\n{content}\n\nStudy Guide:",
        "timeline": f"Create a timeline of events from the following content:\n\n{content}\n\nTimeline:",
        "briefing": f"Create a briefing document from the following content:\n\n{content}\n\nBriefing:"
    }
    return prompts.get(processing_type, "Summarize the following content:")