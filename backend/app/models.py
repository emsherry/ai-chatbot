"""Pydantic models for API requests and responses."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, validator


class ChatRole(str, Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Individual chat message."""
    role: ChatRole = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Message timestamp")


class ChatQueryRequest(BaseModel):
    """Request model for chat queries."""
    query: str = Field(..., min_length=1, max_length=1000, description="User's query")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    max_tokens: Optional[int] = Field(default=150, ge=10, le=1000, description="Maximum response tokens")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Response creativity")
    
    @validator('query')
    def validate_query(cls, v: str) -> str:
        """Validate query content."""
        v = v.strip()
        if not v:
            raise ValueError("Query cannot be empty")
        return v


class ChatQueryResponse(BaseModel):
    """Response model for chat queries."""
    response: str = Field(..., description="AI-generated response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: List[str] = Field(default_factory=list, description="Relevant source documents")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence score")
    tokens_used: int = Field(..., description="Number of tokens used")
    response_time: float = Field(..., description="Response time in seconds")


class ScrapeRequest(BaseModel):
    """Request model for scraping."""
    url: str = Field(..., description="URL to scrape")
    max_depth: Optional[int] = Field(default=1, ge=1, le=5, description="Maximum crawl depth")
    include_pdfs: Optional[bool] = Field(default=False, description="Include PDF documents")
    force_refresh: Optional[bool] = Field(default=False, description="Force refresh existing data")


class ScrapeResponse(BaseModel):
    """Response model for scraping."""
    url: str = Field(..., description="Scraped URL")
    pages_scraped: int = Field(..., description="Number of pages scraped")
    documents_processed: int = Field(..., description="Number of documents processed")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    processing_time: float = Field(..., description="Processing time in seconds")


class HealthCheck(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    version: str = Field(..., description="API version")
    dependencies: Dict[str, str] = Field(default_factory=dict, description="Dependency status")


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    path: Optional[str] = Field(None, description="Request path")


class ConversationSummary(BaseModel):
    """Conversation summary for history."""
    conversation_id: str = Field(..., description="Unique conversation ID")
    title: str = Field(..., description="Conversation title")
    last_message: datetime = Field(..., description="Last message timestamp")
    message_count: int = Field(..., description="Total message count")
    preview: str = Field(..., description="Last message preview")


class SearchResult(BaseModel):
    """Search result from vector store."""
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    score: float = Field(..., description="Relevance score")
    source: str = Field(..., description="Document source")
