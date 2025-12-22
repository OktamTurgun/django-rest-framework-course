"""
Misol 05: Yagona Bildirishnoma Menejeri
========================================

Bu misolda quyidagilar ko'rsatiladi:
- Email, SMS va Push uchun yagona interfeys
- Foydalanuvchi bildirishnoma sozlamalari
- Ko'p kanalli yetkazish
- Yetkazilishni kuzatish va loglash
- Xatolarni boshqarish va qayta urinish mantiqи

Talablar:
    pip install twilio firebase-admin python-decouple

Bu oldingi misollardan tushunchalarni ishlab chiqarishga tayyor
bildirishnoma boshqaruv tizimiga birlashtiradi.
"""

from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials, messaging
from decouple import config
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import json


class BildirishnomaTuri(Enum):
    """Bildirishnoma turlari"""
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'


class BildirishnomаHolati(Enum):
    """Yetkazilish holati"""
    KUTILMOQDA = 'kutilmoqda'
    YUBORILDI = 'yuborildi'
    YETKAZILDI = 'yetkazildi'
    XATO = 'xato'
    QAYTA_URINILMOQDA = 'qayta_urinilmoqda'


@dataclass
class FoydalanuvchiSozlamalari:
    """Foydalanuvchi bildirishnoma sozlamalari"""
    foydalanuvchi_id: str
    email_yoqilgan: bool = True
    sms_yoqilgan: bool = True
    push_yoqilgan: bool = True
    sokin_soatlar_boshi: Optional[str] = None  # "22:00"
    sokin_soatlar_oxiri: Optional[str] = None    # "08:00"


@dataclass
class BildirishnomаLog:
    """Bildirishnoma yetkazilish logi"""
    bildirishnoma_id: str
    foydalanuvchi_id: str
    tur: BildirishnomaTuri
    holat: BildirishnomаHolati
    sarlavha: str
    xabar: str
    yuborilgan_vaqt: datetime
    yetkazilgan_vaqt: Optional[datetime] = None
    xato: Optional[str] = None


class BildirishnomaMenejeri:
    """
    Email, SMS va Push uchun yagona bildirishnoma menejeri
    """
    
    def __init__(self):
        """Barcha bildirishnoma xizmatlarini ishga tushirish"""
        # Twilio SMS
        self.twilio_client = Client(
            config('TWILIO_ACCOUNT_SID'),
            config('TWILIO_AUTH_TOKEN')
        )
        self.twilio_raqam = config('TWILIO_PHONE_NUMBER')
        
        # Firebase Push
        if not firebase_admin._apps:
            kred = credentials.Certificate(
                config('FIREBASE_CREDENTIALS_PATH')
            )
            firebase_admin.initialize_app(kred)
        
        # Loglar uchun saqlash (ishlab chiqarishda ma'lumotlar bazasidan foydalaning)
        self.loglar: List[BildirishnomаLog] = []
        
        # Foydalanuvchi sozlamalari (ishlab chiqarishda ma'lumotlar bazasidan yuklang)
        self.sozlamalar: Dict[str, FoydalanuvchiSozlamalari] = {}
        
        print("✓ Bildirishnoma Menejeri ishga tushdi")
        print("  - SMS: Twilio")
        print("  - Push: Firebase FCM")
        print("  - Email: (integratsiya qilinishi kerak)")
    
    def sozlamalarni_belgilash(self, foydalanuvchi_id: str, sozlamalar: FoydalanuvchiSozlamalari):
        """Foydalanuvchi bildirishnoma sozlamalarini belgilash"""
        self.sozlamalar[foydalanuvchi_id] = sozlamalar
        print(f"\n✓ Sozlamalar yangilandi: {foydalanuvchi_id}")
    
    def sozlamalarni_olish(self, foydalanuvchi_id: str) -> FoydalanuvchiSozlamalari:
        """Foydalanuvchi sozlamalarini olish yoki sukutlarni qaytarish"""
        return self.sozlamalar.get(
            foydalanuvchi_id,
            FoydalanuvchiSozlamalari(foydalanuvchi_id=foydalanuvchi_id)
        )
    
    def hozir_yuborish_kerakmi(self, foydalanuvchi_id: str) -> bool:
        """Hozir bildirishnoma yuborish kerakligini tekshirish (sokin soatlar)"""
        sozlamalar = self.sozlamalarni_olish(foydalanuvchi_id)
        
        if not sozlamalar.sokin_soatlar_boshi or not sozlamalar.sokin_soatlar_oxiri:
            return True
        
        # Oddiy sokin soatlar tekshiruvi (ishlab chiqarish uchun vaqt mintaqasi boshqaruvi kerak)
        joriy_soat = datetime.now().hour
        bosh_soat = int(sozlamalar.sokin_soatlar_boshi.split(':')[0])
        oxir_soat = int(sozlamalar.sokin_soatlar_oxiri.split(':')[0])
        
        if bosh_soat > oxir_soat:  # Yarim tunni kesib o'tadi
            return joriy_soat < bosh_soat and joriy_soat >= oxir_soat
        else:
            return joriy_soat < bosh_soat or joriy_soat >= oxir_soat
    
    def sms_yuborish(self, foydalanuvchi_id: str, telefon: str, xabar: str) -> Optional[str]:
        """SMS bildirishnoma yuborish"""
        sozlamalar = self.sozlamalarni_olish(foydalanuvchi_id)
        
        if not sozlamalar.sms_yoqilgan:
            print(f"  SMS o'chirilgan: {foydalanuvchi_id}")
            return None
        
        if not self.hozir_yuborish_kerakmi(foydalanuvchi_id):
            print(f"  SMS kechiktirildi (sokin soatlar): {foydalanuvchi_id}")
            return None
        
        try:
            msg = self.twilio_client.messages.create(
                body=xabar,
                from_=self.twilio_raqam,
                to=telefon
            )
            
            # Log
            log = BildirishnomаLog(
                bildirishnoma_id=msg.sid,
                foydalanuvchi_id=foydalanuvchi_id,
                tur=BildirishnomaTuri.SMS,
                holat=BildirishnomаHolati.YUBORILDI,
                sarlavha="SMS",
                xabar=xabar,
                yuborilgan_vaqt=datetime.now()
            )
            self.loglar.append(log)
            
            print(f"  ✓ SMS yuborildi: {msg.sid}")
            return msg.sid
            
        except Exception as e:
            print(f"  ✗ SMS xatosi: {str(e)}")
            
            # Xatolikni loglash
            log = BildirishnomаLog(
                bildirishnoma_id=f"sms_{datetime.now().timestamp()}",
                foydalanuvchi_id=foydalanuvchi_id,
                tur=BildirishnomaTuri.SMS,
                holat=BildirishnomаHolati.XATO,
                sarlavha="SMS",
                xabar=xabar,
                yuborilgan_vaqt=datetime.now(),
                xato=str(e)
            )
            self.loglar.append(log)
            return None
    
    def push_yuborish(self, foydalanuvchi_id: str, token: str, sarlavha: str, matn: str, malumot: Dict = None) -> Optional[str]:
        """Push bildirishnoma yuborish"""
        sozlamalar = self.sozlamalarni_olish(foydalanuvchi_id)
        
        if not sozlamalar.push_yoqilgan:
            print(f"  Push o'chirilgan: {foydalanuvchi_id}")
            return None
        
        if not self.hozir_yuborish_kerakmi(foydalanuvchi_id):
            print(f"  Push kechiktirildi (sokin soatlar): {foydalanuvchi_id}")
            return None
        
        try:
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title=sarlavha,
                    body=matn
                ),
                data=malumot or {},
                token=token
            )
            
            javob = messaging.send(xabar)
            
            # Log
            log = BildirishnomаLog(
                bildirishnoma_id=javob,
                foydalanuvchi_id=foydalanuvchi_id,
                tur=BildirishnomaTuri.PUSH,
                holat=BildirishnomаHolati.YUBORILDI,
                sarlavha=sarlavha,
                xabar=matn,
                yuborilgan_vaqt=datetime.now()
            )
            self.loglar.append(log)
            
            print(f"  ✓ Push yuborildi: {javob}")
            return javob
            
        except Exception as e:
            print(f"  ✗ Push xatosi: {str(e)}")
            
            # Xatolikni loglash
            log = BildirishnomаLog(
                bildirishnoma_id=f"push_{datetime.now().timestamp()}",
                foydalanuvchi_id=foydalanuvchi_id,
                tur=BildirishnomaTuri.PUSH,
                holat=BildirishnomаHolati.XATO,
                sarlavha=sarlavha,
                xabar=matn,
                yuborilgan_vaqt=datetime.now(),
                xato=str(e)
            )
            self.loglar.append(log)
            return None
    
    def bildirishnoma_yuborish(self, foydalanuvchi_id: str, sarlavha: str, xabar: str, 
                         telefon: Optional[str] = None, 
                         fcm_token: Optional[str] = None,
                         email: Optional[str] = None,
                         malumot: Dict = None) -> Dict[str, Optional[str]]:
        """
        Barcha yoqilgan kanallar orqali bildirishnoma yuborish
        
        Har bir kanal uchun xabar ID'lari bilan dict qaytaradi
        """
        print(f"\n📧 Foydalanuvchiga bildirishnoma yuborilmoqda: {foydalanuvchi_id}")
        print(f"  Sarlavha: {sarlavha}")
        print(f"  Xabar: {xabar}")
        
        natijalar = {
            'email': None,
            'sms': None,
            'push': None
        }
        
        # SMS yuborish
        if telefon:
            natijalar['sms'] = self.sms_yuborish(foydalanuvchi_id, telefon, xabar)
        
        # Push yuborish
        if fcm_token:
            natijalar['push'] = self.push_yuborish(foydalanuvchi_id, fcm_token, sarlavha, xabar, malumot)
        
        # Email yuborish (amalga oshirilishi kerak)
        if email:
            print(f"  Email yuborish hali amalga oshirilmagan")
        
        return natijalar
    
    def yetkazilish_statistikasi(self, foydalanuvchi_id: Optional[str] = None) -> Dict:
        """Yetkazilish statistikasini olish"""
        loglar = self.loglar
        if foydalanuvchi_id:
            loglar = [log for log in loglar if log.foydalanuvchi_id == foydalanuvchi_id]
        
        jami = len(loglar)
        tur_boyicha = {}
        holat_boyicha = {}
        
        for log in loglar:
            # Tur bo'yicha hisoblash
            tur_kalit = log.tur.value
            tur_boyicha[tur_kalit] = tur_boyicha.get(tur_kalit, 0) + 1
            
            # Holat bo'yicha hisoblash
            holat_kalit = log.holat.value
            holat_boyicha[holat_kalit] = holat_boyicha.get(holat_kalit, 0) + 1
        
        return {
            'jami': jami,
            'tur_boyicha': tur_boyicha,
            'holat_boyicha': holat_boyicha,
            'muvaffaqiyat_darajasi': (holat_boyicha.get('yuborildi', 0) + holat_boyicha.get('yetkazildi', 0)) / jami * 100 if jami > 0 else 0
        }
    
    def loglarni_chop_etish(self, foydalanuvchi_id: Optional[str] = None):
        """Bildirishnoma loglarini chop etish"""
        loglar = self.loglar
        if foydalanuvchi_id:
            loglar = [log for log in loglar if log.foydalanuvchi_id == foydalanuvchi_id]
        
        print(f"\n📊 Bildirishnoma Loglari ({len(loglar)} jami)")
        print("=" * 80)
        
        for log in loglar:
            holat_belgisi = "✓" if log.holat in [BildirishnomаHolati.YUBORILDI, BildirishnomаHolati.YETKAZILDI] else "✗"
            print(f"{holat_belgisi} [{log.tur.value.upper()}] {log.sarlavha}")
            print(f"   Foydalanuvchi: {log.foydalanuvchi_id}")
            print(f"   Holat: {log.holat.value}")
            print(f"   Yuborildi: {log.yuborilgan_vaqt.strftime('%Y-%m-%d %H:%M:%S')}")
            if log.xato:
                print(f"   Xato: {log.xato}")
            print()


