# 臨時 api/caesar.py (Vercel 官方最簡範例)
from http.server import BaseHTTPRequestHandler
from urllib import parse

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # 設置 HTTP 狀態碼
        self.send_response(200)
        # 設置返回內容類型
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # 寫入返回內容
        message = "Hello from Vercel Python!"
        self.wfile.write(message.encode())
        return

# 備註：如果是 Flask 應用，Vercel 只需要 app = Flask(__name__) 即可。

# 如果您仍然想用 Flask，請確保它是：
# from flask import Flask, jsonify
# app = Flask(__name__)
# @app.route('/api/caesar')
# def handle_test():
#     return jsonify({"message": "Flask test success!"})