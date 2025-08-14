"""FastAPI application entry point with production configurations."""

import logging
import sys
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.config import settings
from app.routes import chat_router, scrape_router
from app.services.scraper_service import scraper
from app.services.vectorstore_service import vectorstore

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("Starting I2C AI Chatbot API...")
    
    # Create necessary directories
    settings.create_directories()
    
    # Initialize services
    try:
        logger.info("Initializing services...")
        
        # Initialize vector store collection
        vectorstore.get_collection()
        
        # Production startup scraping
        if settings.is_production():
            logger.info("Starting automatic scraping...")
            try:
                scraped_content = await scraper.scrape_website(
                    base_url=settings.BASE_URL,
                    max_pages=settings.MAX_SCRAPE_PAGES,
                    delay=settings.SCRAPE_DELAY
                )
                
                documents_processed = 0
                for content in scraped_content:
                    try:
                        vectorstore.add_webpage(
                            url=content["url"],
                            content=content["content"],
                            title=content["title"],
                            metadata=content.get("metadata", {})
                        )
                        documents_processed += 1
                    except Exception as e:
                        logger.error(f"Error adding document to vectorstore: {e}")
                
                logger.info(f"Added {documents_processed} documents to vectorstore")
            except Exception as e:
                logger.error(f"Error during startup scraping: {e}")
                
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down I2C AI Chatbot API...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered chatbot for i2cinc.com",
    version="1.0.0",
    docs_url="/api/docs" if not settings.is_production() else None,
    redoc_url="/api/redoc" if not settings.is_production() else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(chat_router, prefix=settings.API_V1_PREFIX + "/chat")
app.include_router(scrape_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"{settings.APP_NAME} API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    if settings.is_production():
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__}
    )
