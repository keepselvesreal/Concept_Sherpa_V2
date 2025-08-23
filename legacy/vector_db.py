"""
Vector Database Service for Knowledge Sherpa
Handles vector storage and similarity search using ChromaDB
"""

import logging
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import numpy as np

logger = logging.getLogger(__name__)


class VectorDatabase:
    """Service for managing vector database operations"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize vector database service
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory
        self._client = None
        self._collections = {}
        
        # Ensure persist directory exists
        os.makedirs(persist_directory, exist_ok=True)
    
    def _get_client(self):
        """Get or create ChromaDB client"""
        if self._client is None:
            logger.info(f"Initializing ChromaDB client with persist directory: {self.persist_directory}")
            self._client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
        return self._client
    
    def create_collection(self, collection_name: str, embedding_dimension: int = None) -> Any:
        """
        Create or get a collection
        
        Args:
            collection_name: Name of the collection
            embedding_dimension: Dimension of embeddings (optional)
            
        Returns:
            ChromaDB collection object
        """
        client = self._get_client()
        
        try:
            # Try to get existing collection
            collection = client.get_collection(collection_name)
            logger.info(f"Retrieved existing collection: {collection_name}")
        except Exception:
            # Create new collection if it doesn't exist
            collection = client.create_collection(
                name=collection_name,
                metadata={"embedding_dimension": embedding_dimension} if embedding_dimension else {}
            )
            logger.info(f"Created new collection: {collection_name}")
        
        self._collections[collection_name] = collection
        return collection
    
    def get_collection(self, collection_name: str) -> Any:
        """
        Get an existing collection
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            ChromaDB collection object
        """
        if collection_name in self._collections:
            return self._collections[collection_name]
        
        client = self._get_client()
        collection = client.get_collection(collection_name)
        self._collections[collection_name] = collection
        return collection
    
    def list_collections(self) -> List[str]:
        """
        List all collections in the database
        
        Returns:
            List of collection names
        """
        client = self._get_client()
        collections = client.list_collections()
        return [col.name for col in collections]
    
    def add_documents(self, 
                     collection_name: str,
                     documents: List[str],
                     embeddings: List[np.ndarray],
                     metadatas: List[Dict[str, Any]],
                     ids: List[str]) -> None:
        """
        Add documents to a collection
        
        Args:
            collection_name: Name of the collection
            documents: List of document texts
            embeddings: List of embedding vectors
            metadatas: List of metadata dictionaries
            ids: List of unique document IDs
        """
        collection = self.get_collection(collection_name)
        
        # Convert numpy arrays to lists for ChromaDB
        embeddings_list = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in embeddings]
        
        collection.add(
            documents=documents,
            embeddings=embeddings_list,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(documents)} documents to collection {collection_name}")
    
    def search_similar(self,
                      collection_name: str,
                      query_embedding: np.ndarray,
                      n_results: int = 10,
                      where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for similar documents using vector similarity
        
        Args:
            collection_name: Name of the collection to search
            query_embedding: Query embedding vector
            n_results: Number of results to return
            where: Optional metadata filter
            
        Returns:
            Dictionary with search results
        """
        collection = self.get_collection(collection_name)
        
        # Convert numpy array to list for ChromaDB
        query_embedding_list = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
        
        results = collection.query(
            query_embeddings=[query_embedding_list],
            n_results=n_results,
            where=where,
            include=['documents', 'metadatas', 'distances']
        )
        
        return {
            'documents': results['documents'][0] if results['documents'] else [],
            'metadatas': results['metadatas'][0] if results['metadatas'] else [],
            'distances': results['distances'][0] if results['distances'] else [],
            'count': len(results['documents'][0]) if results['documents'] else 0
        }
    
    def search_by_text(self,
                      collection_name: str,
                      query_text: str,
                      embedding_service,
                      n_results: int = 10,
                      where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for similar documents using text query
        
        Args:
            collection_name: Name of the collection to search
            query_text: Text query to search for
            embedding_service: EmbeddingService instance to create query embedding
            n_results: Number of results to return
            where: Optional metadata filter
            
        Returns:
            Dictionary with search results
        """
        # Create embedding for query text
        query_embedding = embedding_service.create_embedding(query_text)
        
        return self.search_similar(
            collection_name=collection_name,
            query_embedding=query_embedding,
            n_results=n_results,
            where=where
        )
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Get statistics about a collection
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Dictionary with collection statistics
        """
        collection = self.get_collection(collection_name)
        count = collection.count()
        
        return {
            'name': collection_name,
            'document_count': count,
            'metadata': collection.metadata
        }
    
    def delete_collection(self, collection_name: str) -> None:
        """
        Delete a collection
        
        Args:
            collection_name: Name of the collection to delete
        """
        client = self._get_client()
        client.delete_collection(collection_name)
        
        if collection_name in self._collections:
            del self._collections[collection_name]
        
        logger.info(f"Deleted collection: {collection_name}")
    
    def update_document(self,
                       collection_name: str,
                       document_id: str,
                       document: Optional[str] = None,
                       embedding: Optional[np.ndarray] = None,
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Update a document in the collection
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the document to update
            document: New document text (optional)
            embedding: New embedding vector (optional)
            metadata: New metadata (optional)
        """
        collection = self.get_collection(collection_name)
        
        update_data = {'ids': [document_id]}
        
        if document is not None:
            update_data['documents'] = [document]
        
        if embedding is not None:
            embedding_list = embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
            update_data['embeddings'] = [embedding_list]
        
        if metadata is not None:
            update_data['metadatas'] = [metadata]
        
        collection.update(**update_data)
        logger.info(f"Updated document {document_id} in collection {collection_name}")
    
    def delete_documents(self, collection_name: str, document_ids: List[str]) -> None:
        """
        Delete documents from a collection
        
        Args:
            collection_name: Name of the collection
            document_ids: List of document IDs to delete
        """
        collection = self.get_collection(collection_name)
        collection.delete(ids=document_ids)
        logger.info(f"Deleted {len(document_ids)} documents from collection {collection_name}")


class KnowledgeVectorDB:
    """High-level interface for Knowledge Sherpa vector database operations"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize Knowledge Vector Database
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.vector_db = VectorDatabase(persist_directory)
        self.core_collection = "knowledge_core_embeddings"
        self.detail_collection = "knowledge_detail_embeddings"
    
    def setup_collections(self, embedding_dimension: int) -> None:
        """
        Setup the core and detail collections
        
        Args:
            embedding_dimension: Dimension of the embeddings
        """
        self.vector_db.create_collection(self.core_collection, embedding_dimension)
        self.vector_db.create_collection(self.detail_collection, embedding_dimension)
        logger.info("Setup core and detail collections")
    
    def add_core_content(self,
                        content: str,
                        embedding: np.ndarray,
                        metadata: Dict[str, Any],
                        content_id: str) -> None:
        """
        Add core content to the core embeddings collection
        
        Args:
            content: Core content text
            embedding: Content embedding
            metadata: Content metadata
            content_id: Unique content ID
        """
        self.vector_db.add_documents(
            collection_name=self.core_collection,
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[content_id]
        )
    
    def add_detail_content(self,
                          content: str,
                          embedding: np.ndarray,
                          metadata: Dict[str, Any],
                          content_id: str) -> None:
        """
        Add detail content to the detail embeddings collection
        
        Args:
            content: Detail content text
            embedding: Content embedding
            metadata: Content metadata
            content_id: Unique content ID
        """
        self.vector_db.add_documents(
            collection_name=self.detail_collection,
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[content_id]
        )
    
    def search_core_content(self, query_text: str, embedding_service, n_results: int = 5) -> Dict[str, Any]:
        """
        Search core content using text query
        
        Args:
            query_text: Text to search for
            embedding_service: EmbeddingService instance
            n_results: Number of results to return
            
        Returns:
            Search results from core collection
        """
        return self.vector_db.search_by_text(
            collection_name=self.core_collection,
            query_text=query_text,
            embedding_service=embedding_service,
            n_results=n_results
        )
    
    def search_detail_content(self, query_text: str, embedding_service, n_results: int = 10) -> Dict[str, Any]:
        """
        Search detail content using text query
        
        Args:
            query_text: Text to search for
            embedding_service: EmbeddingService instance
            n_results: Number of results to return
            
        Returns:
            Search results from detail collection
        """
        return self.vector_db.search_by_text(
            collection_name=self.detail_collection,
            query_text=query_text,
            embedding_service=embedding_service,
            n_results=n_results
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics for both collections
        
        Returns:
            Dictionary with statistics for core and detail collections
        """
        return {
            'core': self.vector_db.get_collection_stats(self.core_collection),
            'detail': self.vector_db.get_collection_stats(self.detail_collection)
        }