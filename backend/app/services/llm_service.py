"""Optimized cloud-based LLM service for intelligent responses with minimal memory usage."""

import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from loguru import logger
from app.config import settings


class LLMService:
    """Memory-efficient cloud-based LLM service using free open-source APIs."""
    
    def __init__(self):
        # Use lazy loading to reduce memory
        self._session = None
        self._endpoints = {
            "together": "https://api.together.xyz/v1/chat/completions",
            "openrouter": "https://openrouter.ai/api/v1/chat/completions"
        }
        
    async def _get_session(self):
        """Lazy-loaded aiohttp session to reduce memory usage."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                connector=aiohttp.TCPConnector(limit=10, limit_per_host=5)
            )
        return self._session
    
    async def close(self):
        """Close session to free memory."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    def _build_optimized_prompt(self, query: str, context: List[Dict[str, Any]]) -> str:
        """Build optimized prompt with minimal token usage."""
        
        if not context:
            return f"""You are Sarah, i2c customer support AI assistant. 
            
User Query: {query}

Please provide a helpful, specific response based on the user's question. If you need more information to provide a complete answer, ask clarifying questions."""
        
        # Use only top 2 most relevant context items to reduce tokens
        relevant_context = context[:2]
        context_text = "\n".join([
            f"From {item.get('metadata', {}).get('title', 'i2c documentation')}: {item.get('content', '')[:300]}..." 
            for item in relevant_context
        ])
        
        return f"""You are Sarah, i2c customer support AI assistant.

Based on the following information from i2c documentation:

{context_text}

User Query: {query}

Please provide a helpful, specific response using the provided context. Be concise but informative."""
    
    async def generate_response(
        self,
        query: str,
        context: List[Dict[str, Any]] = None,
        max_tokens: int = 200
    ) -> str:
        """Generate optimized response using cloud APIs."""
        
        prompt = self._build_optimized_prompt(query, context or [])
        
        # Check if API keys are configured
        has_together = bool(settings.TOGETHER_API_KEY and settings.TOGETHER_API_KEY.strip())
        has_openrouter = bool(settings.OPENROUTER_API_KEY and settings.OPENROUTER_API_KEY.strip())
        
        if not has_together and not has_openrouter:
            logger.warning("No API keys configured. Using enhanced fallback response.")
            return self._get_enhanced_fallback_response(query, context)
        
        # Try APIs in order of preference
        for api_name, endpoint in self._endpoints.items():
            try:
                response = await self._call_api(api_name, endpoint, prompt, max_tokens)
                if response and len(response.strip()) > 5:
                    return response
            except Exception as e:
                logger.debug(f"API {api_name} failed: {str(e)}")
                continue
        
        # Enhanced fallback with context awareness
        return self._get_enhanced_fallback_response(query, context)
    
    async def _call_api(self, api_name: str, endpoint: str, prompt: str, max_tokens: int) -> str:
        """Make optimized API call."""
        
        session = await self._get_session()
        
        # Use Together AI as primary (free tier available)
        if api_name == "together" and settings.TOGETHER_API_KEY:
            payload = {
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": [
                    {"role": "system", "content": "You are Sarah, i2c customer support AI assistant for i2c Inc. Provide helpful, accurate responses based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            headers = {
                "Authorization": f"Bearer {settings.TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            async with session.post(endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
        
        # Use OpenRouter as fallback
        elif api_name == "openrouter" and settings.OPENROUTER_API_KEY:
            payload = {
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are Sarah, i2c customer support AI assistant for i2c Inc. Provide helpful, accurate responses based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000"
            }
            
            async with session.post(endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
        
        return ""
    
    def _get_enhanced_fallback_response(self, query: str, context: List[Dict[str, Any]] = None) -> str:
        """Enhanced fallback response that provides more useful information."""
        
        # Check if we have context from vectorstore
        if context and len(context) > 0:
            # Use context to provide better response
            sources = [item.get('metadata', {}).get('title', 'i2c documentation') for item in context]
            return f"""I found some relevant information for your query about "{query}". Based on the available documentation from {', '.join(set(sources))}, I'd be happy to help you with more specific details. Could you please let me know what specific aspect you'd like assistance with?"""
        
        # Provide more helpful fallback
        return f"""Hi! I'm Sarah, your i2c support assistant. I see you're asking about "{query}". 

To provide you with the most accurate assistance, I'm currently checking our knowledge base. In the meantime, could you tell me more specifically what you'd like help with regarding i2c's services? For example:
- Are you looking for information about our products?
- Do you need help with integration?
- Are you interested in our APIs or documentation?

I'm here to help with any i2c-related questions!"""
    
    async def health_check(self) -> Dict[str, Any]:
        """Memory-efficient health check."""
        has_together = bool(settings.TOGETHER_API_KEY and settings.TOGETHER_API_KEY.strip())
        has_openrouter = bool(settings.OPENROUTER_API_KEY and settings.OPENROUTER_API_KEY.strip())
        
        return {
            "status": "healthy",
            "apis_available": {
                "together": has_together,
                "openrouter": has_openrouter
            },
            "fallback_mode": not (has_together or has_openrouter)
        }

# Create singleton instance
llm_service = LLMService()
