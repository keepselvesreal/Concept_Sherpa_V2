"""
Test script for the embedding and vector database system
"""

import logging
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedding_service import EmbeddingService
from vector_db import KnowledgeVectorDB, VectorDatabase
from create_embeddings import ChapterEmbeddingProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_embedding_service():
    """Test the embedding service functionality"""
    logger.info("=== Testing Embedding Service ===")
    
    try:
        # Initialize embedding service
        embedding_service = EmbeddingService()
        
        # Test single embedding
        test_text = "OOP 복잡성의 근본 원인과 DOP 동기"
        embedding = embedding_service.create_embedding(test_text)
        logger.info(f"Single embedding shape: {embedding.shape}")
        logger.info(f"Embedding dimension: {embedding_service.embedding_dimension}")
        
        # Test batch embeddings
        test_texts = [
            "OOP 복잡성의 근본 원인",
            "Data-Oriented Programming benefits",
            "클래스 설계와 상속 구조"
        ]
        batch_embeddings = embedding_service.create_embeddings_batch(test_texts)
        logger.info(f"Batch embeddings count: {len(batch_embeddings)}")
        logger.info(f"Each embedding shape: {batch_embeddings[0].shape}")
        
        # Test text chunking
        long_text = "This is a very long text that should be chunked into smaller pieces. " * 50
        chunks = embedding_service.chunk_text(long_text, max_chunk_size=200, overlap=50)
        logger.info(f"Text chunked into {len(chunks)} pieces")
        logger.info(f"First chunk length: {len(chunks[0])}")
        
        logger.info("✅ Embedding Service tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Embedding Service test failed: {str(e)}")
        return False


def test_vector_database():
    """Test the vector database functionality"""
    logger.info("=== Testing Vector Database ===")
    
    try:
        # Initialize vector database
        vector_db = VectorDatabase("./test_chroma_db")
        
        # Test collection creation
        collection_name = "test_collection"
        collection = vector_db.create_collection(collection_name, embedding_dimension=384)
        logger.info(f"Created collection: {collection_name}")
        
        # Test document addition
        embedding_service = EmbeddingService()
        test_docs = [
            "First test document about OOP complexity",
            "Second test document about DOP benefits",
            "Third test document about class design"
        ]
        
        embeddings = embedding_service.create_embeddings_batch(test_docs)
        metadatas = [
            {"type": "test", "index": 0, "topic": "oop"},
            {"type": "test", "index": 1, "topic": "dop"},
            {"type": "test", "index": 2, "topic": "design"}
        ]
        ids = ["test_doc_1", "test_doc_2", "test_doc_3"]
        
        vector_db.add_documents(collection_name, test_docs, embeddings, metadatas, ids)
        logger.info(f"Added {len(test_docs)} documents to collection")
        
        # Test similarity search
        query = "object oriented programming problems"
        query_embedding = embedding_service.create_embedding(query)
        results = vector_db.search_similar(collection_name, query_embedding, n_results=2)
        
        logger.info(f"Search results for '{query}':")
        for i, (doc, meta, distance) in enumerate(zip(results['documents'], 
                                                     results['metadatas'], 
                                                     results['distances'])):
            logger.info(f"  {i+1}. Distance: {distance:.3f}, Topic: {meta.get('topic')}")
            logger.info(f"     Content: {doc[:50]}...")
        
        # Test text search
        text_results = vector_db.search_by_text(collection_name, query, embedding_service, n_results=2)
        logger.info(f"Text search returned {text_results['count']} results")
        
        # Test collection stats
        stats = vector_db.get_collection_stats(collection_name)
        logger.info(f"Collection stats: {stats}")
        
        # Clean up test collection
        vector_db.delete_collection(collection_name)
        logger.info(f"Cleaned up test collection")
        
        logger.info("✅ Vector Database tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Video Database test failed: {str(e)}")
        return False


