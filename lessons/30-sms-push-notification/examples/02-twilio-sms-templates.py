"""
Misol 02: Twilio SMS Shablonlar Bilan
======================================

Bu misolda quyidagilar ko'rsatiladi:
- SMS shablonlarini yaratish
- Shablon o'zgaruvchilaridan foydalanish
- Dinamik xabar yaratish
- Turli xabar turlari (xush kelibsiz, eslatma, ogohlantirish)

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
from datetime import datetime, timedelta


class SMSShablon:
    """SMS Shablon tizimi"""
    
    # Shablon ta'riflari
    SHABLONLAR = {
        'xush_kelibsiz': """
Salom {ism}!

Kutubxona Tizimiga xush kelibsiz! Sizning akkauntingiz muvaffaqiyatli yaratildi.

Foydalanuvchi: {username}
Email: {email}

Hoziroq kolleksiyamizni ko'rishni boshlang!
        """.strip(),
        
        'kitob_olindi': """
Kitob Olindi

Salom {ism},

Siz ushbu kitobni oldingiz: "{kitob_nomi}"
Muallif: {muallif}

Qaytarish Muddati: {muddat}
Kechikish to'lovlaridan qochish uchun o'z vaqtida qaytaring.

Yaxshi o'qishlar!
        """.strip(),
        
        'muddat_eslatma': """
Eslatma: Kitob Muddati Yaqinlashmoqda

Salom {ism},

Sizning "{kitob_nomi}" kitobingiz {qolgan_kunlar} kundan keyin muddati tugaydi.

Muddat: {muddat}

Iltimos, o'z vaqtida qaytaring.
        """.strip(),
        
        'muddati_otgan': """
MUDDATI O'TGAN OGOHLANTIRISH

Salom {ism},

Sizning "{kitob_nomi}" kitobingiz {otgan_kunlar} kun kechikdi!

Kechikish To'lovi: ${tolov}

Iltimos, zudlik bilan qaytaring.
        """.strip(),
        
        'tasdiqlash': """
Tasdiqlash Kodi

Sizning Kutubxona Tizimi tasdiqlash kodingiz:

{kod}

Bu kod {daqiqalar} daqiqada amal qiladi.

