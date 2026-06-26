import os
import httpx
from app.schemas.models import Asset
from app.utils.rate_limiter import pexels_limiter, with_retry

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

@with_retry()
async def search_pexels(query: str, orientation: str = "portrait", limit: int = 3) -> dict:
    headers = {"Authorization": PEXELS_API_KEY}
    videos = []
    images = []
    
    if not PEXELS_API_KEY:
        return {"videos": videos, "images": images}

    async with pexels_limiter:
        async with httpx.AsyncClient() as client:
            try:
                # Search videos
                v_res = await client.get(
                    "https://api.pexels.com/videos/search",
                    params={"query": query, "orientation": orientation, "per_page": limit},
                    headers=headers
                )
                if v_res.status_code == 200:
                    v_data = v_res.json()
                    for v in v_data.get("videos", []):
                        video_files = sorted(v.get("video_files", []), key=lambda x: x.get("width", 0), reverse=True)
                        url = video_files[0]["link"] if video_files else v.get("url")
                        
                        videos.append(Asset(
                            id=f"pexels-vid-{v['id']}",
                            preview=v.get("image", ""),
                            source="Pexels",
                            url=url,
                            resolution=f"{v.get('width')}x{v.get('height')}",
                            type="video"
                        ))
                
                # Search images
                i_res = await client.get(
                    "https://api.pexels.com/v1/search",
                    params={"query": query, "orientation": orientation, "per_page": limit},
                    headers=headers
                )
                if i_res.status_code == 200:
                    i_data = i_res.json()
                    for i in i_data.get("photos", []):
                        images.append(Asset(
                            id=f"pexels-img-{i['id']}",
                            preview=i["src"]["medium"],
                            source="Pexels",
                            url=i["src"]["original"],
                            resolution=f"{i.get('width')}x{i.get('height')}",
                            type="image"
                        ))
            except Exception as e:
                print(f"Error fetching from Pexels: {e}")

    return {"videos": videos, "images": images}
