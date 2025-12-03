# api/caesar.py
from flask import Flask, request, jsonify

app = Flask(__name__)

def caesar_cipher(text, shift, mode="encrypt"):
    """
    執行凱撒密碼加密或解密。
    mode: "encrypt" (加密) 或 "decrypt" (解密)。
    """
    if mode == "decrypt":
        shift = -shift
    
    result = []
    
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            # 使用模數運算確保偏移量在 0-25 之間
            shifted_ord = (ord(char) - start + shift) % 26
            result.append(chr(shifted_ord + start))
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shifted_ord = (ord(char) - start + shift) % 26
            result.append(chr(shifted_ord + start))
        else:
            # 非字母字符（數字、符號、空格）保持不變
            result.append(char)
            
    return "".join(result)

@app.route('/api/caesar', methods=['POST'])
def handle_caesar():
    """Vercel 部署時，Vercel 會調用這個函式來處理 HTTP 請求。"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        shift = int(data.get('shift', 3)) # 預設偏移量為 3
        mode = data.get('mode', 'encrypt')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # 進行加密或解密
        output = caesar_cipher(text, shift, mode)
        
        return jsonify({
            "success": True,
            "original_text": text,
            "shift": shift,
            "mode": mode,
            "output_text": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 為了 Vercel 部署，通常只需要匯出 app 實例
# if __name__ == '__main__':
#     app.run(debug=True)