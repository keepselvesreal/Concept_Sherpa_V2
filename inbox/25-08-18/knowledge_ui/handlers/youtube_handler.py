"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: YouTube URL 처리 및 대본 추출 핸들러
상세 내용:
    - YouTubeHandler: YouTube 대본 추출 메인 클래스
    - extract_transcript(url): URL에서 대본을 추출하여 파일로 저장
    - _extract_video_id(url): YouTube URL에서 video ID 추출
    - _get_transcript_data(video_id): 대본 데이터 추출
    - _format_transcript(data, url, language): 마크다운 형식으로 포맷팅
    - _save_transcript(content, video_id): 파일로 저장
상태: 활성
주소: knowledge_ui/handlers/youtube_handler
참조: ../../youtube_transcript_extractor.py
"""

import re
import os
import sys
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


class YouTubeHandler:
    def __init__(self):
        """YouTube 핸들러 초기화"""
        # 출력 디렉토리 설정
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'transcripts')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def extract_transcript(self, url):
        """
        YouTube URL에서 대본을 추출하여 파일로 저장합니다.
        
        Args:
            url (str): YouTube URL
            
        Returns:
            dict: 처리 결과 정보
        """
        try:
            # Video ID 추출
            video_id = self._extract_video_id(url)
            if not video_id:
                return {
                    'success': False,
                    'error': '유효한 YouTube URL이 아닙니다.'
                }
            
            # 대본 데이터 추출
            transcript_data, language_used = self._get_transcript_data(video_id)
            if not transcript_data:
                return {
                    'success': False,
                    'error': '대본을 추출할 수 없습니다. (대본이 비활성화되었거나 존재하지 않음)'
                }
            
            # 마크다운 포맷팅
            markdown_content = self._format_transcript(transcript_data, url, language_used)
            
            # 파일 저장
            filename = self._save_transcript(markdown_content, video_id)
            
            return {
                'success': True,
                'filename': filename,
                'language': language_used,
                'item_count': len(transcript_data),
                'video_id': video_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'처리 중 오류 발생: {str(e)}'
            }
    
    def _extract_video_id(self, url):
        """
        YouTube URL에서 video ID를 추출합니다.
        
        Args:
            url (str): YouTube URL
            
        Returns:
            str: Video ID 또는 None
        """
        patterns = [
            r'(?:youtube\.com/watch\?v=)([^&\n?#]+)',
            r'(?:youtube\.com/embed/)([^&\n?#]+)',
            r'(?:youtu\.be/)([^&\n?#]+)',
            r'(?:youtube\.com/v/)([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _get_transcript_data(self, video_id, language_codes=['ko', 'en']):
        """
        YouTube 영상의 대본 데이터를 추출합니다.
        
        Args:
            video_id (str): YouTube video ID
            language_codes (list): 선호 언어 코드 리스트
            
        Returns:
            tuple: (transcript_data, language_used) 또는 (None, None)
        """
        try:
            api = YouTubeTranscriptApi()
            
            # 선호 언어 순서대로 시도
            fetched_transcript = api.fetch(video_id, languages=language_codes)
            used_language = fetched_transcript.language_code
            
            # 대본 데이터 추출
            transcript_data = []
            for snippet in fetched_transcript.snippets:
                transcript_data.append({
                    'text': snippet.text,
                    'start': snippet.start,
                    'duration': snippet.duration
                })
            
            return transcript_data, used_language
            
        except (TranscriptsDisabled, NoTranscriptFound):
            return None, None
        except Exception:
            return None, None
    
    def _format_transcript(self, transcript_data, video_url, language_used):
        """
        대본 데이터를 마크다운 형식으로 포맷팅합니다.
        
        Args:
            transcript_data (list): 대본 데이터
            video_url (str): 원본 YouTube URL
            language_used (str): 사용된 언어 코드
            
        Returns:
            str: 마크다운 형식의 대본
        """
        if not transcript_data:
            return ""
        
        # 헤더 생성
        header = f"""# YouTube 대본

**영상 URL:** {video_url}
**추출 언어:** {language_used}
**추출 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        # 대본 내용 포맷팅
        content_lines = []
        
        for entry in transcript_data:
            start_time = entry['start']
            text = entry['text'].strip()
            
            # 시간을 분:초 형식으로 변환
            minutes = int(start_time // 60)
            seconds = int(start_time % 60)
            time_stamp = f"[{minutes:02d}:{seconds:02d}]"
            
            # 텍스트가 있는 경우에만 추가
            if text:
                content_lines.append(f"{time_stamp} {text}")
        
        # 전체 내용 조합
        full_content = header + "\n".join(content_lines)
        
        return full_content
    
    def _save_transcript(self, content, video_id):
        """
        대본 내용을 파일로 저장합니다.
        
        Args:
            content (str): 저장할 내용
            video_id (str): YouTube video ID
            
        Returns:
            str: 저장된 파일의 전체 경로
        """
        filename = f"youtube_transcript_{video_id}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath