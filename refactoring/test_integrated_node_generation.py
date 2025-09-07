# 생성 시간: Sat Sep  7 22:25:15 KST 2025
# 핵심 내용: IntegratedNodeGenerationStage를 사용한 unified_info_docs 생성 테스트
# 상세 내용:
#   - IntegratedNodeGenerationStage로 통합 문서 생성
#   - 생성된 unified_info_docs 확인
#   - ContentProcessingStage에서 사용할 수 있는 데이터 준비
# 상태: active

import sys
import asyncio
import os
import shutil
import json
from pathlib import Path

# 프로젝트 경로 추가
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/refactoring')

from src.stages.integrated_node_generation_stage_v3 import IntegratedNodeGenerationStage
from src.utils.config_manager import ConfigManager

async def test_integrated_node_generation():
    '''📖 IntegratedNodeGenerationStage로 unified_info_docs 생성 테스트'''
    print('\n🔍 === IntegratedNodeGenerationStage 통합 문서 생성 테스트 ===')
    
    # 소스 경로 (실제 book content가 있는 경로)
    source_path = Path('/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming')
    
    # 테스트 결과 경로
    test_data_dir = Path('/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data')
    temp_dir = test_data_dir / 'integrated_node_generation_test'
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    chapter_name = source_path.name
    test_chapter = temp_dir / chapter_name
    test_chapter.mkdir(parents=True, exist_ok=True)
    
    # 필요한 파일들 복사
    if (source_path / f'{chapter_name}_content.md').exists():
        shutil.copy2(source_path / f'{chapter_name}_content.md', test_chapter / f'{chapter_name}_content.md')
        print(f'📄 Content 파일 복사 완료')
    
    if (source_path / f'{chapter_name}_toc.json').exists():
        shutil.copy2(source_path / f'{chapter_name}_toc.json', test_chapter / f'{chapter_name}_toc.json')
        print(f'📋 TOC 파일 복사 완료')
    
    print(f'📁 테스트 디렉터리: {test_chapter}')
    
    try:
        # ConfigManager 초기화
        config_manager = ConfigManager()
        
        # IntegratedNodeGenerationStage 초기화 및 실행
        print('\n🚀 IntegratedNodeGenerationStage 실행...')
        stage = IntegratedNodeGenerationStage(config_manager)
        
        result = await stage.process({'book_directory': str(test_chapter)})
        
        if result.get('success', False):
            print('✅ IntegratedNodeGenerationStage 실행 성공!')
            
            # 결과 확인
            unified_docs_dir = test_chapter / 'unified_info_docs'
            if unified_docs_dir.exists():
                generated_files = list(unified_docs_dir.glob('*.md'))
                print(f'📊 생성된 통합 문서 수: {len(generated_files)}개')
                
                # 몇 개 파일의 구조 확인
                for i, file_path in enumerate(generated_files[:3]):
                    print(f'\n📄 파일 {i+1}: {file_path.name}')
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 섹션별 내용 길이 확인
                    sections = {
                        '# 속성': '속성 섹션',
                        '# 추출': '추출 섹션',
                        '# 내용': '내용 섹션',
                        '# 구성': '구성 섹션'
                    }
                    
                    for section_header, section_name in sections.items():
                        if section_header in content:
                            section_start = content.find(section_header)
                            next_section_start = len(content)
                            for other_header in sections.keys():
                                if other_header != section_header:
                                    other_start = content.find(other_header, section_start + 1)
                                    if other_start != -1 and other_start < next_section_start:
                                        next_section_start = other_start
                            
                            section_content = content[section_start:next_section_start].strip()
                            content_length = len(section_content)
                            print(f'  - {section_name}: {content_length} 문자')
                
                print(f'\n📁 결과 경로: {unified_docs_dir}')
                return str(test_chapter)
            else:
                print('❌ unified_info_docs 폴더가 생성되지 않음')
                return None
        else:
            print(f'❌ IntegratedNodeGenerationStage 실행 실패: {result}')
            return None
            
    except Exception as e:
        print(f'❌ IntegratedNodeGenerationStage 실행 중 에러: {e}')
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_integrated_node_generation())