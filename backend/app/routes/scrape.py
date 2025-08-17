"""Enhanced scraping endpoints for i2c content discovery."""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.scraper_service import scraper
from app.services.lightweight_crawler import lightweight_crawler
from pydantic import BaseModel

router = APIRouter()

class ScrapingRequest(BaseModel):
    url: Optional[str] = None
    max_pages: int = 10
    max_depth: int = 3
    include_keywords: bool = True

class ScrapingResponse(BaseModel):
    content: List[dict]
    total_found: int
    sources: List[str]
    keywords: List[str]
    metadata: dict

@router.post("/scrape-enhanced", response_model=ScrapingResponse)
async def scrape_enhanced(request: ScrapingRequest):
    """Enhanced scraping with i2c content discovery."""
    try:
        # Use enhanced scraper
        content = await scraper.scrape_website(
            max_pages=request.max_pages,
            base_url=request.url
        )
        
        # Extract unique sources
        sources = list(set(item['url'] for item in content))
        
        # Extract keywords
        keywords = []
        for item in content:
            if item.get('keywords'):
                keywords.extend(item['keywords'].split(','))
        
        keywords = list(set(keywords))
        
        return ScrapingResponse(
            content=content,
            total_found=len(content),
            sources=sources,
            keywords=keywords,
            metadata={
                "scraping_method": "enhanced",
                "max_pages": request.max_pages,
                "url": request.url or "https://i2cinc.com"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/crawl-discovery", response_model=ScrapingResponse)
async def crawl_discovery(
    url: str = Query(..., description="URL to crawl"),
    max_pages: int = Query(20, description="Maximum pages to crawl"),
    max_depth: int = Query(2, description="Maximum crawl depth")
):
    """Advanced crawling with link discovery."""
    try:
        # Use lightweight crawler
        content = await lightweight_crawler.get_real_time_data(url)
        
        # Filter and enhance content
        enhanced_content = []
        for item in content:
            enhanced_content.append({
                'url': item['url'],
                'title': item['title'],
                'content': item['content'],
                'description': item['description'],
                'keywords': item.get('keywords', ''),
                'source': 'crawler',
                'relevance_score': item.get('relevance_score', 0.5)
            })
        
        sources = list(set(item['url'] for item in enhanced_content))
        keywords = []
        for item in enhanced_content:
            if item.get('keywords'):
                keywords.extend(item['keywords'].split(','))
        
        keywords = list(set(keywords))
        
        return ScrapingResponse(
            content=enhanced_content,
            total_found=len(enhanced_content),
            sources=sources,
            keywords=keywords,
            metadata={
                "scraping_method": "crawler",
                "max_pages": max_pages,
                "max_depth": max_depth,
                "url": url
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scrape-stats")
async def get_scraping_stats():
    """Get scraping statistics."""
    try:
        scraper_stats = scraper.get_scraping_stats()
        crawler_stats = lightweight_crawler.get_crawling_stats()
        
        return {
            "enhanced_scraper": scraper_stats,
            "lightweight_crawler": crawler_stats,
            "total_unique_urls": len(set(
                list(scraper_stats.keys()) + list(crawler_stats.keys())
            ))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/keywords")
async def get_i2c_keywords():
    """Get i2c-specific keywords for filtering."""
    return {
        "keywords": [
            "i2c", "issuer", "processing", "card", "payment", "fintech",
            "banking", "digital", "transformation", "loyalty", "marketing",
            "platform", "api", "integration", "solution", "product",
            "documentation", "guide", "tutorial", "case study", "whitepaper"
        ],
        "categories": {
            "api": ["api", "documentation", "reference", "guide", "endpoint", "integration", "sdk"],
            "product": ["product", "solution", "platform", "feature", "capability", "offering"],
            "content": ["blog", "article", "news", "update", "announcement", "insights"],
            "resources": ["whitepaper", "ebook", "report", "research", "study", "analysis"]
        }
    }
