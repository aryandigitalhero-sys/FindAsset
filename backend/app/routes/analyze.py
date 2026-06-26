from fastapi import APIRouter, HTTPException
from app.schemas.models import ScriptRequest, SceneAnalysisResponse
from app.services.groq import split_scenes

router = APIRouter()

@router.post("/analyze-script", response_model=SceneAnalysisResponse)
async def analyze_script(request: ScriptRequest):
    scenes = await split_scenes(request.script)
    if not scenes:
        raise HTTPException(status_code=500, detail="Failed to split script into scenes")
    return SceneAnalysisResponse(scenes=scenes)
