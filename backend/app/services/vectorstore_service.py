"""Memory-efficient vector store service with intelligent caching."""

import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Any, Optional
import hashlib
import json
from sentence_transformers import SentenceTransformer
import numpy as np

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
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {e}")
            self.embedding_model = None
    
    def get_collection(self):
        """Get or create collection with memory optimization."""
        if not self.collection:
            self.collection = self.client.get_or_create_collection(
                name="i2c_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
        return self.collection
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for given texts."""
        if not self.embedding_model:
            logger.error("Embedding model not initialized")
            return [[0.0] * 384] * len(texts)
        
        try:
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            return [[0.0] * 384] * len(texts)
    
    def add_webpage(self, url: str, content: str, title: str, metadata: Dict[str, Any] = None):
        """Add webpage content to vector store."""
        try:
            collection = self.get_collection()
            
            # Create unique ID
            doc_id = hashlib.md5(url.encode()).hexdigest()
            
            # Create embedding for the content
            embedding = self.create_embeddings([content])
            
            # Add to collection
            collection.add(
                documents=[content],
                embeddings=embedding,
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
            
            # Create embedding for the query
            query_embedding = self.create_embeddings([query])
            
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=k
            )
            
            formatted_results = []
            if results['documents'] and len(results['documents']) > 0:
                for doc, meta, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    formatted_results.append({
                        'content': doc,
                        'metadata': meta,
                        'score': 1 - distance
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
            if results['metadatas']:
                for meta in results['metadatas']:
                    url = meta.get('url', 'unknown')
                    sources[url] = sources.get(url, 0) + 1
            
            return {
                "total_documents": count,
                "unique_sources": len(sources),
                "sources": sources
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"total_documents": 0, "unique_sources": 0, "sources": {}}

    def populate_initial_data(self):
        """Populate vector store with comprehensive I2C documentation."""
        try:
            # Check if already populated
            stats = self.get_collection_stats()
            if stats["total_documents"] > 50:
                logger.info("Vector store already populated")
                return
            
            # Add comprehensive I2C documentation
            comprehensive_docs = [
                {
                    "url": "https://www.i2cinc.com/about",
                    "title": "About I2C Inc - Company Overview",
                    "content": "I2C Inc is a global leader in digital payment and banking technology, empowering financial institutions, fintech companies, and corporations to create and manage innovative payment programs and banking services."
                },
                {
                    "url": "https://www.i2cinc.com/platform",
                    "title": "I2C Platform - Unified Payment & Banking Solution",
                    "content": "The I2C platform is a comprehensive, cloud-native solution that unifies payment processing, card management, and digital banking services in a single, integrated ecosystem."
                },
                {
                    "url": "https://www.i2cinc.com/platform/api",
                    "title": "I2C API Platform - Developer Integration Guide",
                    "content": "I2C's API-first architecture provides developers with comprehensive RESTful APIs for seamless integration of payment and banking services."
                },
                {
                    "url": "https://www.i2cinc.com/solutions/consumer-credit",
                    "title": "Consumer Credit Solutions - Digital Lending Platform",
                    "content": "I2C's consumer credit solutions provide end-to-end digital lending capabilities including instant credit decisioning, automated underwriting, dynamic credit limit management, and real-time risk assessment."
                },
                {
                    "url": "https://www.i2cinc.com/solutions/commercial-credit",
                    "title": "Commercial Credit & Corporate Card Solutions",
                    "content": "I2C's commercial credit solutions cater to businesses of all sizes, from startups to large enterprises."
                },
                {
                    "url": "https://www.i2cinc.com/solutions/buy-now-pay-later",
                    "title": "Buy Now Pay Later (BNPL) Solutions",
                    "content": "I2C's BNPL solution enables merchants and financial institutions to offer flexible payment options at the point of sale."
                },
                {
                    "url": "https://www.i2cinc.com/platform/loyalty-marketing",
                    "title": "Loyalty & Marketing Solutions",
                    "content": "I2C's loyalty and marketing platform enables the creation of sophisticated customer engagement programs with personalized rewards, targeted campaigns, and behavioral analytics."
                },
                {
                    "url": "https://www.i2cinc.com/services/implementation",
                    "title": "Implementation Services - Expert Deployment Support",
                    "content": "I2C's implementation services provide comprehensive support for deploying payment and banking solutions, from initial planning through go-live and ongoing optimization."
                },
                {
                    "url": "https://www.i2cinc.com/services/fraud-management",
                    "title": "Fraud Management & Security Solutions",
                    "content": "I2C's fraud management solutions provide multi-layered security with real-time transaction monitoring, behavioral analytics, and machine learning-based fraud detection."
                },
                {
                    "url": "https://www.i2cinc.com/team",
                    "title": "I2C Leadership & Expert Team",
                    "content": "I2C is led by a team of industry veterans with deep expertise in payments, banking, and financial technology."
                }
            ]
            
            for doc in comprehensive_docs:
                try:
                    self.add_webpage(
                        url=doc["url"],
                        content=doc["content"],
                        title=doc["title"]
                    )
                except Exception as e:
                    logger.error(f"Error adding document {doc['title']}: {e}")
            
            logger.info("Initial data population completed")
            
        except Exception as e:
            logger.error(f"Error populating initial data: {e}")

# Create singleton instance
vectorstore = VectorStoreService()