def main():
    """Asosiy misol"""
    
    print("=" * 60)
    print("Yagona Bildirishnoma Menejeri Misoli")
    print("=" * 60)
    
    # Menejerni ishga tushirish
    menejer = BildirishnomaMenejeri()
    
    # Misol foydalanuvchi
    foydalanuvchi_id = "user123"
    telefon = "+998901234567"  # Almashtiring!
    fcm_token = "SIZNING_FCM_TOKEN"  # Almashtiring!
    
    # Misol 1: Foydalanuvchi sozlamalarini belgilash
    print("\n--- Misol 1: Foydalanuvchi Sozlamalari ---")
    sozlamalar = FoydalanuvchiSozlamalari(
        foydalanuvchi_id=foydalanuvchi_id,
        email_yoqilgan=True,
        sms_yoqilgan=True,
        push_yoqilgan=True,
        sokin_soatlar_boshi="22:00",
        sokin_soatlar_oxiri="08:00"
    )
    menejer.sozlamalarni_belgilash(foydalanuvchi_id, sozlamalar)
    
    # Misol 2: Ko'p kanalli bildirishnoma yuborish
    print("\n--- Misol 2: Ko'p Kanalli Bildirishnoma ---")
    menejer.bildirishnoma_yuborish(
        foydalanuvchi_id=foydalanuvchi_id,
        sarlavha="Kutubxonaga Xush Kelibsiz! 📚",
        xabar="Sizning akkauntingiz muvaffaqiyatli yaratildi.",
        telefon=telefon,
        fcm_token=fcm_token,
        malumot={'tur': 'xush_kelibsiz'}
    )
    
    # Misol 3: Kitob olingan bildirishnomasi
    print("\n--- Misol 3: Kitob Olindi ---")
    menejer.bildirishnoma_yuborish(
        foydalanuvchi_id=foydalanuvchi_id,
        sarlavha="Kitob Olindi",
        xabar="Siz 'Ikki Eshik Orasi' kitobini oldingiz. Muddat: 15 Yanvar, 2025",
        telefon=telefon,
        fcm_token=fcm_token,
        malumot={
            'tur': 'kitob_olindi',
            'kitob_id': '123',
            'muddat': '2025-01-15'
        }
    )
    
    # Misol 4: SMS'ni o'chirish
    print("\n--- Misol 4: SMS'ni O'chirish ---")
    sozlamalar.sms_yoqilgan = False
    menejer.sozlamalarni_belgilash(foydalanuvchi_id, sozlamalar)
    
    menejer.bildirishnoma_yuborish(
        foydalanuvchi_id=foydalanuvchi_id,
        sarlavha="Eslatma",
        xabar="Kitob ertaga muddati tugaydi!",
        telefon=telefon,
        fcm_token=fcm_token
    )
    
    # Misol 5: Loglarni ko'rish
    print("\n--- Misol 5: Bildirishnoma Loglari ---")
    menejer.loglarni_chop_etish(foydalanuvchi_id=foydalanuvchi_id)
    
    # Misol 6: Statistika
    print("\n--- Misol 6: Yetkazilish Statistikasi ---")
    statistika = menejer.yetkazilish_statistikasi(foydalanuvchi_id=foydalanuvchi_id)
    print(f"Jami bildirishnomalar: {statistika['jami']}")
    print(f"Tur bo'yicha: {json.dumps(statistika['tur_boyicha'], indent=2, ensure_ascii=False)}")
    print(f"Holat bo'yicha: {json.dumps(statistika['holat_boyicha'], indent=2, ensure_ascii=False)}")
    print(f"Muvaffaqiyat darajasi: {statistika['muvaffaqiyat_darajasi']:.2f}%")
    
    print("\n" + "=" * 60)
    print("Misol tugadi!")
    print("=" * 60)


