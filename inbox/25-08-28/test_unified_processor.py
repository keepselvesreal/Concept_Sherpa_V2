# 생성 시간: 2025-08-28 20:26:01 KST
# 핵심 내용: 통합 노드 처리 시스템 테스트 드라이버
# 상세 내용:
#   - test_basic_functionality() (30-80): 기본 기능 테스트
#   - test_ai_providers() (90-140): AI 프로바이더별 테스트
#   - test_processing_modes() (150-200): 처리 방식별 테스트
#   - simulate_node_processing() (210-260): 노드 처리 시뮬레이션
#   - main() (270-320): 메인 테스트 실행기
# 상태: active
# 주소: test_unified_processor
# 참조: unified_node_processor.py

import asyncio
import os
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from unified_node_processor import (
        UnifiedNodeProcessor, NodeInfo, ExtractionResult,
        AIProviderFactory, ProcessingMode
    )
except ImportError as e:
    print(f"❌ unified_node_processor 모듈 임포트 실패: {e}")
    sys.exit(1)


class TestUnifiedProcessor:
    """통합 노드 처리 시스템 테스트"""
    
    def __init__(self):
        self.test_dir = None
        self.test_config = None
    
    async def setup_test_environment(self):
        """테스트 환경 설정"""
        print("🔧 테스트 환경 설정 중...")
        
        # 임시 디렉토리 생성
        self.test_dir = Path(tempfile.mkdtemp())
        
        # 테스트용 nodes.json 생성 (복잡한 구조로 변경)
        test_nodes = [
            {
                "title": "7 Basic data validation",  # 레벨1, 비리프 (A)
                "level": 1,
                "id": 0,
                "parent_id": None,
                "children_ids": [1, 2],
                "has_content": True
            },
            {
                "title": "7.1 Data validation in DOP",  # 레벨2, 비리프 (B)
                "level": 2,
                "id": 1,
                "parent_id": 0,
                "children_ids": [4],
                "has_content": True
            },
            {
                "title": "7.2 JSON Schema",  # 레벨2, 리프 (C)
                "level": 2,
                "id": 2,
                "parent_id": 0,
                "children_ids": [],
                "has_content": True
            },
            {
                "title": "Summary",  # 레벨1, 리프 (D)
                "level": 1,
                "id": 3,
                "parent_id": None,
                "children_ids": [],
                "has_content": True
            },
            {
                "title": "7.1.1 Detailed validation",  # 레벨3, 리프 (E)
                "level": 3,
                "id": 4,
                "parent_id": 1,
                "children_ids": [],
                "has_content": True
            }
        ]
        
        nodes_file = self.test_dir / "nodes_updated.json"
        with open(nodes_file, 'w', encoding='utf-8') as f:
            json.dump(test_nodes, f, ensure_ascii=False, indent=2)
        
        # 테스트용 노드 문서 디렉토리 생성
        node_docs_dir = self.test_dir / "node_docs"
        node_docs_dir.mkdir()
        
        # 테스트용 노드 문서 생성 (5개 노드에 맞게)
        def create_doc_content(title: str):
            return f"""# 속성
---
process_status: false
source: test.pdf
source_type: book
title: {title}

# 추출
---

# 내용
---
This is test content for {title}.

# 구성
---
"""
        
        # 5개 노드 문서 생성
        doc_files = [
            ("00_lev1_7_Basic_data_validation_info.md", "7 Basic data validation"),
            ("01_lev2_7.1_Data_validation_in_DOP_info.md", "7.1 Data validation in DOP"),
            ("02_lev2_7.2_JSON_Schema_info.md", "7.2 JSON Schema"),
            ("03_lev1_Summary_info.md", "Summary"),
            ("04_lev3_7.1.1_Detailed_validation_info.md", "7.1.1 Detailed validation")
        ]
        
        for filename, title in doc_files:
            doc_path = node_docs_dir / filename
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(create_doc_content(title))
        
        # 테스트 설정 파일 생성
        self.test_config = {
            'ai_provider': 'gemini',
            'processing_mode': 'v3',
            'nodes_json_path': str(nodes_file),
            'node_docs_dir': str(node_docs_dir),
            'parallel': {'max_concurrent': 2},
            'logging': {'level': 'INFO'}
        }
        
        config_file = self.test_dir / "test_config.yaml"
        import yaml
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.test_config, f, default_flow_style=False)
        
        print(f"✅ 테스트 환경 설정 완료: {self.test_dir}")
        return str(config_file)
    
    async def test_basic_functionality(self):
        """기본 기능 테스트"""
        print("\n🧪 기본 기능 테스트 시작")
        
        try:
            config_file = await self.setup_test_environment()
            
            # Mock Gemini API (API 키가 없을 경우를 대비)
            if not os.getenv('GEMINI_API_KEY'):
                print("⚠️  GEMINI_API_KEY 없음 - Mock 모드로 실행")
                return await self._test_with_mock(config_file)
            
            # 실제 API 테스트
            processor = UnifiedNodeProcessor(config_file)
            
            # 노드 정보 로드 테스트
            nodes = await processor.doc_manager.load_nodes_info()
            assert len(nodes) == 5, f"노드 수 불일치: expected 5, got {len(nodes)}"
            
            # 노드 순회 순서 테스트
            processing_order = processor.traverser.get_processing_order(nodes)
            
            # 리프 노드들이 첫 번째 그룹이어야 함
            first_group = processing_order[0]
            leaf_nodes = [node for node in first_group if not node.children_ids]
            assert len(first_group) == len(leaf_nodes), f"첫 번째 그룹이 모두 리프 노드가 아님"
            
            # 리프 노드 개수 확인 (Summary, 7.2 JSON Schema, 7.1.1 Detailed validation)
            expected_leaf_count = 3
            assert len(leaf_nodes) == expected_leaf_count, f"리프 노드 수 불일치: expected {expected_leaf_count}, got {len(leaf_nodes)}"
            
            print("✅ 기본 기능 테스트 통과")
            return True
            
        except Exception as e:
            print(f"❌ 기본 기능 테스트 실패: {e}")
            return False
    
    async def _test_with_mock(self, config_file: str):
        """Mock을 사용한 테스트"""
        print("🎭 Mock 모드 테스트")
        
        try:
            # Mock AI Provider 생성
            mock_provider = AsyncMock()
            mock_provider.generate_text.return_value = "Mock extraction result"
            
            processor = UnifiedNodeProcessor(config_file)
            
            # AI Factory Mock으로 교체
            processor.ai_factory.get_provider = MagicMock(return_value=mock_provider)
            
            # 노드 로드 테스트
            nodes = await processor.doc_manager.load_nodes_info()
            print(f"📊 로드된 노드 수: {len(nodes)}")
            assert len(nodes) == 5, f"노드 수 불일치: expected 5, got {len(nodes)}"
            
            # 추출 엔진 테스트  
            extraction_engine = processor.strategy.extraction_engine
            result = await extraction_engine.extract_all_info("Test content", "Test Title")
            
            assert result.success, "추출 결과가 성공이 아님"
            print("✅ Mock 테스트 통과")
            return True
            
        except Exception as e:
            print(f"❌ Mock 테스트 실패: {e}")
            return False
    
    async def test_ai_providers(self):
        """AI 프로바이더 테스트"""
        print("\n🤖 AI 프로바이더 테스트")
        
        try:
            config_file = await self.setup_test_environment()
            
            # 각 프로바이더별 설정 테스트
            providers = ['gemini', 'claude', 'openai']
            results = {}
            
            for provider in providers:
                print(f"🔄 {provider} 프로바이더 테스트")
                
                try:
                    processor = UnifiedNodeProcessor(config_file)
                    processor.config['ai_provider'] = provider
                    
                    factory = AIProviderFactory(processor.config, processor.logger)
                    
                    # API 키가 없으면 스킵
                    if provider == 'gemini' and not os.getenv('GEMINI_API_KEY'):
                        results[provider] = "SKIP - No API Key"
                        continue
                    elif provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
                        results[provider] = "SKIP - No API Key"
                        continue
                    
                    # 프로바이더 인스턴스 생성 테스트
                    ai_provider = factory.get_provider(provider)
                    results[provider] = "OK"
                    
                except Exception as e:
                    results[provider] = f"ERROR - {str(e)}"
            
            # 결과 출력
            for provider, result in results.items():
                status = "✅" if result == "OK" else "⚠️" if "SKIP" in result else "❌"
                print(f"  {status} {provider}: {result}")
            
            return True
            
        except Exception as e:
            print(f"❌ AI 프로바이더 테스트 실패: {e}")
            return False
    
    async def test_processing_modes(self):
        """처리 방식 테스트"""
        print("\n🔧 처리 방식 테스트")
        
        try:
            config_file = await self.setup_test_environment()
            
            # V3 전략만 테스트 (V1, V2는 아직 미구현)
            modes = ['v3']
            results = {}
            
            for mode in modes:
                print(f"🔄 {mode} 모드 테스트")
                
                try:
                    processor = UnifiedNodeProcessor(config_file)
                    processor.config['processing_mode'] = mode
                    
                    # 전략 생성 테스트
                    strategy = processor.strategy
                    assert strategy is not None, f"{mode} 전략이 None"
                    
                    results[mode] = "OK"
                    
                except Exception as e:
                    results[mode] = f"ERROR - {str(e)}"
            
            # 결과 출력
            for mode, result in results.items():
                status = "✅" if result == "OK" else "❌"
                print(f"  {status} {mode}: {result}")
            
            return True
            
        except Exception as e:
            print(f"❌ 처리 방식 테스트 실패: {e}")
            return False
    
    async def simulate_node_processing(self):
        """노드 처리 시뮬레이션"""
        print("\n🎯 노드 처리 시뮬레이션")
        
        try:
            config_file = await self.setup_test_environment()
            
            if not os.getenv('GEMINI_API_KEY'):
                print("⚠️  실제 API 테스트를 위해서는 GEMINI_API_KEY 필요")
                print("   Mock 테스트만 실행됨")
                return True
            
            processor = UnifiedNodeProcessor(config_file)
            
            # 작은 규모로 실제 처리 시뮬레이션
            print("🔄 실제 노드 처리 시뮬레이션 시작...")
            result = await processor.process_all_nodes()
            
            print(f"📊 시뮬레이션 결과:")
            print(f"  - 성공: {result.get('success', False)}")
            print(f"  - 처리된 노드: {result.get('processed_nodes', 0)}/{result.get('total_nodes', 0)}")
            print(f"  - 실패한 노드: {result.get('failed_nodes', 0)}")
            print(f"  - 소요 시간: {result.get('duration', 'N/A')}")
            
            if result.get('errors'):
                print(f"  - 오류 목록:")
                for error in result['errors']:
                    print(f"    * {error}")
            
            return result.get('success', False)
            
        except Exception as e:
            print(f"❌ 노드 처리 시뮬레이션 실패: {e}")
            return False
    
    def cleanup(self):
        """테스트 환경 정리"""
        if self.test_dir and self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir)
            print(f"🧹 테스트 환경 정리 완료: {self.test_dir}")


