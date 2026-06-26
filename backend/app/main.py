from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

from app.routes import analyze, asset_search, remove_bg

app = FastAPI(title="AI Asset Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api")
app.include_router(asset_search.router, prefix="/api")
app.include_router(remove_bg.router, prefix="/api")

@app.get("/")
@app.head("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to AI Asset Finder API"}
