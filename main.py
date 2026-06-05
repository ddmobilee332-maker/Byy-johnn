import asyncio
import sys
import config
from logo import BANNER
from checker import check_bot_status
from sender import start_sending_process
from server import start_local_server

async def main_menu():
    config.clear_screen()
    print("Welcome to Termux Project Launcher")
    input("\n📥 กด [Enter] เพื่อส่งข้อมูลและเริ่มต้นรันโปรเจค...")
    
    config.clear_screen()
    print(BANNER)
    
    # สั่งเปิดเซิร์ฟเวอร์หลังบ้านเพื่อรอรับแจ้งเตือน Real-time ทันที
    start_local_server()
    
    while True:
        print("\n⚡ [ เมนูคำสั่งควบคุม (Termux) ] ⚡")
        print("1. oopp  - ตรวจสอบสถานะและดึงข้อมูลบอท (ดึงข้อมูลอย่างเดียว ไม่เปิดออน)")
        print("2. oopp2 - ตั้งค่าการยิงข้อความมั่วสลับตอบกลับและลบ")
        print("3. exit  - ออกจากโปรแกรม")
        
        choice = input("\nเลือกคำสั่งหลักที่ต้องการทำ: ").strip()
        
        if choice == "oopp":
            token = input("\n🔑 กรุณาใส่ Token Bot เพื่อตรวจสอบ: ").strip()
            if not token:
                print("❌ Token ห้ามว่าง!")
                continue
            
            print("🔍 กำลังดึงข้อมูลและตรวจเช็คสถานะ...")
            res = check_bot_status(token)
            
            if res["success"]:
                config.bot_token = token
                print("\n=============================================")
                print(f"📊 รายละเอียดของบอทที่ตรวจพบ:")
                print(f"🎈 ชื่อบอท: {res['name']}")
                print(f"🆔 ID บอท: {res['id']}")
                print(f"🟢 สถานะ: {res['status']}")
                print("=============================================")
                print("✅ บันทึก Token ลงในระบบดึงข้อมูลเรียบร้อย!")
            else:
                print(f"\n❌ ตรวจสอบล้มเหลว โทเคนอาจไม่ถูกต้อง หรือบอทไม่ได้เปิดใช้งาน (Error: {res['error']})")
                
        elif choice == "oopp2":
            if not config.bot_token:
                print("\n❌ กรุณาใส่ Token และกดเช็คสเตตัสด้วยคำสั่ง oopp ก่อนค่ะ!")
                continue
            if not config.target_channel_id:
                print("\n❌ ยังไม่มีข้อมูลช่องปลายทาง! (กรุณาเปิดรันไฟล์ bot.js และกดยิงคำสั่ง /ติดตั้ง ในดิสคอร์ดก่อน)")
                continue
                
            try:
                count = int(input("\n🔢 ใส่จำนวนครั้งที่จะส่งข้อความ: ").strip())
            except ValueError:
                print("❌ กรุณาใส่เฉพาะตัวเลขเท่านั้น!")
                continue
                
            msg_text = input("✍️ ใส่ข้อความที่ต้องการส่ง (ใส่ได้ทุกรูปแบบ): ")
            
            print("\n📋 เลือกโหมดความเร็วสำหรับการทำงาน:")
            print("- [ n ] : โหมดรัว (เร็วสุดขีด ดีเลย์ 0.1 วินาที)")
            print("- [ g ] : โหมดแรง (ความเร็วระดับกลาง ดีเลย์ 0.5 วินาที)")
            print("- [ a ] : โหมดเบา (เรื่อยๆ สบายๆ ดีเลย์ 1.5 วินาที)")
            
            mode = input("👉 พิมพ์ตัวเลือก (n / g / a): ").strip().lower()
            if mode not in ['n', 'g', 'a']:
                mode = 'a'
                
            await start_sending_process(count, msg_text, mode)
            
        elif choice == "exit":
            print("\nปิดการทำงานโปรแกรม. ขอบคุณค่ะคุณพี่!")
            sys.exit()

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print("\n\nปิดการทำงานโปรแกรม.")
          
