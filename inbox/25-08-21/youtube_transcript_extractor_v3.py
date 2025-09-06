"""
생성 시간: 2025-08-21 15:30:45 KST
핵심 내용: YouTube 영상 URL에서 대본과 제목을 추출하여 마크다운 파일로 저장하는 개선된 스크립트
상세 내용:
    - extract_video_id(url): YouTube URL에서 video ID 추출
    - get_video_title(video_id): YouTube 영상 제목 추출
    - get_transcript(video_id, language_codes): 대본 추출 (한국어/영어 우선)
    - format_transcript(transcript_data, video_url, language_used, video_title): 개선된 마크다운 형식으로 포맷팅
    - save_to_markdown(content, filename): 마크다운 파일로 저장
    - main(): 메인 실행 함수
상태: 활성
주소: youtube_transcript_extractor_v2
참조: youtube_transcript_extractor
"""

import re
import sys
import requests
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def extract_video_id(url):
    """
    YouTube URL에서 video ID를 추출합니다.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: Video ID 또는 None
    """
    # 다양한 YouTube URL 형식 지원
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


def get_video_title(video_id):
    """
    YouTube 영상의 제목을 추출합니다.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: 영상 제목 또는 기본값
    """
    try:
        # YouTube 페이지에서 제목 추출
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 제목 패턴 검색
        title_pattern = r'<title>([^<]+)</title>'
        match = re.search(title_pattern, response.text)
        
        if match:
            title = match.group(1)
            # YouTube 페이지 제목에서 불필요한 부분 제거
            title = title.replace(' - YouTube', '')
            return title.strip()
        
    except Exception as e:
        print(f"⚠️ 제목 추출 중 오류 발생: {str(e)}")
    
    return f"YouTube Video {video_id}"


def get_transcript(video_id, language_codes=['ko', 'en']):
    """
    YouTube 영상의 대본을 추출합니다.
    
    Args:
        video_id (str): YouTube video ID
        language_codes (list): 선호 언어 코드 리스트
        
    Returns:
        tuple: (transcript_data, language_used)
    """
    try:
        api = YouTubeTranscriptApi()
        
        # 선호 언어 순서대로 시도
        try:
            fetched_transcript = api.fetch(video_id, languages=language_codes)
            # 실제 사용된 언어 확인
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
            
        except Exception as e:
            print(f"❌ 대본 추출 중 오류 발생: {str(e)}")
            return None, None
                
    except TranscriptsDisabled:
        print("❌ 이 영상은 대본이 비활성화되어 있습니다.")
        return None, None
    except Exception as e:
        print(f"❌ 대본 추출 중 오류 발생: {str(e)}")
        return None, None


def format_transcript(transcript_data, video_url, language_used, video_title):
    """
    대본 데이터를 개선된 마크다운 형식으로 포맷팅합니다.
    
    Args:
        transcript_data (list): 대본 데이터
        video_url (str): 원본 YouTube URL
        language_used (str): 사용된 언어 코드
        video_title (str): 영상 제목
        
    Returns:
        str: 마크다운 형식의 대본
    """
    if not transcript_data:
        return ""
    
    # 개선된 헤더 생성 (체크박스 형태)
    source_type_checkboxes = "- [ ] book\n- [ ] post\n- [x] youtube"
    
    # 언어별 체크박스
    if language_used == 'ko':
        language_checkboxes = "- [x] korean\n- [ ] english\n- [ ] other"
    elif language_used == 'en':
        language_checkboxes = "- [ ] korean\n- [x] english\n- [ ] other"
    else:
        language_checkboxes = "- [ ] korean\n- [ ] english\n- [x] other"
    
    structure_type_checkboxes = "- [x] standalone\n- [ ] component"
    content_processing_checkboxes = "- [x] unified\n- [ ] segmented"
    
    header = f"""# {video_title}

**Source Type:**
{source_type_checkboxes}

**Source:** {video_url}

**Source Language:**
{language_checkboxes}

**Structure Type:**
{structure_type_checkboxes}

**Content Processing:**
{content_processing_checkboxes}

**Extracted Time:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
    
    # 대본 내용 포맷팅
    content_lines = []
    
    for entry in transcript_data:
        start_time = entry['start']
        duration = entry.get('duration', 0)
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


def save_to_markdown(content, filename):
    """
    내용을 마크다운 파일로 저장합니다.
    
    Args:
        content (str): 저장할 내용
        filename (str): 파일명
        
    Returns:
        bool: 저장 성공 여부
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {str(e)}")
        return False


def main():
    """
    메인 실행 함수
    """
    print("🎥 YouTube 대본 추출기 v2")
    print("=" * 50)
    
    # URL 입력받기
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = input("YouTube URL을 입력하세요: ").strip()
    
    if not video_url:
        print("❌ URL이 입력되지 않았습니다.")
        return
    
    # Video ID 추출
    video_id = extract_video_id(video_url)
    if not video_id:
        print("❌ 유효한 YouTube URL이 아닙니다.")
        return
    
    print(f"📺 Video ID: {video_id}")
    
    # 영상 제목 추출
    print("🔍 영상 제목 추출 중...")
    video_title = get_video_title(video_id)
    print(f"🎬 제목: {video_title}")
    
    # 대본 추출
    print("🔍 대본 추출 중...")
    transcript_data, language_used = get_transcript(video_id)
    
    if not transcript_data:
        print("❌ 대본을 추출할 수 없습니다.")
        return
    
    print(f"✅ 대본 추출 완료 (언어: {language_used})")
    print(f"📝 총 {len(transcript_data)}개의 대본 항목 발견")
    
    # 마크다운 포맷팅
    print("📄 마크다운 형식으로 변환 중...")
    markdown_content = format_transcript(transcript_data, video_url, language_used, video_title)
    
    # 파일명 생성 (날짜+순번+유튜브ID 방식)
    from datetime import datetime
    today = datetime.now().strftime("%y%m%d")
    
    # 기존 파일들을 확인해서 순번 결정
    import glob
    existing_files = glob.glob(f"{today}_*_{video_id}.md")
    if existing_files:
        # 동일한 비디오가 이미 존재하면 기존 파일명 사용
        filename = os.path.basename(existing_files[0])
        print(f"⚠️ 기존 파일 발견: {filename}")
    else:
        # 새로운 순번 결정
        existing_today = glob.glob(f"{today}_*.md")
        next_num = len(existing_today) + 1
        filename = f"{today}_{next_num:03d}_{video_id}.md"
    
    # 파일 저장
    print(f"💾 파일 저장 중: {filename}")
    if save_to_markdown(markdown_content, filename):
        print(f"✅ 성공적으로 저장되었습니다: {filename}")
    else:
        print("❌ 파일 저장에 실패했습니다.")


if __name__ == "__main__":
    main()