# 생성 시간: 2025-08-29 11:39:28 KST  
# 핵심 내용: 단일 부모 노드 업데이트 테스트 및 변경 전후 내용 확인 시스템
# 상세 내용:
#   - main() 함수 (40-80): 메인 테스트 실행 함수 - 노드 선택 및 처리
#   - test_single_parent_node() 함수 (90-140): 단일 부모 노드 업데이트 테스트
#   - display_update_history() 함수 (150-200): 업데이트 히스토리 파일 내용 출력
#   - find_update_files() 함수 (210-250): 특정 노드의 업데이트 파일 검색
# 상태: active  
# 주소: test_single_node
# 참조: unified_node_processor_v2.py

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

# 현재 파일의 디렉토리를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent))

from unified_node_processor_v2 import UnifiedNodeProcessor, NodeInfo


def setup_logging():
    """테스트용 로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


async def test_single_parent_node(node_id: int = None, node_title: str = None) -> bool:
    """단일 부모 노드 업데이트 테스트"""
    print(f"🔥 단일 부모 노드 업데이트 테스트 시작")
    print(f"📋 테스트 대상: ID={node_id}, Title={node_title}")
    
    try:
        # 프로세서 초기화
        processor = UnifiedNodeProcessor('./test_config.yaml')
        
        # 모든 노드 정보 로드
        nodes = await processor.doc_manager.load_nodes_info()
        
        # 테스트 대상 노드 찾기
        target_node = None
        if node_id is not None:
            target_node = next((node for node in nodes if node.id == node_id), None)
        elif node_title is not None:
            target_node = next((node for node in nodes if node_title.lower() in node.title.lower()), None)
        
        if not target_node:
            print(f"❌ 테스트 대상 노드를 찾을 수 없음: ID={node_id}, Title={node_title}")
            return False
        
        # 부모 노드인지 확인
        if not target_node.children_ids:
            print(f"❌ 리프 노드는 부모 업데이트 테스트 불가: {target_node.title}")
            return False
        
        print(f"✅ 테스트 대상 노드 발견: {target_node.title} (ID: {target_node.id})")
        print(f"📊 자식 노드 수: {len(target_node.children_ids)}")
        
        # 업데이트 히스토리 디렉토리 확인
        update_history_dir = Path(processor.config.get('update_history_dir', './update_history'))
        print(f"📁 업데이트 히스토리 저장 경로: {update_history_dir}")
        
        # 기존 히스토리 파일 수 확인
        existing_files = list(update_history_dir.glob(f"*{target_node.title.replace(' ', '_')}*")) if update_history_dir.exists() else []
        print(f"📝 기존 히스토리 파일 수: {len(existing_files)}")
        
        # 노드 처리 실행
        print(f"\n🚀 노드 처리 시작...")
        success = await processor._process_single_node(target_node)
        
        if success:
            print(f"✅ 노드 처리 성공: {target_node.title}")
            
            # 새로 생성된 히스토리 파일 확인
            new_files = list(update_history_dir.glob(f"*{target_node.title.replace(' ', '_')}*")) if update_history_dir.exists() else []
            created_files = [f for f in new_files if f not in existing_files]
            
            print(f"📈 새로 생성된 히스토리 파일 수: {len(created_files)}")
            
            # 생성된 히스토리 파일들 출력
            if created_files:
                print(f"\n📄 생성된 업데이트 히스토리 파일들:")
                for file_path in sorted(created_files, key=lambda x: x.stat().st_mtime):
                    print(f"  - {file_path.name}")
                    await display_update_history(file_path)
            else:
                print(f"⚠️ 새로운 히스토리 파일이 생성되지 않았음")
            
            return True
        else:
            print(f"❌ 노드 처리 실패: {target_node.title}")
            return False
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


async def display_update_history(file_path: Path, max_lines: int = 50):
    """업데이트 히스토리 파일 내용 출력"""
    try:
        print(f"\n{'='*80}")
        print(f"📄 파일: {file_path.name}")
        print(f"📅 생성 시간: {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        if len(lines) <= max_lines:
            print(content)
        else:
            # BEFORE_UPDATE와 AFTER_UPDATE 섹션을 찾아서 각각 일부만 출력
            before_start = None
            after_start = None
            
            for i, line in enumerate(lines):
                if '[BEFORE_UPDATE]' in line:
                    before_start = i
                elif '[AFTER_UPDATE]' in line:
                    after_start = i
            
            # 헤더 부분 출력
            header_end = before_start if before_start else 10
            print('\n'.join(lines[:header_end]))
            
            # BEFORE_UPDATE 부분 (처음 10줄만)
            if before_start:
                print('\n'.join(lines[before_start:before_start + min(15, len(lines) - before_start)]))
                if after_start and after_start - before_start > 15:
                    print(f"\n... ({after_start - before_start - 15} 줄 생략) ...")
            
            # AFTER_UPDATE 부분 (처음 10줄만)
            if after_start:
                print('\n'.join(lines[after_start:after_start + min(15, len(lines) - after_start)]))
                if len(lines) - after_start > 15:
                    print(f"\n... ({len(lines) - after_start - 15} 줄 생략) ...")
        
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"❌ 히스토리 파일 읽기 실패: {e}")


def find_update_files(node_title: str, update_history_dir: Path = None) -> List[Path]:
    """특정 노드의 업데이트 파일 검색"""
    if update_history_dir is None:
        update_history_dir = Path('./update_history')
    
    if not update_history_dir.exists():
        return []
    
    safe_title = node_title.replace(' ', '_').replace('/', '_')
    pattern = f"*{safe_title}*"
    
    return list(update_history_dir.glob(pattern))


async def list_available_parent_nodes() -> List[NodeInfo]:
    """사용 가능한 부모 노드들 목록 출력"""
    try:
        processor = UnifiedNodeProcessor('./test_config.yaml')
        nodes = await processor.doc_manager.load_nodes_info()
        
        # 부모 노드들만 필터링
        parent_nodes = [node for node in nodes if node.children_ids]
        
        print(f"\n📊 사용 가능한 부모 노드들 ({len(parent_nodes)}개):")
        print(f"{'ID':<4} {'레벨':<4} {'자식수':<6} {'제목'}")
        print(f"{'-'*60}")
        
        for node in sorted(parent_nodes, key=lambda x: (x.level, x.id)):
            print(f"{node.id:<4} {node.level:<4} {len(node.children_ids):<6} {node.title}")
        
        return parent_nodes
        
    except Exception as e:
        print(f"❌ 노드 목록 로드 실패: {e}")
        return []


async def main():
    """메인 테스트 함수"""
    setup_logging()
    
    print("🧪 단일 부모 노드 업데이트 테스트 도구")
    print("="*60)
    
    # 사용 가능한 부모 노드들 표시
    parent_nodes = await list_available_parent_nodes()
    
    if not parent_nodes:
        print("❌ 테스트 가능한 부모 노드가 없습니다.")
        return
    
    print("\n🎯 테스트 방법:")
    print("1. 특정 ID로 테스트: python test_single_node.py --id <노드ID>")
    print("2. 제목 검색으로 테스트: python test_single_node.py --title <제목키워드>")
    print("3. 대화형 모드: python test_single_node.py")
    
    # 명령행 인수 처리
    if len(sys.argv) > 1:
        if '--id' in sys.argv:
            try:
                idx = sys.argv.index('--id')
                node_id = int(sys.argv[idx + 1])
                await test_single_parent_node(node_id=node_id)
            except (IndexError, ValueError) as e:
                print(f"❌ ID 인수 오류: {e}")
        elif '--title' in sys.argv:
            try:
                idx = sys.argv.index('--title')
                node_title = sys.argv[idx + 1]
                await test_single_parent_node(node_title=node_title)
            except IndexError as e:
                print(f"❌ 제목 인수 오류: {e}")
    else:
        # 대화형 모드
        print("\n🔍 대화형 모드")
        try:
            user_input = input("노드 ID 입력 (또는 'q' 종료): ").strip()
            if user_input.lower() == 'q':
                print("👋 테스트 종료")
                return
            
            node_id = int(user_input)
            await test_single_parent_node(node_id=node_id)
            
        except ValueError:
            print("❌ 올바른 숫자를 입력하세요.")
        except KeyboardInterrupt:
            print("\n👋 테스트 중단")


if __name__ == "__main__":
    asyncio.run(main())