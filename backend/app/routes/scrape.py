"""Scraping API endpoints."""

import time
from typing import List

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from app.models import (
    ScrapeRequest,
    ScrapeResponse,
    ErrorResponse,
)
from app.services.scraper_service import scraper
from app.services.lightweight_crawler import lightweight_crawler
from app.services.vectorstore_service import vectorstore

router = APIRouter(prefix="/scrape", tags=["scrape"])


@router.post(
    "/",
    response_model=ScrapeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def scrape_website(
    request: ScrapeRequest
) -> ScrapeResponse:
    """Scrape website content and update vector store."""
    start_time = time.time()
    
    try:
        logger.info(f"Starting scrape for: {request.url}")
        
        # Use the new lightweight crawler for inner link discovery
        async with lightweight_crawler as crawler:
            scraped_content = await crawler.get_real_time_data(
                start_url=request.url
            )
        
        if not scraped_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No content found to scrape"
            )
        
        # Process and add to vector store
        documents_processed = 0
        errors = []
        
        for content in scraped_content:
            try:
                # Add to vector store
                vectorstore.add_webpage(
                    url=content["url"],
                    content=content["content"],
                    title=content["title"],
                    metadata={
                        "url": content["url"],
                        "title": content["title"],
                        "source": "enhanced_crawler"
                    }
                )
                documents_processed += 1
                
            except Exception as e:
                error_msg = f"Error processing {content['url']}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        return ScrapeResponse(
            url=request.url,
            pages_scraped=len(scraped_content),
            documents_processed=documents_processed,
            errors=errors,
            processing_time=time.time() - start_time
        )
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/enhanced",
    response_model=ScrapeResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def scrape_website_enhanced(
    request: ScrapeRequest
) -> ScrapeResponse:
    """Enhanced scraping with inner link discovery using lightweight crawler."""
    start_time = time.time()
    
    try:
        logger.info(f"Starting enhanced scrape for: {request.url}")
        
        # Use the new lightweight crawler for inner link discovery
        async with lightweight_crawler as crawler:
            scraped_content = await crawler.crawl_with_discovery(
                start_url=request.url,
                max_depth=2
            )
        
        if not scraped_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No content found to scrape"
            )
        
        # Process and add to vector store
        documents_processed = 0
        errors = []
        
        for content in scraped_content:
            try:
                # Add to vector store
                vectorstore.add_webpage(
                    url=content["url"],
                    content=content["content"],
                    title=content["title"],
                    metadata={
                        "url": content["url"],
                        "title": content["title"],
                        "source": "enhanced_crawler"
                    }
                )
                documents_processed += 1
                
            except Exception as e:
                error_msg = f"Error processing {content['url']}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        return ScrapeResponse(
            url=request.url,
            pages_scraped=len(scraped_content),
            documents_processed=documents_processed,
            errors=errors,
            processing_time=time.time() - start_time
        )
        
    except Exception as e:
        logger.error(f"Error during enhanced scraping: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/stats",
    response_model=dict,
    status_code=status.HTTP_200_OK
)
async def get_scraping_stats():
    """Get scraping statistics."""
    try:
        stats = vectorstore.get_collection_stats()
        return {
            "total_documents": stats["total_documents"],
            "unique_sources": stats["unique_sources"],
            "sources": stats["sources"]
        }
        
    except Exception as e:
        logger.error(f"Error getting scraping stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
