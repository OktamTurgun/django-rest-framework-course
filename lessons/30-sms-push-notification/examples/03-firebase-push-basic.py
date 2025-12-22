"""
Misol 03: Firebase Push Bildirishnomalar Asoslari
==================================================

Bu misolda quyidagilar ko'rsatiladi:
- Firebase Admin SDK sozlash
- Bitta qurilmaga push bildirishnoma yuborish
- Ko'p qurilmalarga yuborish
- Asosiy bildirishnoma strukturasi

Talablar:
    pip install firebase-admin python-decouple

Sozlash:
1. console.firebase.google.com da Firebase loyihasini yarating
2. Project Settings → Service Accounts ga o'ting
3. Yangi private key yarating (JSON fayl)
4. 'serviceAccountKey.json' sifatida saqlang
5. Yo'lni .env fayliga qo'shing

Muhit O'zgaruvchilari (.env):
    FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json ga yo'l
"""

import firebase_admin
from firebase_admin import credentials, messaging
from decouple import config
import json


class FirebasePushAsoslari:
    """Asosiy Firebase Cloud Messaging"""
    
    def __init__(self):
        """Firebase Admin SDK ni ishga tushirish"""
        # Kredensial yo'lini olish
        kred_yoli = config('FIREBASE_CREDENTIALS_PATH')
        
        # Firebase'ni ishga tushirish
        kred = credentials.Certificate(kred_yoli)
        firebase_admin.initialize_app(kred)
        
        print("✓ Firebase ishga tushdi")
    
    def tokenga_yuborish(self, token, sarlavha, matn, malumot=None):
        """
        Bitta qurilmaga push bildirishnoma yuborish
        
        Args:
            token (str): Qurilma FCM tokeni
            sarlavha (str): Bildirishnoma sarlavhasi
            matn (str): Bildirishnoma matni
            malumot (dict): Ixtiyoriy ma'lumot yuklash
            
        Returns:
            str: Muvaffaqiyatli bo'lsa xabar ID, aks holda None
        """
        try:
            # Xabar yaratish
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title=sarlavha,
                    body=matn
                ),
                data=malumot or {},
                token=token
            )
            
            # Xabar yuborish
            javob = messaging.send(xabar)
            
            print(f"\n✓ Bildirishnoma yuborildi!")
            print(f"  Xabar ID: {javob}")
            print(f"  Sarlavha: {sarlavha}")
            print(f"  Matn: {matn}")
            if malumot:
                print(f"  Ma'lumot: {json.dumps(malumot, indent=2, ensure_ascii=False)}")
            
            return javob
            
        except firebase_admin.exceptions.FirebaseError as e:
            print(f"\n✗ Firebase xatosi: {str(e)}")
            return None
            
        except Exception as e:
            print(f"\n✗ Kutilmagan xato: {str(e)}")
            return None
    
    def ko_p_qurilmaga_yuborish(self, tokenlar, sarlavha, matn):
        """
        Ko'p qurilmalarga push bildirishnoma yuborish
        
        Args:
            tokenlar (list): Qurilma FCM tokenlari ro'yxati
            sarlavha (str): Bildirishnoma sarlavhasi
            matn (str): Bildirishnoma matni
            
        Returns:
            dict: Muvaffaqiyat/xatolik soni bilan batch javobi
        """
        try:
            # Xabar yaratish
            xabar = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=sarlavha,
                    body=matn
                ),
                tokens=tokenlar
            )
            
            # Ko'p qurilmalarga yuborish
            javob = messaging.send_multicast(xabar)
            
            print(f"\n✓ Batch bildirishnoma yuborildi!")
            print(f"  Muvaffaqiyatli: {javob.success_count}/{len(tokenlar)}")
            print(f"  Xatolik: {javob.failure_count}/{len(tokenlar)}")
            
            # Xatolarni chop etish
            if javob.failure_count > 0:
                print("\n  Xatolik tokenlar:")
                for idx, jav in enumerate(javob.responses):
                    if not jav.success:
                        print(f"    - Token {idx}: {jav.exception}")
            
            return {
                'muvaffaqiyat_soni': javob.success_count,
                'xatolik_soni': javob.failure_count,
                'javoblar': javob.responses
            }
            
        except Exception as e:
            print(f"\n✗ Batch yuborishda xato: {str(e)}")
            return None
    
    def mavzuga_yuborish(self, mavzu, sarlavha, matn):
        """
        Mavzuga obuna bo'lgan barcha qurilmalarga bildirishnoma yuborish
        
        Args:
            mavzu (str): Mavzu nomi (masalan, 'yangiliklar', 'yangilanishlar')
            sarlavha (str): Bildirishnoma sarlavhasi
            matn (str): Bildirishnoma matni
            
        Returns:
            str: Muvaffaqiyatli bo'lsa xabar ID
        """
        try:
            # Xabar yaratish
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title=sarlavha,
                    body=matn
                ),
                topic=mavzu
            )
            
            # Mavzuga yuborish
            javob = messaging.send(xabar)
            
            print(f"\n✓ Mavzu bildirishnomasi yuborildi!")
            print(f"  Mavzu: {mavzu}")
            print(f"  Xabar ID: {javob}")
            
            return javob
            
        except Exception as e:
            print(f"\n✗ Mavzuga yuborishda xato: {str(e)}")
            return None


