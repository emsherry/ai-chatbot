"""Conversation memory and context management service."""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import hashlib

class ConversationService:
    
    def __init__(self):
        self.conversation_memory = {}
        self.response_templates = {
            "technical": {
                "greeting": "Hello! I'm Sarah, i2c's technical support specialist. I'm here to help with your technical questions.",
                "context_intro": "Based on our technical documentation",
                "follow_up": "Would you like me to elaborate on any specific technical aspect?"
            },
            "business": {
                "greeting": "Hi! I'm Sarah, your i2c solutions consultant. Let me help you explore how i2c can benefit your business.",
                "context_intro": "From our business solutions documentation",
                "follow_up": "What specific business challenge are you looking to address?"
            },
            "support": {
                "greeting": "Hello! I'm Sarah, i2c's customer success manager. I'm here to ensure you get the support you need.",
                "context_intro": "According to our support resources",
                "follow_up": "Is there anything else about this topic I can help clarify?"
            }
        }
        
    def detect_query_intent(self, query: str) -> Dict[str, float]:
        """Detect the intent and style of the user query."""
        query_lower = query.lower()
        
        # Intent classification
        intents = {
            "technical": 0.0,
            "business": 0.0,
            "support": 0.0,
            "general": 0.0
        }
        
        # Technical keywords
        technical_words = ["api", "integration", "code", "technical", "developer", "endpoint", "documentation"]
        business_words = ["business", "solution", "enterprise", "client", "partner", "revenue", "growth"]
        support_words = ["help", "issue", "problem", "error", "support", "question", "clarify"]
        
        for word in technical_words:
            if word in query_lower:
                intents["technical"] += 0.2
        
        for word in business_words:
            if word in query_lower:
                intents["business"] += 0.2
                
        for word in support_words:
            if word in support_words:
                intents["support"] += 0.2
                
        # Normalize scores
        max_score = max(intents.values()) if max(intents.values()) > 0 else 1
        intents = {k: v/max_score for k, v in intents.items()}
        
        # Default to general if no strong intent
        if max(intents.values()) < 0.3:
            intents["general"] = 1.0
            
        return intents
    
    def generate_confidence_score(self, context: List[Dict], response: str, query: str) -> float:
        """Calculate confidence score for the response."""
        if not context:
            return 0.3
            
        # Context relevance score
        context_score = min(1.0, len(context) * 0.3)
        
        # Response length appropriateness
        response_length = len(response.split())
        length_score = 1.0 if 50 <= response_length <= 200 else 0.7
        
        # Query coverage score
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        coverage = len(query_words.intersection(response_words)) / len(query_words)
        coverage_score = min(1.0, coverage * 2)
        
        return min(0.95, (context_score + length_score + coverage_score) / 3)
    
    def build_enhanced_prompt(self, query: str, context: List[Dict], intent: str) -> str:
        """Build contextually aware prompt with personality."""
        
        template = self.response_templates.get(intent, self.response_templates["support"])
        
        if not context:
            return f"""{template['greeting']}

User Query: {query}

Please provide a helpful, specific response. {template['follow_up']}"""
        
        # Build context summary
        context_parts = []
        sources = []
        
        for item in context[:2]:  # Limit to top 2 contexts
            title = item.get('metadata', {}).get('title', 'i2c documentation')
            content = item.get('content', '')[:400]  # Limit content length
            url = item.get('metadata', {}).get('url', '')
            
            context_parts.append(f"From {title}: {content}")
            if url:
                sources.append(url)
        
        context_text = "\n\n".join(context_parts)
        
        return f"""{template['greeting']}

{template['context_intro']}:

{context_text}

User Query: {query}

Please provide a comprehensive response that:
1. Directly addresses the user's question
2. Uses specific details from the provided context
3. Maintains a helpful, professional tone
4. {template['follow_up']}

If the context doesn't fully answer the question, acknowledge this and offer to help find additional information."""
    
    def store_conversation_context(self, conversation_id: str, query: str, response: str):
        """Store conversation context for future reference."""
        if conversation_id not in self.conversation_memory:
            self.conversation_memory[conversation_id] = []
            
        self.conversation_memory[conversation_id].append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 5 conversations to manage memory
        self.conversation_memory[conversation_id] = self.conversation_memory[conversation_id][-5:]
    
    def get_conversation_context(self, conversation_id: str) -> str:
        """Retrieve recent conversation context."""
        if conversation_id not in self.conversation_memory:
            return ""
            
        recent = self.conversation_memory[conversation_id][-2:]  # Last 2 exchanges
        context_parts = []
        
        for exchange in recent:
            context_parts.append(f"User: {exchange['query']}")
            context_parts.append(f"Assistant: {exchange['response']}")
            
        return "\n".join(context_parts)
    
    def generate_follow_up_questions(self, query: str, response: str) -> List[str]:
        """Generate relevant follow-up questions."""
        follow_ups = []
        
        # Based on query type
        if any(word in query.lower() for word in ["api", "integration"]):
            follow_ups.extend([
                "Would you like to see code examples for this integration?",
                "Are you looking for specific API documentation?",
                "Do you need help with authentication setup?"
            ])
        
        if any(word in query.lower() for word in ["business", "solution"]):
            follow_ups.extend([
                "Would you like to discuss how this applies to your specific use case?",
                "Are you interested in learning about our implementation timeline?",
                "Would you like to see case studies from similar businesses?"
            ])
            
        return follow_ups[:2]  # Return max 2 follow-ups
    
    def create_response_summary(self, query: str, response: str, sources: List[str]) -> Dict[str, Any]:
        """Create response summary with metadata."""
        return {
            "query": query,
            "response": response,
            "sources": sources,
            "confidence": self.generate_confidence_score([], response, query),
            "timestamp": datetime.now().isoformat(),
            "response_hash": hashlib.md5(response.encode()).hexdigest()[:8]
