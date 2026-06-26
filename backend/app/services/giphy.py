import os
import httpx
from app.schemas.models import Asset
from app.utils.rate_limiter import giphy_limiter, with_retry

GIPHY_API_KEY = os.environ.get("GIPHY_API_KEY")

@with_retry()
async def search_giphy(query: str, limit: int = 3) -> dict:
    gifs = []
    
    if not GIPHY_API_KEY:
        return {"gifs": gifs}

    async with giphy_limiter:
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(
                    "https://api.giphy.com/v1/gifs/search",
                    params={"api_key": GIPHY_API_KEY, "q": query, "limit": limit}
                )
                if res.status_code == 200:
                    data = res.json()
                    for g in data.get("data", []):
                        gifs.append(Asset(
                            id=f"giphy-{g['id']}",
                            preview=g["images"]["fixed_height"]["url"],
                            source="Giphy",
                            url=g["images"]["original"]["url"],
                            resolution=f"{g['images']['original']['width']}x{g['images']['original']['height']}",
                            type="gif"
                        ))
            except Exception as e:
                print(f"Error fetching from Giphy: {e}")

    return {"gifs": gifs}
