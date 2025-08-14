"""Memory-efficient vector store service with intelligent caching."""

import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Any, Optional
import hashlib
import json

logger = logging.getLogger(__name__)

class VectorStoreService:
    """Lightweight vector store with smart caching."""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="chroma_db",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        self.collection = None
        self.cache = {}
        self.max_cache_size = 100
        
    def get_collection(self):
        """Get or create collection with memory optimization."""
        if not self.collection:
            self.collection = self.client.get_or_create_collection(
                name="i2c_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
        return self.collection
    
    def add_webpage(self, url: str, content: str, title: str, metadata: Dict[str, Any] = None):
        """Add webpage content to vector store."""
        try:
            collection = self.get_collection()
            
            # Create unique ID
            doc_id = hashlib.md5(url.encode()).hexdigest()
            
            # Add to collection
            collection.add(
                documents=[content],
                metadatas=[{"url": url, "title": title, **(metadata or {})}],
                ids=[doc_id]
            )
            
            logger.info(f"Added webpage: {title}")
            
        except Exception as e:
            logger.error(f"Error adding webpage: {e}")
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Perform efficient similarity search with caching."""
        try:
            collection = self.get_collection()
            
            # Check cache first
            cache_key = hashlib.md5(query.encode()).hexdigest()
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            results = collection.query(
                query_texts=[query],
                n_results=k
            )
            
            formatted_results = []
            if results['documents']:
                for doc, meta, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    formatted_results.append({
                        'content': doc,
                        'metadata': meta,
                        'score': 1 - distance  # Convert to similarity
                    })
            
            # Cache results
            self.cache[cache_key] = formatted_results
            
            # Limit cache size
            if len(self.cache) > self.max_cache_size:
                self.cache = dict(list(self.cache.items())[-50:])
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        try:
            collection = self.get_collection()
            count = collection.count()
            
            # Get unique sources
            results = collection.get()
            sources = {}
            for meta in results['metadatas']:
                url = meta.get('url', 'unknown')
                sources[url] = sources.get(url, 0) + 1
            
            return {
                "total_documents": count,
                "unique_sources": len(sources),
                "sources": sources
            }
        except:
            return {"total_documents": 0, "unique_sources": 0, "sources": {}}

    def populate_initial_data(self):
        """Populate vector store with initial I2C documentation."""
        try:
            # Check if already populated
            stats = self.get_collection_stats()
            if stats["total_documents"] > 0:
                logger.info("Vector store already populated")
                return
            
            # Add initial I2C documentation
            initial_docs = [
                {
                    "url": "https://www.i2cinc.com/about",
                    "title": "About I2C Inc",
                    "content": "I2C Inc is a leading provider of digital payment and banking technology solutions. Our platform enables financial institutions, fintechs, and corporations to create and manage innovative payment programs and banking services. We provide comprehensive issuer processing, loyalty and marketing solutions, and API-driven platforms for modern financial services."
                },
                {
                    "url": "https://www.i2cinc.com/platform",
                    "title": "I2C Platform Overview",
                    "content": "The I2C platform provides a unified solution for payment processing, card management, and banking services. Key features include real-time transaction processing, multi-currency support, fraud detection, compliance management, and comprehensive reporting. The platform supports various card types including credit, debit, prepaid, and virtual cards."
                },
                {
                    "url": "https://www.i2cinc.com/api",
                    "title": "I2C API Documentation",
                    "content": "I2C provides RESTful APIs for integrating payment and banking services. The API supports account management, transaction processing, card operations, customer management, and reporting. Authentication is handled via API keys and OAuth 2.0. Rate limiting and webhooks are supported for production integrations."
                }
            ]
            
            for doc in initial_docs:
                self.add_webpage(
                    url=doc["url"],
                    content=doc["content"],
                    title=doc["title"],
                    metadata={"source": "i2cinc.com", "type": "documentation"}
                )
            
            logger.info("Successfully populated vector store with initial I2C documentation")
            
        except Exception as e:
            logger.error(f"Error populating initial data: {e}")

# Create singleton instance
vectorstore = VectorStoreService()