def test_knowledge_vector_db():
    """Test the high-level Knowledge Vector DB interface"""
    logger.info("=== Testing Knowledge Vector DB ===")
    
    try:
        # Initialize knowledge vector DB
        knowledge_db = KnowledgeVectorDB("./test_knowledge_db")
        embedding_service = EmbeddingService()
        
        # Setup collections
        knowledge_db.setup_collections(embedding_service.embedding_dimension)
        
        # Test adding core content
        core_content = "OOP 복잡성의 근본 원인과 DOP 동기: 객체지향 프로그래밍의 구조적 문제점"
        core_embedding = embedding_service.create_embedding(core_content)
        core_metadata = {
            "section_title": "Test Core Section",
            "key_concept": "OOP 복잡성",
            "content_type": "core_summary",
            "language": "korean"
        }
        
        knowledge_db.add_core_content(core_content, core_embedding, core_metadata, "test_core_1")
        logger.info("Added test core content")
        
        # Test adding detail content
        detail_content = "Object-oriented programming creates complexity through the coupling of code and data within classes, leading to unpredictable behavior and difficult maintenance."
        detail_embedding = embedding_service.create_embedding(detail_content)
        detail_metadata = {
            "file_name": "test_section.md",
            "section_type": "subsection",
            "content_type": "detailed_section",
            "language": "english"
        }
        
        knowledge_db.add_detail_content(detail_content, detail_embedding, detail_metadata, "test_detail_1")
        logger.info("Added test detail content")
        
        # Test searching core content
        core_results = knowledge_db.search_core_content("OOP 문제점", embedding_service, n_results=3)
        logger.info(f"Core search returned {core_results['count']} results")
        
        # Test searching detail content
        detail_results = knowledge_db.search_detail_content("object oriented complexity", embedding_service, n_results=3)
        logger.info(f"Detail search returned {detail_results['count']} results")
        
        # Test getting stats
        stats = knowledge_db.get_stats()
        logger.info(f"Knowledge DB stats: {stats}")
        
        # Clean up
        knowledge_db.vector_db.delete_collection(knowledge_db.core_collection)
        knowledge_db.vector_db.delete_collection(knowledge_db.detail_collection)
        logger.info("Cleaned up test collections")
        
        logger.info("✅ Knowledge Vector DB tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Knowledge Vector DB test failed: {str(e)}")
        return False


def test_chapter_processor():
    """Test the chapter embedding processor"""
    logger.info("=== Testing Chapter Processor ===")
    
    try:
        # Check if chapter path exists
        chapter_path = "/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_Manning/Part1_Flexibility/Chapter1"
        if not Path(chapter_path).exists():
            logger.warning(f"Chapter path does not exist: {chapter_path}")
            logger.info("Skipping chapter processor test")
            return True
        
        # Initialize processor with test database
        processor = ChapterEmbeddingProcessor(
            chapter_path=chapter_path,
            vector_db_path="./test_chapter_db"
        )
        
        # Test parsing core content
        core_content_file = Path(chapter_path) / "chapter1_core_content.md"
        if core_content_file.exists():
            core_sections = processor.parse_core_content(str(core_content_file))
            logger.info(f"Parsed {len(core_sections)} core sections")
            
            if core_sections:
                logger.info(f"First core section: {core_sections[0]['section_title']}")
        
        # Test parsing detail sections
        sections_path = Path(chapter_path) / "content" / "sections"
        if sections_path.exists():
            detail_sections = processor.parse_detail_sections(str(sections_path))
            logger.info(f"Parsed {len(detail_sections)} detail sections")
            
            if detail_sections:
                logger.info(f"First detail section: {detail_sections[0]['metadata'].get('title', 'Unknown')}")
        
        # Clean up test database
        import shutil
        test_db_path = Path("./test_chapter_db")
        if test_db_path.exists():
            shutil.rmtree(test_db_path)
            logger.info("Cleaned up test chapter database")
        
        logger.info("✅ Chapter Processor tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Chapter Processor test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    logger.info("🚀 Starting Knowledge Sherpa Vector System Tests")
    
    test_results = []
    
    # Run all tests
    test_results.append(test_embedding_service())
    test_results.append(test_vector_database())
    test_results.append(test_knowledge_vector_db())
    test_results.append(test_chapter_processor())
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    
    logger.info(f"\n📊 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! The vector embedding system is working correctly.")
    else:
        logger.error(f"❌ {total - passed} tests failed. Please check the errors above.")
    
    # Clean up any remaining test databases
    import shutil
    test_dirs = ["./test_chroma_db", "./test_knowledge_db", "./test_chapter_db"]
    for test_dir in test_dirs:
        if Path(test_dir).exists():
            shutil.rmtree(test_dir)
            logger.info(f"Cleaned up {test_dir}")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)