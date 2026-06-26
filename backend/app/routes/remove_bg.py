from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import httpx
from rembg import remove
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class RemoveBgRequest(BaseModel):
    url: str

@router.post("/remove-bg")
async def remove_background(req: RemoveBgRequest):
    try:
        logger.info(f"Downloading image for bg removal: {req.url}")
        async with httpx.AsyncClient() as client:
            response = await client.get(req.url)
            response.raise_for_status()
            input_image_bytes = response.content

        logger.info("Processing image with rembg...")
        # rembg.remove returns the processed image as bytes
        output_image_bytes = remove(input_image_bytes)

        logger.info("Background removal successful")
        return Response(content=output_image_bytes, media_type="image/png")

    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred while fetching image: {e}")
        raise HTTPException(status_code=400, detail="Failed to fetch image from URL")
    except Exception as e:
        logger.error(f"Error during background removal: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during background removal")
