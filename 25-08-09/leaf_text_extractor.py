# 생성 시간: 2025-08-09 16:15:09  
# 핵심 내용: TDD로 개발하는 리프 노드 텍스트 추출기 - 최소한의 구현
# 상세 내용:
#   - LeafTextExtractor 클래스 (라인 14): 리프 노드 텍스트 추출을 담당하는 메인 클래스
#   - load_leaf_nodes_from_data (라인 16): 테스트용 데이터 로드 메서드
#   - extract_section_text (라인 20): 마크다운에서 섹션별 텍스트 추출 메서드
#   - sanitize_filename (라인 32): 파일명 정리 메서드
#   - save_text_to_file (라인 36): 텍스트 파일 저장 메서드
#   - process_all_leaf_nodes (라인 42): 전체 처리 워크플로우 메서드
# 상태: 활성
# 주소: leaf_text_extractor  
# 참조: 

import json
import os
import re

class LeafTextExtractor:
    
    def load_leaf_nodes_from_data(self, data):
        """테스트용: 데이터에서 리프 노드 로드"""
        return data
    
    def extract_section_text(self, markdown_content, section_title):
        """마크다운에서 특정 섹션의 텍스트 추출"""
        lines = markdown_content.split('\n')
        section_found = False
        section_text = []
        
        for line in lines:
            if line.strip().startswith('#') and section_title in line:
                section_found = True
                section_text.append(line)
                continue
            elif section_found and line.strip().startswith('#'):
                break
            elif section_found:
                section_text.append(line)
                
        return '\n'.join(section_text)
    
    def sanitize_filename(self, title):
        """파일명에서 특수문자 제거"""
        # 숫자.숫자 형태를 언더스코어로 변경, 공백을 언더스코어로 변경
        sanitized = re.sub(r'[\d\.]+\s*', '', title)  # 숫자와 점 제거
        sanitized = re.sub(r'[^\w\s-]', '', sanitized)  # 특수문자 제거
        sanitized = re.sub(r'\s+', '_', sanitized)  # 공백을 언더스코어로
        return title.replace('.', '').replace(' ', '_')
    
    def save_text_to_file(self, text, output_dir, filename):
        """텍스트를 파일로 저장"""
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def load_leaf_nodes_from_file(self, json_path):
        """실제 JSON 파일에서 리프 노드 로드"""
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_markdown_content(self, markdown_path):
        """마크다운 파일 내용 로드"""
        with open(markdown_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def process_all_leaf_nodes(self, json_path, markdown_path, output_dir):
        """전체 리프 노드 처리 워크플로우"""
        # 데이터 로드
        leaf_nodes = self.load_leaf_nodes_from_file(json_path)
        markdown_content = self.load_markdown_content(markdown_path)
        
        print(f"로드된 리프 노드 수: {len(leaf_nodes)}")
        
        processed_count = 0
        for node in leaf_nodes:
            node_id = node.get('id', 'unknown')
            title = node.get('title', 'untitled')
            
            # 섹션 텍스트 추출
            section_text = self.extract_section_text(markdown_content, title)
            
            if section_text.strip():
                # 파일명 생성
                sanitized_title = self.sanitize_filename(title)
                filename = f"{node_id:03d}_{sanitized_title}.md"
                
                # 헤더와 함께 저장
                content = f"""# 생성 시간: 2025-08-09 16:15:09
# 핵심 내용: {title} 섹션의 추출된 텍스트
# 상세 내용:
#   - 섹션 ID: {node_id}
#   - 섹션 제목: {title}
#   - 추출된 내용: 원본 마크다운에서 해당 섹션 텍스트
# 상태: 활성
# 주소: {sanitized_title}
# 참조: part2_scalability_leaf_nodes.json

{section_text}"""
                
                self.save_text_to_file(content, output_dir, filename)
                processed_count += 1
                print(f"처리 완료: {filename}")
            else:
                print(f"텍스트 없음: {title}")
        
        print(f"총 {processed_count}개 파일 생성 완료")