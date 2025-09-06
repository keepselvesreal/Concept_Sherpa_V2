"""
Neon PostgreSQL 기반 대화형 지식 검색 시스템
Claude Code 에이전트가 질문을 받으면 Neon DB를 조회하여 답변 생성
"""

from embedding_service_v2 import get_embedding_service
from neon_vector_db import NeonVectorDB
import json
import re
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeChat:
    """
    Neon DB 기반 대화형 지식 검색 시스템
    """
    
    def __init__(self):
        """지식 채팅 시스템 초기화"""
        self.embedding_service = get_embedding_service()
        self.neon_db = NeonVectorDB()
        self.chat_history = []
        
        logger.info("지식 채팅 시스템 초기화 완료")
    
    def search_knowledge(self, question: str, search_type: str = "both", 
                        max_results: int = 3) -> Dict[str, Any]:
        """
        질문에 대해 Neon DB에서 관련 지식 검색
        
        Args:
            question: 사용자 질문
            search_type: 검색 타입 ("core", "detailed", "both")
            max_results: 최대 결과 수
            
        Returns:
            검색 결과 딕셔너리
        """
        try:
            # 질문을 임베딩으로 변환
            question_embedding = self.embedding_service.create_embedding(question)
            
            results = {
                "question": question,
                "timestamp": datetime.now().isoformat(),
                "core_results": [],
                "detailed_results": [],
                "total_sources": 0
            }
            
            # 핵심 내용 검색
            if search_type in ["core", "both"]:
                core_results = self.neon_db.search_core_content(
                    question_embedding, max_results
                )
                results["core_results"] = core_results
                
            # 상세 내용 검색
            if search_type in ["detailed", "both"]:
                detailed_results = self.neon_db.search_detailed_content(
                    question_embedding, max_results
                )
                # 상세 내용에 원문 추가
                for result in detailed_results:
                    if result['core_ref']:
                        original = self.neon_db.get_core_content_by_id(result['core_ref'])
                        if original:
                            result['original_content'] = original['document']
                
                results["detailed_results"] = detailed_results
            
            results["total_sources"] = len(results["core_results"]) + len(results["detailed_results"])
            
            logger.info(f"지식 검색 완료: {results['total_sources']}개 소스 발견")
            return results
            
        except Exception as e:
            logger.error(f"지식 검색 실패: {e}")
            return {
                "question": question,
                "error": str(e),
                "core_results": [],
                "detailed_results": [],
                "total_sources": 0
            }
    
    def format_answer(self, search_results: Dict[str, Any]) -> str:
        """
        검색 결과를 기반으로 답변 포매팅
        
        Args:
            search_results: 검색 결과
            
        Returns:
            포매팅된 답변 문자열
        """
        if search_results.get("error"):
            return f"❌ 검색 중 오류가 발생했습니다: {search_results['error']}"
        
        if search_results["total_sources"] == 0:
            return "🤔 관련된 정보를 찾을 수 없습니다. 다른 방식으로 질문해보세요."
        
        answer = f"## 📚 '{search_results['question']}'에 대한 답변\n\n"
        
        # 핵심 내용 기반 답변
        if search_results["core_results"]:
            answer += "### 🎯 핵심 내용\n\n"
            
            for i, result in enumerate(search_results["core_results"], 1):
                distance = result['distance']
                confidence = max(0, (1 - distance) * 100)  # 신뢰도 계산
                
                answer += f"**{i}. {result['id']}** (신뢰도: {confidence:.1f}%)\n"
                
                # 문서 내용 파싱
                doc = result['document']
                if doc.startswith('{'):  # JSON 형태 (composite section)
                    try:
                        doc_obj = json.loads(doc)
                        answer += f"- **제목**: {doc_obj.get('title', 'N/A')}\n"
                        answer += f"- **요약**: {doc_obj.get('content_summary', 'N/A')}\n"
                        if doc_obj.get('composed_of'):
                            answer += f"- **구성**: {', '.join(doc_obj['composed_of'])}\n"
                    except:
                        answer += f"- **내용**: {doc[:200]}...\n"
                else:  # 일반 텍스트 (leaf section)
                    # 마크다운 헤더 추출
                    title_match = re.search(r'^# (.+)', doc, re.MULTILINE)
                    if title_match:
                        answer += f"- **제목**: {title_match.group(1)}\n"
                    
                    # 첫 번째 단락 추출
                    content_lines = [line for line in doc.split('\n') if line.strip() and not line.startswith('#') and not line.startswith('**')]
                    if content_lines:
                        first_paragraph = content_lines[0][:300]
                        answer += f"- **내용**: {first_paragraph}...\n"
                
                answer += "\n"
        
        # 상세 내용 기반 답변
        if search_results["detailed_results"]:
            answer += "### 🔍 상세 분석\n\n"
            
            for i, result in enumerate(search_results["detailed_results"], 1):
                distance = result['distance']
                confidence = max(0, (1 - distance) * 100)
                
                answer += f"**{i}. {result['id']}** (신뢰도: {confidence:.1f}%)\n"
                answer += f"- **원문 참조**: {result['core_ref']}\n"
                
                # 원문이 있는 경우 제목 추출
                if result.get('original_content'):
                    original = result['original_content']
                    if original.startswith('{'):
                        try:
                            doc_obj = json.loads(original)
                            answer += f"- **관련 섹션**: {doc_obj.get('title', 'N/A')}\n"
                        except:
                            pass
                    else:
                        title_match = re.search(r'^# (.+)', original, re.MULTILINE)
                        if title_match:
                            answer += f"- **관련 섹션**: {title_match.group(1)}\n"
                
                answer += "\n"
        
        # 검색 통계
        answer += f"\n---\n"
        answer += f"🔍 **검색 결과**: {search_results['total_sources']}개 소스에서 정보 수집\n"
        answer += f"📅 **검색 시간**: {search_results['timestamp']}\n"
        
        return answer
    
    def ask(self, question: str, search_type: str = "both", 
            max_results: int = 3, save_history: bool = True) -> str:
        """
        질문하고 답변 받기
        
        Args:
            question: 사용자 질문
            search_type: 검색 타입
            max_results: 최대 결과 수
            save_history: 대화 이력 저장 여부
            
        Returns:
            포매팅된 답변
        """
        # 지식 검색
        search_results = self.search_knowledge(question, search_type, max_results)
        
        # 답변 생성
        answer = self.format_answer(search_results)
        
        # 대화 이력 저장
        if save_history:
            self.chat_history.append({
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "search_results": search_results,
                "answer": answer
            })
        
        return answer
    
    def show_stats(self) -> str:
        """시스템 통계 표시"""
        db_stats = self.neon_db.get_statistics()
        
        stats = f"""
## 📊 Knowledge Sherpa 시스템 정보

### 데이터베이스 통계
- **데이터베이스**: {db_stats['database']}
- **핵심 내용**: {db_stats['core_content_count']}개
- **상세 내용**: {db_stats['detailed_content_count']}개
- **전체 항목**: {db_stats['total_count']}개

### 대화 이력
- **총 질문 수**: {len(self.chat_history)}개

### 임베딩 모델
- **모델**: {self.embedding_service.get_model_info()['model_name']}
- **차원**: {self.embedding_service.get_model_info()['dimension']}
        """
        
        return stats.strip()
    
    def show_help(self) -> str:
        """도움말 표시"""
        help_text = """
## 🤖 Knowledge Sherpa 사용법

### 기본 질문
```python
chat.ask("OOP의 복잡성 원인은 무엇인가요?")
```

### 검색 타입 지정
```python
chat.ask("클래스 설계 문제점", search_type="core")      # 핵심 내용만
chat.ask("상속의 문제점", search_type="detailed")        # 상세 내용만  
chat.ask("데이터와 코드 분리", search_type="both")       # 전체 검색
```

### 결과 수 조정
```python
chat.ask("DOP의 장점", max_results=5)  # 최대 5개 결과
```

### 시스템 명령어
- `chat.show_stats()`: 시스템 통계
- `chat.show_help()`: 도움말
- `chat.get_history()`: 대화 이력

### 검색 가능한 주제
- OOP의 복잡성과 문제점
- 클래스 설계 과정
- 상속 구조의 한계
- 데이터와 코드의 분리
- DOP(Data-Oriented Programming) 접근법
        """
        
        return help_text.strip()
    
    def get_history(self, limit: int = 5) -> str:
        """
        대화 이력 조회
        
        Args:
            limit: 표시할 대화 수
            
        Returns:
            포매팅된 대화 이력
        """
        if not self.chat_history:
            return "📝 아직 대화 이력이 없습니다."
        
        history = "## 📝 최근 대화 이력\n\n"
        
        recent_chats = self.chat_history[-limit:]
        
        for i, chat in enumerate(recent_chats, 1):
            timestamp = datetime.fromisoformat(chat['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            sources = chat['search_results']['total_sources']
            
            history += f"**{i}. [{timestamp}]**\n"
            history += f"❓ **질문**: {chat['question']}\n"
            history += f"📊 **소스**: {sources}개\n\n"
        
        return history
    
    def close(self):
        """리소스 정리"""
        self.neon_db.close()
        logger.info("지식 채팅 시스템 종료")

def main():
    """메인 함수 - 대화형 인터페이스"""
    print("🤖 Knowledge Sherpa에 오신 것을 환영합니다!")
    print("Data-Oriented Programming 관련 질문을 해보세요.")
    print("'help'로 도움말, 'stats'로 통계, 'history'로 이력, 'quit'로 종료\n")
    
    chat = KnowledgeChat()
    
    try:
        while True:
            question = input("\n❓ 질문: ").strip()
            
            if not question:
                continue
                
            if question.lower() in ['quit', 'exit', 'q']:
                break
            elif question.lower() == 'help':
                print(chat.show_help())
            elif question.lower() == 'stats':
                print(chat.show_stats())
            elif question.lower() == 'history':
                print(chat.get_history())
            else:
                print("\n🔍 검색 중...")
                answer = chat.ask(question)
                print(answer)
    
    except KeyboardInterrupt:
        print("\n\n👋 대화를 종료합니다.")
    
    finally:
        chat.close()

if __name__ == "__main__":
    main()