if __name__ == "__main__":
    main()


"""
Ishlab Chiqarish Mulohazalari:
===============================

1. Ma'lumotlar Bazasi Integratsiyasi
   - Loglarni ma'lumotlar bazasida saqlash
   - Foydalanuvchi sozlamalarini keshlash
   - Yetkazilish holatini kuzatish

2. Navbat Tizimi (Celery)
   - Asinxron bildirishnoma yuborish
   - Xato bo'lgan bildirishnomalarni qayta urinish
   - Rejalashtirilgan bildirishnomalar

3. Monitoring
   - Yetkazilish tezligini kuzatish
   - Xatolik tezligini monitoring qilish
   - Xarajat tahlili

4. Foydalanuvchi Boshqaruvi
   - Sozlamalar UI
   - Opt-out mexanizmlari
   - GDPR muvofiqlik

5. Test Qilish
   - Birlik testlari
   - Integratsiya testlari
   - Yuk testi

6. Xavfsizlik
   - Xavfsiz kredensial saqlash
   - Tezlikni cheklash
   - Kiritish validatsiyasi


Django Integratsiya Misoli:
============================

```python
# notifications/services.py
from .notification_manager import BildirishnomaMenejeri

class DjangoBildirishnomаXizmati:
    def __init__(self):
        self.menejer = BildirishnomaMenejeri()
    
    def foydalanuvchiga_xabar_yuborish(self, user, sarlavha, xabar, kanallar=None):
        telefon = user.profile.telefon_raqami if hasattr(user, 'profile') else None
        fcm_token = user.device_tokens.first().token if user.device_tokens.exists() else None
        
        return self.menejer.bildirishnoma_yuborish(
            foydalanuvchi_id=str(user.id),
            sarlavha=sarlavha,
            xabar=xabar,
            telefon=telefon,
            fcm_token=fcm_token,
            email=user.email
        )
```


Signal Integratsiyasi:
======================

```python
# accounts/signals.py
from django.db.models.signals import post_save
from notifications.services import DjangoBildirishnomаXizmati

@receiver(post_save, sender=User)
def xush_kelibsiz_bildirishnomasi_yuborish(sender, instance, created, **kwargs):
    if created:
        xizmat = DjangoBildirishnomаXizmati()
        xizmat.foydalanuvchiga_xabar_yuborish(
            user=instance,
            sarlavha="Xush kelibsiz!",
            xabar="Sizning akkauntingiz yaratildi."
        )
```
"""