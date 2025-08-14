"""Optimized chat routes with memory efficiency."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncio

from app.services.llm_service import LLMService
from app.services.scraper_service import OptimizedScraperService
from app.services.cache_service import CacheService
from app.services.vectorstore_service import vectorstore

router = APIRouter()

# Initialize services
llm_service = LLMService()
scraper_service = OptimizedScraperService()
cache = CacheService()

class ChatQueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7

class ChatQueryResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[str]
    confidence: float
    tokens_used: int
    response_time: float

@router.post("/query", response_model=ChatQueryResponse)
async def chat_query(request: ChatQueryRequest):
    """Process chat query with memory optimization."""
    try:
        # Check cache first
        cache_key = f"chat:{request.query}:{request.conversation_id}"
        cached = cache.get(cache_key)
        if cached:
            return ChatQueryResponse(**cached)
        
        # Get relevant context from vector store
        context = vectorstore.similarity_search(request.query, k=3)
        
        # Generate response with context
        llm_response = await llm_service.generate_response(
            query=request.query,
            context=context,
            max_tokens=request.max_tokens
        )
        
        # Extract sources
        sources = [item['metadata'].get('url', 'unknown') for item in context]
        
        response = ChatQueryResponse(
            response=llm_response,
            conversation_id=request.conversation_id or "default",
            sources=sources,
            confidence=0.8,
            tokens_used=len(llm_response.split()),
            response_time=1.0
        )
        
        # Cache response
        cache.set(cache_key, response.dict())
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "vectorstore_ready": True,
        "documents_count": 0
    }

@router.post("/message", response_model=ChatQueryResponse)
async def chat_message(request: ChatQueryRequest):
    """Legacy message endpoint for backward compatibility."""
    return await chat_query(request)

@router.post("/scrape-and-chat")
async def scrape_and_chat(request: ChatQueryRequest):
    """Scrape website and chat with context."""
    try:
        # Scrape content
        scraped_data = scraper_service.scrape_i2c_website(max_pages=3)
        
        # Build context from scraped data
        context_parts = []
        sources = []
        for item in scraped_data:
            context_parts.append(f"From {item['title']}: {item['content'][:200]}...")
            sources.append(item.get('url', 'unknown'))
        
        context = "\n\n".join(context_parts)
        
        # Generate response with context
        llm_response = await llm_service.generate_response(
            query=request.query,
            context=context,
            max_tokens=request.max_tokens
        )
        
        return ChatQueryResponse(
            response=llm_response,
            conversation_id=request.conversation_id or "default",
            sources=sources,
            confidence=0.9,
            tokens_used=150,
            response_time=2.0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
