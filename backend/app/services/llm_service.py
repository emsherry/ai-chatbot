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
        """Build enhanced prompt for detailed, conversational responses."""
        
        if not context:
            return f"""You are Sarah, an expert I2C customer support AI assistant with deep knowledge of I2C's products, services, and solutions. Your role is to provide comprehensive, helpful responses that encourage users to explore and understand I2C's offerings better.

User Query: {query}

Please provide a detailed, informative response that:
1. Directly answers the user's question with specific details
2. Provides additional context and explanations
3. Suggests related topics or follow-up questions
4. Uses a friendly, conversational tone that encourages further interaction
5. Focuses on helping the user understand I2C's solutions without forcing them to visit external websites

If the query is broad, break it down into specific aspects and explain each thoroughly."""
        
        # Use more context items for richer responses
        relevant_context = context[:5]  # Increased from 2 to 5 for better coverage
        context_parts = []
        
        for item in relevant_context:
            content = item.get('content', '')
            title = item.get('metadata', {}).get('title', 'I2C documentation')
            url = item.get('metadata', {}).get('url', '')
            
            # Extract meaningful content without truncation
            content_preview = content[:800] if len(content) > 800 else content
            if len(content) > 800:
                content_preview += "..."
            
            context_parts.append(f"📋 **From {title}** ({url}):\n{content_preview}")
        
        context_text = "\n\n".join(context_parts)
        
        return f"""You are Sarah, an expert I2C customer support AI assistant with comprehensive knowledge of I2C's platform, products, and services.

Based on the following detailed information from I2C's documentation and knowledge base:

{context_text}

---

**User Query:** {query}

**Your Response Guidelines:**
1. **Be Comprehensive**: Provide detailed explanations that fully address the user's question
2. **Be Conversational**: Use a friendly, engaging tone that makes users want to ask more questions
3. **Be Educational**: Explain concepts clearly and provide context that helps users understand I2C's offerings
4. **Be Proactive**: Suggest related topics, features, or services the user might find interesting
5. **Be Specific**: Use concrete examples and specific details from the provided context
6. **Encourage Exploration**: End with questions or suggestions that prompt further interaction

**Structure your response to:**
- Start with a direct answer to their question
- Provide additional context and explanations
- Include specific examples or use cases
- Suggest related topics they might want to explore
- End with an engaging question or invitation to learn more

Remember: Your goal is to provide such valuable information that users feel satisfied and encouraged to explore more about I2C's solutions, not to redirect them to websites."""
    
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
