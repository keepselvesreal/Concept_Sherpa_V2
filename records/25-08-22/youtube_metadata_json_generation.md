# 유튜브 URL 메타정보 추출 및 JSON 생성 기능 구현

## goal
extraction-system에서 사용자가 유튜브 URL 입력 시 UI의 메타정보를 기반으로 JSON 파일을 생성하는 기능 구현

## Expected_outcomes
- 사용자가 유튜브 URL 입력 후 전송 버튼 클릭 시 메타정보 JSON 파일 생성
- JSON 파일이 '/home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/YouTube_250822' 형태의 폴더에 저장
- 기존 스크립트 추출 기능이 생성된 폴더를 활용하도록 수정

## success_criteria
- 유튜브 URL 입력 → 전송 → JSON 파일 생성까지 전체 플로우가 정상 작동
- 생성된 JSON에 UI의 모든 메타정보 필드가 포함됨
- 폴더 생성 로직이 JSON 파일 생성 시점으로 변경됨
- 스크립트 추출 시 기존 생성된 폴더 활용

## context
- 기존 스크립트를 extraction-system으로 통합하는 작업 중
- 현재 URL 입력 시 스크립트 추출 후 저장되는 구조
- UI에 있는 메타정보 필드를 그대로 JSON 구조로 활용
- 예시 메타정보: source_type, source_language, structure_type, content_processing
- UI 파일 위치: /home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/index.html

## process_log
- 2025-08-22 09:30: JSON 생성 기능 구현 완료
  - metadata_manager.py 별도 모듈 생성
  - server.py에서 JSON 모듈 사용하도록 수정  
  - index.html UI 응답 처리 추가
- 2025-08-22 09:45: 연속 처리 기능 구현 완료
  - youtube_extractor.py에 target_folder 파라미터 추가
  - server.py에서 JSON 생성 → 스크립트 추출 연속 처리
  - UI에서 완료/부분처리/실패 상태별 메시지 처리
- 2025-08-22 09:50: 스크립트 파일 형식 단순화
  - format_transcript 함수에서 메타정보 체크박스 제거
  - 제목 + Source URL + Extracted Time + 내용만 포함
  - 메타정보는 metadata.json 파일에서 관리
- 다음 단계: 전체 플로우 테스트 필요