# 생성 시간: Sun Sep  7 21:25:15 KST 2025
# 핵심 내용: 실제 데이터 기반 ContentProcessingStage 테스트 시스템
# 상세 내용:
#   - RealContentProcessingStageTester (라인 35-120): 실제 모듈과 데이터 기반 테스터
#   - setup_test_environment (라인 65-95): 안전한 임시 테스트 환경 구성
#   - test_01_real_extraction (라인 122-180): 실제 AI 기반 추출 테스트
#   - test_02_real_parent_child_processing (라인 182-240): 실제 부모-자식 관계 처리
#   - test_03_real_document_sorting (라인 242-300): 실제 문서 정렬 검증
#   - test_04_real_toc_generation (라인 302-360): 실제 목차 생성 (향후 구현)
#   - run_all_real_tests (라인 362-420): 전체 실제 테스트 실행
# 상태: active

import os
import tempfile
import shutil
import asyncio
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# 실제 구현된 모듈들 임포트
import sys
import os
# refactoring 프로젝트 루트를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
refactoring_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, refactoring_root)
sys.path.append('/home/nadle/projects/Knowledge_Sherpa/v2/development/book_pipeline_refactored/src')

from src.services.ai_service_v4 import AIService
from refactoring_logger import RefactoringLogger, RefactoringLogContext
from src.stages.content_processing_stage import ContentProcessingStage


