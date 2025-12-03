# api/index.py
from flask import Flask, request, jsonify
from api.caesar_logic import handle_caesar_request
from api.pigpen_logic import handle_pigpen_request
from flask_cors import CORS # 關鍵：導入 CORS 擴展

# Vercel 尋找的入口點必須是 'app'
app = Flask(__name__)
CORS(app) # 關鍵：為所有路由啟用 CORS

# 使用變數路由來捕獲所有對 /api/encrypt/ 的請求
@app.route('/api/encrypt/<cipher_type>', methods=['POST'])
def handle_encrypt(cipher_type):
    """主 API 處理器，根據 URL 路徑分發到不同的邏輯函數。"""
    
    if request.method != "POST":
        return jsonify({"error": "Method not allowed"}), 405
        
    try:
        data = request.get_json()
    except:
        # 處理空請求體或無效 JSON
        return jsonify({"error": "Invalid JSON data or empty request body"}), 400

    
    if cipher_type == 'caesar':
        response_data, status_code = handle_caesar_request(data)
    elif cipher_type == 'pigpen':
        response_data, status_code = handle_pigpen_request(data)
    else:
        # 如果路徑是 /api/encrypt/xxx，且 xxx 不是 caesar 或 pigpen
        return jsonify({"error": f"Unknown cipher type: {cipher_type}"}), 404
        
    # 返回 JSON 響應
    return jsonify(response_data), status_code

# -------------------------------------------------------------
# 為了避免 Vercel 找不到根 /api/，我們也定義一個簡單的根 API 狀態
@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({"status": "API is running", "available_ciphers": ["caesar", "pigpen"]}), 200
# -------------------------------------------------------------