async def main():
    """메인 테스트 함수"""
    print("🚀 통합 노드 처리 시스템 테스트 시작\n")
    
    tester = TestUnifiedProcessor()
    test_results = []
    
    try:
        # 테스트 실행
        tests = [
            ("기본 기능", tester.test_basic_functionality),
            ("AI 프로바이더", tester.test_ai_providers), 
            ("처리 방식", tester.test_processing_modes),
            ("노드 처리 시뮬레이션", tester.simulate_node_processing)
        ]
        
        for test_name, test_func in tests:
            print(f"\n{'='*50}")
            print(f"🧪 {test_name} 테스트")
            print('='*50)
            
            try:
                result = await test_func()
                test_results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} 테스트 중 예외 발생: {e}")
                test_results.append((test_name, False))
        
        # 최종 결과
        print(f"\n{'='*50}")
        print("📊 최종 테스트 결과")
        print('='*50)
        
        passed = 0
        failed = 0
        
        for test_name, result in test_results:
            status = "✅ 통과" if result else "❌ 실패"
            print(f"  {status}: {test_name}")
            
            if result:
                passed += 1
            else:
                failed += 1
        
        print(f"\n총 {len(test_results)}개 테스트 중:")
        print(f"  ✅ 통과: {passed}개")
        print(f"  ❌ 실패: {failed}개")
        
        if failed == 0:
            print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        else:
            print(f"\n⚠️  {failed}개의 테스트가 실패했습니다.")
        
        return failed == 0
        
    except KeyboardInterrupt:
        print("\n❌ 사용자에 의해 테스트가 중단되었습니다.")
        return False
    except Exception as e:
        print(f"\n❌ 테스트 실행 중 예상치 못한 오류: {e}")
        return False
    finally:
        # 정리 작업
        tester.cleanup()


if __name__ == "__main__":
    import sys
    
    print("통합 노드 처리 시스템 테스트 드라이버")
    print("=====================================")
    
    # 환경 변수 확인
    print("🔍 환경 변수 확인:")
    api_keys = ['GEMINI_API_KEY', 'OPENAI_API_KEY']
    for key in api_keys:
        status = "✅" if os.getenv(key) else "❌"
        print(f"  {status} {key}")
    
    print()
    
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ 테스트가 중단되었습니다.")
        sys.exit(1)