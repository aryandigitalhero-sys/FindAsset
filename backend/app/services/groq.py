import os
import json
from groq import AsyncGroq
from app.schemas.models import Scene, VisualKeywords
from app.utils.rate_limiter import groq_limiter, with_retry

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

@with_retry()
async def split_scenes(script: str) -> list[Scene]:
    async with groq_limiter:
        prompt = f"""
    You are an expert social media video editor specializing in high-engagement TikToks, Instagram Reels, and YouTube Shorts.
    Split the following script into fast-paced, highly visual, and engaging scenes designed for maximum audience retention.
    Return ONLY a JSON array of objects, where each object has a 'scene' number and 'text'.
    No markdown formatting or extra text.

    Script:
    {script}
    """
    try:
        completion = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        # Handle the case where groq returns it wrapped in another key or directly
        response_content = completion.choices[0].message.content
        data = json.loads(response_content)
        
        # If it's a dict containing a list, try to extract it
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, list):
                    return [Scene(**item) for item in v]
            # fallback
            return []
        elif isinstance(data, list):
            return [Scene(**item) for item in data]
    except Exception as e:
        print(f"Error in split_scenes: {e}")
        return []

@with_retry()
async def generate_visual_plan(scene_text: str) -> VisualKeywords:
    async with groq_limiter:
        prompt = f"""
    You are an expert art director for viral social media content (Reels, TikToks). Analyze the following scene text and extract the core visual elements that drive high engagement and visual hooks.
    Be highly specific and literal. Focus on tangible objects, environments, bold lighting, and dynamic actions.
    
    CRITICAL INSTRUCTION: If the scene text contains explicit visual directions enclosed in brackets (e.g., [Visual: ...], [Meme: ...]), you MUST prioritize extracting your keywords directly from those bracketed instructions over the rest of the text.

    Provide:
    - 'keywords': A list of 3-5 highly descriptive, visual nouns or short phrases (e.g., "neon-lit alleyway", "steaming coffee cup"). Do not include abstract concepts.
    - 'style': The visual aesthetic (e.g., "cinematic", "cyberpunk", "minimalist", "documentary").
    - 'emotion': The mood of the scene.

    Return ONLY a JSON object with these exact keys: 'keywords', 'style', 'emotion'.
    No markdown formatting or extra text.

    Scene Text:
    {scene_text}
    """
    try:
        completion = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)
        return VisualKeywords(**data)
    except Exception as e:
        print(f"Error in generate_visual_plan: {e}")
        return VisualKeywords(keywords=[], style="", emotion="")

@with_retry()
async def optimize_search_query(keywords: list[str], style: str, emotion: str) -> str:
    async with groq_limiter:
        prompt = f"""
    You are an expert search engine optimizer for stock photo/video websites (Pexels, Unsplash).
    Your goal is to find eye-catching, high-quality vertical videos suitable for social media edits (Reels/TikToks).
    Stock APIs prefer short, literal, and highly specific noun-based queries. 
    They fail if given long sentences or abstract concepts.

    Input:
    Keywords: {', '.join(keywords)}
    Style: {style}
    Emotion: {emotion}

    Task: Combine the best, most visually prominent keywords and style into a single, highly effective search query of 2 to 5 words maximum.
    (Example: "cinematic neon alleyway" or "happy family beach").

    Return ONLY the exact search query string. Do not use quotes or any other text.
    """
    try:
        completion = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in optimize_search_query: {e}")
        return " ".join(keywords)
