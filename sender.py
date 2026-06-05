import asyncio
import random
import string
import urllib.request
import json
import config

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_discord_message(token, channel_id, text):
    """ฟังก์ชันส่งข้อความแบบดึง API ตรงผ่าน HTTP ไม่ต้องออนบอทแช่"""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    
    # 1. ส่งข้อความสุ่มมั่วๆ
    rand_data = json.dumps({"content": generate_random_string()}).encode('utf-8')
    req1 = urllib.request.Request(url, data=rand_data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req1) as res1:
            res1_data = json.loads(res1.read().decode())
            first_msg_id = res1_data['id']
            
            # 2. ส่งข้อความ Reply หาอันแรก
            reply_data = json.dumps({
                "content": text,
                "message_reference": {"message_id": first_msg_id}
            }).encode('utf-8')
            req2 = urllib.request.Request(url, data=reply_data, headers=headers, method='POST')
            
            with urllib.request.urlopen(req2) as res2:
                # 3. สั่งลบข้อความแรกทันที
                del_url = f"{url}/{first_msg_id}"
                req_del = urllib.request.Request(del_url, headers=headers, method='DELETE')
                with urllib.request.urlopen(req_del) as _:
                    pass
            return True
    except Exception:
        return False

async def start_sending_process(count, message_text, mode):
    if not config.bot_token or not config.target_channel_id:
        print("\n[❌] ข้อผิดพลาด: ข้อมูล Token หรือ ID ช่องไม่ครบถ้วน (ต้องตรวจสอบบอทและใช้คำสั่งติดตั้งก่อน)")
        return

    if mode == 'n': delay = 0.1
    elif mode == 'g': delay = 0.5
    else: delay = 1.5

    print(f"\n🚀 เริ่มต้นทำงานส่งข้อความทั้งหมด {count} ครั้ง...")
    print("---------------------------------------------")

    for i in range(1, count + 1):
        # รันผ่าน Thread เพื่อไม่ให้บล็อคลูปหลักในการทำความเร็ว
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, send_discord_message, config.bot_token, config.target_channel_id, message_text)
        
        if success:
            print(f"{i}. ส่งข้อความสำเร็จ ✅")
        else:
            print(f"{i}. ส่งข้อความล้มเหลว ❌")
            
        await asyncio.sleep(delay)
        
    print("---------------------------------------------")
    print("✨ ทำงานตามจำนวนที่กำหนดเสร็จสิ้น!")
  
