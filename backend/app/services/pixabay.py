import os
import httpx
from app.schemas.models import Asset
from app.utils.rate_limiter import pixabay_limiter, with_retry

PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY")

@with_retry()
async def search_pixabay(query: str, limit: int = 3) -> dict:
    videos = []
    images = []

    if not PIXABAY_API_KEY:
        return {"videos": videos, "images": images}

    async with pixabay_limiter:
        async with httpx.AsyncClient() as client:
            try:
                # Search videos
                v_res = await client.get(
                    "https://pixabay.com/api/videos/",
                    params={"key": PIXABAY_API_KEY, "q": query, "per_page": limit}
                )
                if v_res.status_code == 200:
                    v_data = v_res.json()
                    for v in v_data.get("hits", []):
                        videos.append(Asset(
                            id=f"pixabay-vid-{v['id']}",
                            preview=v.get("picture_id") and f"https://i.vimeocdn.com/video/{v['picture_id']}_640x360.jpg" or "",
                            source="Pixabay",
                            url=v["videos"]["large"]["url"],
                            resolution=f"{v['videos']['large']['width']}x{v['videos']['large']['height']}",
                            type="video"
                        ))

                # Search images
                i_res = await client.get(
                    "https://pixabay.com/api/",
                    params={"key": PIXABAY_API_KEY, "q": query, "per_page": limit}
                )
                if i_res.status_code == 200:
                    i_data = i_res.json()
                    for i in i_data.get("hits", []):
                        images.append(Asset(
                            id=f"pixabay-img-{i['id']}",
                            preview=i["webformatURL"],
                            source="Pixabay",
                            url=i["largeImageURL"],
                            resolution=f"{i.get('imageWidth')}x{i.get('imageHeight')}",
                            type="image"
                        ))
            except Exception as e:
                print(f"Error fetching from Pixabay: {e}")

    return {"videos": videos, "images": images}
