# api/pigpen_logic.py
import json

PIGPEN_MAP = {
    'A': 'ᚱ', 'B': 'ᚢ', 'C': 'ᚦ', 'D': 'ᚩ', 'E': 'ᚷ', 'F': 'ᚹ',
    'G': 'ᚻ', 'H': 'ᚾ', 'I': 'ᛁ', 'J': 'ᛡ', 'K': 'ᛒ', 'L': 'ᛚ',
    'M': 'ᛘ', 'N': 'ᛝ', 'O': 'ᛠ', 'P': 'ᛣ', 'Q': 'ᛦ', 'R': 'ᛤ',
    'S': 'ᛥ', 'T': 'ᛗ', 'U': 'ᛐ', 'V': 'ᛓ', 'W': 'ᛁ', 'X': 'ᛩ', 
    'Y': 'ᛨ', 'Z': 'ᛪ',
}
REVERSE_PIGPEN_MAP = {v: k for k, v in PIGPEN_MAP.items()}

def pigpen_cipher_logic(text, mode="encrypt"):
    """執行豬圈密碼加密或解密的核心邏輯。"""
    result = []
    if mode == "encrypt":
        for char in text.upper():
            result.append(PIGPEN_MAP.get(char, char))
    elif mode == "decrypt":
        for char in text:
            result.append(REVERSE_PIGPEN_MAP.get(char, char))
            
    return "".join(result)

def handle_pigpen_request(data):
    """處理 Pigpen API 請求的數據轉換與返回。"""
    text = data.get('text', '')
    mode = data.get('mode', 'encrypt')
    
    if not text:
        return {"error": "No text provided"}, 400
    
    output = pigpen_cipher_logic(text, mode)
    
    return {
        "success": True,
        "original_text": text,
        "mode": mode,
        "output_text": output
    }, 200