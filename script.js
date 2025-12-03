// script.js
document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const shiftValue = document.getElementById('shiftValue');
    const encryptBtn = document.getElementById('encryptBtn');
    const decryptBtn = document.getElementById('decryptBtn');
    const statusMessage = document.getElementById('statusMessage');

    const CAESAR_API_URL = '/api/caesar'; // 這是 Vercel 上的 Serverless Function 路徑

    /**
     * 處理凱撒密碼的加密或解密請求
     * @param {string} mode - "encrypt" 或 "decrypt"
     */
    async function handleCaesar(mode) {
        statusMessage.textContent = '處理中...';
        statusMessage.style.color = '#ffc107'; // 黃色
        outputText.value = '';

        const text = inputText.value;
        const shift = parseInt(shiftValue.value);

        if (!text || isNaN(shift) || shift < 1 || shift > 25) {
            statusMessage.textContent = '錯誤：請輸入文本並確保偏移量在 1 到 25 之間。';
            statusMessage.style.color = '#dc3545'; // 紅色
            return;
        }

        try {
            const response = await fetch(CAESAR_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    shift: shift,
                    mode: mode
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                outputText.value = data.output_text;
                statusMessage.textContent = `${mode === 'encrypt' ? '加密' : '解密'}成功！使用偏移量：${data.shift}`;
                statusMessage.style.color = '#28a745'; // 綠色
            } else {
                // 處理 API 返回的錯誤
                throw new Error(data.error || 'API 處理失敗。');
            }

        } catch (error) {
            statusMessage.textContent = `伺服器錯誤: ${error.message}`;
            statusMessage.style.color = '#dc3545';
        }
    }

    // 綁定事件監聽器
    encryptBtn.addEventListener('click', () => handleCaesar('encrypt'));
    decryptBtn.addEventListener('click', () => handleCaesar('decrypt'));
});