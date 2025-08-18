"""
생성 시간: 2025-08-18 21:10:31 KST
핵심 내용: YouTube 대본을 주요 내용 단위로 그룹화하여 추출하는 개선된 스크립트
상세 내용:
    - extract_video_id(url): YouTube URL에서 video ID 추출
    - get_transcript(video_id, language_codes): 대본 추출 (한국어/영어 우선)
    - group_by_content_blocks(transcript_data, time_threshold): 내용 단위로 그룹화
    - clean_and_merge_sentences(text_block): 문장 정리 및 병합
    - format_grouped_transcript(grouped_data, video_url, language_used): 그룹화된 대본 포맷팅
    - save_to_markdown(content, filename): 마크다운 파일로 저장
    - main(): 메인 실행 함수
상태: 활성
주소: youtube_transcript_extractor_v2
참조: youtube_transcript_extractor
"""

import re
import sys
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


def group_by_content_blocks(transcript_data, time_threshold=15):
    """
    타임스탬프를 기준으로 내용을 의미있는 블록으로 그룹화합니다.
    
    Args:
        transcript_data (list): 대본 데이터
        time_threshold (int): 그룹화 기준 시간(초)
        
    Returns:
        list: 그룹화된 대본 블록들
    """
    if not transcript_data:
        return []
    
    grouped_blocks = []
    current_block = {
        'start_time': transcript_data[0]['start'],
        'end_time': transcript_data[0]['start'] + transcript_data[0].get('duration', 0),
        'texts': [transcript_data[0]['text']]
    }
    
    for i in range(1, len(transcript_data)):
        current_entry = transcript_data[i]
        time_gap = current_entry['start'] - current_block['end_time']
        
        # 시간 간격이 threshold보다 크거나, 블록이 너무 길면 새 블록 시작
        block_duration = current_block['end_time'] - current_block['start_time']
        
        if time_gap > time_threshold or block_duration > 45:  # 45초 이상이면 강제 분할
            # 현재 블록 완료
            grouped_blocks.append(current_block)
            
            # 새 블록 시작
            current_block = {
                'start_time': current_entry['start'],
                'end_time': current_entry['start'] + current_entry.get('duration', 0),
                'texts': [current_entry['text']]
            }
        else:
            # 현재 블록에 추가
            current_block['texts'].append(current_entry['text'])
            current_block['end_time'] = current_entry['start'] + current_entry.get('duration', 0)
    
    # 마지막 블록 추가
    if current_block['texts']:
        grouped_blocks.append(current_block)
    
    return grouped_blocks


def clean_and_merge_sentences(text_block):
    """
    텍스트 블록에서 불필요한 반복어를 제거하고 문장을 자연스럽게 병합합니다.
    
    Args:
        text_block (list): 텍스트 리스트
        
    Returns:
        str: 정리된 텍스트
    """
    # 텍스트 병합
    combined_text = ' '.join(text_block)
    
    # 불필요한 반복어 및 추임새 제거
    filler_words = [
        r'\b(um|uh|ah|you know|like|actually|basically|literally|right\?|okay\?|alright\?)\b',
        r'\b(well|so|now|then|but|and then|you see|I mean|let me|let\'s see)\b(?=\s)',
        r'\b(here\'s the thing|the thing is|what I\'m saying is)\b',
    ]
    
    cleaned_text = combined_text
    for pattern in filler_words:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
    
    # 중복 공백 제거
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # 문장 부호 정리
    cleaned_text = re.sub(r'\s+([.!?])', r'\1', cleaned_text)
    cleaned_text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', cleaned_text)
    
    # 불완전한 문장 처리
    sentences = re.split(r'[.!?]+', cleaned_text)
    complete_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10:  # 너무 짧은 문장 제외
            # 첫 글자 대문자화
            if sentence:
                sentence = sentence[0].upper() + sentence[1:]
                complete_sentences.append(sentence)
    
    return '. '.join(complete_sentences) + '.' if complete_sentences else ''


def format_grouped_transcript(grouped_data, video_url, language_used):
    """
    그룹화된 대본 데이터를 마크다운 형식으로 포맷팅합니다.
    
    Args:
        grouped_data (list): 그룹화된 대본 데이터
        video_url (str): 원본 YouTube URL
        language_used (str): 사용된 언어 코드
        
    Returns:
        str: 마크다운 형식의 대본
    """
    if not grouped_data:
        return ""
    
    # 헤더 생성
    header = f"""# YouTube 대본 (내용 단위 그룹화)

**영상 URL:** {video_url}
**추출 언어:** {language_used}
**추출 시간:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**처리 방식:** 주요 내용 단위로 그룹화 및 정리

---

"""
    
    # 대본 블록들 포맷팅
    content_blocks = []
    
    for i, block in enumerate(grouped_data, 1):
        start_time = block['start_time']
        end_time = block['end_time']
        
        # 시간을 분:초 형식으로 변환
        start_minutes = int(start_time // 60)
        start_seconds = int(start_time % 60)
        end_minutes = int(end_time // 60)
        end_seconds = int(end_time % 60)
        
        time_range = f"{start_minutes:02d}:{start_seconds:02d} - {end_minutes:02d}:{end_seconds:02d}"
        
        # 텍스트 정리
        cleaned_content = clean_and_merge_sentences(block['texts'])
        
        if cleaned_content:  # 빈 내용이 아닌 경우에만 추가
            block_content = f"## {time_range}\n{cleaned_content}\n"
            content_blocks.append(block_content)
    
    # 전체 내용 조합
    full_content = header + "\n".join(content_blocks)
    
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
    print("🎥 YouTube 대본 추출기 v2 (내용 단위 그룹화)")
    print("=" * 60)
    
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
    
    # 대본 추출
    print("🔍 대본 추출 중...")
    transcript_data, language_used = get_transcript(video_id)
    
    if not transcript_data:
        print("❌ 대본을 추출할 수 없습니다.")
        return
    
    print(f"✅ 대본 추출 완료 (언어: {language_used})")
    print(f"📝 총 {len(transcript_data)}개의 대본 항목 발견")
    
    # 내용 블록으로 그룹화
    print("🔄 내용 단위로 그룹화 중...")
    grouped_blocks = group_by_content_blocks(transcript_data, time_threshold=15)
    print(f"📋 {len(grouped_blocks)}개의 내용 블록으로 그룹화됨")
    
    # 마크다운 포맷팅
    print("📄 마크다운 형식으로 변환 중...")
    markdown_content = format_grouped_transcript(grouped_blocks, video_url, language_used)
    
    # 파일명 생성
    filename = f"youtube_transcript_{video_id}_grouped.md"
    
    # 파일 저장
    print(f"💾 파일 저장 중: {filename}")
    if save_to_markdown(markdown_content, filename):
        print(f"✅ 성공적으로 저장되었습니다: {filename}")
        print(f"📊 총 {len(grouped_blocks)}개의 내용 블록으로 구성됨")
    else:
        print("❌ 파일 저장에 실패했습니다.")


if __name__ == "__main__":
    main()