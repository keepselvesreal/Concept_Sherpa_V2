문제 상황

  현재 상황을 보자:
  - 설정 파일: ../extraction-system/references (상대 경로)
  - 스크립트 위치: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-27/supplementary_context_analyzer.py
  - 터미널 실행 위치: /home/nadle/projects/Knowledge_Sherpa/v2/ (프로젝트 루트)

  상대 경로 계산의 차이

  1. 현재 작업 디렉토리(CWD) 기준 (문제 상황)

  # 터미널에서 실행할 때
  pwd  # /home/nadle/projects/Knowledge_Sherpa/v2/

  이때 ../extraction-system/references를 계산하면:
  - /home/nadle/projects/Knowledge_Sherpa/v2/../extraction-system/references
  - = /home/nadle/projects/Knowledge_Sherpa/extraction-system/references ❌

  2. 스크립트 디렉토리 기준 (올바른 방법)

  script_dir = Path(__file__).parent  # /home/nadle/projects/Knowledge_Sherpa/v2/25-08-27/
  folder_path = script_dir / "../extraction-system/references"

  이때 계산 결과:
  - /home/nadle/projects/Knowledge_Sherpa/v2/25-08-27/../extraction-system/references
  - = /home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/references ✅

  왜 이런 일이 발생하나?

  Python의 상대 경로 해석 규칙

  Python에서 Path("../extraction-system/references")처럼 상대 경로를 사용하면:
  - 기본적으로 현재 작업 디렉토리(CWD)를 기준으로 해석
  - 스크립트가 있는 디렉토리와는 무관

  실제 예시

  import os
  from pathlib import Path

  # 터미널에서 /home/nadle/projects/Knowledge_Sherpa/v2/ 에서 실행할 때
  print("현재 작업 디렉토리:", os.getcwd())
  # 출력: /home/nadle/projects/Knowledge_Sherpa/v2/

  print("스크립트 디렉토리:", Path(__file__).parent)
  # 출력: /home/nadle/projects/Knowledge_Sherpa/v2/25-08-27/

  # 문제가 되는 방식 (CWD 기준)
  bad_path = Path("../extraction-system/references")
  print("잘못된 경로:", bad_path.resolve())
  # 출력: /home/nadle/projects/Knowledge_Sherpa/extraction-system/references ❌

  # 올바른 방식 (스크립트 디렉토리 기준)
  script_dir = Path(__file__).parent
  good_path = script_dir / "../extraction-system/references"
  print("올바른 경로:", good_path.resolve())
  # 출력: /home/nadle/projects/Knowledge_Sherpa/v2/extraction-system/references ✅

  왜 IndividualDocumentProcessor는 작동했나?

  IndividualDocumentProcessor를 다시 보면:

  # IndividualDocumentProcessor에서
  ref_config = self.config.get('references', {})
  folder_path = Path(ref_config.get('folder_path', './references'))

  if not folder_path.is_absolute():
      folder_path = self.script_dir / folder_path  # 스크립트 디렉토리 기준으로 계산

  여기서는 self.script_dir를 사용해서 스크립트 디렉토리 기준으로 계산했어. 그런데
  supplementary_context_analyzer에서는 이 로직이 빠져있었던 거야.

  수정한 코드의 의미

  # 상대 경로인 경우 스크립트 디렉토리 기준으로 절대 경로 계산
  if not folder_path.is_absolute():
      script_dir = Path(__file__).parent  # 스크립트가 있는 디렉토리
      folder_path = script_dir / folder_path  # 스크립트 기준으로 상대 경로 계산

  이렇게 하면:
  - 어떤 디렉토리에서 스크립트를 실행하든
  - 항상 스크립트 파일 기준으로 상대 경로를 계산
  - 일관된 결과를 얻을 수 있어

  왜 이게 중요한가?

  1. 일관성: 어디서 실행하든 같은 결과
  2. 이식성: 다른 환경에서도 동일하게 작동
  3. 예측 가능성: 설정 파일의 경로가 스크립트 기준으로 해석됨