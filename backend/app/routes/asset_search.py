import asyncio
from fastapi import APIRouter
from app.schemas.models import ScriptRequest, SceneResult, SceneAssets, VisualKeywords
from app.services.groq import split_scenes, generate_visual_plan, optimize_search_query
from app.services.pexels import search_pexels
from app.services.pixabay import search_pixabay
from app.services.unsplash import search_unsplash
from app.services.giphy import search_giphy
from app.services.iconfinder import search_iconfinder
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

async def process_scene(scene) -> SceneResult:
    logger.info(f"Processing scene {scene.scene}: {scene.text[:30]}...")
    
    # 1. Visual Understanding
    visual_plan: VisualKeywords = await generate_visual_plan(scene.text)
    logger.info(f"Scene {scene.scene} visual plan: {visual_plan.keywords}")
    
    # 2. Keyword generation / optimization
    search_query = await optimize_search_query(visual_plan.keywords, visual_plan.style, visual_plan.emotion)
    logger.info(f"Scene {scene.scene} optimized query: '{search_query}'")
    
    # 3. Parallel Asset Search
    logger.info(f"Scene {scene.scene} starting parallel asset search...")
    results = await asyncio.gather(
        search_pexels(search_query),
        search_pixabay(search_query),
        search_unsplash(search_query),
        search_giphy(search_query),
        search_iconfinder(search_query)
    )
    
    pexels_res, pixabay_res, unsplash_res, giphy_res, iconfinder_res = results
    
    # Combine results
    videos = pexels_res["videos"] + pixabay_res["videos"]
    images = pexels_res["images"] + pixabay_res["images"] + unsplash_res["images"]
    gifs = giphy_res["gifs"]
    icons = iconfinder_res["icons"]
    
    logger.info(f"Scene {scene.scene} search complete: {len(videos)} videos, {len(images)} images, {len(gifs)} gifs, {len(icons)} icons")
    
    return SceneResult(
        scene=scene.scene,
        text=scene.text,
        keywords=visual_plan.keywords,
        assets=SceneAssets(
            videos=videos,
            images=images,
            gifs=gifs,
            icons=icons
        )
    )

@router.post("/generate", response_model=list[SceneResult])
async def generate_assets(request: ScriptRequest):
    logger.info(f"Received script for generation ({len(request.script)} characters)")
    
    # 1. Split script into scenes
    scenes = await split_scenes(request.script)
    
    if not scenes:
        logger.error("Failed to split script into scenes, or 0 scenes returned.")
        return []

    logger.info(f"Script split into {len(scenes)} scenes. Processing in parallel...")
    # 2. Process all scenes in parallel
    scene_results = await asyncio.gather(*(process_scene(scene) for scene in scenes))
    
    logger.info(f"Successfully processed all {len(scenes)} scenes.")
    # Return sorted by scene number
    return sorted(list(scene_results), key=lambda x: x.scene)
