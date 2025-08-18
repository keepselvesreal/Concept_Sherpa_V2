"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: YouTube 대본 추출 API 엔드포인트
상세 내용:
    - YouTubeExtractRequest: YouTube URL 요청 모델
    - extract_transcript(): YouTube 대본 추출 API 엔드포인트
    - 기존 youtube_transcript_extractor.py 로직 활용
    - 비동기 처리 및 오류 처리
상태: 활성
주소: knowledge_web/api/youtube
참조: ../knowledge_ui/handlers/youtube_handler.py
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import re
import os
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

router = APIRouter()

# 출력 디렉토리 설정
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'transcripts')
os.makedirs(OUTPUT_DIR, exist_ok=True)


class YouTubeExtractRequest(BaseModel):
    url: str

    class Config:
        schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }


def extract_video_id(url: str) -> str:
    """YouTube URL에서 video ID를 추출합니다."""
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


def get_transcript_data(video_id: str, language_codes=['ko', 'en']):
    """YouTube 영상의 대본 데이터를 추출합니다."""
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


def format_transcript(transcript_data: list, video_url: str, language_used: str) -> str:
    """대본 데이터를 마크다운 형식으로 포맷팅합니다."""
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


def save_transcript(content: str, video_id: str) -> str:
    """대본 내용을 파일로 저장합니다."""
    filename = f"youtube_transcript_{video_id}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


@router.post("/extract")
async def extract_transcript(request: YouTubeExtractRequest):
    """
    YouTube URL에서 대본을 추출합니다.
    
    - **url**: YouTube 영상 URL
    """
    try:
        url = request.url.strip()
        
        # Video ID 추출
        video_id = extract_video_id(url)
        if not video_id:
            raise HTTPException(
                status_code=400, 
                detail="유효한 YouTube URL이 아닙니다."
            )
        
        print(f"🎥 YouTube 대본 추출 시작: {video_id}")
        
        # 대본 데이터 추출
        transcript_data, language_used = get_transcript_data(video_id)
        if not transcript_data:
            raise HTTPException(
                status_code=404,
                detail="대본을 추출할 수 없습니다. (대본이 비활성화되었거나 존재하지 않음)"
            )
        
        print(f"✅ 대본 추출 완료 - 언어: {language_used}, 항목: {len(transcript_data)}개")
        
        # 마크다운 포맷팅
        markdown_content = format_transcript(transcript_data, url, language_used)
        
        # 파일 저장
        filepath = save_transcript(markdown_content, video_id)
        
        print(f"💾 파일 저장 완료: {filepath}")
        
        return {
            "success": True,
            "filename": os.path.basename(filepath),
            "file_path": filepath,
            "language": language_used,
            "item_count": len(transcript_data),
            "video_id": video_id,
            "message": "대본이 성공적으로 추출되었습니다."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ YouTube 대본 추출 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"대본 추출 중 오류가 발생했습니다: {str(e)}"
        )