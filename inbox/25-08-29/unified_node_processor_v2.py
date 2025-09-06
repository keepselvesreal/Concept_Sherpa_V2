# 생성 시간: 2025-08-29 10:49:48 KST
# 핵심 내용: 통합 노드 정보 문서의 추출 섹션 자동 생성/업데이트 시스템 - 구성 노드 기반 정보 타입별 업데이트 방식
# 상세 내용:
#   - UnifiedNodeProcessor 클래스 (50-120): 메인 처리 시스템 및 작업 조율
#   - AIProviderFactory 클래스 (130-200): AI 프로바이더 추상화 팩토리
#   - ProcessingStrategy 클래스 (210-280): 작업 방식 전략 패턴 (v1,v2,v3)
#   - NodeDocumentManager 클래스 (290-360): 노드 문서 파싱 및 관리  
#   - ExtractionEngine 클래스 (370-450): 5개 정보 타입 병렬 추출 엔진
#   - UpdateEngine 클래스 (460-540): 구성 노드 기반 정보 타입별 업데이트 엔진
#   - NodeTraverser 클래스 (550-620): bottom-up 노드 순회 관리
#   - ProgressTracker 클래스 (630-700): 진행률 추적 및 오류 복구
#   - DebugManager 클래스 (710-780): 디버깅용 기준/참조 문서 저장
# 상태: active
# 주소: unified_node_processor_v2
# 참조: unified_node_processor.py

import asyncio
import json
import logging
import os
import yaml
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

# .env 파일 로딩
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv가 없으면 무시

# AI 프로바이더 임포트 (조건부)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from claude_code_sdk import query as claude_query, ClaudeCodeOptions
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ProcessingMode(Enum):
    """처리 모드"""
    V1 = "v1"
    V2 = "v2" 
    V3 = "v3"  # 추출→업데이트 방식


class AIProvider(Enum):
    """AI 프로바이더"""
    GEMINI = "gemini"
    CLAUDE = "claude"
    OPENAI = "openai"


@dataclass
class NodeInfo:
    """노드 정보"""
    id: int
    title: str
    level: int
    parent_id: Optional[int]
    children_ids: List[int]
    has_content: bool
    document_path: Optional[str] = None
    process_status: bool = False


@dataclass
class ExtractionResult:
    """추출 결과"""
    core_content: str = ""
    detailed_core_content: str = ""
    detailed_content: str = ""  # 새로 추가된 정보 타입
    main_topics: str = ""
    sub_topics: str = ""
    success: bool = False
    error: Optional[str] = None


@dataclass
class ProcessingStatus:
    """처리 상태"""
    total_nodes: int = 0
    processed_nodes: int = 0
    failed_nodes: int = 0
    current_node: Optional[str] = None
    start_time: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)


class DebugManager:
    """디버깅용 기준/참조 문서 저장 관리자"""
    
    def __init__(self, debug_dir: str = "./25-08-29"):
        self.debug_dir = Path(debug_dir)
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.DebugManager")
    
    async def save_update_documents(self, node_title: str, section_type: str, 
                                  base_document: str, reference_documents: List[str]):
        """정보 타입별 업데이트 시 기준/참조 문서 저장"""
        try:
            # 노드명과 섹션 타입으로 폴더 생성
            node_dir = self.debug_dir / f"{node_title}_{section_type}_{datetime.now().strftime('%H%M%S')}"
            node_dir.mkdir(parents=True, exist_ok=True)
            
            # 기준 문서 저장
            base_file = node_dir / "base_document.md"
            with open(base_file, 'w', encoding='utf-8') as f:
                f.write(f"# 기준 문서 - {node_title} ({section_type})\n\n")
                f.write(base_document)
            
            # 참조 문서들 저장
            for i, ref_doc in enumerate(reference_documents, 1):
                if ref_doc.strip():
                    ref_file = node_dir / f"reference_document_{i}.md"
                    with open(ref_file, 'w', encoding='utf-8') as f:
                        f.write(f"# 참조 문서 {i} - {node_title} ({section_type})\n\n")
                        f.write(ref_doc)
            
            self.logger.info(f"📁 디버깅 문서 저장: {node_dir}")
            
        except Exception as e:
            self.logger.error(f"❌ 디버깅 문서 저장 실패: {e}")


class UpdateLogger:
    """업데이트 히스토리 로깅 시스템 - 원시 데이터 변경 전후 추적"""
    
    def __init__(self, log_dir: str = "./update_history"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"{__name__}.UpdateLogger")
    
    
    def _sanitize_filename(self, filename: str) -> str:
        """파일명에서 특수문자 제거"""
        import re
        # 파일명에 사용할 수 없는 문자들을 언더스코어로 대체
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 연속된 언더스코어 제거 및 공백을 언더스코어로 변경
        safe_name = re.sub(r'_+', '_', safe_name.replace(' ', '_'))
        # 최대 50자로 제한
        return safe_name[:50]
    
    

    def _format_simple_extraction_log(self, system_prompt: str, prompt: str, result: str) -> str:
        """간단한 추출 로그 형식 생성 - 프롬프트와 결과만"""
        return f"""[SYSTEM_PROMPT]
{system_prompt}

[PROMPT]
{prompt}

[추출 결과]
{result}"""

    async def log_update_with_prompt(self, node_title: str, info_type: str,
                                    prompt: str, system_prompt: str, 
                                    update_content: str,
                                    operation_type: str = "parent_update"):
        """업데이트 작업 시 프롬프트와 결과 저장"""
        try:
            # 시간 형식: HHMM
            time_stamp = datetime.now().strftime('%H%M')
            
            # 파일명 생성: update_{정보유형}_{title}_{HHMM}.txt
            safe_title = self._sanitize_filename(node_title)
            filename = f"update_{info_type}_{safe_title}_{time_stamp}.txt"
            log_file = self.log_dir / filename
            
            # 로그 내용 구성 (프롬프트와 업데이트 내용만 포함)
            log_content = self._format_simple_update_log(
                system_prompt, prompt, update_content
            )
            
            # 파일 저장
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.logger.info(f"📝 업데이트 히스토리 저장: {filename}")
            return str(log_file)
            
        except Exception as e:
            self.logger.error(f"❌ 업데이트 히스토리 저장 실패: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _format_simple_update_log(self, system_prompt: str, prompt: str, update_content: str) -> str:
        """간단한 업데이트 로그 형식 생성 - 프롬프트와 업데이트 내용만"""
        return f"""[SYSTEM_PROMPT]
{system_prompt}

[PROMPT]
{prompt}

[업데이트 내용]
{update_content}"""
    
    
    async def log_extraction_with_prompt(self, node_title: str, info_type: str,
                                        prompt: str, system_prompt: str,
                                        before_data: str, after_data: str,
                                        operation_type: str = "leaf_extraction"):
        """프롬프트와 함께 정보 유형별 추출 결과 로깅"""
        try:
            # 시간 형식: HHMM
            time_stamp = datetime.now().strftime('%H%M')
            
            # 파일명 생성: extraction_{정보유형}_{title}_{HHMM}.txt
            safe_title = self._sanitize_filename(node_title)
            filename = f"extraction_{info_type}_{safe_title}_{time_stamp}.txt"
            log_file = self.log_dir / filename
            
            # 로그 내용 구성 (프롬프트와 추출 결과만 포함)
            log_content = self._format_simple_extraction_log(
                system_prompt, prompt, after_data
            )
            
            # 파일 저장
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.logger.info(f"📝 정보 유형별 추출 히스토리 저장: {filename}")
            return str(log_file)
            
        except Exception as e:
            self.logger.error(f"❌ 정보 유형별 추출 히스토리 저장 실패: {e}")
            return None


class UnifiedNodeProcessor:
    """통합 노드 정보 문서 처리 시스템"""
    
    def __init__(self, config_path: str = "./config.yaml"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        
        # 컴포넌트 초기화
        self.ai_factory = AIProviderFactory(self.config, self.logger)
        self.strategy = ProcessingStrategyFactory.create_strategy(
            ProcessingMode(self.config.get('processing_mode', 'v3')),
            self.ai_factory,
            self.logger
        )
        self.doc_manager = NodeDocumentManager(self.config, self.logger)
        self.traverser = NodeTraverser(self.logger)
        self.progress = ProgressTracker(self.logger)
        self.debug_manager = DebugManager(self.config.get('debug_dir', './25-08-29'))
        self.update_logger = UpdateLogger(self.config.get('update_history_dir', './update_history'))
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # 기본 설정
            return {
                'ai_provider': 'gemini',
                'processing_mode': 'v3',
                'nodes_json_path': './process/nodes_updated.json',
                'node_docs_dir': './process/node_docs',
                'debug_dir': './25-08-29',
                'update_history_dir': './update_history',
                'parallel': {'max_concurrent': 5},
                'logging': {'level': 'INFO'}
            }
    
    def _setup_logging(self) -> logging.Logger:
        """로깅 설정"""
        logger = logging.getLogger(__name__)
        level = getattr(logging, self.config.get('logging', {}).get('level', 'INFO'))
        logger.setLevel(level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    async def process_all_nodes(self) -> Dict[str, Any]:
        """전체 노드 처리 메인 함수"""
        self.logger.info("🚀 통합 노드 처리 시작")
        self.progress.start_processing()
        
        try:
            # 1. 노드 정보 로드
            nodes = await self.doc_manager.load_nodes_info()
            self.progress.set_total_nodes(len(nodes))
            
            # 2. 처리 순서 결정 (bottom-up)
            processing_order = self.traverser.get_processing_order(nodes)
            
            # 3. 각 레벨별 처리
            for level_nodes in processing_order:
                await self._process_level_nodes(level_nodes)
            
            # 4. 결과 반환
            return self.progress.get_final_result()
            
        except Exception as e:
            self.logger.error(f"❌ 전체 처리 중 오류: {e}")
            self.progress.add_error(str(e))
            return self.progress.get_final_result()
    
    async def _process_level_nodes(self, nodes: List[NodeInfo]):
        """단계별 노드 처리 (process_status=false인 노드만)"""
        # 단계 정보 결정
        if not nodes:
            return
            
        if not nodes[0].children_ids:
            stage_name = "리프 노드"
        else:
            stage_name = f"레벨 {nodes[0].level}"
        
        # process_status별 노드 분류
        pending_nodes = [node for node in nodes if not node.process_status]
        completed_nodes = [node for node in nodes if node.process_status]
        
        self.logger.info(f"📊 {stage_name} 처리 시작: 총 {len(nodes)}개 (대기 {len(pending_nodes)}개, 완료 {len(completed_nodes)}개)")
        
        # 이미 완료된 노드들 로그
        for node in completed_nodes:
            self.logger.info(f"⏭️  스킵: {node.title} (이미 완료)")
        
        # 대기 중인 노드가 없으면 종료
        if not pending_nodes:
            self.logger.info(f"✅ {stage_name}: 처리할 노드 없음")
            return
        
        # 순차 처리
        processed_nodes = []
        for node in pending_nodes:
            try:
                result = await self._process_single_node(node)
                if result:
                    self.progress.mark_completed(node.title)
                    processed_nodes.append(node.title)
                else:
                    self.progress.mark_failed(node.title, "처리 실패")
            except Exception as e:
                self.logger.error(f"❌ 노드 처리 실패: {node.title} - {e}")
                self.progress.mark_failed(node.title, str(e))
        
        self.logger.info(f"✅ {stage_name} 완료: {len(processed_nodes)}개 처리됨")
    
    async def _process_single_node(self, node: NodeInfo) -> bool:
        """단일 노드 처리"""
        self.progress.set_current_node(node.title)
        self.logger.info(f"🔄 처리 중: {node.title}")
        
        try:
            # 전략 패턴으로 처리
            success = await self.strategy.process_node(node, self.doc_manager, self.debug_manager, self.update_logger)
            
            if success:
                # process_status 업데이트
                await self.doc_manager.update_process_status(node, True)
                self.logger.info(f"✅ 완료: {node.title}")
            else:
                self.logger.error(f"❌ 실패: {node.title}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"❌ 노드 처리 중 오류: {node.title} - {e}")
            self.progress.add_error(f"{node.title}: {str(e)}")
            return False


class AIProviderFactory:
    """AI 프로바이더 추상화 팩토리"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self._providers = {}
    
    def get_provider(self, provider_type: str = None) -> 'BaseAIProvider':
        """프로바이더 인스턴스 반환"""
        if not provider_type:
            provider_type = self.config.get('ai_provider', 'gemini')
        
        if provider_type not in self._providers:
            self._providers[provider_type] = self._create_provider(provider_type)
        
        return self._providers[provider_type]
    
    def _create_provider(self, provider_type: str) -> 'BaseAIProvider':
        """프로바이더 인스턴스 생성"""
        if provider_type == 'gemini' and GEMINI_AVAILABLE:
            return GeminiProvider(self.config, self.logger)
        elif provider_type == 'claude' and CLAUDE_AVAILABLE:
            return ClaudeProvider(self.config, self.logger)
        elif provider_type == 'openai' and OPENAI_AVAILABLE:
            return OpenAIProvider(self.config, self.logger)
        else:
            raise ValueError(f"지원하지 않는 AI 프로바이더: {provider_type}")


class BaseAIProvider(ABC):
    """AI 프로바이더 기본 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
    
    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """텍스트 생성"""
        pass


class GeminiProvider(BaseAIProvider):
    """Gemini API 프로바이더"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        
        if not GEMINI_AVAILABLE:
            raise ImportError("Gemini API 사용을 위해 google-generativeai 설치 필요")
        
        # API 키 설정
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않음")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            self.config.get('providers', {}).get('gemini', {}).get('model', 'models/gemini-2.0-flash-lite')
        )
    
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """Gemini로 텍스트 생성"""
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = await asyncio.to_thread(self.model.generate_content, full_prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Gemini API 오류: {e}")
            raise


class ClaudeProvider(BaseAIProvider):
    """Claude SDK 프로바이더"""
    
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """Claude로 텍스트 생성"""
        try:
            messages = []
            options = ClaudeCodeOptions(
                max_turns=1,
                system_prompt=system_prompt or "텍스트 분석 전문가",
                allowed_tools=[]
            )
            
            async for message in claude_query(prompt=prompt, options=options):
                messages.append(message)
            
            return self._extract_content_from_messages(messages)
        except Exception as e:
            self.logger.error(f"Claude SDK 오류: {e}")
            raise
    
    def _extract_content_from_messages(self, messages: List) -> str:
        """메시지에서 텍스트 추출"""
        content = ""
        for message in messages:
            if hasattr(message, 'content'):
                if isinstance(message.content, list):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            content += block.text
                else:
                    content += str(message.content)
        return content.strip()


class OpenAIProvider(BaseAIProvider):
    """OpenAI API 프로바이더"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        super().__init__(config, logger)
        
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI API 사용을 위해 openai 설치 필요")
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않음")
        
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = self.config.get('providers', {}).get('openai', {}).get('model', 'gpt-4')
    
    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """OpenAI로 텍스트 생성"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.config.get('providers', {}).get('openai', {}).get('temperature', 0.7)
            )
            
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI API 오류: {e}")
            raise


class ProcessingStrategy(ABC):
    """처리 전략 기본 클래스"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
    
    @abstractmethod
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager', 
                          debug_manager: DebugManager = None, 
                          update_logger: 'UpdateLogger' = None) -> bool:
        """노드 처리"""
        pass


class V3Strategy(ProcessingStrategy):
    """V3 전략: 추출→업데이트 방식"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        super().__init__(ai_factory, logger)
        self.extraction_engine = ExtractionEngine(ai_factory, logger)
        self.update_engine = UpdateEngine(ai_factory, logger)
    
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager', 
                          debug_manager: DebugManager = None,
                          update_logger: 'UpdateLogger' = None) -> bool:
        """V3 방식으로 노드 처리"""
        try:
            # 1. 추출 작업
            content = await doc_manager.get_combined_content(node)
            extraction_result = await self.extraction_engine.extract_all_info(content, node.title, update_logger)
            
            if not extraction_result.success:
                return False
            
            # 2. 추출 섹션 업데이트
            await doc_manager.update_extraction_section(node, extraction_result, update_logger)
            
            # 3. 부모 노드가 아닌 경우 여기서 종료 (리프 노드)
            if not node.children_ids:
                return True
            
            # 4. 부모 노드인 경우 업데이트 작업 수행
            # 4-1. 구성 노드 추출 섹션들 로드
            composition_extractions = await doc_manager.get_composition_extractions(node)
            
            # 4-2. 정보 타입별로 부모 노드 업데이트
            updated_current = await self.update_engine.update_parent_extraction(
                extraction_result, composition_extractions, node.title, debug_manager, update_logger
            )
            await doc_manager.save_extraction_section(node, updated_current, update_logger)
            
            # 4-3. 구성 노드들 추출 섹션 업데이트  
            await self.update_engine.update_composition_extractions(
                node, updated_current, doc_manager, update_logger
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"V3 처리 중 오류: {node.title} - {e}")
            return False


class V1Strategy(ProcessingStrategy):
    """V1 전략: 기본 전략 (구현 예정)"""
    
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager', 
                          debug_manager: DebugManager = None,
                          update_logger: 'UpdateLogger' = None) -> bool:
        """V1 방식으로 노드 처리"""
        raise NotImplementedError("V1 전략은 아직 구현되지 않음")


class V2Strategy(ProcessingStrategy):
    """V2 전략: 향상된 전략 (구현 예정)"""
    
    async def process_node(self, node: NodeInfo, doc_manager: 'NodeDocumentManager', 
                          debug_manager: DebugManager = None,
                          update_logger: 'UpdateLogger' = None) -> bool:
        """V2 방식으로 노드 처리"""
        raise NotImplementedError("V2 전략은 아직 구현되지 않음")


class ProcessingStrategyFactory:
    """처리 전략 팩토리"""
    
    @staticmethod
    def create_strategy(mode: ProcessingMode, ai_factory: AIProviderFactory, 
                       logger: logging.Logger) -> ProcessingStrategy:
        """전략 인스턴스 생성"""
        if mode == ProcessingMode.V3:
            return V3Strategy(ai_factory, logger)
        elif mode == ProcessingMode.V1:
            return V1Strategy(ai_factory, logger)
        elif mode == ProcessingMode.V2:
            return V2Strategy(ai_factory, logger)
        else:
            raise ValueError(f"지원하지 않는 처리 모드: {mode}")


class NodeDocumentManager:
    """노드 문서 관리 클래스"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.nodes_json_path = Path(config.get('nodes_json_path', './process/nodes_updated.json'))
        self.node_docs_dir = Path(config.get('node_docs_dir', './process/node_docs'))
    
    async def load_nodes_info(self) -> List[NodeInfo]:
        """노드 정보 로드"""
        try:
            with open(self.nodes_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            nodes = []
            for item in data:
                node = NodeInfo(
                    id=item['id'],
                    title=item['title'],
                    level=item['level'],
                    parent_id=item.get('parent_id'),
                    children_ids=item.get('children_ids', []),
                    has_content=item.get('has_content', False)
                )
                
                # 문서 경로 설정
                doc_filename = self._get_doc_filename(node)
                node.document_path = str(self.node_docs_dir / doc_filename)
                
                # process_status 읽기
                node.process_status = await self._read_process_status(node)
                
                nodes.append(node)
            
            self.logger.info(f"✅ 노드 정보 로드 완료: {len(nodes)}개")
            return nodes
            
        except Exception as e:
            self.logger.error(f"❌ 노드 정보 로드 실패: {e}")
            raise
    
    def _get_doc_filename(self, node: NodeInfo) -> str:
        """노드 문서 파일명 생성"""
        # ID를 2자리로 포맷팅 + 레벨 + 제목
        title_clean = node.title.replace('/', '_').replace(' ', '_')
        return f"{node.id:02d}_lev{node.level}_{title_clean}_info.md"
    
    async def _read_process_status(self, node: NodeInfo) -> bool:
        """문서에서 process_status 읽기"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                return False
            
            with open(node.document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # YAML 헤더에서 process_status 찾기
            if content.startswith('# 속성\n---\n'):
                yaml_end = content.find('\n# 추출\n---')
                if yaml_end != -1:
                    yaml_content = content[len('# 속성\n---\n'):yaml_end]
                    try:
                        metadata = yaml.safe_load(yaml_content)
                        return metadata.get('process_status', False)
                    except yaml.YAMLError:
                        pass
            
            return False
            
        except Exception as e:
            self.logger.warning(f"process_status 읽기 실패: {node.title} - {e}")
            return False
    
    async def get_combined_content(self, node: NodeInfo) -> str:
        """노드의 결합된 내용 반환"""
        try:
            # 현재 노드의 내용 섹션 읽기
            current_content = await self._read_content_section(node)
            
            # 자식 노드가 없으면 현재 내용만 반환
            if not node.children_ids:
                return current_content
            
            # 부모 노드의 구성 섹션에서 자식 파일명들 읽기
            child_filenames = await self._read_composition_section(node)
            
            # 자식 노드들의 내용 섹션 결합
            combined = current_content
            for i, child_filename in enumerate(child_filenames, 1):
                child_path = str(self.node_docs_dir / child_filename)
                child_node = NodeInfo(id=i, title="", level=0, parent_id=None, children_ids=[], has_content=True)
                child_node.document_path = child_path
                child_content = await self._read_content_section(child_node)
                if child_content:
                    combined += f"\n\n=== 구성 노드 {i} ===\n{child_content}"
            
            return combined
            
        except Exception as e:
            self.logger.error(f"결합 내용 생성 실패: {node.title} - {e}")
            return ""
    
    async def _read_composition_section(self, node: NodeInfo) -> List[str]:
        """노드 문서의 구성 섹션에서 자식 파일명들 읽기"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                return []
            
            with open(node.document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # "# 구성" 섹션 찾기
            composition_start = content.find('\n# 구성\n---\n')
            if composition_start == -1:
                return []
            
            composition_start += len('\n# 구성\n---\n')
            composition_content = content[composition_start:].strip()
            
            # 파일명들 추출 (줄별로 분할하여 .md 파일만)
            filenames = []
            for line in composition_content.split('\n'):
                line = line.strip()
                if line and line.endswith('_info.md') and not line.startswith('#'):
                    filenames.append(line)
            
            return filenames
            
        except Exception as e:
            self.logger.error(f"구성 섹션 읽기 실패: {node.title} - {e}")
            return []
    
    async def get_composition_extractions(self, node: NodeInfo, doc_manager=None) -> List[str]:
        """구성 노드들의 추출 섹션 반환 (update_composition_extractions와 동일한 로직)"""
        extractions = []
        try:
            # doc_manager가 없으면 생성
            if not doc_manager:
                from unified_node_processor_v2 import NodeDocumentManager
                doc_manager = NodeDocumentManager(self.node_docs_dir, self.ai_factory, self.debug_manager, self.update_logger)
            
            # 1. 모든 자식 노드 정보 로드
            all_nodes = await doc_manager.load_nodes_info()
            composition_nodes = [node for node in all_nodes if node.id in node.children_ids]
            
            if not composition_nodes:
                self.logger.warning("⚠️ 구성 노드를 찾을 수 없음")
                return extractions
            
            self.logger.info(f"🔍 구성 노드 파일들: {len(composition_nodes)}개")
            
            # 2. 모든 구성 노드의 현재 추출 섹션 로드
            for i, child in enumerate(composition_nodes, 1):
                try:
                    child_doc_content = await doc_manager.load_node_document_content(child)
                    parsed_sections = doc_manager.parse_extraction_section(child_doc_content)
                    
                    # 추출 섹션을 하나의 문자열로 합치기 (모든 5개 정보 유형 포함)
                    extraction_parts = []
                    if parsed_sections.get('core_content'):
                        extraction_parts.append(f"## 핵심 내용\n{parsed_sections['core_content']}")
                    if parsed_sections.get('detailed_core_content'):
                        extraction_parts.append(f"## 상세 핵심 내용\n{parsed_sections['detailed_core_content']}")
                    if parsed_sections.get('detailed_content'):
                        extraction_parts.append(f"## 상세 정보\n{parsed_sections['detailed_content']}")
                    if parsed_sections.get('main_topics'):
                        extraction_parts.append(f"## 주요 화제\n{parsed_sections['main_topics']}")
                    if parsed_sections.get('sub_topics'):
                        extraction_parts.append(f"## 부차 화제\n{parsed_sections['sub_topics']}")
                    
                    extraction_section = '\n\n'.join(extraction_parts)
                    
                    # 추출 섹션이 비어있으면 오류
                    if not extraction_section.strip():
                        self.logger.error(f"❌ 구성 노드 {i} 추출 섹션이 비어있음: {child.title}")
                        extractions.append("")
                    else:
                        extractions.append(extraction_section)
                        self.logger.info(f"✅ 구성 노드 {i} 추출 완료: {child.title}")
                    
                except Exception as e:
                    self.logger.warning(f"구성 노드 추출 실패: {child.title if 'child' in locals() else 'Unknown'} - {e}")
                    extractions.append("")
            
            return extractions
            
        except Exception as e:
            self.logger.error(f"구성 노드들 추출 섹션 로드 실패: {node.title} - {e}")
            return []
    
    def _extract_section_content(self, content: str, section_marker: str) -> str:
        """문서에서 특정 섹션 내용만 추출"""
        # 파일 시작에서 섹션 찾기 (개행문자 없이)
        start_marker = f"{section_marker}\n---"
        start_pos = content.find(start_marker)
        if start_pos == -1:
            # 개행문자 포함한 패턴도 시도
            start_marker = f"\n{section_marker}\n---"
            start_pos = content.find(start_marker)
            if start_pos == -1:
                return ""
            start_pos += 1  # \n 문자 건너뛰기
        
        start_pos += len(start_marker.lstrip('\n')) + 1  # --- 다음 개행까지
        
        # 다음 섹션 찾기
        next_section = content.find('\n# ', start_pos)
        if next_section == -1:
            return content[start_pos:].strip()
        else:
            return content[start_pos:next_section].strip()
    
    async def _read_content_section(self, node: NodeInfo) -> str:
        """노드 문서의 내용 섹션 읽기"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                return ""
            
            with open(node.document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # "# 내용" 섹션 추출
            content_start = content.find('\n# 내용\n---\n')
            if content_start == -1:
                return ""
            
            content_start += len('\n# 내용\n---\n')
            
            # 다음 섹션(구성) 시작점 찾기
            next_section = content.find('\n# 구성\n---', content_start)
            if next_section == -1:
                return content[content_start:].strip()
            else:
                return content[content_start:next_section].strip()
                
        except Exception as e:
            self.logger.error(f"내용 섹션 읽기 실패: {node.title} - {e}")
            return ""
    
    async def update_extraction_section(self, node: NodeInfo, result: ExtractionResult,
                                       update_logger: 'UpdateLogger' = None):
        """추출 섹션 업데이트"""
        try:
            extraction_content = self._format_extraction_section(result)
            await self.save_extraction_section(node, extraction_content, update_logger)
        except Exception as e:
            self.logger.error(f"추출 섹션 업데이트 실패: {node.title} - {e}")
            raise
    
    def _format_extraction_section(self, result: ExtractionResult) -> str:
        """추출 결과를 섹션 형식으로 포맷팅"""
        sections = []
        
        if result.core_content:
            sections.append(f"## 핵심 내용\n{result.core_content}")
        
        if result.detailed_core_content:
            sections.append(f"## 상세 핵심 내용\n{result.detailed_core_content}")
        
        if result.detailed_content:
            sections.append(f"## 상세 정보\n{result.detailed_content}")
        
        if result.main_topics:
            sections.append(f"## 주요 화제\n{result.main_topics}")
        
        if result.sub_topics:
            sections.append(f"## 부차 화제\n{result.sub_topics}")
        
        return "\n\n".join(sections)
    
    async def save_extraction_section(self, node: NodeInfo, extraction_content: str, 
                                     update_logger: 'UpdateLogger' = None):
        """추출 섹션 저장"""
        try:
            if not node.document_path:
                return
            
            doc_path = Path(node.document_path)
            if not doc_path.exists():
                return
            
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 기존 추출 섹션 내용 추출 (로깅용)
            before_extraction = ""
            extraction_start = content.find('\n# 추출\n---\n')
            if extraction_start != -1:
                extraction_start += len('\n# 추출\n---\n')
                next_section = content.find('\n# 내용\n---', extraction_start)
                if next_section == -1:
                    before_extraction = content[extraction_start:].strip()
                else:
                    before_extraction = content[extraction_start:next_section].strip()
            
            # 추출 섹션 교체 (부모 노드처럼 --- 바로 다음에 삽입)
            if extraction_start == -1:
                return
            
            # extraction_content 앞뒤 공백 정리하고 개행문자 통일
            clean_extraction = extraction_content.strip()
            
            if next_section == -1:
                # 마지막 섹션
                new_content = content[:extraction_start] + clean_extraction + "\n"
            else:
                new_content = content[:extraction_start] + clean_extraction + "\n" + content[next_section:]
            

            
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.logger.info(f"💾 추출 섹션 저장 완료: {node.title}")
            
        except Exception as e:
            self.logger.error(f"추출 섹션 저장 실패: {node.title} - {e}")
            raise
    
    async def update_process_status(self, node: NodeInfo, status: bool):
        """process_status 업데이트"""
        try:
            if not node.document_path:
                return
            
            doc_path = Path(node.document_path)
            if not doc_path.exists():
                return
            
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # YAML 헤더의 process_status 업데이트
            if content.startswith('# 속성\n---\n'):
                yaml_end = content.find('\n# 추출\n---')
                if yaml_end != -1:
                    yaml_part = content[len('# 속성\n---\n'):yaml_end]
                    # process_status 라인 찾아서 교체
                    lines = yaml_part.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('process_status:'):
                            lines[i] = f'process_status: {str(status).lower()}'
                            break
                    
                    new_yaml = '\n'.join(lines)
                    extraction_marker = '\n# 추출\n---'
                    new_content = f"# 속성\n---\n{new_yaml}{extraction_marker}{content[yaml_end+len(extraction_marker):]}"
                    
                    with open(doc_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    self.logger.info(f"🔄 process_status 업데이트: {node.title} -> {status}")
            
        except Exception as e:
            self.logger.error(f"process_status 업데이트 실패: {node.title} - {e}")
    
    async def load_node_document_content(self, node: NodeInfo) -> str:
        """노드 문서 전체 내용 로드"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                self.logger.warning(f"문서 파일 없음: {node.title}")
                return ""
            
            with open(node.document_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"문서 로드 실패: {node.title} - {e}")
            return ""
    
    def parse_extraction_section(self, content: str) -> Dict[str, str]:
        """문서에서 추출 섹션 파싱"""
        sections = {}
        
        # # 추출 섹션 찾기
        extraction_start = content.find('# 추출\n---\n')
        if extraction_start == -1:
            return sections
        
        # # 내용 섹션 시작점 찾기
        content_start = content.find('# 내용\n---', extraction_start)
        if content_start == -1:
            extraction_content = content[extraction_start + len('# 추출\n---\n'):]
        else:
            extraction_content = content[extraction_start + len('# 추출\n---\n'):content_start]
        
        # 추출 섹션 내용 파싱
        current_section = None
        current_content = []
        
        for line in extraction_content.split('\n'):
            line = line.strip()
            if line.startswith('## 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'core_content'
                current_content = []
            elif line.startswith('## 상세 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_core_content'
                current_content = []
            elif line.startswith('## 상세 정보'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_content'
                current_content = []
            elif line.startswith('## 주요 화제'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'main_topics'
                current_content = []
            elif line.startswith('## 부차 화제'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'sub_topics'
                current_content = []
            elif current_section and line:
                current_content.append(line)
        
        # 마지막 섹션 처리
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    async def update_node_section(self, node: NodeInfo, section_type: str, new_content: str,
                                 update_logger: 'UpdateLogger' = None):
        """노드 문서의 특정 섹션 업데이트"""
        try:
            if not node.document_path or not Path(node.document_path).exists():
                self.logger.warning(f"문서 파일 없음: {node.title}")
                return
            
            # 현재 문서 내용 로드
            with open(node.document_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 추출 섹션 파싱
            sections = self.parse_extraction_section(content)
            
            # 기존 섹션 내용 저장 (로깅용)
            before_content = sections.get(section_type, "")
            
            # 해당 섹션 업데이트
            sections[section_type] = new_content
            
            # 구성 노드 업데이트 로깅은 추후 구현 (AI 프롬프트가 없는 단순 교체)
            
            # 업데이트된 추출 섹션 재구성
            section_names = {
                'core_content': '## 핵심 내용',
                'detailed_core_content': '## 상세 핵심 내용',
                'detailed_content': '## 상세 정보',
                'main_topics': '## 주요 화제',
                'sub_topics': '## 부차 화제'
            }
            
            updated_sections = []
            for key in ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']:
                if key in sections and sections[key]:
                    updated_sections.append(f"{section_names[key]}\n{sections[key]}")
            
            new_extraction_content = '\n\n'.join(updated_sections)
            
            # 문서에서 추출 섹션 교체
            extraction_start = content.find('# 추출\n---\n')
            content_start = content.find('# 내용\n---', extraction_start)
            
            if extraction_start != -1 and content_start != -1:
                new_content_full = (
                    content[:extraction_start + len('# 추출\n---\n')] + 
                    '\n' + new_extraction_content + '\n\n' +
                    content[content_start:]
                )
                
                # 파일 저장
                with open(node.document_path, 'w', encoding='utf-8') as f:
                    f.write(new_content_full)
                
                self.logger.info(f"✅ {section_type} 섹션 업데이트: {node.title}")
            else:
                self.logger.warning(f"추출 섹션을 찾을 수 없음: {node.title}")
                
        except Exception as e:
            self.logger.error(f"섹션 업데이트 실패: {node.title} - {e}")


class ExtractionEngine:
    """추출 엔진 - 5개 정보 타입 병렬 처리"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
    
    async def extract_all_info(self, content: str, title: str, 
                              update_logger: 'UpdateLogger' = None) -> ExtractionResult:
        """5개 정보 타입 병렬 추출"""
        self.logger.info(f"🔍 추출 시작: {title}")
        
        try:
            # 5개 추출 작업을 병렬로 실행 (모든 정보 유형 개별 로깅)
            tasks = [
                self._extract_core_content(content, title, update_logger),
                self._extract_detailed_core_content(content, title, update_logger),
                self._extract_detailed_content(content, title, update_logger),
                self._extract_main_topics(content, title, update_logger),
                self._extract_sub_topics(content, title, update_logger)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 결과 정리
            result = ExtractionResult()
            success_count = 0
            
            if not isinstance(results[0], Exception):
                result.core_content = results[0]
                success_count += 1
            
            if not isinstance(results[1], Exception):
                result.detailed_core_content = results[1]
                success_count += 1
            
            if not isinstance(results[2], Exception):
                result.detailed_content = results[2]
                success_count += 1
            
            if not isinstance(results[3], Exception):
                result.main_topics = results[3]
                success_count += 1
            
            if not isinstance(results[4], Exception):
                result.sub_topics = results[4]
                success_count += 1
            
            result.success = success_count >= 3  # 5개 중 3개 이상 성공
            self.logger.info(f"✅ 추출 완료: {title} ({success_count}/5)")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 추출 실패: {title} - {e}")
            result = ExtractionResult()
            result.success = False
            result.error = str(e)
            return result
    
    async def _extract_core_content(self, content: str, title: str,
                                   update_logger: 'UpdateLogger' = None) -> str:
        """핵심 내용 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용의 핵심을 2-3문장으로 간결하게 요약해주세요.
응답에 헤더나 마크다운 형식은 사용하지 마세요."""

        system_prompt = f"텍스트 분석 전문가. {title}의 핵심 내용을 간결하고 명확하게 요약하세요."
        
        provider = self.ai_factory.get_provider()
        result = await provider.generate_text(prompt, system_prompt)
        
        # 추출 작업 로깅 (리프 노드 추출)
        if update_logger:
            # 파일명: extraction_노드제목_핵심_HHMM.txt
            import re
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = re.sub(r'_+', '_', safe_title.replace(' ', '_'))[:30]
            
            await update_logger.log_extraction_with_prompt(
                safe_title, "핵심", prompt, system_prompt, "", result, "leaf_extraction"
            )
        
        return result
    
    async def _extract_detailed_core_content(self, content: str, title: str,
                                            update_logger: 'UpdateLogger' = None) -> str:
        """상세 핵심 내용 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용의 상세 핵심 내용을 체계적으로 정리해주세요.
헤더를 사용할 경우 ### 3레벨부터 사용하고, 응답에 '상세 핵심 내용'이라는 헤더는 포함하지 마세요."""

        system_prompt = f"텍스트 분석 전문가. {title}의 상세한 내용을 체계적이고 포괄적으로 정리하세요."
        
        provider = self.ai_factory.get_provider()
        result = await provider.generate_text(prompt, system_prompt)
        
        # 추출 작업 로깅 (리프 노드 추출)
        if update_logger:
            # 파일명: extraction_노드제목_상세핵심_HHMM.txt
            import re
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = re.sub(r'_+', '_', safe_title.replace(' ', '_'))[:30]
            
            await update_logger.log_extraction_with_prompt(
                safe_title, "상세핵심", prompt, system_prompt, "", result, "leaf_extraction"
            )
        
        return result
    
    async def _extract_detailed_content(self, content: str, title: str,
                                       update_logger: 'UpdateLogger' = None) -> str:
        """상세 정보 추출 (새로운 정보 타입)"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용에서 이전에 다루지 않았던 새로운 상세 정보들을 추출해주세요.
기존 핵심 내용에서 다루지 않은 추가적인 세부 사항, 예시, 구체적인 구현 방법 등을 포함해주세요."""

        system_prompt = f"텍스트 분석 전문가. {title}에서 추가적인 상세 정보와 새로운 내용을 식별하여 정리하세요."
        
        provider = self.ai_factory.get_provider()
        result = await provider.generate_text(prompt, system_prompt)
        
        # 추출 작업 로깅 (리프 노드 추출)
        if update_logger:
            # 파일명: extraction_노드제목_상세_HHMM.txt
            import re
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = re.sub(r'_+', '_', safe_title.replace(' ', '_'))[:30]
            
            await update_logger.log_extraction_with_prompt(
                safe_title, "상세", prompt, system_prompt, "", result, "leaf_extraction"
            )
        
        return result
    
    async def _extract_main_topics(self, content: str, title: str,
                                  update_logger: 'UpdateLogger' = None) -> str:
        """주요 화제 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용에서 다루는 주요 화제들을 추출해주세요.
다음 형식으로 답변해주세요 (- 기호로 시작):
- 주요 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 주요 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""

        system_prompt = f"텍스트 분석 전문가. {title}에서 다루는 주요 화제를 체계적으로 식별하고 정리하세요."
        
        provider = self.ai_factory.get_provider()
        result = await provider.generate_text(prompt, system_prompt)
        
        # 추출 작업 로깅 (리프 노드 추출)
        if update_logger:
            import re
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = re.sub(r'_+', '_', safe_title.replace(' ', '_'))[:30]
            
            await update_logger.log_extraction_with_prompt(
                safe_title, "주요화제", prompt, system_prompt, "", result, "leaf_extraction"
            )
        
        return result
    
    async def _extract_sub_topics(self, content: str, title: str,
                                 update_logger: 'UpdateLogger' = None) -> str:
        """부차 화제 추출"""
        prompt = f"""다음은 "{title}"의 내용입니다:

{content}

이 내용에서 다루는 부차적인 화제들을 추출해주세요.
다음 형식으로 답변해주세요 (- 기호로 시작):
- 부차 화제1(구체적인 주제명): 이 화제에 대해 다루는 내용
- 부차 화제2(구체적인 주제명): 이 화제에 대해 다루는 내용

반드시 - 기호로 시작하는 목록 형태로만 답변해주세요."""

        system_prompt = f"텍스트 분석 전문가. {title}에서 다루는 부차 화제를 체계적으로 식별하고 정리하세요."
        
        provider = self.ai_factory.get_provider()
        result = await provider.generate_text(prompt, system_prompt)
        
        # 추출 작업 로깅 (리프 노드 추출)
        if update_logger:
            import re
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = re.sub(r'_+', '_', safe_title.replace(' ', '_'))[:30]
            
            await update_logger.log_extraction_with_prompt(
                safe_title, "부차화제", prompt, system_prompt, "", result, "leaf_extraction"
            )
        
        return result


class UpdateEngine:
    """업데이트 엔진 - 구성 노드 기반 정보 타입별 업데이트"""
    
    def __init__(self, ai_factory: AIProviderFactory, logger: logging.Logger):
        self.ai_factory = ai_factory
        self.logger = logger
    
    async def update_parent_extraction(self, current_result: ExtractionResult, 
                                     composition_extractions: List[str], title: str,
                                     debug_manager: DebugManager = None,
                                     update_logger: 'UpdateLogger' = None) -> str:
        """부모 노드 추출 섹션을 정보 타입별로 업데이트"""
        self.logger.info(f"🔄 부모 업데이트 (정보 타입별): {title}")
        
        try:
            # 현재 추출 결과를 딕셔너리로 변환
            current_sections = {
                'core_content': current_result.core_content,
                'detailed_core_content': current_result.detailed_core_content,
                'detailed_content': current_result.detailed_content,
                'main_topics': current_result.main_topics,
                'sub_topics': current_result.sub_topics
            }
            
            # 구성 노드들의 추출 섹션을 정보 타입별로 파싱
            composition_sections = []
            for i, extraction in enumerate(composition_extractions, 1):
                if extraction:
                    parsed = self._parse_extraction_content(extraction)
                    composition_sections.append((f"구성노드{i}", parsed))
            
            updated_sections = {}
            
            # 5가지 정보 타입별로 개별 업데이트
            section_types = ['core_content', 'detailed_core_content', 'detailed_content', 
                           'main_topics', 'sub_topics']
            
            for section_type in section_types:
                # 기존 내용 보준
                before_content = current_sections[section_type]
                
                # 업데이트 수행 (결과, 프롬프트, 시스템프롬프트 반환)
                update_result = await self._update_single_section(
                    section_type, before_content, 
                    composition_sections, title, debug_manager, update_logger
                )
                
                updated_content, actual_prompt, actual_system_prompt = update_result
                updated_sections[section_type] = updated_content
                
                # 정보 유형별 개별 로깅 (실제 프롬프트 사용)
                if update_logger and actual_prompt:
                    # 정보 유형명 매핑
                    info_type_names = {
                        'core_content': '핵심',
                        'detailed_core_content': '상세핵심', 
                        'detailed_content': '상세',
                        'main_topics': '주요화제',
                        'sub_topics': '부차화제'
                    }
                    
                    info_type_name = info_type_names.get(section_type, section_type)
                    
                    # 실제 프롬프트로 로깅
                    await update_logger.log_update_with_prompt(
                        title, info_type_name, actual_prompt, actual_system_prompt, 
                        updated_content, "parent_update"
                    )
            
            # 결과를 문자열 형식으로 포맷팅
            return self._format_updated_sections(updated_sections)
            
        except Exception as e:
            self.logger.error(f"부모 업데이트 실패: {title} - {e}")
            return self._format_extraction_result(current_result)
    
    def _parse_extraction_content(self, extraction: str) -> Dict[str, str]:
        """추출 섹션 내용을 정보 타입별로 파싱"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in extraction.split('\n'):
            line = line.strip()
            if line.startswith('## 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'core_content'
                current_content = []
            elif line.startswith('## 상세 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_core_content'
                current_content = []
            elif line.startswith('## 상세 정보'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_content'
                current_content = []
            elif line.startswith('## 주요 화제'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'main_topics'
                current_content = []
            elif line.startswith('## 부차 화제'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'sub_topics'
                current_content = []
            elif current_section and line:
                current_content.append(line)
        
        # 마지막 섹션 처리
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    async def _update_single_section(self, section_type: str, base_content: str,
                                   composition_sections: List[Tuple[str, Dict[str, str]]],
                                   title: str, debug_manager: DebugManager = None,
                                   update_logger: 'UpdateLogger' = None) -> Tuple[str, str, str]:
        """단일 정보 타입에 대한 업데이트"""
        section_names = {
            'core_content': '핵심 내용',
            'detailed_core_content': '상세 핵심 내용',
            'detailed_content': '상세 정보',
            'main_topics': '주요 화제',
            'sub_topics': '부차 화제'
        }
        
        section_name = section_names.get(section_type, section_type)
        
        # 구성 노드들의 해당 섹션 내용 수집
        reference_contents = []
        for node_name, sections in composition_sections:
            content = sections.get(section_type, '')
            if content:
                reference_contents.append(f"=== {node_name} {section_name} ===\n{content}")
        
        # 디버깅용 문서 저장
        if debug_manager:
            await debug_manager.save_update_documents(
                title, section_type, base_content, reference_contents
            )
        
        # 참조 문서가 없으면 기존 내용 그대로 반환 (결과, 빈프롬프트, 빈시스템프롬프트)
        if not reference_contents:
            return base_content, "", ""
        
        # AI 프롬프트 생성 및 실행
        combined_references = "\n\n".join(reference_contents)
        
        prompt = f"""다음은 부모 노드의 {section_name} 업데이트 작업입니다.

**기준 문서 (현재 부모 노드의 {section_name}):**
{base_content}

**참조 문서들 (구성 노드들의 {section_name}):**
{combined_references}

기준 문서를 바탕으로 참조 문서들의 정보를 반영하여 부모 노드의 {section_name}을 업데이트해주세요.

**업데이트 지침:**
1. 기준 문서의 핵심은 유지하되, 구성 노드들의 정보를 포함하여 보완
2. 구성 노드별 정보는 출처를 명시하여 포함 (예: "내용 (출처: 구성노드1)")
3. 전체적인 일관성과 체계성 유지
4. 중복 정보는 정리하되 누락 없이 포함

응답에는 헤더 없이 업데이트된 {section_name} 내용만 작성해주세요."""
        
        try:
            system_prompt = f"문서 업데이트 전문가. {title}의 {section_name}을 구성 노드 정보를 반영하여 체계적으로 개선하세요."
            provider = self.ai_factory.get_provider()
            result = await provider.generate_text(prompt, system_prompt)
            
            self.logger.info(f"✅ {section_name} 업데이트 완료: {title}")
            # (결과, 프롬프트, 시스템프롬프트) 반환
            return result.strip(), prompt, system_prompt
            
        except Exception as e:
            self.logger.error(f"❌ {section_name} 업데이트 실패: {title} - {e}")
            return base_content, "", ""
    
    def _format_updated_sections(self, sections: Dict[str, str]) -> str:
        """업데이트된 섹션들을 문자열 형식으로 포맷팅"""
        formatted_sections = []
        
        section_order = ['core_content', 'detailed_core_content', 'detailed_content', 
                        'main_topics', 'sub_topics']
        section_names = {
            'core_content': '## 핵심 내용',
            'detailed_core_content': '## 상세 핵심 내용',
            'detailed_content': '## 상세 정보',
            'main_topics': '## 주요 화제',
            'sub_topics': '## 부차 화제'
        }
        
        for section_key in section_order:
            if section_key in sections and sections[section_key]:
                formatted_sections.append(f"{section_names[section_key]}\n{sections[section_key]}")
        
        return "\n\n".join(formatted_sections)
    
    def _format_extraction_result(self, result: ExtractionResult) -> str:
        """추출 결과를 문자열로 포맷팅"""
        sections = []
        
        if result.core_content:
            sections.append(f"## 핵심 내용\n{result.core_content}")
        
        if result.detailed_core_content:
            sections.append(f"## 상세 핵심 내용\n{result.detailed_core_content}")
        
        if result.detailed_content:
            sections.append(f"## 상세 정보\n{result.detailed_content}")
        
        if result.main_topics:
            sections.append(f"## 주요 화제\n{result.main_topics}")
        
        if result.sub_topics:
            sections.append(f"## 부차 화제\n{result.sub_topics}")
        
        return "\n\n".join(sections)
    
    async def update_composition_extractions(self, parent_node: NodeInfo, 
                                           updated_parent_extraction: str, 
                                           doc_manager: 'NodeDocumentManager',
                                           update_logger: 'UpdateLogger' = None):
        """구성 노드들의 추출 섹션 배치 업데이트"""
        self.logger.info(f"🔄 구성 노드들 배치 업데이트: {parent_node.title}")
        
        if not parent_node.children_ids:
            self.logger.info("🔄 구성 노드 없음 - 업데이트 스킵")
            return
        
        try:
            # 1. 모든 자식 노드 정보 로드
            all_nodes = await doc_manager.load_nodes_info()
            composition_nodes = [node for node in all_nodes if node.id in parent_node.children_ids]
            
            if not composition_nodes:
                self.logger.warning("⚠️ 구성 노드를 찾을 수 없음")
                return
            
            # 2. 부모 노드의 업데이트된 추출 섹션 파싱
            parent_sections = self._parse_parent_extraction_sections(updated_parent_extraction)
            
            # 3. 모든 구성 노드의 현재 추출 섹션 로드
            composition_sections = {}
            for child in composition_nodes:
                child_doc_content = await doc_manager.load_node_document_content(child)
                parsed_sections = doc_manager.parse_extraction_section(child_doc_content)
                
                # 빈 섹션 확인 및 로깅
                if not any(parsed_sections.values()):
                    self.logger.warning(f"⚠️ 구성 노드 {child.id}({child.title}) 추출 섹션이 비어있음")
                else:
                    self.logger.info(f"✅ 구성 노드 {child.id}({child.title}) 추출 섹션 로드 완료: {list(parsed_sections.keys())}")
                
                composition_sections[child.id] = {
                    'node': child,
                    'sections': parsed_sections
                }
            
            # 4. 3개 정보 타입별로 배치 업데이트 (핵심 내용, 상세 핵심 내용, 상세 정보)
            # 주요화제, 부차화제는 각 구성 노드의 기존 내용 보존
            update_sections = ['core_content', 'detailed_core_content', 'detailed_content']
            
            # 4.1. 모든 섹션별 업데이트 내용을 먼저 수집
            all_updated_content = {}  # {child_id: {section_type: content}}
            
            for section_type in update_sections:
                updated_composition = await self._batch_update_composition_section(
                    parent_node, section_type, parent_sections.get(section_type, ''), composition_sections, update_logger
                )
                
                # 각 구성 노드별로 업데이트된 내용 저장
                for child_id, updated_content in updated_composition.items():
                    if child_id not in all_updated_content:
                        all_updated_content[child_id] = {}
                    all_updated_content[child_id][section_type] = updated_content
                    
                self.logger.info(f"✅ {section_type} 배치 업데이트 완료: {len(updated_composition)}개 구성 노드")
            
            # 4.2. 각 구성 노드별로 모든 섹션을 한 번에 업데이트
            for child_id, updated_sections_dict in all_updated_content.items():
                child_node = composition_sections[child_id]['node']
                existing_sections = composition_sections[child_id]['sections']
                
                # 모든 섹션을 종합하여 한 번에 업데이트
                await self._update_all_sections_preserving_topics(
                    child_node, updated_sections_dict, existing_sections, doc_manager, update_logger
                )
            
            self.logger.info(f"✅ 모든 구성 노드 배치 업데이트 완료: {len(composition_nodes)}개")
            
        except Exception as e:
            self.logger.error(f"❌ 구성 노드 배치 업데이트 실패: {e}")
            raise
    
    async def _update_node_section_preserving_topics(self, child_node: NodeInfo, section_type: str, 
                                                    updated_content: str, existing_sections: Dict[str, str],
                                                    doc_manager: 'NodeDocumentManager', update_logger: 'UpdateLogger' = None):
        """구성 노드의 특정 섹션만 업데이트하면서 주요화제/부차화제는 보존"""
        try:
            # 1. 기존 섹션들 중 주요화제, 부차화제 보존
            preserved_sections = {}
            if existing_sections.get('main_topics'):
                preserved_sections['main_topics'] = existing_sections['main_topics']
            if existing_sections.get('sub_topics'):
                preserved_sections['sub_topics'] = existing_sections['sub_topics']
            
            # 2. 업데이트할 섹션 설정 (빈 섹션도 기본 구조 제공)
            updated_sections = existing_sections.copy()
            updated_sections[section_type] = updated_content
            
            # 빈 구성 노드의 경우 기존 상세 정보 섹션은 보존 (핵심, 상세핵심만 새로 추가)
            if not existing_sections:
                # 원본 문서에서 상세 정보 섹션 직접 읽어서 보존
                try:
                    original_content = await doc_manager.load_node_document_content(child_node)
                    original_detailed_info = doc_manager.parse_extraction_section(original_content).get('detailed_content', '')
                    if original_detailed_info and section_type != 'detailed_content':
                        updated_sections['detailed_content'] = original_detailed_info
                        self.logger.info(f"📋 기존 상세 정보 보존: {child_node.title}")
                except Exception as e:
                    self.logger.warning(f"⚠️ 기존 상세 정보 로드 실패: {child_node.title} - {e}")
            
            # 3. 주요화제/부차화제가 있으면 복원
            if preserved_sections:
                updated_sections.update(preserved_sections)
                self.logger.info(f"📌 주요화제/부차화제 보존: {child_node.title} - {list(preserved_sections.keys())}")
            
            # 4. 전체 추출 섹션 재구성
            extraction_parts = []
            section_order = ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']
            section_titles = {
                'core_content': '## 핵심 내용',
                'detailed_core_content': '## 상세 핵심 내용', 
                'detailed_content': '## 상세 정보',
                'main_topics': '## 주요 화제',
                'sub_topics': '## 부차 화제'
            }
            
            for section_key in section_order:
                if updated_sections.get(section_key):
                    extraction_parts.append(f"{section_titles[section_key]}\n{updated_sections[section_key]}")
            
            if extraction_parts:
                full_extraction = '\n\n'.join(extraction_parts)
                
                # 5. 문서에 전체 추출 섹션 업데이트
                await doc_manager.save_extraction_section(child_node, full_extraction, update_logger)
                self.logger.info(f"✅ 구성 노드 섹션 업데이트 완료 (주요화제/부차화제 보존): {child_node.title}")
            else:
                self.logger.warning(f"⚠️ 구성 노드 {child_node.title} - 업데이트할 내용이 없음")
                
        except Exception as e:
            self.logger.error(f"❌ 구성 노드 섹션 업데이트 실패: {child_node.title} - {e}")
            raise
    
    async def _update_all_sections_preserving_topics(self, child_node: NodeInfo, updated_sections_dict: Dict[str, str],
                                                    existing_sections: Dict[str, str], doc_manager: 'NodeDocumentManager', 
                                                    update_logger: 'UpdateLogger' = None):
        """구성 노드의 모든 섹션을 한 번에 업데이트하면서 주요화제/부차화제와 기존 상세 정보 보존"""
        try:
            # 1. 최종 업데이트될 섹션들 준비
            final_sections = {}
            
            # 1.1. 업데이트된 3개 섹션 적용
            final_sections.update(updated_sections_dict)
            
            # 1.2. 기존 주요화제, 부차화제 보존
            if existing_sections.get('main_topics'):
                final_sections['main_topics'] = existing_sections['main_topics']
            if existing_sections.get('sub_topics'):
                final_sections['sub_topics'] = existing_sections['sub_topics']
            
            # 1.3. 빈 구성 노드의 경우 기존 상세 정보 보존
            if not existing_sections:
                try:
                    original_content = await doc_manager.load_node_document_content(child_node)
                    original_sections = doc_manager.parse_extraction_section(original_content)
                    if original_sections.get('detailed_content') and 'detailed_content' not in updated_sections_dict:
                        final_sections['detailed_content'] = original_sections['detailed_content']
                        self.logger.info(f"📋 기존 상세 정보 보존: {child_node.title}")
                except Exception as e:
                    self.logger.warning(f"⚠️ 기존 상세 정보 로드 실패: {child_node.title} - {e}")
            
            # 2. 전체 추출 섹션 재구성
            extraction_parts = []
            section_order = ['core_content', 'detailed_core_content', 'detailed_content', 'main_topics', 'sub_topics']
            section_titles = {
                'core_content': '## 핵심 내용',
                'detailed_core_content': '## 상세 핵심 내용', 
                'detailed_content': '## 상세 정보',
                'main_topics': '## 주요 화제',
                'sub_topics': '## 부차 화제'
            }
            
            for section_key in section_order:
                if final_sections.get(section_key):
                    extraction_parts.append(f"{section_titles[section_key]}\n{final_sections[section_key]}")
            
            if extraction_parts:
                full_extraction = '\n\n'.join(extraction_parts)
                
                # 3. 문서에 전체 추출 섹션 업데이트
                await doc_manager.save_extraction_section(child_node, full_extraction, update_logger)
                
                preserved_info = []
                if existing_sections.get('main_topics'):
                    preserved_info.append('주요화제')
                if existing_sections.get('sub_topics'):
                    preserved_info.append('부차화제')
                
                preserved_text = f" ({', '.join(preserved_info)} 보존)" if preserved_info else ""
                self.logger.info(f"✅ 구성 노드 전체 업데이트 완료{preserved_text}: {child_node.title}")
            else:
                self.logger.warning(f"⚠️ 구성 노드 {child_node.title} - 업데이트할 내용이 없음")
                
        except Exception as e:
            self.logger.error(f"❌ 구성 노드 전체 업데이트 실패: {child_node.title} - {e}")
            raise
    
    def _parse_parent_extraction_sections(self, extraction: str) -> Dict[str, str]:
        """부모 노드 추출 섹션을 정보 타입별로 파싱"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in extraction.split('\n'):
            line = line.strip()
            if line.startswith('## 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'core_content'
                current_content = []
            elif line.startswith('## 상세 핵심 내용'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_core_content'
                current_content = []
            elif line.startswith('## 상세 정보'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'detailed_content'
                current_content = []
            elif line.startswith('## 주요 화제') or line.startswith('## 부차 화제'):
                # 주요/부차 화제는 구성 노드 업데이트에서 제외
                if current_section and current_section in ['core_content', 'detailed_core_content', 'detailed_content']:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = None
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # 마지막 섹션 처리
        if current_section and current_section in ['core_content', 'detailed_core_content', 'detailed_content']:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    async def _batch_update_composition_section(self, node, section_type: str, parent_section: str,
                                              composition_sections: Dict[int, Dict], update_logger=None) -> Dict[int, str]:
        """특정 정보 타입에 대해 모든 구성 노드를 배치 업데이트"""
        section_names = {
            'core_content': '핵심 내용',
            'detailed_core_content': '상세 핵심 내용', 
            'detailed_content': '상세 정보'
        }
        
        section_name = section_names.get(section_type, section_type)
        
        # 프롬프트 구성: 부모 섹션 + 모든 구성 섹션들
        composition_info = []
        for child_id, data in composition_sections.items():
            child_node = data['node']
            child_section = data['sections'].get(section_type, '없음')
            composition_info.append(f"구성노드{child_id}({child_node.title}): {child_section}")
        
        prompt = f"""다음은 부모 노드의 업데이트된 {section_name}을 바탕으로 구성 노드들의 {section_name}을 개선하는 작업입니다.

**부모 노드 {section_name} (업데이트됨):**
{parent_section}

**구성 노드들의 현재 {section_name}:**
{chr(10).join(composition_info)}

부모 노드의 업데이트된 {section_name}을 반영하여 각 구성 노드의 {section_name}을 개선해주세요.
각 구성 노드의 고유한 특성은 유지하되, 부모와의 일관성과 연결성을 반영해주세요.

다음 형식으로 답변해주세요:
구성노드[ID]: [개선된 {section_name}]
구성노드[ID]: [개선된 {section_name}]
..."""

        system_prompt = f"문서 전문가. 부모-구성 노드 관계를 고려하여 {section_name}의 일관성을 유지하면서 각 구성 노드의 특성을 살려 개선하세요."
        
        provider = self.ai_factory.get_provider()
        result = await provider.generate_text(
            prompt,
            system_prompt
        )
        
        # 구성 노드 업데이트 로깅
        if update_logger:
            await update_logger.log_update_with_prompt(
                node.title, 
                section_type,
                prompt,
                system_prompt,
                result,
                "composition_update"
            )
        
        # 결과 파싱하여 딕셔너리로 변환 (다중 라인 내용 지원)
        updated_composition = {}
        
        # 구성노드별로 분할하여 다중 라인 내용 처리
        import re
        
        # "구성노드N:" 패턴으로 분할
        node_pattern = r'\n구성노드(\d+):\s*'
        parts = re.split(node_pattern, result)
        
        # parts[0]은 첫 부분(보통 빈 문자열 또는 설명), 이후 [node_id, content, node_id, content, ...] 패턴
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                try:
                    child_id = int(parts[i])
                    content = parts[i + 1].strip()
                    
                    if child_id in composition_sections and content:
                        updated_composition[child_id] = content
                        self.logger.debug(f"✅ 구성노드{child_id} 내용 파싱 완료: {len(content)} 문자")
                except (ValueError, IndexError) as e:
                    self.logger.warning(f"결과 파싱 오류: 구성노드{parts[i] if i < len(parts) else 'Unknown'} - {e}")
        
        return updated_composition


class NodeTraverser:
    """노드 순회 관리 클래스"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def get_processing_order(self, nodes: List[NodeInfo]) -> List[List[NodeInfo]]:
        """처리 순서 반환 (리프 노드 먼저, 그 다음 레벨별 bottom-up)"""
        # 1. 리프 노드와 비리프 노드 분리
        leaf_nodes = [node for node in nodes if not node.children_ids]
        non_leaf_nodes = [node for node in nodes if node.children_ids]
        
        self.logger.info(f"📊 리프 노드: {len(leaf_nodes)}개")
        self.logger.info(f"📊 비리프 노드: {len(non_leaf_nodes)}개")
        
        processing_order = []
        
        # 2. 리프 노드들을 먼저 처리 그룹으로 추가
        if leaf_nodes:
            processing_order.append(leaf_nodes)
            self.logger.info(f"📊 1단계 (리프 노드): {len(leaf_nodes)}개 노드")
        
        # 3. 비리프 노드들을 레벨별로 그룹화 (하위 레벨부터)
        if non_leaf_nodes:
            level_groups = {}
            for node in non_leaf_nodes:
                if node.level not in level_groups:
                    level_groups[node.level] = []
                level_groups[node.level].append(node)
            
            # 가장 하위 레벨부터 상위 레벨 순으로 처리
            sorted_levels = sorted(level_groups.keys(), reverse=True)
            
            for i, level in enumerate(sorted_levels):
                processing_order.append(level_groups[level])
                stage = i + 2  # 리프 노드가 1단계이므로 2단계부터
                self.logger.info(f"📊 {stage}단계 (레벨 {level}): {len(level_groups[level])}개 노드")
        
        return processing_order


class ProgressTracker:
    """진행률 추적 및 오류 복구 클래스"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.status = ProcessingStatus()
    
    def start_processing(self):
        """처리 시작"""
        self.status.start_time = datetime.now()
        self.logger.info("🚀 처리 시작")
    
    def set_total_nodes(self, total: int):
        """전체 노드 수 설정"""
        self.status.total_nodes = total
        self.logger.info(f"📊 전체 노드: {total}개")
    
    def set_current_node(self, node_title: str):
        """현재 처리 노드 설정"""
        self.status.current_node = node_title
    
    def mark_completed(self, node_title: str):
        """완료 처리"""
        self.status.processed_nodes += 1
        progress = (self.status.processed_nodes / self.status.total_nodes) * 100
        self.logger.info(f"✅ 완료: {node_title} ({progress:.1f}%)")
    
    def mark_failed(self, node_title: str, error: str):
        """실패 처리"""
        self.status.failed_nodes += 1
        self.status.errors.append(f"{node_title}: {error}")
        self.logger.error(f"❌ 실패: {node_title} - {error}")
    
    def add_error(self, error: str):
        """오류 추가"""
        self.status.errors.append(error)
    
    def get_final_result(self) -> Dict[str, Any]:
        """최종 결과 반환"""
        end_time = datetime.now()
        duration = end_time - self.status.start_time if self.status.start_time else None
        
        return {
            'success': self.status.failed_nodes == 0,
            'total_nodes': self.status.total_nodes,
            'processed_nodes': self.status.processed_nodes,
            'failed_nodes': self.status.failed_nodes,
            'errors': self.status.errors,
            'duration': str(duration) if duration else None,
            'start_time': self.status.start_time.isoformat() if self.status.start_time else None,
            'end_time': end_time.isoformat()
        }


# CLI 인터페이스
async def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='통합 노드 정보 문서 처리 시스템 v2')
    parser.add_argument('--config', default='./config.yaml', help='설정 파일 경로')
    parser.add_argument('--ai-provider', choices=['gemini', 'claude', 'openai'], 
                       help='AI 프로바이더 선택')
    parser.add_argument('--processing-mode', choices=['v1', 'v2', 'v3'], default='v3',
                       help='처리 방식 선택')
    parser.add_argument('--debug-dir', default='./25-08-29',
                       help='디버깅 폴더 경로')
    
    args = parser.parse_args()
    
    # 설정 오버라이드
    config_path = args.config
    overrides = {}
    if args.ai_provider:
        overrides['ai_provider'] = args.ai_provider
    if args.processing_mode:
        overrides['processing_mode'] = args.processing_mode
    if args.debug_dir:
        overrides['debug_dir'] = args.debug_dir
    
    try:
        processor = UnifiedNodeProcessor(config_path)
        
        # 설정 오버라이드 적용
        for key, value in overrides.items():
            processor.config[key] = value
        
        print(f"🚀 통합 노드 처리 시작 (v2)")
        print(f"📋 AI 프로바이더: {processor.config.get('ai_provider', 'gemini')}")
        print(f"📋 처리 방식: {processor.config.get('processing_mode', 'v3')}")
        print(f"📁 디버깅 폴더: {processor.config.get('debug_dir', './25-08-29')}")
        
        result = await processor.process_all_nodes()
        
        if result['success']:
            print(f"\n✅ 전체 처리 완료!")
            print(f"📊 처리된 노드: {result['processed_nodes']}/{result['total_nodes']}")
            print(f"⏱️ 소요 시간: {result['duration']}")
        else:
            print(f"\n❌ 처리 실패!")
            print(f"📊 실패한 노드: {result['failed_nodes']}/{result['total_nodes']}")
            for error in result['errors']:
                print(f"  - {error}")
            
    except Exception as e:
        print(f"❌ 시스템 오류: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))