"""
Embedding Service for Knowledge Sherpa
Handles text embedding generation using sentence-transformers
"""

import logging
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize embedding service with specified model
        
        Args:
            model_name: Name of the sentence-transformer model to use
                       Default model supports Korean and English
        """
        self.model_name = model_name
        self._model = None
        self._embedding_dimension = None
        
    def _load_model(self):
        """Lazy load the embedding model"""
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            # Get embedding dimension by encoding a test string
            test_embedding = self._model.encode(["test"])
            self._embedding_dimension = test_embedding.shape[1]
            logger.info(f"Model loaded successfully. Embedding dimension: {self._embedding_dimension}")
    
    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension of the current model"""
        if self._embedding_dimension is None:
            self._load_model()
        return self._embedding_dimension
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for embedding
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Cleaned and preprocessed text
        """
        # Remove extra whitespace and normalize
        text = " ".join(text.split())
        
        # Remove page markers if present
        import re
        text = re.sub(r'=== PAGE \d+ ===', '', text)
        
        # Clean up any remaining artifacts
        text = text.strip()
        
        return text
    
    def create_embedding(self, text: str) -> np.ndarray:
        """
        Create embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        self._load_model()
        
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Generate embedding
        embedding = self._model.encode([processed_text])
        
        return embedding[0]
    
    def create_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Create embeddings for multiple texts in batch
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        self._load_model()
        
        # Preprocess texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Generate embeddings in batch (more efficient)
        embeddings = self._model.encode(processed_texts)
        
        return [embedding for embedding in embeddings]
    
    def chunk_text(self, text: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into chunks for embedding
        
        Args:
            text: Text to chunk
            max_chunk_size: Maximum size of each chunk in characters
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + max_chunk_size
            
            # If this isn't the last chunk, try to find a good breaking point
            if end < len(text):
                # Look for sentence boundaries within the last 200 characters
                search_start = max(start + max_chunk_size - 200, start)
                sentence_ends = []
                
                for i in range(search_start, min(end, len(text))):
                    if text[i] in '.!?。':
                        sentence_ends.append(i + 1)
                
                if sentence_ends:
                    end = sentence_ends[-1]
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def create_section_embeddings(self, section_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create embeddings for a section with metadata
        
        Args:
            section_content: Dictionary containing section data with keys:
                - content: The text content
                - metadata: Dictionary with section metadata
                
        Returns:
            Dictionary with embeddings and metadata
        """
        content = section_content.get('content', '')
        metadata = section_content.get('metadata', {})
        
        # For long content, create chunks
        chunks = self.chunk_text(content)
        
        # Create embeddings for chunks
        embeddings = self.create_embeddings_batch(chunks)
        
        return {
            'chunks': chunks,
            'embeddings': embeddings,
            'metadata': metadata,
            'chunk_count': len(chunks)
        }