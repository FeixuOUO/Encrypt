// script.js
document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const shiftValue = document.getElementById('shiftValue');
    const statusMessage = document.getElementById('statusMessage');

    // API URL 映射
    const API_URLS = {
        'caesar': '/api/caesar',
        'pigpen': '/api/pigpen'
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
        const apiUrl = API_URLS[cipher];
        
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

            const data = await response.json();

            if (response.ok && data.success) {
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
            statusMessage.textContent = `伺服器錯誤: ${error.message}`;
            statusMessage.style.color = '#dc3545';
        }
    }

    // 統一綁定所有按鈕的事件監聽器
    document.querySelectorAll('.control-panel button').forEach(button => {
        button.addEventListener('click', () => {
            const cipher = button.getAttribute('data-cipher');
            const mode = button.getAttribute('data-mode');
            handleCipher(cipher, mode);
        });
    });
});