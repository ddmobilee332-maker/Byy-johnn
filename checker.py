import urllib.request
import json

def check_bot_status(token):
    """ดึงข้อมูลจาก Discord Gateway ตรงๆ เพื่อเช็คข้อมูลบอทและสถานะออนไลน์"""
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": f"Bot {token}"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            # ดึงเกตเวย์มาตรวจสอบดูว่าระบบเปิดรับเครือข่ายบอทตัวนี้ไหม (เป็นการเช็คว่าโทเคนพร้อมใช้)
            gw_url = "https://discord.com/api/v10/gateway/bot"
            gw_req = urllib.request.Request(gw_url, headers=headers)
            
            try:
                with urllib.request.urlopen(gw_req) as gw_res:
                    gw_data = json.loads(gw_res.read().decode())
                    # ถ้าดึงผ่านแสดงว่าบอทพร้อมใช้งานระบบเซิร์ฟเวอร์
                    status_str = "ONLINE / READY (บอทเปิดระบบใช้งานได้)"
            except:
                status_str = "UNKNOWN (Token ถูกต้องแต่ไม่สามารถดึงเกตเวย์ได้)"

            return {
                "success": True,
                "name": data.get("username"),
                "id": data.get("id"),
                "status": status_str
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
      
