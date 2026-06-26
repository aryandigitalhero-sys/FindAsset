from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ScriptRequest(BaseModel):
    script: str

class Scene(BaseModel):
    scene: int
    text: str

class SceneAnalysisResponse(BaseModel):
    scenes: List[Scene]

class VisualKeywords(BaseModel):
    keywords: List[str]
    style: str
    emotion: str

class Asset(BaseModel):
    id: str
    preview: str
    source: str
    url: str
    resolution: Optional[str] = None
    type: str # video, image, gif, icon

class SceneAssets(BaseModel):
    videos: List[Asset] = []
    images: List[Asset] = []
    gifs: List[Asset] = []
    icons: List[Asset] = []

class SceneResult(BaseModel):
    scene: int
    text: str
    keywords: List[str]
    assets: SceneAssets
