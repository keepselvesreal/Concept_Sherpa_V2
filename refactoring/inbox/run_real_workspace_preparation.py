#!/usr/bin/env python3
# 실제 WorkspacePreparationStage를 사용해서 실제 PDF 처리 및 ResultLogger 확인

import asyncio
import os
import sys
from pathlib import Path

# 프로젝트 경로 설정
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

async def run_real_workspace_preparation():
    """실제 WorkspacePreparationStage 실행"""
    
    print("🚀 실제 WorkspacePreparationStage 실행 시작")
    
    # 실제 PDF 경로
    pdf_path = "/home/nadle/projects/Knowledge_Sherpa/v2/data/2022_Data-Oriented Programming_Manning.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF 파일이 없습니다: {pdf_path}")
        return
    
    try:
        # 의존성 임포트
        from utils.config_manager import ConfigManager
        from utils.logger import LoggerFactory
        from stages.workspace_preparation import WorkspacePreparationStage
        
        print("✅ 모든 모듈 임포트 성공")
        
        # ConfigManager 설정
        config_manager = ConfigManager()
        
        # 테스트 설정 - 1장만 처리하도록 설정
        config_manager.data = {
            "test": {
                "enabled": True,
                "selected_chapters": [1]  # 1장만 처리
            },
            "workspace_preparation": {
                "folder_structure": {
                    "base_path": str(project_root / "output")
                }
            },
            "global": {
                "logs_base_dir": str(project_root / "logs"),
                "results_base_dir": str(project_root / "output")
            }
        }
        
        print(f"📁 출력 디렉토리: {project_root / 'output'}")
        print(f"📋 테스트 모드: 1장만 처리")
        
        # LoggerFactory 및 WorkspacePreparationStage 초기화
        logger_factory = LoggerFactory(config_manager)
        workspace_stage = WorkspacePreparationStage(config_manager, logger_factory)
        
        print(f"📖 처리할 PDF: {pdf_path}")
        print("🔄 워크스페이스 준비 실행 중...")
        
        # 실제 실행
        input_data = {"pdf_path": pdf_path}
        result = await workspace_stage.process(input_data)
        
        # 결과 확인
        if not result.get('success', False):
            print(f"❌ 처리 실패: {result.get('error', 'Unknown error')}")
            return
        
        print("✅ 워크스페이스 준비 성공!")
        print(f"📖 책 제목: {result.get('book_title', 'Unknown')}")
        print(f"📊 총 장 수: {result.get('total_chapters', 0)}")
        print(f"📁 생성된 폴더 수: {len(result.get('created_folders', []))}")
        
        # ResultLogger 결과 확인
        if hasattr(workspace_stage, 'result_logger') and workspace_stage.result_logger:
            result_logger = workspace_stage.result_logger
            saved_results = result_logger.list_results()
            
            print(f"\n💾 ResultLogger 결과:")
            print(f"   저장된 파일 수: {len(saved_results)}")
            print(f"   저장 위치: {result_logger.results_dir}")
            
            # 파일별 상세 정보
            json_files = [r for r in saved_results if r['format'] == 'json']
            md_files = [r for r in saved_results if r['format'] == 'md']
            
            print(f"   📄 JSON 파일 (목차): {len(json_files)}개")
            print(f"   📝 MD 파일 (내용): {len(md_files)}개")
            
            # 실제 파일 내용 확인
            for i, file_info in enumerate(saved_results):
                file_path = Path(file_info['path'])
                size_mb = file_info['size'] / 1024 / 1024
                
                print(f"\n📁 파일 {i+1}: {file_path.name}")
                print(f"   📊 크기: {size_mb:.2f}MB")
                print(f"   🕐 생성시간: {file_info['created']}")
                
                if file_info['format'] == 'json':
                    # JSON 파일 내용 미리보기
                    try:
                        import json
                        with open(file_path, 'r', encoding='utf-8') as f:
                            toc_data = json.load(f)
                        
                        chapter_info = toc_data.get('chapter_info', {})
                        sections = toc_data.get('sections', [])
                        
                        print(f"   📋 장 정보: {chapter_info.get('number')}장 - {chapter_info.get('title')}")
                        print(f"   📄 페이지: {chapter_info.get('start_page')}-{chapter_info.get('end_page')}")
                        print(f"   🔗 섹션 수: {len(sections)}개")
                        
                        # 주요 섹션 출력
                        if sections:
                            print(f"   📝 주요 섹션:")
                            for idx, section in enumerate(sections[:5]):
                                print(f"      {idx+1}. {section.get('title', 'No title')} (p.{section.get('page', '?')})")
                                
                    except Exception as e:
                        print(f"   ⚠️ JSON 파일 읽기 실패: {e}")
                
                elif file_info['format'] == 'md':
                    # 마크다운 파일 내용 미리보기  
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            md_content = f.read()
                        
                        lines = md_content.split('\n')
                        headers = [line for line in lines if line.startswith('#')]
                        
                        print(f"   📝 총 라인: {len(lines)}")
                        print(f"   📑 헤더 수: {len(headers)}개")
                        
                        if headers:
                            print(f"   📋 주요 헤더:")
                            for idx, header in enumerate(headers[:5]):
                                print(f"      {idx+1}. {header}")
                                
                    except Exception as e:
                        print(f"   ⚠️ 마크다운 파일 읽기 실패: {e}")
            
            print(f"\n🎯 실제 WorkspacePreparationStage를 통해 생성된 결과를 확인했습니다!")
            print(f"📁 결과 파일들은 {result_logger.results_dir}에 저장되어 있습니다.")
            
        else:
            print("⚠️ ResultLogger가 초기화되지 않았습니다.")
            
    except ImportError as e:
        print(f"❌ 모듈 임포트 실패: {e}")
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_real_workspace_preparation())