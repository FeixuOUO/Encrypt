# api/index.py
from flask import Flask, request, jsonify
from api.caesar_logic import handle_caesar_request
from api.pigpen_logic import handle_pigpen_request

# Vercel 尋找的入口點必須是 'app'
app = Flask(__name__)

# 使用變數路由來捕獲所有對 /api/encrypt/ 的請求
@app.route('/api/encrypt/<cipher_type>', methods=['POST'])
def handle_encrypt(cipher_type):
    """主 API 處理器，根據 URL 路徑分發到不同的邏輯函數。"""
    
    if request.method != "POST":
        return jsonify({"error": "Method not allowed"}), 405
        
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Invalid JSON data"}), 400

    
    if cipher_type == 'caesar':
        response_data, status_code = handle_caesar_request(data)
    elif cipher_type == 'pigpen':
        response_data, status_code = handle_pigpen_request(data)
    else:
        return jsonify({"error": f"Unknown cipher type: {cipher_type}"}), 404
        
    return jsonify(response_data), status_code

# -------------------------------------------------------------
# 為了避免 Vercel 找不到根 /api/，我們也定義一個簡單的根 API 狀態
@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({"status": "API is running", "available_ciphers": ["caesar", "pigpen"]}), 200
# -------------------------------------------------------------