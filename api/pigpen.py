# api/pigpen.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# 豬圈密碼標準映射表 (使用 Rune 符號作為視覺化展示)
# 這是標準的 3x3 網格、X 網格和點的組合。
PIGPEN_MAP = {
    # 3x3 網格
    'A': 'ᚱ', 'B': 'ᚢ', 'C': 'ᚦ',
    'D': 'ᚩ', 'E': 'ᚷ', 'F': 'ᚹ',
    'G': 'ᚻ', 'H': 'ᚾ', 'I': 'ᛁ',

    # 3x3 網格，帶點
    'J': 'ᛡ', 'K': 'ᛒ', 'L': 'ᛚ',
    'M': 'ᛘ', 'N': 'ᛝ', 'O': 'ᛠ',
    'P': 'ᛣ', 'Q': 'ᛦ', 'R': 'ᛤ',
    
    # X 網格
    'S': 'ᛥ', 'T': 'ᛗ', 'U': 'ᛐ', 'V': 'ᛓ',
    
    # X 網格，帶點
    'W': 'ᛁ', 'X': 'ᛩ', 'Y': 'ᛨ', 'Z': 'ᛪ',
}

# 反向映射表 (用於解密)
REVERSE_PIGPEN_MAP = {v: k for k, v in PIGPEN_MAP.items()}

def pigpen_cipher(text, mode="encrypt"):
    result = []
    
    if mode == "encrypt":
        # 加密：將字母轉換為符號
        for char in text.upper():
            # 使用 .get() 查找映射，如果找不到（非字母或空格），則保留原字符
            result.append(PIGPEN_MAP.get(char, char))
    elif mode == "decrypt":
        # 解密：將符號轉換為字母
        for char in text:
            # 查找反向映射，如果找不到（不是符號），則保留原字符
            result.append(REVERSE_PIGPEN_MAP.get(char, char))
            
    return "".join(result)

@app.route('/api/pigpen', methods=['POST'])
def handle_pigpen():
    """處理豬圈密碼的加密和解密請求。"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        # 豬圈密碼通常沒有 shift，但我們可以接受 mode
        mode = data.get('mode', 'encrypt')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        output = pigpen_cipher(text, mode)
        
        return jsonify({
            "success": True,
            "original_text": text,
            "mode": mode,
            "output_text": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500