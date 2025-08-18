"""
생성 시간: 2025-08-18 11:25:30
핵심 내용: 노드 문서 처리기 사용법 예시 스크립트
상세 내용:
    - example_single_file 함수 (라인 20-35): 단일 파일 처리 예시
    - example_directory_processing 함수 (라인 37-55): 디렉토리 일괄 처리 예시
    - example_query_results 함수 (라인 57-80): 저장된 결과 조회 예시
    - 사용법 가이드 및 실행 예시
상태: 
주소: example_usage
참조: node_document_processor, db_manager
"""

from node_document_processor import NodeDocumentProcessor
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_single_file():
    """단일 파일 처리 예시"""
    print("=== 단일 파일 처리 예시 ===")
    
    processor = NodeDocumentProcessor(project_name="knowledge_sherpa")
    
    try:
        # 현재 디렉토리의 info.md 파일 처리
        file_path = "00_lev0_retrieval_agents_actually_solved_ai_codings_biggest_problem_info.md"
        
        if Path(file_path).exists():
            doc_id = processor.process_node_document(file_path, generate_embeddings=True)
            print(f"✅ 문서 처리 완료: {doc_id}")
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            
    except Exception as e:
        print(f"❌ 처리 실패: {e}")
    finally:
        processor.close()

def example_directory_processing():
    """디렉토리 일괄 처리 예시"""
    print("\n=== 디렉토리 일괄 처리 예시 ===")
    
    processor = NodeDocumentProcessor(project_name="knowledge_sherpa")
    
    try:
        # 현재 디렉토리의 모든 *_info.md 파일 처리
        current_dir = "."
        pattern = "*_info.md"
        
        processed_docs = processor.process_directory(current_dir, pattern)
        
        if processed_docs:
            print(f"✅ 처리 완료: {len(processed_docs)}개 문서")
            for doc_id in processed_docs:
                print(f"   - {doc_id}")
        else:
            print(f"❌ 패턴 '{pattern}'에 맞는 파일이 없습니다")
            
    except Exception as e:
        print(f"❌ 처리 실패: {e}")
    finally:
        processor.close()

def example_query_results():
    """저장된 결과 조회 예시"""
    print("\n=== 저장된 결과 조회 예시 ===")
    
    import subprocess
    
    try:
        # 저장된 문서 목록 조회
        print("📄 저장된 문서 목록:")
        result = subprocess.run([
            "python", "db_manager.py", "--project", "knowledge_sherpa", 
            "data", "query", "documents", "--limit", "5"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 문서 조회 성공")
        else:
            print(f"❌ 문서 조회 실패: {result.stderr}")
        
        # 임베딩 통계 조회
        print("\n🔍 임베딩 통계:")
        embedding_tables = [
            "core_content_embeddings",
            "detailed_core_embeddings", 
            "main_topic_embeddings",
            "sub_topic_embeddings"
        ]
        
        for table in embedding_tables:
            result = subprocess.run([
                "python", "db_manager.py", "--project", "knowledge_sherpa",
                "data", "query", table, "--limit", "1"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {table}: 데이터 존재")
            else:
                print(f"❌ {table}: 조회 실패")
                
    except Exception as e:
        print(f"❌ 조회 실패: {e}")

def main():
    """메인 실행 함수"""
    print("🚀 노드 문서 처리기 사용법 예시")
    print("=" * 50)
    
    # 1. 단일 파일 처리
    example_single_file()
    
    # 2. 디렉토리 일괄 처리  
    example_directory_processing()
    
    # 3. 결과 조회
    example_query_results()
    
    print("\n" + "=" * 50)
    print("📖 사용법 가이드:")
    print()
    print("1. 단일 파일 처리:")
    print("   python node_document_processor.py --file <파일경로>")
    print()
    print("2. 디렉토리 일괄 처리:")
    print("   python node_document_processor.py --directory <디렉토리경로>")
    print()
    print("3. 특정 패턴 파일 처리:")
    print("   python node_document_processor.py --directory <디렉토리경로> --pattern '*_info.md'")
    print()
    print("4. 임베딩 없이 처리:")
    print("   python node_document_processor.py --file <파일경로> --no-embeddings")
    print()
    print("5. 다른 프로젝트 사용:")
    print("   python node_document_processor.py --file <파일경로> --project <프로젝트명>")
    print()
    print("6. 저장된 데이터 조회:")
    print("   python db_manager.py --project knowledge_sherpa data query documents")
    print()
    print("7. 특정 문서 검색:")
    print("   python db_manager.py --project knowledge_sherpa data query documents --where \"source_type='youtube'\"")

if __name__ == "__main__":
    main()