# api/caesar_logic.py
import json

def caesar_cipher_logic(text, shift, mode="encrypt"):
    """執行凱撒密碼加密或解密的核心邏輯。"""
    if mode == "decrypt":
        shift = -shift
    
    result = []
    
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shifted_ord = (ord(char) - start + shift) % 26
            result.append(chr(shifted_ord + start))
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_ord = (ord(char) - start + shift) % 26
            result.append(chr(shifted_ord + start))
        else:
            result.append(char)
            
    return "".join(result)

def handle_caesar_request(data):
    """處理 Caesar API 請求的數據轉換與返回。"""
    text = data.get('text', '')
    shift = int(data.get('shift', 3))
    mode = data.get('mode', 'encrypt')
    
    if not text:
        return {"error": "No text provided"}, 400
    
    output = caesar_cipher_logic(text, shift, mode)
    
    return {
        "success": True,
        "original_text": text,
        "shift": shift,
        "mode": mode,
        "output_text": output
    }, 200