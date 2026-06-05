from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import config

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rdfs.read(content_length) if hasattr(self, 'rdfs') else self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            event = data.get("event")
            
            print("\n---------------------------------------------")
            if event == "install":
                config.target_channel_id = data.get("channel_id")
                print(f"[🔔 REAL-TIME] มีคนใช้คำสั่ง [/ติดตั้ง] ในดิสคอร์ด!")
                print(f"[📍 LOCATION] ช่อง: {data.get('channel_name')} (ID: {config.target_channel_id})")
                print(f"[📍 USER] ผู้ใช้งาน: {data.get('user')}")
            elif event == "stop":
                config.target_channel_id = None
                print(f"[⚠️ WARNING] มีคนใช้คำสั่ง [/หยุดติดตั้ง] ตัวเชื่อมโยงถูกตัดออกแล้ว")
            print("---------------------------------------------\n")
            
            self.send_response(200)
            self.end_headers()
        except Exception:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        return # ซ่อน Log หน้าจอไม่ให้ขยะรกตา

def start_local_server():
    # เปิด Port 5000 ในเครื่องเพื่อรอรับข้อมูลแบบ Real-time จาก .js
    server = HTTPServer(('127.0.0.1', 5000), WebhookHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
  
