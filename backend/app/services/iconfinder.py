import os
import httpx
from app.schemas.models import Asset
from app.utils.rate_limiter import iconfinder_limiter, with_retry

ICONFINDER_API_KEY = os.environ.get("ICONFINDER_API_KEY")

@with_retry()
async def search_iconfinder(query: str, limit: int = 3) -> dict:
    icons = []
    
    if not ICONFINDER_API_KEY:
        return {"icons": icons}

    async with iconfinder_limiter:
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(
                    "https://api.iconfinder.com/v4/icons/search",
                    params={"query": query, "count": limit, "premium": False},
                    headers={"Authorization": f"Bearer {ICONFINDER_API_KEY}"}
                )
                if res.status_code == 200:
                    data = res.json()
                    for icon in data.get("icons", []):
                        # find largest size
                        raster_sizes = sorted(icon.get("raster_sizes", []), key=lambda x: x.get("size", 0), reverse=True)
                        if raster_sizes:
                            best_format = raster_sizes[0].get("formats", [])[0]
                            preview_url = best_format.get("preview_url")
                            
                            if preview_url:
                                icons.append(Asset(
                                    id=f"iconfinder-{icon['icon_id']}",
                                    preview=preview_url,
                                    source="Iconfinder",
                                    url=preview_url, # Iconfinder requires auth to download, so we just use preview as url
                                    resolution=f"{raster_sizes[0]['size']}x{raster_sizes[0]['size']}",
                                    type="icon"
                                ))
            except Exception as e:
                print(f"Error fetching from Iconfinder: {e}")

    return {"icons": icons}
