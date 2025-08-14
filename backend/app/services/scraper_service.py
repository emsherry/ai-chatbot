"""Lightweight scraper service with intelligent content extraction."""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
import time
from app.config import settings

logger = logging.getLogger(__name__)

class OptimizedScraperService:
    """Memory-efficient web scraper."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.scraped_urls = set()
        
    async def scrape_website(self, max_pages: int = 5, base_url: str = None, delay: float = None) -> List[Dict[str, str]]:
        """Scrape I2C website efficiently."""
        # Use environment variables with fallbacks
        base_url = base_url or settings.SCRAPER_BASE_URL
        delay = delay or settings.SCRAPE_DELAY
        
        try:
            urls = [
                base_url,
                f"{base_url}/about",
                f"{base_url}/platform/api",
                f"{base_url}/issuer-processing",
                f"{base_url}/platform/loyalty-marketing",
                f"{base_url}/services",
                f"{base_url}/solutions",
                f"{base_url}/products",
                f"{base_url}/contact"
            ]
            
            results = []
            
            for url in urls[:max_pages]:
                if url in self.scraped_urls:
                    continue
                    
                try:
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Extract main content
                    content_parts = []
                    
                    # Get title
                    title = soup.find('title')
                    if title:
                        content_parts.append(f"Title: {title.get_text().strip()}")
                    
                    # Get meta description
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if meta_desc:
                        content_parts.append(f"Description: {meta_desc.get('content', '').strip()}")
                    
                    # Get headings
                    for heading in soup.find_all(['h1', 'h2', 'h3'])[:5]:
                        text = heading.get_text().strip()
                        if len(text) > 10:
                            content_parts.append(text)
                    
                    # Get paragraphs
                    for p in soup.find_all('p')[:10]:
                        text = p.get_text().strip()
                        if len(text) > 50:
                            content_parts.append(text)
                    
                    if content_parts:
                        content = "\n\n".join(content_parts)
                        results.append({
                            'content': content[:2000],  # Limit content size
                            'url': url,
                            'title': title.get_text().strip() if title else url,
                            'metadata': {
                                'url': url,
                                'title': title.get_text().strip() if title else url,
                                'source': 'i2cinc.com'
                            }
                        })
                    
                    self.scraped_urls.add(url)
                    time.sleep(delay)  # Use configurable delay
                    
                except Exception as e:
                    logger.error(f"Error scraping {url}: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return []
    
    def clear_cache(self):
        """Clear scraped URLs cache."""
        self.scraped_urls.clear()

# Create singleton instance
scraper = OptimizedScraperService()