def main():
    """Asosiy misol funksiyasi"""
    
    print("=" * 50)
    print("Firebase Push Bildirishnomalar Asoslari")
    print("=" * 50)
    
    # Firebase'ni ishga tushirish
    fcm = FirebasePushAsoslari()
    
    # MUHIM: Haqiqiy qurilma tokeni bilan almashtiring!
    # Qurilma tokenini mobil ilovangizdan oling
    qurilma_tokeni = "SIZNING_QURILMA_TOKENI_BU_YERDA"
    
    # Misol 1: Oddiy bildirishnoma
    print("\n--- Misol 1: Oddiy Bildirishnoma ---")
    fcm.tokenga_yuborish(
        token=qurilma_tokeni,
        sarlavha="Kutubxonaga Xush Kelibsiz! 📚",
        matn="Sizning akkauntingiz muvaffaqiyatli yaratildi."
    )
    
    # Misol 2: Ma'lumot bilan bildirishnoma
    print("\n--- Misol 2: Ma'lumot Bilan Bildirishnoma ---")
    fcm.tokenga_yuborish(
        token=qurilma_tokeni,
        sarlavha="Kitob Olindi",
        matn="Siz 'Ikki Eshik Orasi' kitobini oldingiz",
        malumot={
            'tur': 'kitob_olindi',
            'kitob_id': '123',
            'kitob_nomi': 'Ikki Eshik Orasi',
            'muddat': '2025-01-15'
        }
    )
    
    # Misol 3: Ko'p qurilmalar
    print("\n--- Misol 3: Ko'p Qurilmalarga Yuborish ---")
    qurilma_tokenlari = [
        "token1_bu_yerda",
        "token2_bu_yerda",
        "token3_bu_yerda"
    ]
    fcm.ko_p_qurilmaga_yuborish(
        tokenlar=qurilma_tokenlari,
        sarlavha="Yangi Kitoblar Mavjud! 📖",
        matn="Kutubxonaga yangi qo'shilgan kitoblarni ko'ring."
    )
    
    # Misol 4: Mavzu obunasi
    print("\n--- Misol 4: Mavzuga Yuborish ---")
    fcm.mavzuga_yuborish(
        mavzu='kutubxona_yangiliklari',
        sarlavha="Kutubxona E'loni",
        matn="Kutubxona dushanba kuni ta'mirlash uchun yopiq bo'ladi."
    )
    
    print("\n" + "=" * 50)
    print("Misollar tugadi!")
    print("=" * 50)


