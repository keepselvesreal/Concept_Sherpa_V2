// Knowledge Sherpa JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // DOM 요소들
    const youtubeForm = document.getElementById('youtube-form');
    const fileForm = document.getElementById('file-form');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileBtn = document.getElementById('file-btn');
    const results = document.getElementById('results');
    const clearBtn = document.getElementById('clear-results');

    // 파일 선택 처리
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            fileInfo.innerHTML = `
                <strong>선택된 파일:</strong> ${file.name}<br>
                <strong>크기:</strong> ${formatFileSize(file.size)}<br>
                <strong>타입:</strong> ${file.type || '알 수 없음'}
            `;
            fileInfo.classList.add('show');
            fileBtn.disabled = false;
            
            addResult('info', `파일 선택됨: ${file.name} (${formatFileSize(file.size)})`);
        } else {
            fileInfo.classList.remove('show');
            fileBtn.disabled = true;
        }
    });

    // YouTube 폼 처리
    youtubeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const url = document.getElementById('youtube-url').value.trim();
        if (!url) {
            addResult('error', 'YouTube URL을 입력해주세요.');
            return;
        }

        const btn = document.getElementById('youtube-btn');
        const btnText = btn.querySelector('span');
        const loading = btn.querySelector('.loading');
        
        // 버튼 상태 변경
        btn.disabled = true;
        btnText.textContent = '처리 중...';
        loading.style.display = 'block';
        
        addResult('info', `YouTube 대본 추출 시작: ${url}`);
        
        try {
            const response = await fetch('/api/youtube/extract', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });
            
            const data = await response.json();
            
            if (data.success) {
                addResult('success', 
                    `✅ 대본 추출 완료!\n` +
                    `파일: ${data.filename}\n` +
                    `언어: ${data.language}\n` +
                    `항목 수: ${data.item_count}개`
                );
            } else {
                addResult('error', `❌ 대본 추출 실패: ${data.error}`);
            }
        } catch (error) {
            addResult('error', `❌ 요청 실패: ${error.message}`);
        } finally {
            // 버튼 상태 복원
            btn.disabled = false;
            btnText.textContent = '대본 추출';
            loading.style.display = 'none';
        }
    });

    // 파일 폼 처리
    fileForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            addResult('error', '파일을 선택해주세요.');
            return;
        }

        const btn = document.getElementById('file-btn');
        const btnText = btn.querySelector('span');
        const loading = btn.querySelector('.loading');
        
        // 버튼 상태 변경
        btn.disabled = true;
        btnText.textContent = '처리 중...';
        loading.style.display = 'block';
        
        addResult('info', `파일 처리 시작: ${file.name}`);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                addResult('success', 
                    `✅ 파일 처리 완료!\n` +
                    `파일명: ${data.filename}\n` +
                    `저장 경로: ${data.file_path}\n` +
                    `크기: ${formatFileSize(data.file_size || 0)}\n` +
                    `타입: ${data.content_type || '알 수 없음'}\n\n` +
                    `💡 콘솔에서 파일 경로 확인 가능!`
                );
            } else {
                addResult('error', `❌ 파일 처리 실패: ${data.error}`);
            }
        } catch (error) {
            addResult('error', `❌ 요청 실패: ${error.message}`);
        } finally {
            // 버튼 상태 복원
            btn.disabled = true; // 파일 다시 선택해야 함
            btnText.textContent = '파일 처리';
            loading.style.display = 'none';
        }
    });

    // 결과 지우기
    clearBtn.addEventListener('click', function() {
        results.innerHTML = `
            <div class="result-item">
                <div class="result-timestamp">초기화 시간: ${new Date().toLocaleString('ko-KR')}</div>
                <div class="result-content">결과가 지워졌습니다.</div>
            </div>
        `;
    });

    // 유틸리티 함수들
    function addResult(type, message) {
        const resultItem = document.createElement('div');
        resultItem.className = `result-item result-${type}`;
        
        resultItem.innerHTML = `
            <div class="result-timestamp">${new Date().toLocaleString('ko-KR')}</div>
            <div class="result-content">${message}</div>
        `;
        
        results.insertBefore(resultItem, results.firstChild);
        
        // 스크롤을 맨 위로
        results.scrollTop = 0;
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // URL 유효성 검사
    document.getElementById('youtube-url').addEventListener('input', function(e) {
        const url = e.target.value;
        const isValid = isYouTubeUrl(url);
        
        if (url && !isValid) {
            e.target.style.borderColor = '#e53e3e';
        } else {
            e.target.style.borderColor = '#e2e8f0';
        }
    });

    function isYouTubeUrl(url) {
        const patterns = [
            /(?:youtube\.com\/watch\?v=)([^&\n?#]+)/,
            /(?:youtube\.com\/embed\/)([^&\n?#]+)/,
            /(?:youtu\.be\/)([^&\n?#]+)/,
            /(?:youtube\.com\/v\/)([^&\n?#]+)/
        ];
        
        return patterns.some(pattern => pattern.test(url));
    }
});