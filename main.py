from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YouTube Transcript API",
    description="API to fetch YouTube video transcripts with Azure Key Vault integration",
    version="1.0.0",
    # Configure URLs for AKS deployment
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    message: str

# Configuration class to handle secrets
class Config:
    def __init__(self):
        # Note: YouTube Transcript API doesn't require an API key
        # Only keeping this for potential future use with YouTube Data API
        self.youtube_api_key = None
        self._load_youtube_api_key()
    
    def _load_youtube_api_key(self):
        """Load YouTube API key from Azure Key Vault, environment variable, or local settings file"""
        try:
            # First, try Azure Key Vault
            key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
            if key_vault_url:
                self.youtube_api_key = self._get_secret_from_key_vault(key_vault_url, "YouTubeApiKey")
                if self.youtube_api_key:
                    logger.info("YouTube API key loaded from Azure Key Vault")
                    return
        except Exception as e:
            logger.warning(f"Failed to load from Azure Key Vault: {e}")
        
        # Second, try environment variable
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        if self.youtube_api_key:
            logger.info("YouTube API key loaded from environment variable")
            return
        
        # Third, try local settings file
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    self.youtube_api_key = settings.get("youtube_api_key")
                    if self.youtube_api_key:
                        logger.info("YouTube API key loaded from local settings file")
                        return
        except Exception as e:
            logger.warning(f"Failed to load from settings file: {e}")
        
        logger.info("No YouTube API key found - transcript API will work without it")
    
    def _get_secret_from_key_vault(self, key_vault_url: str, secret_name: str) -> Optional[str]:
        """Retrieve secret from Azure Key Vault"""
        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=key_vault_url, credential=credential)
            secret = client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            logger.error(f"Error retrieving secret from Key Vault: {e}")
            return None

# Initialize configuration
config = Config()

# Create routers for both paths
api_router = APIRouter(prefix="/api")

@api_router.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="YouTube Transcript API is running"
    )

@api_router.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Service is running. YouTube Transcript API ready."
    )

# Add debug endpoint to check URLs
@api_router.get("/debug/urls")
async def debug_urls():
    """Debug endpoint to check configured URLs"""
    return {
        "docs_url": app.docs_url,
        "redoc_url": app.redoc_url,
        "openapi_url": app.openapi_url,
        "root_path": app.root_path,
        "available_endpoints": [
            "/api/docs",
            "/api/redoc", 
            "/api/openapi.json",
            "/api/swagger.json",
            "/api/health",
            "/api/debug/urls"
        ]
    }

# OpenAPI endpoints for both paths
@api_router.get("/openapi.json", include_in_schema=False)
async def openapi_json():
    """OpenAPI JSON schema"""
    return JSONResponse(app.openapi())

# Keep swagger.json for compatibility
@api_router.get("/swagger.json", include_in_schema=False)
async def swagger_json():
    return JSONResponse(app.openapi())

@api_router.get("/docs", include_in_schema=False)
async def aks_docs():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/yt/api/openapi.json", title="YouTube Transcript API")

@api_router.get("/redoc", include_in_schema=False)
async def aks_redoc():
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(openapi_url="/yt/api/openapi.json", title="YouTube Transcript API")
# Add this after your existing endpoints

# Include routers
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
