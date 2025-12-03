# api/caesar.py
from http.server import BaseHTTPRequestHandler
import json
from vercel_sdk import Response, Request # 假設 Vercel 提供的 SDK 存在 (雖然在實際 Edge Function 運行時是隱式提供的)

# --- 核心邏輯 (與 Flask 版本相同) ---

def caesar_cipher(text, shift, mode="encrypt"):
    """執行凱撒密碼加密或解密。"""
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

# --- Vercel Edge Function 入口點 ---

def handler(request):
    """Vercel Python Edge Function 的標準入口點。"""
    
    # 1. 檢查請求方法
    if request.method != "POST":
        return Response("Method Not Allowed. Only POST is supported.", status=405)

    try:
        # 2. 從 request.json() 獲取 JSON 數據
        data = request.json()
        text = data.get('text', '')
        shift = int(data.get('shift', 3))
        mode = data.get('mode', 'encrypt')
        
        if not text:
            return Response.json({"error": "No text provided"}, status=400)
        
        # 3. 處理加密
        output = caesar_cipher(text, shift, mode)
        
        # 4. 返回 JSON 響應
        return Response.json({
            "success": True,
            "original_text": text,
            "shift": shift,
            "mode": mode,
            "output_text": output
        }, status=200)

    except Exception as e:
        # 返回 500 內部錯誤
        return Response.json({"error": f"Internal Server Error: {str(e)}"}, status=500)