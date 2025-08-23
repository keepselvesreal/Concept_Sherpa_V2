"""
Embedding Processor for Knowledge Sherpa
Creates and stores embeddings from chapter content
"""

import logging
import os
import json
import re
from typing import Dict, List, Any
from pathlib import Path

from embedding_service import EmbeddingService
from vector_db import KnowledgeVectorDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChapterEmbeddingProcessor:
    """Processor for creating embeddings from chapter content"""
    
    def __init__(self, 
                 chapter_path: str,
                 embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                 vector_db_path: str = "./chroma_db"):
        """
        Initialize the embedding processor
        
        Args:
            chapter_path: Path to the chapter directory
            embedding_model: Name of the embedding model to use
            vector_db_path: Path to store vector database
        """
        self.chapter_path = Path(chapter_path)
        self.embedding_service = EmbeddingService(embedding_model)
        self.vector_db = KnowledgeVectorDB(vector_db_path)
        
        # Validate chapter path
        if not self.chapter_path.exists():
            raise ValueError(f"Chapter path does not exist: {chapter_path}")
        
        logger.info(f"Initialized processor for chapter: {chapter_path}")
    
    def parse_core_content(self, core_content_path: str) -> List[Dict[str, Any]]:
        """
        Parse core content from chapter1_core_content.md
        
        Args:
            core_content_path: Path to the core content file
            
        Returns:
            List of core content sections with metadata
        """
        with open(core_content_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        core_sections = []
        
        # Split by sections using regex
        section_pattern = r'### (.*?) 핵심 내용\s*\n\*\*(.*?)\*\*:\s*(.*?)(?=\n###|\n####|\n---|\Z)'
        matches = re.findall(section_pattern, content, re.DOTALL)
        
        for match in matches:
            section_title, key_concept, description = match
            section_title = section_title.strip()
            key_concept = key_concept.strip()
            description = description.strip()
            
            # Create full content
            full_content = f"{key_concept}: {description}"
            
            core_sections.append({
                'section_title': section_title,
                'key_concept': key_concept,
                'description': description,
                'full_content': full_content,
                'content_type': 'core_summary',
                'language': 'korean'
            })
        
        # Also parse subsections (marked with ####)
        subsection_pattern = r'#### (.*?) 핵심 내용\s*\n\*\*(.*?)\*\*:\s*(.*?)(?=\n###|\n####|\n---|\Z)'
        subsection_matches = re.findall(subsection_pattern, content, re.DOTALL)
        
        for match in subsection_matches:
            section_title, key_concept, description = match
            section_title = section_title.strip()
            key_concept = key_concept.strip()
            description = description.strip()
            
            # Create full content
            full_content = f"{key_concept}: {description}"
            
            core_sections.append({
                'section_title': section_title,
                'key_concept': key_concept,
                'description': description,
                'full_content': full_content,
                'content_type': 'core_subsection',
                'language': 'korean'
            })
        
        logger.info(f"Parsed {len(core_sections)} core content sections")
        return core_sections
    
    def parse_section_file(self, section_file_path: str) -> Dict[str, Any]:
        """
        Parse a single section file
        
        Args:
            section_file_path: Path to the section file
            
        Returns:
            Dictionary with section content and metadata
        """
        with open(section_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata from the beginning of the file
        metadata = {}
        lines = content.split('\n')
        
        # Parse metadata
        for i, line in enumerate(lines):
            if line.startswith('**설명:**'):
                metadata['description'] = line.replace('**설명:**', '').strip()
            elif line.startswith('**페이지 범위:**'):
                metadata['page_range'] = line.replace('**페이지 범위:**', '').strip()
            elif line.startswith('**섹션 유형:**'):
                metadata['section_type'] = line.replace('**섹션 유형:**', '').strip()
            elif line.startswith('# '):
                metadata['title'] = line.replace('# ', '').strip()
                # Content starts after metadata
                content_start = i + 1
                break
        
        # Extract main content (skip metadata)
        main_content = '\n'.join(lines[content_start:]).strip()
        
        # Clean up content - remove page markers and extra whitespace
        main_content = re.sub(r'=== PAGE \d+ ===', '', main_content)
        main_content = re.sub(r'\n\s*\n', '\n\n', main_content)
        main_content = main_content.strip()
        
        # Determine language (primarily English content with some Korean metadata)
        metadata['language'] = 'english'
        metadata['content_type'] = 'detailed_section'
        metadata['file_name'] = os.path.basename(section_file_path)
        
        return {
            'content': main_content,
            'metadata': metadata
        }
    
    def parse_detail_sections(self, sections_path: str) -> List[Dict[str, Any]]:
        """
        Parse all detail sections from the sections directory
        
        Args:
            sections_path: Path to the sections directory
            
        Returns:
            List of detail sections with content and metadata
        """
        sections_dir = Path(sections_path)
        if not sections_dir.exists():
            raise ValueError(f"Sections directory does not exist: {sections_path}")
        
        detail_sections = []
        
        # Get all .md files in the sections directory
        section_files = list(sections_dir.glob('*.md'))
        section_files.sort()  # Sort for consistent processing
        
        for section_file in section_files:
            try:
                section_data = self.parse_section_file(str(section_file))
                detail_sections.append(section_data)
            except Exception as e:
                logger.warning(f"Failed to parse section file {section_file}: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(detail_sections)} detail sections")
        return detail_sections
    
    def create_core_embeddings(self) -> None:
        """Create and store embeddings for core content"""
        logger.info("Creating core embeddings...")
        
        # Parse core content
        core_content_file = self.chapter_path / "chapter1_core_content.md"
        if not core_content_file.exists():
            logger.error(f"Core content file not found: {core_content_file}")
            return
        
        core_sections = self.parse_core_content(str(core_content_file))
        
        # Setup collections
        self.vector_db.setup_collections(self.embedding_service.embedding_dimension)
        
        # Create embeddings and store them
        for i, section in enumerate(core_sections):
            try:
                # Create embedding
                embedding = self.embedding_service.create_embedding(section['full_content'])
                
                # Create unique ID
                content_id = f"core_{i}_{section['section_title'].replace(' ', '_').replace('.', '_')}"
                
                # Store in vector database
                self.vector_db.add_core_content(
                    content=section['full_content'],
                    embedding=embedding,
                    metadata=section,
                    content_id=content_id
                )
                
                logger.info(f"Stored core embedding: {section['section_title']}")
                
            except Exception as e:
                logger.error(f"Failed to create embedding for core section {section['section_title']}: {str(e)}")
                continue
        
        logger.info(f"Created and stored {len(core_sections)} core embeddings")
    
    def create_detail_embeddings(self) -> None:
        """Create and store embeddings for detail content"""
        logger.info("Creating detail embeddings...")
        
        # Parse detail sections
        sections_path = self.chapter_path / "content" / "sections"
        if not sections_path.exists():
            logger.error(f"Sections directory not found: {sections_path}")
            return
        
        detail_sections = self.parse_detail_sections(str(sections_path))
        
        # Process each section
        for i, section in enumerate(detail_sections):
            try:
                content = section['content']
                metadata = section['metadata']
                
                # For long content, create chunks
                chunks = self.embedding_service.chunk_text(content)
                
                # Create embeddings for chunks
                embeddings = self.embedding_service.create_embeddings_batch(chunks)
                
                # Store each chunk as a separate document
                for j, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    # Create unique ID for chunk
                    base_id = metadata.get('file_name', f'section_{i}').replace('.md', '')
                    chunk_id = f"detail_{base_id}_chunk_{j}"
                    
                    # Add chunk-specific metadata
                    chunk_metadata = metadata.copy()
                    chunk_metadata.update({
                        'chunk_index': j,
                        'total_chunks': len(chunks),
                        'chunk_length': len(chunk)
                    })
                    
                    # Store in vector database
                    self.vector_db.add_detail_content(
                        content=chunk,
                        embedding=embedding,
                        metadata=chunk_metadata,
                        content_id=chunk_id
                    )
                
                logger.info(f"Stored detail embeddings for {metadata.get('file_name', 'unknown')}: {len(chunks)} chunks")
                
            except Exception as e:
                logger.error(f"Failed to create embedding for detail section {i}: {str(e)}")
                continue
        
        logger.info(f"Created and stored detail embeddings for {len(detail_sections)} sections")
    
    def process_chapter(self) -> None:
        """Process the entire chapter - create both core and detail embeddings"""
        logger.info(f"Processing chapter: {self.chapter_path}")
        
        try:
            # Create core embeddings
            self.create_core_embeddings()
            
            # Create detail embeddings
            self.create_detail_embeddings()
            
            # Print statistics
            stats = self.vector_db.get_stats()
            logger.info("Processing completed!")
            logger.info(f"Core embeddings: {stats['core']['document_count']} documents")
            logger.info(f"Detail embeddings: {stats['detail']['document_count']} documents")
            
        except Exception as e:
            logger.error(f"Failed to process chapter: {str(e)}")
            raise
    
    def search_demo(self, query: str) -> None:
        """Demonstrate search functionality"""
        logger.info(f"\nSearching for: '{query}'")
        
        # Search core content
        core_results = self.vector_db.search_core_content(query, self.embedding_service, n_results=3)
        logger.info(f"\nCore Content Results ({core_results['count']} found):")
        for i, (doc, meta, distance) in enumerate(zip(core_results['documents'], 
                                                     core_results['metadatas'], 
                                                     core_results['distances'])):
            logger.info(f"{i+1}. [{meta.get('section_title', 'Unknown')}] (Distance: {distance:.3f})")
            logger.info(f"   Content: {doc[:100]}...")
        
        # Search detail content
        detail_results = self.vector_db.search_detail_content(query, self.embedding_service, n_results=3)
        logger.info(f"\nDetail Content Results ({detail_results['count']} found):")
        for i, (doc, meta, distance) in enumerate(zip(detail_results['documents'], 
                                                     detail_results['metadatas'], 
                                                     detail_results['distances'])):
            logger.info(f"{i+1}. [{meta.get('file_name', 'Unknown')}] (Distance: {distance:.3f})")
            logger.info(f"   Content: {doc[:100]}...")


def main():
    """Main function to run the embedding processor"""
    # Configuration
    chapter_path = "/home/nadle/projects/Knowledge_Sherpa/v2/Data-Oriented_Programming_Manning/Part1_Flexibility/Chapter1"
    
    # Create processor
    processor = ChapterEmbeddingProcessor(chapter_path)
    
    # Process the chapter
    processor.process_chapter()
    
    # Demo searches
    processor.search_demo("OOP 복잡성")
    processor.search_demo("객체지향 프로그래밍 문제점")
    processor.search_demo("data oriented programming benefits")
    processor.search_demo("클래스 설계")


if __name__ == "__main__":
    main()