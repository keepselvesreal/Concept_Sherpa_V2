"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: 파일 처리 API 엔드포인트 - 파일 정보 조회 및 로그 관리
상세 내용:
    - get_file_info(): 업로드된 파일 정보 조회
    - get_processing_log(): 파일 처리 로그 조회
    - clear_uploads(): 업로드 파일 정리
    - 파일 유효성 검사 및 메타데이터 추출
상태: 활성
주소: knowledge_web/api/file_handler
참조: ../knowledge_ui/handlers/file_handler.py
"""

from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
import os
import shutil
from datetime import datetime
from pathlib import Path

router = APIRouter()

# 디렉토리 설정
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'processed_files')
LOG_FILE = os.path.join(OUTPUT_DIR, 'file_processing_log.txt')

# 디렉토리 생성
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


class FileInfoResponse(BaseModel):
    success: bool
    filename: str
    file_path: str
    file_size: int
    content_type: str
    modified_time: str
    message: str


def get_file_metadata(file_path: str) -> dict:
    """파일의 메타데이터를 추출합니다."""
    try:
        stat_info = os.stat(file_path)
        filename = os.path.basename(file_path)
        name, extension = os.path.splitext(filename)
        
        return {
            'filename': filename,
            'name': name,
            'extension': extension.lower() if extension else '',
            'size_bytes': stat_info.st_size,
            'size_mb': stat_info.st_size / (1024 * 1024),
            'modified_time': datetime.fromtimestamp(stat_info.st_mtime),
            'created_time': datetime.fromtimestamp(stat_info.st_ctime),
            'absolute_path': os.path.abspath(file_path)
        }
        
    except Exception as e:
        return {
            'filename': os.path.basename(file_path),
            'error': f'메타데이터 추출 실패: {str(e)}'
        }


def log_file_processing(file_path: str, file_info: dict):
    """파일 처리 내역을 로그 파일에 기록합니다."""
    try:
        log_entry = f"""
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 파일 처리 로그 (웹 UI)
파일 경로: {file_path}
파일명: {file_info.get('filename', 'Unknown')}
파일 크기: {file_info.get('size_mb', 0):.2f} MB
확장자: {file_info.get('extension', 'Unknown')}
처리 상태: 성공 (업로드 및 경로 전달 완료)
처리 방식: FastAPI 웹 인터페이스
{'=' * 80}
"""
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
    except Exception as e:
        print(f"⚠️ 로그 기록 실패: {str(e)}")


@router.get("/info/{filename}")
async def get_file_info(filename: str):
    """
    업로드된 파일의 정보를 조회합니다.
    
    - **filename**: 조회할 파일명
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"파일을 찾을 수 없습니다: {filename}"
            )
        
        # 파일 메타데이터 추출
        file_metadata = get_file_metadata(file_path)
        
        if 'error' in file_metadata:
            raise HTTPException(
                status_code=500,
                detail=file_metadata['error']
            )
        
        # 콘솔에 파일 정보 출력
        print("=" * 60)
        print("📄 파일 정보 조회")
        print("=" * 60)
        print(f"파일명: {file_metadata['filename']}")
        print(f"절대 경로: {file_metadata['absolute_path']}")
        print(f"크기: {file_metadata['size_mb']:.2f} MB")
        print(f"확장자: {file_metadata['extension']}")
        print(f"수정 시간: {file_metadata['modified_time']}")
        print("=" * 60)
        
        # 로그 기록
        log_file_processing(file_path, file_metadata)
        
        return {
            "success": True,
            "filename": file_metadata['filename'],
            "file_path": file_metadata['absolute_path'],
            "file_size": file_metadata['size_bytes'],
            "size_mb": file_metadata['size_mb'],
            "extension": file_metadata['extension'],
            "modified_time": file_metadata['modified_time'].isoformat(),
            "message": "파일 정보 조회 완료"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 파일 정보 조회 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"파일 정보 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/log")
async def get_processing_log():
    """
    파일 처리 로그를 조회합니다.
    """
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            return {
                "success": True,
                "log_content": log_content,
                "log_file": LOG_FILE,
                "message": "로그 조회 완료"
            }
        else:
            return {
                "success": True,
                "log_content": "로그 파일이 없습니다.",
                "log_file": LOG_FILE,
                "message": "로그 파일 없음"
            }
            
    except Exception as e:
        print(f"❌ 로그 조회 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"로그 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/uploads")
async def list_uploaded_files():
    """
    업로드된 파일 목록을 조회합니다.
    """
    try:
        files = []
        
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    file_metadata = get_file_metadata(file_path)
                    if 'error' not in file_metadata:
                        files.append({
                            'filename': filename,
                            'size_mb': file_metadata['size_mb'],
                            'extension': file_metadata['extension'],
                            'modified_time': file_metadata['modified_time'].isoformat()
                        })
        
        return {
            "success": True,
            "files": files,
            "count": len(files),
            "upload_dir": UPLOAD_DIR,
            "message": f"{len(files)}개의 업로드된 파일을 찾았습니다."
        }
        
    except Exception as e:
        print(f"❌ 파일 목록 조회 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"파일 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.delete("/uploads/{filename}")
async def delete_uploaded_file(filename: str):
    """
    업로드된 파일을 삭제합니다.
    
    - **filename**: 삭제할 파일명
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"파일을 찾을 수 없습니다: {filename}"
            )
        
        os.remove(file_path)
        
        print(f"🗑️ 파일 삭제됨: {filename}")
        
        return {
            "success": True,
            "filename": filename,
            "message": "파일이 성공적으로 삭제되었습니다."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 파일 삭제 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"파일 삭제 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/clear-uploads")
async def clear_all_uploads():
    """
    모든 업로드된 파일을 삭제합니다.
    """
    try:
        deleted_files = []
        
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_files.append(filename)
        
        print(f"🧹 {len(deleted_files)}개 파일 삭제 완료")
        
        return {
            "success": True,
            "deleted_files": deleted_files,
            "count": len(deleted_files),
            "message": f"{len(deleted_files)}개의 파일이 삭제되었습니다."
        }
        
    except Exception as e:
        print(f"❌ 파일 정리 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"파일 정리 중 오류가 발생했습니다: {str(e)}"
        )