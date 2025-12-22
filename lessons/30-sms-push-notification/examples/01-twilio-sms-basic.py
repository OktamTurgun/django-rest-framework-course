"""
Misol 01: Twilio SMS Asoslari
==============================

Bu misolda quyidagilar ko'rsatiladi:
- Asosiy Twilio sozlash va konfiguratsiya
- Oddiy SMS xabari yuborish
- Xatolarni boshqarish
- Xabar holatini tekshirish

Talablar:
    pip install twilio python-decouple

Muhit O'zgaruvchilari (.env):
    TWILIO_ACCOUNT_SID=sizning_account_sid
    TWILIO_AUTH_TOKEN=sizning_auth_token
    TWILIO_PHONE_NUMBER=+998901234567
"""

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from decouple import config


class TwilioSMSAsoslari:
    """Asosiy Twilio SMS yuboruvchi"""
    
    def __init__(self):
        """Twilio clientini ishga tushirish"""
        # Kredensiallarni muhit o'zgaruvchilaridan olish
        self.account_sid = config('TWILIO_ACCOUNT_SID')
        self.auth_token = config('TWILIO_AUTH_TOKEN')
        self.from_number = config('TWILIO_PHONE_NUMBER')
        
        # Twilio clientini yaratish
        self.client = Client(self.account_sid, self.auth_token)
        
        print("✓ Twilio client ishga tushdi")
    
    def sms_yuborish(self, qabul_qiluvchi_raqam, xabar):
        """
        Telefon raqamiga SMS yuborish
        
        Args:
            qabul_qiluvchi_raqam (str): Qabul qiluvchi telefon raqami (E.164 format: +998901234567)
            xabar (str): Xabar matni (max 1600 belgi)
            
        Returns:
            dict: Xabar tafsilotlari yoki xatolik bo'lsa None
        """
        try:
            # SMS yuborish
            message = self.client.messages.create(
                body=xabar,
                from_=self.from_number,
                to=qabul_qiluvchi_raqam
            )
            
            print(f"\n✓ SMS muvaffaqiyatli yuborildi!")
            print(f"  SID: {message.sid}")
            print(f"  Holat: {message.status}")
            print(f"  Kimga: {message.to}")
            print(f"  Kimdan: {message.from_}")
            
            return {
                'sid': message.sid,
                'status': message.status,
                'to': message.to,
                'from': message.from_,
                'date_sent': message.date_sent
            }
            
        except TwilioRestException as e:
            print(f"\n✗ Twilio xatosi: {e.msg}")
            print(f"  Xato kodi: {e.code}")
            return None
            
        except Exception as e:
            print(f"\n✗ Kutilmagan xato: {str(e)}")
            return None
    
    def xabar_holatini_tekshirish(self, message_sid):
        """
        Yuborilgan xabar holatini tekshirish
        
        Args:
            message_sid (str): Yuborish vaqtida qaytarilgan xabar SID
            
        Returns:
            str: Xabar holati (queued, sent, delivered, failed, va h.k.)
        """
        try:
            message = self.client.messages(message_sid).fetch()
            
            print(f"\nXabar Holati:")
            print(f"  SID: {message.sid}")
            print(f"  Holat: {message.status}")
            print(f"  Yuborilgan Sana: {message.date_sent}")
            print(f"  Narx: {message.price} {message.price_unit}")
            print(f"  Xato: {message.error_message or 'Yo\'q'}")
            
            return message.status
            
        except TwilioRestException as e:
            print(f"\n✗ Holatni tekshirishda xato: {e.msg}")
            return None


def main():
    """Asosiy misol funksiyasi"""
    
    print("=" * 50)
    print("Twilio SMS Asoslari Misoli")
    print("=" * 50)
    
    # SMS yuboruvchini ishga tushirish
    sms = TwilioSMSAsoslari()
    
    # Misol 1: Oddiy SMS yuborish
    print("\n--- Misol 1: Oddiy SMS Yuborish ---")
    qabul_qiluvchi = "+998901234567"  # O'z raqamingizni qo'ying!
    xabar_matni = "Salom Python'dan! Bu Twilio'dan test SMS."
    
    natija = sms.sms_yuborish(qabul_qiluvchi, xabar_matni)
    
    if natija:
        # Misol 2: Xabar holatini tekshirish
        print("\n--- Misol 2: Xabar Holatini Tekshirish ---")
        import time
        time.sleep(2)  # 2 soniya kutish
        sms.xabar_holatini_tekshirish(natija['sid'])
    
    # Misol 3: Xatolarni boshqarish - noto'g'ri raqam
    print("\n--- Misol 3: Xatolarni Boshqarish ---")
    noto_gri_raqam = "noto'g'ri"
    sms.sms_yuborish(noto_gri_raqam, "Bu xato beradi")
    
    print("\n" + "=" * 50)
    print("Misol tugadi!")
    print("=" * 50)


if __name__ == "__main__":
    # Foydalanish:
    # 1. .env faylini Twilio kredensiallar bilan yarating
    # 2. Telefon raqamini o'zingizniki bilan almashtiring
    # 3. Ishga tushiring: python 01-twilio-sms-basic.py
    
    main()


"""
Kutilayotgan Natija:
====================

==================================================
Twilio SMS Asoslari Misoli
==================================================
✓ Twilio client ishga tushdi

--- Misol 1: Oddiy SMS Yuborish ---

✓ SMS muvaffaqiyatli yuborildi!
  SID: SM1234567890abcdef
  Holat: queued
  Kimga: +998901234567
  Kimdan: +1234567890

--- Misol 2: Xabar Holatini Tekshirish ---

Xabar Holati:
  SID: SM1234567890abcdef
  Holat: sent
  Yuborilgan Sana: 2024-12-21 10:30:45
  Narx: -0.0075 USD
  Xato: Yo'q

--- Misol 3: Xatolarni Boshqarish ---

✗ Twilio xatosi: 'To' raqami noto'g'ri haqiqiy telefon raqami emas.
  Xato kodi: 21211

==================================================
Misol tugadi!
==================================================


Twilio Xabar Holatlari:
========================
- queued: Xabar yuborish uchun navbatda
- sending: Xabar yuborilmoqda
- sent: Xabar operatorga yuborildi
- delivered: Xabar qabul qiluvchiga yetib bordi
- undelivered: Xabar yetib bormadi
- failed: Xabar yuborishda xatolik


Telefon Raqami Formati:
========================
Har doim E.164 formatidan foydalaning: +[mamlakat kodi][raqam]

Misollar:
- AQSh: +1234567890
- Buyuk Britaniya: +441234567890
- O'zbekiston: +998901234567


Narx Ma'lumoti:
===============
- SMS narxi mamlakatga qarab o'zgaradi
- AQSh/Kanada: ~$0.0075 har bir SMS
- Xalqaro: o'zgaruvchan ($0.01 - $0.10)
- Twilio narxlarini tekshiring: https://www.twilio.com/sms/pricing


Bepul Sinov Cheklovlari:
=========================
- $15 bepul kredit
- Faqat tasdiqlangan raqamlarga yuborish mumkin
- To'liq funksionallik uchun yangilash kerak
"""