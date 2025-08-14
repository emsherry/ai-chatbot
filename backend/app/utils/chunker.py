"""Text chunking utilities for processing large documents."""

import re
from typing import List, Optional

from loguru import logger


class TextChunker:
    """Service for chunking large text documents into smaller pieces."""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """Initialize text chunker.
        
        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        if not text.strip():
            return []
        
        # Clean text
        text = self._clean_text(text)
        
        # Split into sentences first
        sentences = self._split_into_sentences(text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                current_chunk = overlap_text + sentence
            else:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
        
        # Add remaining text
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Ensure chunks are not too small
        chunks = [chunk for chunk in chunks if len(chunk.strip()) > 50]
        
        logger.debug(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def chunk_markdown(self, text: str) -> List[str]:
        """Split markdown text into chunks preserving structure.
        
        Args:
            text: Markdown text to chunk
            
        Returns:
            List of markdown chunks
        """
        # Split by headers
        sections = re.split(r'\n#{1,6}\s+', text)
        
        chunks = []
        for section in sections:
            if section.strip():
                sub_chunks = self.chunk_text(section)
                chunks.extend(sub_chunks)
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', ' ', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[\.]{2,}', '.', text)
        
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def chunk_by_paragraph(self, text: str) -> List[str]:
        """Split text by paragraphs.
        
        Args:
            text: Input text
            
        Returns:
            List of paragraph chunks
        """
        paragraphs = text.split('\n\n')
        
        chunks = []
        for paragraph in paragraphs:
            if paragraph.strip():
                sub_chunks = self.chunk_text(paragraph)
                chunks.extend(sub_chunks)
        
        return chunks
    
    def chunk_by_tokens(self, text: str, max_tokens: int = 100) -> List[str]:
        """Split text by approximate token count.
        
        Args:
            text: Input text
            max_tokens: Maximum tokens per chunk
            
        Returns:
            List of token-based chunks
        """
        # Rough token estimation (4 chars per token)
        chars_per_token = 4
        chunk_size_chars = max_tokens * chars_per_token
        
        # Adjust chunk size
        original_chunk_size = self.chunk_size
        self.chunk_size = chunk_size_chars
        
        chunks = self.chunk_text(text)
        
        # Restore original chunk size
        self.chunk_size = original_chunk_size
        
        return chunks


# Global instance
chunker = TextChunker()
