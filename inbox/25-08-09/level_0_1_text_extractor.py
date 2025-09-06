"""
생성 시간: 2025-08-09 16:00:00 KST
핵심 내용: PDF에서 Level 0(Parts)와 Level 1(Chapters) 단위로 텍스트를 추출하여 파일로 저장하는 시스템
상세 내용:
    - TOCProcessor (라인 10-60): JSON 목차 데이터 로드 및 Level 0,1 노드 필터링 기능
    - PDFTextExtractor (라인 62-120): PDF 파일에서 페이지 범위별 텍스트 추출 기능  
    - FileManager (라인 122-160): 추출된 텍스트를 파일로 저장하는 관리 기능
    - main 함수 (라인 162-200): 전체 프로세스 실행 및 오류 처리
상태: 초기 구현 완료
주소: level_0_1_text_extractor
참조: enhanced_toc_with_relationships.json 파일 참조하여 구조 파악
"""

import json
import os
from typing import List, Dict, Any
import pdfplumber


class TOCProcessor:
    """목차 JSON 데이터를 처리하여 Level 0과 1 노드를 추출하는 클래스"""
    
    def __init__(self, toc_file_path: str):
        self.toc_file_path = toc_file_path
        self.toc_data = self.load_toc_data()
    
    def load_toc_data(self) -> List[Dict[str, Any]]:
        """목차 JSON 파일을 로드"""
        try:
            with open(self.toc_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"목차 파일 로드 오류: {e}")
            return []
    
    def get_level_0_1_nodes(self) -> List[Dict[str, Any]]:
        """Level 0(Parts)와 Level 1(Chapters) 노드만 필터링하여 반환"""
        filtered_nodes = []
        for node in self.toc_data:
            if node.get('level') in [0, 1]:
                # 페이지 수가 0인 노드는 제외
                if node.get('page_count', 0) > 0:
                    filtered_nodes.append(node)
        return filtered_nodes
    
    def print_filtered_nodes(self):
        """필터링된 노드들을 출력"""
        nodes = self.get_level_0_1_nodes()
        print(f"\n=== Level 0-1 노드 목록 ({len(nodes)}개) ===")
        for node in nodes:
            level_prefix = "Part" if node['level'] == 0 else "Chapter"
            print(f"[{level_prefix}] {node['title']} (페이지: {node['start_page']}-{node['end_page']}, 총 {node['page_count']}페이지)")


class PDFTextExtractor:
    """PDF에서 지정된 페이지 범위의 텍스트를 추출하는 클래스"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = None
        self.open_document()
    
    def open_document(self):
        """PDF 문서 열기"""
        try:
            self.doc = pdfplumber.open(self.pdf_path)
            print(f"PDF 문서 로드 성공: {len(self.doc.pages)} 페이지")
        except Exception as e:
            print(f"PDF 문서 로드 오류: {e}")
            self.doc = None
    
    def extract_text_from_pages(self, start_page: int, end_page: int) -> str:
        """지정된 페이지 범위에서 텍스트 추출"""
        if not self.doc:
            return ""
        
        extracted_text = []
        try:
            # 페이지는 0-based 인덱스이므로 1을 빼줌
            for page_num in range(start_page - 1, min(end_page, len(self.doc.pages))):
                page = self.doc.pages[page_num]
                text = page.extract_text()
                if text:
                    extracted_text.append(f"=== 페이지 {page_num + 1} ===\n{text}\n")
        except Exception as e:
            print(f"텍스트 추출 오류 (페이지 {start_page}-{end_page}): {e}")
            return ""
        
        return "\n".join(extracted_text)
    
    def close_document(self):
        """PDF 문서 닫기"""
        if self.doc:
            self.doc.close()


class FileManager:
    """파일 저장 및 관리를 담당하는 클래스"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.create_output_directory()
    
    def create_output_directory(self):
        """출력 디렉토리 생성"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"출력 디렉토리 생성: {self.output_dir}")
    
    def sanitize_filename(self, title: str) -> str:
        """파일명으로 사용할 수 없는 문자들을 제거/변환"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, '_')
        return title.strip()
    
    def save_text_to_file(self, node: Dict[str, Any], text: str):
        """추출된 텍스트를 파일로 저장"""
        try:
            # 파일명 생성
            level = node['level']
            title = self.sanitize_filename(node['title'])
            prefix = f"Level{level:02d}" 
            filename = f"{prefix}_{title}.md"
            
            file_path = os.path.join(self.output_dir, filename)
            
            # 파일 내용 구성
            content = self.create_file_content(node, text)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"파일 저장 완료: {filename}")
            
        except Exception as e:
            print(f"파일 저장 오류 ({node['title']}): {e}")
    
    def create_file_content(self, node: Dict[str, Any], text: str) -> str:
        """파일 내용을 구성"""
        header = f"""# {node['title']}

**Level:** {node['level']}
**페이지 범위:** {node['start_page']} - {node['end_page']}
**총 페이지 수:** {node['page_count']}
**ID:** {node['id']}

---

"""
        return header + text


def main():
    """메인 실행 함수"""
    # 파일 경로 설정
    toc_file = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-08/enhanced_toc_with_relationships.json"
    pdf_file = "/home/nadle/projects/Knowledge_Sherpa/v2/2022_Data-Oriented Programming_Manning.pdf"
    output_dir = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-09/extracted_texts"
    
    try:
        # 목차 처리기 초기화
        toc_processor = TOCProcessor(toc_file)
        nodes = toc_processor.get_level_0_1_nodes()
        
        if not nodes:
            print("추출할 노드가 없습니다.")
            return
        
        toc_processor.print_filtered_nodes()
        
        # PDF 텍스트 추출기 초기화
        pdf_extractor = PDFTextExtractor(pdf_file)
        
        # 파일 관리자 초기화
        file_manager = FileManager(output_dir)
        
        # 각 노드별로 텍스트 추출 및 저장
        print(f"\n=== 텍스트 추출 시작 ===")
        for i, node in enumerate(nodes, 1):
            print(f"\n[{i}/{len(nodes)}] 처리 중: {node['title']}")
            
            # 텍스트 추출
            text = pdf_extractor.extract_text_from_pages(
                node['start_page'], 
                node['end_page']
            )
            
            if text:
                # 파일로 저장
                file_manager.save_text_to_file(node, text)
            else:
                print(f"텍스트 추출 실패: {node['title']}")
        
        # PDF 문서 닫기
        pdf_extractor.close_document()
        
        print(f"\n=== 텍스트 추출 완료 ===")
        print(f"총 {len(nodes)}개 파일이 {output_dir}에 저장되었습니다.")
        
    except Exception as e:
        print(f"실행 중 오류 발생: {e}")


if __name__ == "__main__":
    main()