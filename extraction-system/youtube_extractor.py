# 생성 시간: 2025-08-21 15:45:32 KST
# 핵심 내용: YouTube 스크립트 추출기 - extraction-system 통합용 모듈
# 상세 내용:
#   - extract_video_id(url): YouTube URL에서 video ID 추출
#   - get_video_title(video_id): YouTube 영상 제목 추출  
#   - get_transcript(video_id, language_codes): 대본 추출 (한국어/영어 우선)
#   - format_transcript(transcript_data, video_url, language_used, video_title): 마크다운 형식으로 포맷팅
#   - save_to_markdown(content, filename): 마크다운 파일로 저장
#   - process_youtube_url(url): 메인 처리 함수 - URL 입력부터 파일 저장까지
# 상태: active
# 참조: youtube_transcript_extractor_v3.py

import re
import os
import json
import requests
import glob
from datetime import datetime
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
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        title_pattern = r'<title>([^<]+)</title>'
        match = re.search(title_pattern, response.text)
        
        if match:
            title = match.group(1)
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
        
        try:
            fetched_transcript = api.fetch(video_id, languages=language_codes)
            used_language = fetched_transcript.language_code
            
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
    대본 데이터를 간단한 마크다운 형식으로 포맷팅합니다.
    (메타정보는 metadata.json에 있으므로 제목, 추출시간, 내용만 포함)
    
    Args:
        transcript_data (list): 대본 데이터
        video_url (str): 원본 YouTube URL (사용하지 않음, 호환성 유지)
        language_used (str): 사용된 언어 코드 (사용하지 않음, 호환성 유지)
        video_title (str): 영상 제목
        
    Returns:
        str: 마크다운 형식의 대본
    """
    if not transcript_data:
        return ""
    
    header = f"""# {video_title}

**Extracted Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
    
    content_lines = []
    
    for entry in transcript_data:
        start_time = entry['start']
        text = entry['text'].strip()
        
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        time_stamp = f"[{minutes:02d}:{seconds:02d}]"
        
        if text:
            content_lines.append(f"{time_stamp} {text}")
    
    full_content = header + "\n".join(content_lines)
    
    return full_content


def save_to_markdown(content, filepath):
    """
    내용을 마크다운 파일로 저장합니다.
    
    Args:
        content (str): 저장할 내용
        filepath (str): 파일 전체 경로
        
    Returns:
        bool: 저장 성공 여부
    """
    try:
        # 디렉토리 생성
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {str(e)}")
        return False


def process_youtube_url(url, base_upload_dir=".", target_folder=None, metadata=None):
    """
    YouTube URL을 처리하여 스크립트를 추출하고 개별 폴더에 저장합니다.
    
    Args:
        url (str): YouTube URL
        base_upload_dir (str): 기본 업로드 디렉토리
        target_folder (str): 대상 폴더 경로 (지정하면 해당 폴더 사용)
        metadata (dict): 메타데이터 정보 (있으면 개별 폴더에 저장)
        
    Returns:
        dict: 처리 결과 정보
    """
    result = {
        "success": False,
        "message": "",
        "file_info": None,
        "video_info": None
    }
    
    # Video ID 추출
    video_id = extract_video_id(url)
    if not video_id:
        result["message"] = "유효한 YouTube URL이 아닙니다."
        return result
    
    # 영상 제목 추출
    video_title = get_video_title(video_id)
    
    # 대본 추출
    transcript_data, language_used = get_transcript(video_id)
    
    if not transcript_data:
        result["message"] = "대본을 추출할 수 없습니다."
        return result
    
    # 마크다운 포맷팅
    markdown_content = format_transcript(transcript_data, url, language_used, video_title)
    
    # 폴더 경로 결정
    if target_folder:
        # 지정된 폴더 사용 (YouTube_250822 같은 날짜 폴더)
        date_folder_path = target_folder
        # 해당 날짜 폴더 안에 비디오 ID 폴더 생성
        video_folder_path = os.path.join(date_folder_path, video_id)
        folder_name = video_id
    else:
        # 기존 방식: 날짜별 폴더 생성 후 그 안에 비디오 ID 폴더 생성
        today = datetime.now().strftime("%y%m%d")
        date_folder_name = f"YouTube_{today}"
        date_folder_path = os.path.join(base_upload_dir, date_folder_name)
        video_folder_path = os.path.join(date_folder_path, video_id)
        folder_name = video_id
    
    # 비디오 ID 폴더 생성
    os.makedirs(video_folder_path, exist_ok=True)
    
    # 파일명은 transcript.md로 고정
    filename = "transcript.md"
    filepath = os.path.join(video_folder_path, filename)
    
    # 파일 저장
    if save_to_markdown(markdown_content, filepath):
        # 메타데이터가 있으면 개별 폴더에 저장
        if metadata:
            metadata_path = os.path.join(video_folder_path, "metadata.json")
            try:
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"⚠️ 메타데이터 저장 오류: {str(e)}")
        
        result["success"] = True
        result["message"] = "YouTube 스크립트가 성공적으로 추출되었습니다."
        result["file_info"] = {
            "filename": filename,
            "folder": folder_name,
            "full_path": filepath,
            "video_folder_path": video_folder_path,
            "size": len(markdown_content.encode('utf-8'))
        }
        result["video_info"] = {
            "video_id": video_id,
            "title": video_title,
            "language": language_used,
            "transcript_count": len(transcript_data)
        }
    else:
        result["message"] = "파일 저장에 실패했습니다."
    
    return result