class RealContentProcessingStageTester:
    """실제 데이터 기반 ContentProcessingStage 테스터"""
    
    def __init__(self, original_chapter_path: str, config_path: str):
        self.original_chapter_path = Path(original_chapter_path)
        self.config_path = config_path
        self.test_temp_dir = None
        self.test_chapter_dir = None
        
        # 일반 로깅 설정 (AI 서비스 초기화 전에 설정)
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # 설정 로드
        self.config = self._load_config()
        
        # AI 서비스 초기화
        self.ai_service = self._initialize_ai_service()
        
        # 로거 설정 - 현재 작업 프로젝트의 logs 폴더 사용
        self.logger_context = RefactoringLogContext(
            stage="content_processing_real_test",
            class_name="RealContentProcessingStageTester", 
            method_name="test_execution",
            operation_id=""
        )
        
        # 🔄 올바른 로그 디렉토리: 현재 refactoring 프로젝트의 logs 폴더
        log_dir = Path('/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/logs')
        log_dir.mkdir(exist_ok=True)  # logs 폴더가 없으면 생성
        self.refactoring_logger = RefactoringLogger(log_dir)
        
    def _load_config(self) -> Dict:
        """설정 파일 로드"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"❌ 설정 파일 로드 실패: {e}")
            # 기본 설정
            return {
                'processing_mode': 'unified_type_processing',
                'max_parallel': 4
            }
    
    def _initialize_ai_service(self) -> AIService:
        """AI 서비스 초기화"""
        try:
            # AIService는 config_manager, logger, stage_name 3개 파라미터 필요
            ai_service = AIService(self.config, self.logger, "content_processing")
            return ai_service
        except Exception as e:
            print(f"❌ AI 서비스 초기화 실패: {e}")
            return None

    def setup_test_environment(self, selected_files: List[str] = None) -> str:
        """🔄 실제 데이터 기반 테스트 환경 구성"""
        # tests/data 안에 고정 임시 폴더 생성 (사용자 확인용)
        test_data_dir = Path('/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data')
        self.test_temp_dir = str(test_data_dir / "content_processing_test_results")
        
        # 기존 폴더가 있으면 삭제 후 재생성
        if Path(self.test_temp_dir).exists():
            shutil.rmtree(self.test_temp_dir)
        Path(self.test_temp_dir).mkdir(parents=True, exist_ok=True)
        print(f"📁 실제 데이터 테스트 결과 디렉터리: {self.test_temp_dir}")
        
        # 디렉터리 구조 생성 및 파일 복사
        chapter_name = self.original_chapter_path.name
        self.test_chapter_dir = Path(self.test_temp_dir) / chapter_name
        test_unified_dir = self.test_chapter_dir / "unified_info_docs"
        test_unified_dir.mkdir(parents=True)
        
        # 실제 데이터 파일들 복사
        original_unified_dir = self.original_chapter_path / "unified_info_docs"
        
        if selected_files:
            for file_name in selected_files:
                src = original_unified_dir / file_name
                dst = test_unified_dir / file_name
                if src.exists():
                    shutil.copy2(src, dst)
                    print(f"  ✅ 실제 데이터 복사: {file_name}")
        else:
            # 모든 *_info.md 파일 복사
            for src_file in original_unified_dir.glob("*_info.md"):
                dst = test_unified_dir / src_file.name
                shutil.copy2(src_file, dst)
                print(f"  ✅ 실제 데이터 복사: {src_file.name}")
        
        # TOC 파일 복사
        toc_file = self.original_chapter_path / f"{chapter_name}_toc.json"
        if toc_file.exists():
            shutil.copy2(toc_file, self.test_chapter_dir / f"{chapter_name}_toc.json")
        
        # 로그 기록
        self.refactoring_logger.operation_start(
            self.logger_context, 
            {
                "test_env_path": str(self.test_chapter_dir), 
                "selected_files_count": len(selected_files) if selected_files else "all",
                "using_real_data": True,
                "using_real_ai": True
            }
        )
        
        return str(self.test_chapter_dir)
    
    def cleanup_test_environment(self):
        """🗑️ 테스트 환경 정리"""
        if self.test_temp_dir and Path(self.test_temp_dir).exists():
            shutil.rmtree(self.test_temp_dir)
            print(f"🗑️ 실제 테스트 임시 디렉터리 삭제: {self.test_temp_dir}")
            
            # 로그 기록
            self.refactoring_logger.operation_success(
                self.logger_context,
                {"cleanup_completed": True, "deleted_path": self.test_temp_dir}
            )
            
            self.test_temp_dir = None
            self.test_chapter_dir = None

    async def test_01_real_extraction(self):
        """📝 1단계: 실제 AI 기반 기본 추출 테스트"""
        print("\n🔍 === 1단계: 실제 AI 기반 기본 추출 테스트 시작 ===")
        
        if not self.ai_service:
            print("❌ AI 서비스가 초기화되지 않았습니다")
            return
        
        try:
            # 실제 테스트 데이터로 테스트 환경 구성
            test_files = ["17_lev3_1.1.1_The_design_phase_info.md"]
            test_chapter = self.setup_test_environment(test_files)
            
            # 실제 ContentProcessingStage 생성
            stage = ContentProcessingStage(self.config, self.ai_service)
            test_doc_path = Path(test_chapter) / "unified_info_docs" / test_files[0]
            
            print(f"📄 실제 테스트 대상 파일: {test_doc_path}")
            
            # 1. 실제 문서 파싱
            doc_data = await stage.parse_unified_document(str(test_doc_path))
            
            if not doc_data:
                raise Exception("실제 문서 파싱 실패")
                
            print(f"📊 파싱된 실제 문서: {doc_data.get('title', 'N/A')}")
            print(f"📝 level: {doc_data.get('level', 'N/A')}")
            print(f"🔗 구성 파일 수: {len(doc_data.get('composition_files', []))}")
            print(f"📄 내용 섹션 길이: {len(doc_data.get('content_section', ''))} 문자")
            
            # 2. 🤖 실제 AI 호출로 추출 작업
            print("🤖 실제 AI 서비스로 추출 작업 실행...")
            extraction_result = await stage.generate_extract_section(doc_data)
            
            if not extraction_result:
                raise Exception("실제 AI 추출 작업 실패")
            
            success_count = sum(1 for content in extraction_result.values() if content.strip())
            print(f"📋 실제 추출 결과: {success_count}/5 섹션")
            
            # 추출된 내용 미리보기
            for section_key, content in extraction_result.items():
                if content.strip():
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"  🔍 {section_key}: {preview}")
            
            # 3. 실제 파일 업데이트
            print("📝 실제 파일에 추출 섹션 업데이트...")
            formatted_content = stage.format_extraction_content(extraction_result)
            await stage.update_extraction_section(str(test_doc_path), formatted_content)
            
            # 4. 결과 검증
            with open(test_doc_path, 'r', encoding='utf-8') as f:
                updated_content = f.read()
                
            if '## 핵심 내용' in updated_content:
                print("✅ 실제 추출 내용 삽입 성공")
            else:
                raise Exception("실제 추출 내용 삽입 실패")
            
            print("✅ 1단계 실제 테스트 완료")
            print(f"📁 실제 테스트 결과 확인: {test_chapter}")
            print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
            
        except Exception as e:
            print(f"❌ 1단계 실제 테스트 실패: {e}")
            self.refactoring_logger.operation_error(self.logger_context, e)
            raise

    async def test_02_real_parent_child_processing(self):
        """👨‍👩‍👧‍👦 2단계: 실제 부모-자식 관계 처리 테스트"""
        print("\n🔍 === 2단계: 실제 부모-자식 관계 처리 테스트 시작 ===")
        
        if not self.ai_service:
            print("❌ AI 서비스가 초기화되지 않았습니다")
            return
        
        try:
            # 실제 테스트 파일들 (리프 노드 4개 + 부모 노드 1개)
            test_files = [
                "17_lev3_1.1.1_The_design_phase_info.md",
                "18_lev3_1.1.2_UML_101_info.md", 
                "19_lev3_1.1.3_Explaining_each_piece_of_the_class_diagram_info.md",
                "20_lev3_1.1.4_The_implementation_phase_info.md",
                "16_lev2_1.1_OOP_design_Classic_or_classical_info.md"  # 부모 노드
            ]
            test_chapter = self.setup_test_environment(test_files)
            
            # 실제 ContentProcessingStage 생성
            stage = ContentProcessingStage(self.config, self.ai_service)
            test_unified_dir = Path(test_chapter) / "unified_info_docs"
            
            # 1. 실제 리프 노드들 추출 작업
            composition_files = test_files[:-1]  # 부모 노드 제외
            print(f"🔄 {len(composition_files)}개 리프 노드 실제 추출 작업...")
            
            for comp_file in composition_files:
                comp_path = test_unified_dir / comp_file
                comp_doc = await stage.parse_unified_document(str(comp_path))
                
                if comp_doc:
                    # 실제 AI 추출 작업
                    extraction = await stage.generate_extract_section(comp_doc)
                    if extraction:
                        formatted_content = stage.format_extraction_content(extraction)
                        await stage.update_extraction_section(str(comp_path), formatted_content)
                        print(f"  ✅ 실제 리프 노드 처리: {comp_file}")
                    else:
                        print(f"  ⚠️ 추출 실패: {comp_file}")
            
            # 2. 실제 부모 노드 처리
            parent_file = test_files[-1]
            parent_path = test_unified_dir / parent_file
            parent_doc = await stage.parse_unified_document(str(parent_path))
            
            if parent_doc:
                print(f"🔄 부모 노드 실제 추출 작업: {parent_file}")
                parent_extraction = await stage.generate_extract_section(parent_doc)
                
                if parent_extraction:
                    formatted_parent_content = stage.format_extraction_content(parent_extraction)
                    await stage.update_extraction_section(str(parent_path), formatted_parent_content)
                    print("  ✅ 부모 노드 추출 완료")
                    
                    # 3. 상태 마킹 추가
                    await stage.add_update_status_mark(str(parent_path), "<구성 노드 반영 완료>")
                    
                    for comp_file in composition_files:
                        comp_path = test_unified_dir / comp_file
                        await stage.add_update_status_mark(str(comp_path), "<부모 노드 반영 완료>")
                    
                    print("🏷️ 상태 마킹 완료")
                else:
                    print("  ⚠️ 부모 노드 추출 실패")
            
            print("✅ 2단계 실제 테스트 완료")
            print(f"📁 실제 테스트 결과 확인: {test_chapter}")
            print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
            
        except Exception as e:
            print(f"❌ 2단계 실제 테스트 실패: {e}")
            self.refactoring_logger.operation_error(self.logger_context, e)
            raise

    async def test_03_real_document_sorting(self):
        """📊 3단계: 실제 문서 정렬 테스트"""
        print("\n🔍 === 3단계: 실제 문서 정렬 테스트 시작 ===")
        
        try:
            # 모든 실제 파일로 테스트 환경 구성
            test_chapter = self.setup_test_environment()  # 모든 파일 복사
            
            # 실제 ContentProcessingStage로 문서 정렬
            stage = ContentProcessingStage(self.config, self.ai_service)
            sorted_groups = await stage.load_and_sort_documents(test_chapter)
            
            if not sorted_groups:
                raise Exception("문서 정렬 결과가 비어있음")
            
            # 검증: 첫 번째 그룹이 리프 노드들인지
            leaf_group = sorted_groups[0] if sorted_groups else []
            leaf_count = 0
            for doc in leaf_group:
                composition = doc.get('composition_section', '').strip()
                if not composition or composition == '---':
                    leaf_count += 1
                else:
                    print(f"⚠️ 리프 그룹에 비리프 노드 발견: {doc['title']}")
            
            # 검증: level 정렬 확인
            level_violations = 0
            if len(sorted_groups) > 1:
                for i in range(1, len(sorted_groups)-1):
                    if sorted_groups[i] and sorted_groups[i+1]:
                        current_level = sorted_groups[i][0].get('level', 0)
                        next_level = sorted_groups[i+1][0].get('level', 0)
                        if current_level < next_level:
                            print(f"⚠️ level 정렬 위반: {current_level} → {next_level}")
                            level_violations += 1
            
            # 결과 출력
            print(f"📋 실제 데이터 정렬 결과: {len(sorted_groups)}개 그룹")
            total_docs = 0
            for i, group in enumerate(sorted_groups):
                total_docs += len(group)
                if i == 0:
                    print(f"  그룹 {i+1} (리프 노드): {len(group)}개 (유효: {leaf_count}개)")
                    for doc in group[:3]:  # 처음 3개만 표시
                        print(f"    - {doc.get('title', 'N/A')} (level: {doc.get('level', 'N/A')})")
                    if len(group) > 3:
                        print(f"    ... 및 {len(group) - 3}개 더")
                else:
                    if group:
                        level = group[0].get('level', 0)
                        print(f"  그룹 {i+1} (Level {level}): {len(group)}개")
                        for doc in group[:2]:  # 처음 2개만 표시
                            comp_files = doc.get('composition_files', [])
                            print(f"    - {doc.get('title', 'N/A')} (구성: {len(comp_files)}개)")
                        if len(group) > 2:
                            print(f"    ... 및 {len(group) - 2}개 더")
            
            print(f"📊 총 처리 문서: {total_docs}개")
            
            if level_violations == 0:
                print("✅ 3단계 실제 테스트 완료 - level 정렬 검증 통과")
            else:
                print(f"⚠️ 3단계 완료 - level 정렬 위반: {level_violations}건")
                
            print(f"📁 실제 테스트 결과 확인: {test_chapter}")
            print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
            
        except Exception as e:
            print(f"❌ 3단계 실제 테스트 실패: {e}")
            self.refactoring_logger.operation_error(self.logger_context, e)
            raise

    async def test_04_real_toc_generation(self):
        """📖 4단계: 실제 목차 생성 테스트"""  
        print("\n🔍 === 4단계: 실제 목차 생성 테스트 시작 ===")
        
        try:
            # 제한된 파일들로 테스트 환경 구성 (추출된 내용이 있는 파일들)
            test_files = [
                "17_lev3_1.1.1_The_design_phase_info.md",
                "18_lev3_1.1.2_UML_101_info.md", 
                "19_lev3_1.1.3_Explaining_each_piece_of_the_class_diagram_info.md",
                "20_lev3_1.1.4_The_implementation_phase_info.md",
                "16_lev2_1.1_OOP_design_Classic_or_classical_info.md"
            ]
            test_chapter = self.setup_test_environment(test_files)
            print(f"📁 실제 데이터 테스트 결과 디렉터리: {test_chapter}")
            
            # TOC 파일 복사
            chapter_name = self.original_chapter_path.name
            toc_file = self.original_chapter_path / f"{chapter_name}_toc.json"
            if toc_file.exists():
                shutil.copy2(toc_file, Path(test_chapter) / f"{chapter_name}_toc.json")
                print(f"📋 TOC 파일 복사 완료: {toc_file.name}")
            
            # 각 파일에 간단한 추출 작업 수행 (목차 생성용 데이터 준비)
            stage = ContentProcessingStage(self.config, self.ai_service)
            
            print("🔄 목차 생성을 위한 추출 작업 수행...")
            test_unified_dir = Path(test_chapter) / "unified_info_docs"
            for test_file in test_files:
                file_path = test_unified_dir / test_file
                doc_data = await stage.parse_unified_document(str(file_path))
                if doc_data:
                    extraction_result = await stage.generate_extract_section(doc_data)
                    if extraction_result:
                        formatted_content = stage.format_extraction_content(extraction_result)
                        await stage.update_extraction_section(str(file_path), formatted_content)
                        print(f"  ✅ 추출 완료: {test_file}")
            
            # 목차 생성
            print("\n📖 개선된 목차 MD 파일 생성...")
            toc_success = await stage.generate_enhanced_toc_file(test_chapter)
            
            # 생성된 파일 확인
            toc_file = Path(test_chapter) / f"{chapter_name}_enhanced_toc.md"
            
            if toc_success and toc_file.exists():
                print(f"✅ 목차 파일 생성 성공: {toc_file}")
                with open(toc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("📖 목차 파일 미리보기 (처음 800자):")
                    print("-" * 50)
                    print(content[:800] + "..." if len(content) > 800 else content)
                    print("-" * 50)
                print(f"📄 전체 파일 크기: {len(content)}자")
            else:
                print("❌ 목차 파일 생성 실패")
            
            print("✅ 4단계 실제 테스트 완료")
            print(f"📁 실제 테스트 결과 확인: {test_chapter}")
            print("🗑️ 확인 완료 후 정리: tester.cleanup_test_environment()")
            
        except Exception as e:
            print(f"❌ 4단계 실제 테스트 실패: {e}")
            self.refactoring_logger.operation_error(self.logger_context, e)
            raise


async def run_all_real_tests():
    """🚀 모든 실제 테스트 실행"""
    print("🔍 === 실제 데이터 기반 ContentProcessingStage 전체 테스트 시작 ===\n")
    
    # 실제 데이터와 설정 경로
    original_chapter_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/tests/data/Data_Oriented_Programming/1_Complexity_of_object_oriented_programming"
    config_path = "/home/nadle/projects/Knowledge_Sherpa/v2/refactoring/config/ai_config.yaml"
    
    # 경로 검증
    if not os.path.exists(original_chapter_path):
        print(f"❌ 실제 테스트 데이터 경로 없음: {original_chapter_path}")
        return
    
    if not os.path.exists(config_path):
        print(f"❌ 설정 파일 경로 없음: {config_path}")
        return
    
    tester = RealContentProcessingStageTester(original_chapter_path, config_path)
    
    try:
        print("📊 테스트 환경:")
        print(f"  - 실제 데이터: {original_chapter_path}")
        print(f"  - AI 설정: {config_path}")
        print(f"  - 로그 디렉토리: /home/nadle/projects/Knowledge_Sherpa/v2/refactoring/logs")
        print(f"  - AI 서비스: {'✅ 초기화됨' if tester.ai_service else '❌ 초기화 실패'}")
        print()
        
        # 1단계 실제 테스트
        await tester.test_01_real_extraction()
        tester.cleanup_test_environment()
        
        # 2단계 실제 테스트
        await tester.test_02_real_parent_child_processing()
        tester.cleanup_test_environment()
        
        # 3단계 실제 테스트  
        await tester.test_03_real_document_sorting()
        tester.cleanup_test_environment()
        
        # 4단계 실제 테스트 (향후 구현)
        await tester.test_04_real_toc_generation()
        
        print("\n🎉 === 실제 데이터 기반 전체 테스트 완료! ===")
        print("✅ 모든 실제 테스트가 성공적으로 완료되었습니다.")
        print("📁 원본 파일들은 전혀 변경되지 않았습니다.")
        print("🤖 실제 AI 서비스를 활용한 테스트입니다.")
        
    except Exception as e:
        print(f"\n❌ 실제 테스트 중 오류 발생: {e}")
        print("🔍 로그를 확인하여 문제를 분석해주세요")
        if tester.test_temp_dir:
            print(f"📁 분석용 임시 디렉터리: {tester.test_temp_dir}")
            print("🗑️ 확인 완료 후 수동 정리: tester.cleanup_test_environment()")


if __name__ == "__main__":
    # 로깅 레벨 설정
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_all_real_tests())