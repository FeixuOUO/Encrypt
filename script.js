// script.js
document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const shiftValue = document.getElementById('shiftValue');
    const statusMessage = document.getElementById('statusMessage');

    // 關鍵修正：新的 API URL 映射，匹配 vercel.json 的單一入口路由
    const API_URLS = {
        'caesar': '/api/encrypt/caesar',
        'pigpen': '/api/encrypt/pigpen'
    };

    /**
     * 發送請求到對應的 Serverless API
     * @param {string} cipher - 'caesar' 或 'pigpen'
     * @param {string} mode - 'encrypt' 或 'decrypt'
     */
    async function handleCipher(cipher, mode) {
        statusMessage.textContent = '處理中...';
        statusMessage.style.color = '#ffc107'; 
        outputText.value = '';

        const text = inputText.value;
        const apiUrl = API_URLS[cipher]; // 使用新的正確路徑
        
        if (!text) {
            statusMessage.textContent = '錯誤：請輸入文本。';
            statusMessage.style.color = '#dc3545';
            return;
        }

        let requestBody = {
            text: text,
            mode: mode
        };
        
        // 針對凱撒密碼，需要額外添加 shift 參數
        if (cipher === 'caesar') {
            const shift = parseInt(shiftValue.value);
            if (isNaN(shift) || shift < 1 || shift > 25) {
                statusMessage.textContent = '錯誤：凱撒偏移量需在 1 到 25 之間。';
                statusMessage.style.color = '#dc3545';
                return;
            }
            requestBody.shift = shift;
        }

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            // 檢查 HTTP 狀態碼
            if (response.status === 404) {
                 throw new Error(`API 終點 ${apiUrl} 未找到 (404)。請檢查 Vercel 路由。`);
            }
            if (!response.ok) {
                 const errorData = await response.json().catch(() => ({error: '無法解析 API 錯誤響應'}));
                 throw new Error(errorData.error || `HTTP 錯誤：${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                outputText.value = data.output_text;
                let msg = `${cipher.charAt(0).toUpperCase() + cipher.slice(1)} ${mode === 'encrypt' ? '加密' : '解密'}成功！`;
                if (cipher === 'caesar') {
                    msg += ` 使用偏移量：${data.shift}`;
                }
                statusMessage.textContent = msg;
                statusMessage.style.color = '#28a745'; 
            } else {
                throw new Error(data.error || 'API 處理失敗。');
            }

        } catch (error) {
            // 服務器錯誤或 JSON 解析錯誤
            statusMessage.textContent = `伺服器錯誤: ${error.message}`;
            statusMessage.style.color = '#dc3545';
        }
    }

    // 統一綁定所有按鈕的事件監聽器
    document.querySelectorAll('.control-panel button').forEach(button => {
        button.addEventListener('click', () => {
            // 從 data-* 屬性中獲取 cipher 和 mode
            const cipher = button.getAttribute('data-cipher');
            const mode = button.getAttribute('data-mode');
            if (cipher && mode) {
                 handleCipher(cipher, mode);
            }
        });
    });
});