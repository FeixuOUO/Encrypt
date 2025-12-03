# api/pigpen.py
from http.server import BaseHTTPRequestHandler
import json
from vercel_sdk import Response, Request # 假設 Vercel 提供的 SDK 存在

# --- 核心邏輯 ---
PIGPEN_MAP = {
    'A': 'ᚱ', 'B': 'ᚢ', 'C': 'ᚦ', 'D': 'ᚩ', 'E': 'ᚷ', 'F': 'ᚹ',
    'G': 'ᚻ', 'H': 'ᚾ', 'I': 'ᛁ', 'J': 'ᛡ', 'K': 'ᛒ', 'L': 'ᛚ',
    'M': 'ᛘ', 'N': 'ᛝ', 'O': 'ᛠ', 'P': 'ᛣ', 'Q': 'ᛦ', 'R': 'ᛤ',
    'S': 'ᛥ', 'T': 'ᛗ', 'U': 'ᛐ', 'V': 'ᛓ', 'W': 'ᛁ', 'X': 'ᛩ', 
    'Y': 'ᛨ', 'Z': 'ᛪ',
}

# 反向映射表 (用於解密)
REVERSE_PIGPEN_MAP = {v: k for k, v in PIGPEN_MAP.items()}

def pigpen_cipher(text, mode="encrypt"):
    result = []
    
    if mode == "encrypt":
        for char in text.upper():
            result.append(PIGPEN_MAP.get(char, char))
    elif mode == "decrypt":
        for char in text:
            result.append(REVERSE_PIGPEN_MAP.get(char, char))
            
    return "".join(result)

# --- Vercel Edge Function 入口點 ---

def handler(request):
    """Vercel Python Edge Function 的標準入口點。"""

    if request.method != "POST":
        return Response("Method Not Allowed. Only POST is supported.", status=405)

    try:
        data = request.json()
        text = data.get('text', '')
        mode = data.get('mode', 'encrypt')
        
        if not text:
            return Response.json({"error": "No text provided"}, status=400)
        
        output = pigpen_cipher(text, mode)
        
        return Response.json({
            "success": True,
            "original_text": text,
            "mode": mode,
            "output_text": output
        }, status=200)

    except Exception as e:
        return Response.json({"error": f"Internal Server Error: {str(e)}"}, status=500)