if __name__ == "__main__":
    # Foydalanish:
    # 1. Firebase loyihasini sozlang
    # 2. serviceAccountKey.json ni yuklab oling
    # 3. Yo'lni .env fayliga qo'shing
    # 4. Ilovangizdan qurilma tokenini oling
    # 5. qurilma_tokeni o'zgaruvchisini almashtiring
    # 6. Ishga tushiring: python 03-firebase-push-basic.py
    
    main()


"""
Kutilayotgan Natija:
====================

==================================================
Firebase Push Bildirishnomalar Asoslari
==================================================
✓ Firebase ishga tushdi

--- Misol 1: Oddiy Bildirishnoma ---

✓ Bildirishnoma yuborildi!
  Xabar ID: projects/123/messages/abc
  Sarlavha: Kutubxonaga Xush Kelibsiz! 📚
  Matn: Sizning akkauntingiz muvaffaqiyatli yaratildi.

--- Misol 2: Ma'lumot Bilan Bildirishnoma ---

✓ Bildirishnoma yuborildi!
  Xabar ID: projects/123/messages/def
  Sarlavha: Kitob Olindi
  Matn: Siz 'Ikki Eshik Orasi' kitobini oldingiz
  Ma'lumot: {
    "tur": "kitob_olindi",
    "kitob_id": "123",
    "kitob_nomi": "Ikki Eshik Orasi",
    "muddat": "2025-01-15"
  }


Qurilma Tokenini Qanday Olish:
===============================

Android (React Native / Flutter):
```javascript
import messaging from '@react-native-firebase/messaging';

async function getToken() {
  const token = await messaging().getToken();
  console.log('FCM Token:', token);
}
```

iOS (React Native / Flutter):
```javascript
import messaging from '@react-native-firebase/messaging';

async function requestPermission() {
  const authStatus = await messaging().requestPermission();
  const token = await messaging().getToken();
  console.log('FCM Token:', token);
}
```

Web (JavaScript):
```javascript
import { getMessaging, getToken } from "firebase/messaging";

const messaging = getMessaging();
getToken(messaging, { vapidKey: 'SIZNING_VAPID_KEY' })
  .then((token) => {
    console.log('FCM Token:', token);
  });
```


Bildirishnoma Strukturasi:
===========================

xabar = {
    "notification": {
        "title": "Bildirishnoma Sarlavhasi",
        "body": "Bildirishnoma matni"
    },
    "data": {
        "kalit1": "qiymat1",
        "kalit2": "qiymat2"
    },
    "token": "qurilma_fcm_tokeni"
}


Mavzu Obunasi:
===============

Qurilmani mavzuga obuna qilish (mobil ilovadan):
```javascript
messaging().subscribeToTopic('kutubxona_yangiliklari');
```

Obunani bekor qilish:
```javascript
messaging().unsubscribeFromTopic('kutubxona_yangiliklari');
```


Eng Yaxshi Amaliyotlar:
========================

1. Qurilma tokenlarini ma'lumotlar bazasida xavfsiz saqlang
2. Tokenlar o'zgarganda yangilang
3. Noto'g'ri tokenlarni olib tashlang
4. Umumiy xabarlar uchun mavzulardan foydalaning
5. Tegishli ma'lumot yuklamasini qo'shing
6. Ko'p qurilmalarda test qiling
7. Token yangilanishini boshqaring
8. Foydalanuvchi bildirishnoma sozlamalarini hurmat qiling


FCM Kvotalari:
===============
- Xabarlar: Cheksiz
- Mavzular: Ilovaga 2000 ta
- Mavzu obunachilari: Cheksiz
- Xabar hajmi: 4096 bayt
- Narx: BEPUL!


Xatolarni Boshqarish:
======================

Keng tarqalgan xatolar:
- Noto'g'ri token: Token amal qilish muddati tugagan yoki noto'g'ri
- Ro'yxatdan o'tish tokeni ro'yxatdan o'tmagan: Foydalanuvchi ilovani o'chirgan
- MismatchSenderId: Noto'g'ri FCM konfiguratsiyasi
- Noto'g'ri paket nomi: Ilova paketi mos kelmaydi
"""