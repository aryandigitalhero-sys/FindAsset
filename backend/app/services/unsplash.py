import os
import httpx
from app.schemas.models import Asset
from app.utils.rate_limiter import unsplash_limiter, with_retry

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")

@with_retry()
async def search_unsplash(query: str, orientation: str = "portrait", limit: int = 3) -> dict:
    images = []
    
    if not UNSPLASH_ACCESS_KEY:
        return {"images": images}

    async with unsplash_limiter:
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(
                    "https://api.unsplash.com/search/photos",
                    params={"query": query, "orientation": orientation, "per_page": limit},
                    headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
                )
                if res.status_code == 200:
                    data = res.json()
                    for i in data.get("results", []):
                        images.append(Asset(
                            id=f"unsplash-img-{i['id']}",
                            preview=i["urls"]["small"],
                            source="Unsplash",
                            url=i["urls"]["raw"],
                            resolution=f"{i.get('width')}x{i.get('height')}",
                            type="image"
                        ))
            except Exception as e:
                print(f"Error fetching from Unsplash: {e}")

    return {"images": images}
