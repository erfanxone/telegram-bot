from telethon import TelegramClient, events
import asyncio
import re
import os

# تنظیمات API تلگرام
API_ID = '23717113'
API_HASH = '208e450010e2002794c24cfab85590c0'
PHONE = os.getenv('PHONE_NUMBER', '')  # شماره موبایل از متغیرهای محیطی

# آیدی عددی کانال‌ها
SOURCE_CHANNELS = [-1001567904175]
DESTINATION_CHANNEL = -1002358831714

def process_text(text):
    if not text:
        return text
    
    # حذف لینک‌ها و یوزرنیم‌ها
    text = re.sub(r'https?://t\.me/\S+', '', text)
    text = re.sub(r't\.me/\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    
    # تغییر نام کانال
    text = text.replace('POSTED BY "MAK VIP SIGNALS"', 'POSTED BY "Dilek SIGNALS"')
    text = re.sub(r'mak', 'Dilek', text, flags=re.IGNORECASE)
    
    return text.strip()

async def main():
    try:
        # استفاده از StringSession برای ذخیره session
        client = TelegramClient('bot_session', API_ID, API_HASH)
        print("در حال اتصال به تلگرام...")
        
        # اتصال با شماره موبایل از پیش تعیین شده
        await client.start(phone=PHONE)
        print("اتصال برقرار شد!")

        @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
        async def handler(event):
            try:
                message = event.message
                
                if message.text:
                    message.text = process_text(message.text)
                
                if message.media and hasattr(message.media, 'caption') and message.media.caption:
                    message.media.caption = process_text(message.media.caption)
                
                await client.send_message(DESTINATION_CHANNEL, message)
                print("✅ پیام جدید ارسال شد")
                
            except Exception as e:
                print(f"❌ خطا در ارسال: {str(e)}")

        print("🔵 برنامه در حال اجراست...")
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"خطای کلی: {str(e)}")

if __name__ == '__main__':
    asyncio.run(main())
