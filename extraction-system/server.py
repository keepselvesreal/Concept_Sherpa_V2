# 생성 시간: 2025-08-27 12:12 KST
# 핵심 내용: 리팩토링된 FastAPI 서버 - 4단계 개선 적용 (extraction-system 적용)
# 상세 내용:
#   - app = FastAPI(): FastAPI 인스턴스 생성 (라인 22)
#   - /: HTML 페이지 서빙 엔드포인트 (라인 27-30)
#   - /upload: 리팩토링된 업로드 처리 엔드포인트 (라인 45-85)
#   - is_youtube_url(): YouTube URL 검증 함수 (라인 32-43)
#   - YouTubePipeline 통합: 단순화된 파이프라인 실행
# 상태: active
# 주소: server (리팩토링 적용)
# 참조: server_old.py → 4단계 리팩토링 적용

import os
import re
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Union

# 리팩토링된 파이프라인 임포트
from pipeline.youtube_pipeline import YouTubePipeline

app = FastAPI()

# uploads 디렉토리 생성
os.makedirs("uploads", exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """메인 페이지 서빙"""
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


def is_youtube_url(url: str) -> bool:
    """YouTube URL 여부 판별"""
    youtube_patterns = [
        r'(?:youtube\.com/watch\?v=)',
        r'(?:youtube\.com/embed/)',
        r'(?:youtu\.be/)',
        r'(?:youtube\.com/v/)'
    ]
    
    for pattern in youtube_patterns:
        if re.search(pattern, url):
            return True
    return False


@app.post("/upload")
async def upload_file(
    file: Union[UploadFile, None] = File(None),
    text_data: Union[str, None] = Form(None),
    source_type: Union[str, None] = Form(None),
    source_language: Union[str, None] = Form(None),
    structure_type: Union[str, None] = Form(None),
    content_processing: Union[str, None] = Form(None)
):
    """리팩토링된 업로드 처리 엔드포인트"""
    
    # 파일 처리 (기존과 동일)
    result = {}
    if file and file.filename:
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        print(f"📁 파일 업로드됨: {file.filename} ({len(contents)} bytes)")
        result["file_info"] = {
            "filename": file.filename,
            "size": len(contents),
            "content_type": file.content_type,
            "saved_path": file_path
        }
    
    # YouTube URL 처리 (리팩토링된 버전)
    if text_data and text_data.strip():
        if is_youtube_url(text_data.strip()):
            print(f"🎥 YouTube URL 감지: {text_data}")
            
            # 메타정보 구성
            metadata_info = {
                "source_type": source_type or "youtube",
                "source_language": source_language or "korean", 
                "structure_type": structure_type or "standalone",
                "content_processing": content_processing or "unified"
            }
            
            # 🚀 리팩토링된 파이프라인 실행
            try:
                pipeline = YouTubePipeline()
                pipeline_result = await pipeline.execute(text_data.strip(), metadata_info)
                
                if pipeline_result.is_success:
                    # ✅ 성공 응답 (단순화됨)
                    print("🎉 전체 파이프라인 완료!")
                    result.update({
                        "type": "pipeline_success",
                        "status": "success",
                        "data": pipeline_result.data,
                        "progress": {
                            "completed_steps": pipeline_result.step_completed,
                            "total_steps": pipeline_result.total_steps,
                            "progress_percent": pipeline_result.progress_percent
                        }
                    })
                else:
                    # ❌ 실패 응답 (단순화됨)
                    print(f"❌ 파이프라인 실패: {pipeline_result.error}")
                    result.update({
                        "type": "pipeline_failed",
                        "status": "failed",
                        "error": pipeline_result.error,
                        "progress": {
                            "completed_steps": pipeline_result.step_completed,
                            "total_steps": pipeline_result.total_steps,
                            "progress_percent": pipeline_result.progress_percent
                        }
                    })
                
            except Exception as e:
                # 예상치 못한 오류
                error_msg = f"파이프라인 실행 중 오류: {str(e)}"
                print(f"❌ {error_msg}")
                result.update({
                    "type": "pipeline_error",
                    "status": "error", 
                    "error": error_msg
                })
        
        else:
            # 일반 텍스트 처리
            print(f"📝 텍스트 데이터 수신: {text_data}")
            result.update({
                "type": "text",
                "text_data": text_data
            })
    
    # 아무 데이터도 없는 경우
    if not file and not text_data:
        print("⚠️ 파일이나 텍스트 데이터가 없습니다.")
        result.update({
            "type": "no_data",
            "message": "파일이나 텍스트를 입력해주세요."
        })
    
    return result


if __name__ == "__main__":
    import uvicorn
    print("🚀 리팩토링된 서버 시작")
    print("📊 개선 사항:")
    print("  - subprocess 제거 → 직접 함수 호출")
    print("  - 복잡한 에러 처리 → 단순한 성공/실패")
    print("  - 동기/비동기 혼재 → async/await 통일") 
    print("  - 모놀리식 구조 → 파이프라인 클래스화")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)