Bu kodni hech kimga bermang.
        """.strip()
    }
    
    @classmethod
    def render(cls, shablon_nomi, kontekst):
        """
        Shablonni kontekst bilan render qilish
        
        Args:
            shablon_nomi (str): Shablon nomi (xush_kelibsiz, kitob_olindi, va h.k.)
            kontekst (dict): Shablon o'zgaruvchilari
            
        Returns:
            str: Render qilingan xabar
        """
        shablon = cls.SHABLONLAR.get(shablon_nomi)
        
        if not shablon:
            raise ValueError(f"Shablon '{shablon_nomi}' topilmadi")
        
        try:
            return shablon.format(**kontekst)
        except KeyError as e:
            raise ValueError(f"Shablon o'zgaruvchisi yetishmayapti: {e}")


class TwilioSMSShablonlar:
    """Shablonlar bilan Twilio SMS yuboruvchi"""
    
    def __init__(self):
        """Twilio clientini ishga tushirish"""
        self.account_sid = config('TWILIO_ACCOUNT_SID')
        self.auth_token = config('TWILIO_AUTH_TOKEN')
        self.from_number = config('TWILIO_PHONE_NUMBER')
        
        self.client = Client(self.account_sid, self.auth_token)
        print("✓ Twilio SMS Shablonlari ishga tushdi")
    
    def shablon_sms_yuborish(self, qabul_qiluvchi, shablon_nomi, kontekst):
        """
        Shablon yordamida SMS yuborish
        
        Args:
            qabul_qiluvchi (str): Qabul qiluvchi telefon raqami
            shablon_nomi (str): Shablon nomi
            kontekst (dict): Shablon o'zgaruvchilari
            
        Returns:
            dict: Xabar tafsilotlari yoki None
        """
        try:
            # Shablonni render qilish
            xabar_matni = SMSShablon.render(shablon_nomi, kontekst)
            
            # SMS yuborish
            message = self.client.messages.create(
                body=xabar_matni,
                from_=self.from_number,
                to=qabul_qiluvchi
            )
            
            print(f"\n✓ SMS yuborildi ({shablon_nomi})")
            print(f"  SID: {message.sid}")
            print(f"  Kimga: {qabul_qiluvchi}")
            print(f"\n📱 Xabar Ko'rinishi:")
            print("-" * 40)
            print(xabar_matni)
            print("-" * 40)
            
            return {
                'sid': message.sid,
                'status': message.status,
                'template': shablon_nomi
            }
            
        except ValueError as e:
            print(f"\n✗ Shablon xatosi: {str(e)}")
            return None
            
        except TwilioRestException as e:
            print(f"\n✗ Twilio xatosi: {e.msg}")
            return None


def main():
    """Asosiy misol funksiyasi"""
    
    print("=" * 50)
    print("Twilio SMS Shablonlar Misoli")
    print("=" * 50)
    
    # Ishga tushirish
    sms = TwilioSMSShablonlar()
    
    # Test uchun telefon raqamingiz
    test_raqam = "+998901234567"  # O'z raqamingizni qo'ying!
    
    # Misol 1: Xush kelibsiz SMS
    print("\n--- Misol 1: Xush Kelibsiz SMS ---")
    xush_kelibsiz_kontekst = {
        'ism': 'Jasur Aliyev',
        'username': 'jasur_aliyev',
        'email': 'jasur@example.com'
    }
    sms.shablon_sms_yuborish(test_raqam, 'xush_kelibsiz', xush_kelibsiz_kontekst)
    
    # Misol 2: Kitob Olingan SMS
    print("\n--- Misol 2: Kitob Olingan SMS ---")
    kitob_kontekst = {
        'ism': 'Jasur',
        'kitob_nomi': 'Ikki Eshik Orasi',
        'muallif': 'O\'tkir Hoshimov',
        'muddat': (datetime.now() + timedelta(days=14)).strftime('%d %B, %Y')
    }
    sms.shablon_sms_yuborish(test_raqam, 'kitob_olindi', kitob_kontekst)
    
    # Misol 3: Muddat Eslatma SMS
    print("\n--- Misol 3: Muddat Eslatma SMS ---")
    eslatma_kontekst = {
        'ism': 'Jasur',
        'kitob_nomi': 'Ikki Eshik Orasi',
        'qolgan_kunlar': 3,
        'muddat': (datetime.now() + timedelta(days=3)).strftime('%d %B, %Y')
    }
    sms.shablon_sms_yuborish(test_raqam, 'muddat_eslatma', eslatma_kontekst)
    
    # Misol 4: Muddati O'tgan SMS
    print("\n--- Misol 4: Muddati O'tgan Ogohlantirish SMS ---")
    muddati_otgan_kontekst = {
        'ism': 'Jasur',
        'kitob_nomi': 'Ikki Eshik Orasi',
        'otgan_kunlar': 5,
        'tolov': 5.00
    }
    sms.shablon_sms_yuborish(test_raqam, 'muddati_otgan', muddati_otgan_kontekst)
    
    # Misol 5: Tasdiqlash Kodi SMS
    print("\n--- Misol 5: Tasdiqlash Kodi SMS ---")
    tasdiqlash_kontekst = {
        'kod': '123456',
        'daqiqalar': 10
    }
    sms.shablon_sms_yuborish(test_raqam, 'tasdiqlash', tasdiqlash_kontekst)
    
    # Misol 6: Xatolarni boshqarish - yetishmayotgan o'zgaruvchi
    print("\n--- Misol 6: Yetishmayotgan O'zgaruvchi Xatosi ---")
    noto_liq_kontekst = {
        'ism': 'Jasur'
        # 'kitob_nomi', 'qolgan_kunlar', 'muddat' yetishmayapti
    }
    sms.shablon_sms_yuborish(test_raqam, 'muddat_eslatma', noto_liq_kontekst)
    
    print("\n" + "=" * 50)
    print("Misollar tugadi!")
    print("=" * 50)


if __name__ == "__main__":
    # Foydalanish:
    # 1. .env faylini Twilio kredensiallar bilan yarating
    # 2. test_raqam ni o'z telefoningizga o'zgartiring
    # 3. Ishga tushiring: python 02-twilio-sms-templates.py
    
    main()


"""
Kutilayotgan Natija:
====================

==================================================
Twilio SMS Shablonlar Misoli
==================================================
✓ Twilio SMS Shablonlari ishga tushdi

--- Misol 1: Xush Kelibsiz SMS ---

✓ SMS yuborildi (xush_kelibsiz)
  SID: SM1234...
  Kimga: +998901234567

Xabar Ko'rinishi:
----------------------------------------
Salom Jasur Aliyev!

Kutubxona Tizimiga xush kelibsiz! Sizning akkauntingiz muvaffaqiyatli yaratildi.

Foydalanuvchi: jasur_aliyev
Email: jasur@example.com

Hoziroq kolleksiyamizni ko'rishni boshlang!
----------------------------------------


Shablon Eng Yaxshi Amaliyotlar:
================================

1. Xabarlarni qisqa saqlang (iloji bo'lsa 160 belgidan kam)
2. Aniq, harakatga yo'naltirilgan til ishlating
3. Vizual joziba uchun tegishli emojilardan foydalaning
4. Har doim muhim ma'lumotni qo'shing
5. Shaxsiy qiling (qabul qiluvchining ismini ishlating)
6. Aniq harakat chaqiruvini bering
7. Shablonlarni haqiqiy ma'lumotlar bilan test qiling

SMS Uzunlik Yo'riqnomalari:
============================
- Bitta SMS: 160 belgi
- Birlashtirilgan SMS: segmentiga 153 belgi
- Unicode (emojilar): segmentiga 70 belgi

Belgilar soni narx uchun muhim!

Shablon O'zgaruvchilari Maslahatlari:
======================================
- Ta'riflovchi o'zgaruvchi nomlaridan foydalaning
- Render qilishdan oldin kontekstni tekshiring
- Iloji bo'lsa default qiymatlar bering
- Yetishmayotgan o'zgaruvchilarni yaxshi boshqaring
- Turli ma'lumot kombinatsiyalari bilan test qiling

Dinamik Kontent Misollari:
===========================
- Joriy sana/vaqt
- Hisoblangan qiymatlar (kunlar, to'lovlar)
- Foydalanuvchiga xos ma'lumotlar
- Shartli xabarlar
- Mahalliy kontent
"""