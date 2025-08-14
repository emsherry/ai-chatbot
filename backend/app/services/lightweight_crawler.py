"""Memory-efficient real-time crawler with dynamic link discovery."""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from typing import List, Dict, Set, Optional
import time
import re
from collections import deque
import hashlib

logger = logging.getLogger(__name__)

class LightweightCrawler:
    """Memory-optimized crawler that discovers inner links without heavy dependencies."""
    
    def __init__(self, max_pages: int = 20, max_depth: int = 2, delay: float = 0.5):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.delay = delay
        self.visited_urls: Set[str] = set()
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Memory-efficient patterns
        self.ignore_patterns = [
            r'\.(css|js|jpg|jpeg|png|gif|svg|ico|pdf|zip|rar)$',
            r'mailto:|tel:|javascript:',
            r'facebook\.com|twitter\.com|linkedin\.com',
            r'#.*$'
        ]
        
    async def __aenter__(self):
        """Async context manager."""
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={'User-Agent': 'I2CBot/1.0 (Memory-Efficient)'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup."""
        if self.session:
            await self.session.close()
            
    def _should_ignore_url(self, url: str) -> bool:
        """Check if URL should be ignored."""
        return any(re.search(pattern, url, re.IGNORECASE) for pattern in self.ignore_patterns)
        
    def _is_same_domain(self, url: str, base_domain: str) -> bool:
        """Check if URL is same domain."""
        return urlparse(url).netloc == base_domain
        
    def _extract_links(self, html_content: str, base_url: str) -> List[str]:
        """Extract links efficiently."""
        soup = BeautifulSoup(html_content, 'lxml')  # lxml is faster
        
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            # Clean URL
            parsed = urlparse(absolute_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            if (clean_url and 
                not self._should_ignore_url(clean_url) and 
                self._is_same_domain(clean_url, urlparse(base_url).netloc)):
                links.append(clean_url)
                
        return list(set(links))  # Remove duplicates
        
    def _extract_content(self, html_content: str, url: str) -> Dict[str, str]:
        """Extract content efficiently."""
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
            
        # Extract key elements
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ''
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else ''
        
        # Get main content
        main_content = soup.get_text(separator=' ', strip=True)
        
        # Limit content size
        if len(main_content) > 2000:
            main_content = main_content[:2000] + '...'
            
        return {
            'url': url,
            'title': title_text,
            'description': description,
            'content': main_content
        }
        
    async def _fetch_single_url(self, url: str) -> Optional[Dict[str, str]]:
        """Fetch and process a single URL."""
        if url in self.visited_urls:
            return None
            
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Skip if not HTML
                    content_type = response.headers.get('content-type', '')
                    if 'text/html' not in content_type:
                        return None
                        
                    self.visited_urls.add(url)
                    
                    # Extract content and links
                    extracted = self._extract_content(content, url)
                    extracted['links'] = self._extract_links(content, url)
                    
                    return extracted
                    
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            
        return None
        
    async def crawl_with_discovery(self, start_url: str) -> List[Dict[str, str]]:
        """Crawl domain with inner link discovery."""
        base_domain = urlparse(start_url).netloc
        
        # Initialize queue
        queue = deque([(start_url, 0)])  # (url, depth)
        results = []
        
        while queue and len(results) < self.max_pages:
            current_batch = []
            for _ in range(min(self.max_concurrent, len(queue))):
                if queue:
                    url, depth = queue.popleft()
                    if depth <= self.max_depth and url not in self.visited_urls:
                        current_batch.append((url, depth))
                        
            if not current_batch:
                break
                
            # Process batch
            fetch_tasks = [self._fetch_single_url(url) for url, _ in current_batch]
            processed = await asyncio.gather(*fetch_tasks)
            
            for result in processed:
                if result:
                    results.append({
                        'url': result['url'],
                        'title': result['title'],
                        'description': result['description'],
                        'content': result['content'][:1000],  # Limit content
                        'source': 'crawler'
                    })
                    
                    # Add discovered links to queue
                    for link in result.get('links', [])[:5]:  # Limit new links
                        if link not in self.visited_urls:
                            queue.append((link, 1))  # Next level
                            
            await asyncio.sleep(self.delay)  # Be respectful
            
        return results
        
    async def get_real_time_data(self, url: str) -> List[Dict[str, str]]:
        """Get real-time data from URL including inner links."""
        async with self:
            return await self.crawl_with_discovery(url)
            
    def clear_cache(self):
        """Clear visited URLs cache."""
        self.visited_urls.clear()


# Create lightweight instance
lightweight_crawler = LightweightCrawler()
