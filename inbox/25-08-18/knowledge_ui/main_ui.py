"""
생성 시간: 2025-08-18 (한국 시간)
핵심 내용: Knowledge Sherpa UI - YouTube 대본 추출 및 파일 처리를 위한 메인 UI
상세 내용:
    - KnowledgeUI: 메인 UI 클래스 (Tkinter 기반)
    - create_youtube_section(): YouTube URL 입력 및 처리 섹션
    - create_file_section(): 파일 선택 및 처리 섹션
    - create_result_section(): 결과 표시 섹션
    - handle_youtube_url(): YouTube URL 처리 핸들러
    - handle_file_selection(): 파일 선택 처리 핸들러
상태: 활성
주소: knowledge_ui/main_ui
참조: handlers/youtube_handler.py, handlers/file_handler.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from handlers.youtube_handler import YouTubeHandler
from handlers.file_handler import FileHandler


class KnowledgeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knowledge Sherpa UI")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 핸들러 초기화
        self.youtube_handler = YouTubeHandler()
        self.file_handler = FileHandler()
        
        # UI 생성
        self.create_widgets()
        
    def create_widgets(self):
        """UI 위젯들을 생성합니다."""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="Knowledge Sherpa", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # YouTube 섹션
        self.create_youtube_section(main_frame, row=1)
        
        # 구분선
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # 파일 처리 섹션
        self.create_file_section(main_frame, row=3)
        
        # 구분선
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # 결과 섹션
        self.create_result_section(main_frame, row=5)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def create_youtube_section(self, parent, row):
        """YouTube URL 처리 섹션을 생성합니다."""
        # 섹션 프레임
        youtube_frame = ttk.LabelFrame(parent, text="🎥 YouTube 대본 추출", padding="10")
        youtube_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # URL 입력
        ttk.Label(youtube_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(youtube_frame, width=60)
        self.url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.youtube_btn = ttk.Button(youtube_frame, text="대본 추출", 
                                     command=self.handle_youtube_url)
        self.youtube_btn.grid(row=1, column=1, sticky=tk.E)
        
        # 그리드 가중치
        youtube_frame.columnconfigure(0, weight=1)
        
    def create_file_section(self, parent, row):
        """파일 선택 및 처리 섹션을 생성합니다."""
        # 섹션 프레임
        file_frame = ttk.LabelFrame(parent, text="📁 파일 처리", padding="10")
        file_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 파일 선택
        ttk.Label(file_frame, text="파일 선택:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        file_info_frame = ttk.Frame(file_frame)
        file_info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.file_btn = ttk.Button(file_info_frame, text="파일 선택...", 
                                  command=self.handle_file_selection)
        self.file_btn.grid(row=0, column=0, sticky=tk.W)
        
        self.file_label = ttk.Label(file_info_frame, text="선택된 파일이 없습니다.", 
                                   foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # 파일 처리 버튼
        self.process_file_btn = ttk.Button(file_frame, text="파일 처리", 
                                          command=self.handle_file_processing,
                                          state="disabled")
        self.process_file_btn.grid(row=2, column=0, pady=(10, 0), sticky=tk.W)
        
        # 그리드 가중치
        file_frame.columnconfigure(0, weight=1)
        file_info_frame.columnconfigure(1, weight=1)
        
    def create_result_section(self, parent, row):
        """결과 표시 섹션을 생성합니다."""
        # 섹션 프레임
        result_frame = ttk.LabelFrame(parent, text="📄 처리 결과", padding="10")
        result_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 결과 텍스트 영역
        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, width=80)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 초기 메시지
        self.result_text.insert(tk.END, "처리 결과가 여기에 표시됩니다.\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # 그리드 가중치
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
    def handle_youtube_url(self):
        """YouTube URL 처리를 처리합니다."""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("경고", "YouTube URL을 입력해주세요.")
            return
            
        # UI 비활성화
        self.youtube_btn.config(state="disabled", text="처리 중...")
        self.add_result_message("🎥 YouTube 대본 추출 시작...")
        self.add_result_message(f"URL: {url}")
        
        # 별도 스레드에서 처리
        def process_youtube():
            try:
                result = self.youtube_handler.extract_transcript(url)
                
                # UI 업데이트는 메인 스레드에서
                self.root.after(0, lambda: self.youtube_process_complete(result))
                
            except Exception as e:
                self.root.after(0, lambda: self.youtube_process_error(str(e)))
        
        threading.Thread(target=process_youtube, daemon=True).start()
        
    def youtube_process_complete(self, result):
        """YouTube 처리 완료 시 호출됩니다."""
        self.youtube_btn.config(state="normal", text="대본 추출")
        
        if result['success']:
            self.add_result_message(f"✅ 대본 추출 완료!")
            self.add_result_message(f"파일 저장: {result['filename']}")
            self.add_result_message(f"언어: {result['language']}")
            self.add_result_message(f"대본 항목 수: {result['item_count']}")
        else:
            self.add_result_message(f"❌ 대본 추출 실패: {result['error']}")
            
        self.add_result_message("-" * 50)
        
    def youtube_process_error(self, error):
        """YouTube 처리 오류 시 호출됩니다."""
        self.youtube_btn.config(state="normal", text="대본 추출")
        self.add_result_message(f"❌ 처리 중 오류 발생: {error}")
        self.add_result_message("-" * 50)
        
    def handle_file_selection(self):
        """파일 선택을 처리합니다."""
        file_path = filedialog.askopenfilename(
            title="처리할 파일을 선택하세요",
            filetypes=[
                ("모든 파일", "*.*"),
                ("텍스트 파일", "*.txt"),
                ("마크다운 파일", "*.md"),
                ("PDF 파일", "*.pdf"),
                ("워드 문서", "*.docx"),
            ]
        )
        
        if file_path:
            self.selected_file_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"선택됨: {filename}", foreground="blue")
            self.process_file_btn.config(state="normal")
            
            self.add_result_message("📁 파일 선택됨:")
            self.add_result_message(f"파일명: {filename}")
            self.add_result_message(f"경로: {file_path}")
            self.add_result_message("-" * 50)
        
    def handle_file_processing(self):
        """선택된 파일 처리를 실행합니다."""
        if not hasattr(self, 'selected_file_path'):
            messagebox.showwarning("경고", "먼저 파일을 선택해주세요.")
            return
            
        self.add_result_message("🔄 파일 처리 시작...")
        
        # 파일 핸들러로 처리
        result = self.file_handler.process_file(self.selected_file_path)
        
        if result['success']:
            self.add_result_message("✅ 파일 처리 완료!")
            self.add_result_message(f"전달된 경로: {result['file_path']}")
            self.add_result_message(f"처리 메시지: {result['message']}")
        else:
            self.add_result_message(f"❌ 파일 처리 실패: {result['error']}")
            
        self.add_result_message("-" * 50)
        
    def add_result_message(self, message):
        """결과 영역에 메시지를 추가합니다."""
        self.result_text.insert(tk.END, f"{message}\n")
        self.result_text.see(tk.END)  # 자동 스크롤


def main():
    """메인 함수"""
    root = tk.Tk()
    app = KnowledgeUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()