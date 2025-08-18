"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: Knowledge Sherpa FastAPI 웹 애플리케이션 메인 파일
상세 내용:
    - FastAPI 앱 초기화 및 설정
    - 정적 파일 및 템플릿 설정
    - 메인 페이지 라우터
    - API 라우터 포함
    - CORS 설정
상태: 활성
주소: knowledge_web/app
참조: api/youtube.py, api/file_handler.py
"""

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import sys
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# API 라우터 import
from api.youtube import router as youtube_router
from api.file_handler import router as file_router

# FastAPI 앱 생성
app = FastAPI(
    title="Knowledge Sherpa",
    description="YouTube 대본 추출 및 파일 처리 웹 UI",
    version="1.0.0"
)

# CORS 설정 (개발용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 업로드 디렉토리 확인
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# API 라우터 포함
app.include_router(youtube_router, prefix="/api/youtube", tags=["YouTube"])
app.include_router(file_router, prefix="/api/file", tags=["File"])


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    """메인 페이지를 반환합니다."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """서버 상태를 확인합니다."""
    return {"status": "healthy", "message": "Knowledge Sherpa is running"}


# 파일 업로드 처리 (메인 앱에서 직접 처리)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    파일 업로드를 처리합니다.
    """
    try:
        # 업로드된 파일을 임시 저장
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 절대 경로 생성
        absolute_path = os.path.abspath(file_path)
        
        # 콘솔에 파일 경로 출력 (요구사항)
        print("=" * 60)
        print("📁 파일 업로드 완료")
        print("=" * 60)
        print(f"업로드된 파일: {file.filename}")
        print(f"저장 경로: {absolute_path}")
        print(f"파일 크기: {file.size} bytes" if file.size else "파일 크기: 알 수 없음")
        print(f"파일 타입: {file.content_type}")
        print("=" * 60)
        
        return {
            "success": True,
            "message": "파일이 성공적으로 업로드되었습니다.",
            "filename": file.filename,
            "file_path": absolute_path,
            "file_size": file.size,
            "content_type": file.content_type
        }
        
    except Exception as e:
        print(f"❌ 파일 업로드 오류: {str(e)}")
        return {
            "success": False,
            "error": f"파일 업로드 중 오류가 발생했습니다: {str(e)}"
        }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Knowledge Sherpa 웹 서버 시작 중...")
    print("📍 접속 주소: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)