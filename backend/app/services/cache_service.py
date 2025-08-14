"""Ultra-lightweight in-memory cache with TTL and size limits."""

import time
import logging
from typing import Dict, Any, Optional
import hashlib

logger = logging.getLogger(__name__)

class CacheService:
    """Memory-efficient cache with automatic cleanup."""
    
    def __init__(self, max_size: int = 50, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = ttl
        
    def _cleanup_expired(self):
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, value in self.cache.items()
            if current_time - value['timestamp'] > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def _cleanup_oldest(self):
        """Remove oldest entries when cache is full."""
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        self._cleanup_expired()
        
        if key in self.cache:
            value = self.cache[key]
            if time.time() - value['timestamp'] <= self.ttl:
                return value['data']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache."""
        self._cleanup_expired()
        self._cleanup_oldest()
        
        self.cache[key] = {
            'data': value,
            'timestamp': time.time()
        }
    
    def delete(self, key: str):
        """Delete key from cache."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache."""
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        self._cleanup_expired()
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl": self.ttl
        }

# Create singleton instance
cache = CacheService()
