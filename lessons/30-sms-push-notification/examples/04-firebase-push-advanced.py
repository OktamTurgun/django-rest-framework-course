"""
Misol 04: Firebase Push Bildirishnomalar Qo'shimcha
====================================================

Bu misolda quyidagilar ko'rsatiladi:
- Rasm bilan boy bildirishnomalar
- Harakat tugmalari
- Ovoz va nishon sozlash
- Platformaga xos konfiguratsiyalar
- Muhimlik sozlamalari
- Yashash vaqti (TTL)

Talablar:
    pip install firebase-admin python-decouple

Muhit O'zgaruvchilari (.env):
    FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json ga yo'l
"""

import firebase_admin
from firebase_admin import credentials, messaging
from decouple import config


class FirebasePushQoshimcha:
    """Qo'shimcha Firebase Cloud Messaging xususiyatlari"""
    
    def __init__(self):
        """Firebase'ni ishga tushirish"""
        if not firebase_admin._apps:
            kred_yoli = config('FIREBASE_CREDENTIALS_PATH')
            kred = credentials.Certificate(kred_yoli)
            firebase_admin.initialize_app(kred)
        
        print("✓ Firebase Qo'shimcha ishga tushdi")
    
    def boy_bildirishnoma_yuborish(self, token):
        """
        Rasm bilan bildirishnoma yuborish
        
        Args:
            token (str): Qurilma FCM tokeni
        """
        try:
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title='📚 Yangi Kitob Mavjud!',
                    body='O\'tkir Hoshimovning "Ikki Eshik Orasi" kitobini ko\'ring',
                    image='https://example.com/kitob-muqova.jpg'
                ),
                data={
                    'kitob_id': '456',
                    'harakat': 'kitobni_korish'
                },
                token=token
            )
            
            javob = messaging.send(xabar)
            print(f"\n✓ Boy bildirishnoma yuborildi!")
            print(f"  Rasm bilan: Ha")
            print(f"  Xabar ID: {javob}")
            
            return javob
            
        except Exception as e:
            print(f"\n✗ Xato: {str(e)}")
            return None
    
    def harakatlar_bilan_yuborish(self, token):
        """
        Harakat tugmalari bilan bildirishnoma yuborish (faqat Android)
        
        Args:
            token (str): Qurilma FCM tokeni
        """
        try:
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title='⏰ Kitob Ertaga Muddati Tugaydi!',
                    body='"Ikki Eshik Orasi" ertaga muddati tugaydi.'
                ),
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        click_action='FLUTTER_NOTIFICATION_CLICK',
                        sound='default',
                        color='#FF0000'
                    )
                ),
                data={
                    'harakat1': 'uzaytirish',
                    'harakat2': 'qaytarish',
                    'kitob_id': '123'
                },
                token=token
            )
            
            javob = messaging.send(xabar)
            print(f"\n✓ Harakat bildirishnomasi yuborildi!")
            print(f"  Harakatlar: uzaytirish, qaytarish")
            print(f"  Xabar ID: {javob}")
            
            return javob
            
        except Exception as e:
            print(f"\n✗ Xato: {str(e)}")
            return None
    
    def ios_bildirishnoma_yuborish(self, token):
        """
        Nishon va ovoz bilan iOS bildirishnomasi yuborish
        
        Args:
            token (str): Qurilma FCM tokeni
        """
        try:
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title='📱 Yangi Xabar',
                    body='Kutubxonadan sizga yangi xabar bor.'
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            alert=messaging.ApsAlert(
                                title='📱 Yangi Xabar',
                                body='Kutubxonadan sizga yangi xabar bor.'
                            ),
                            badge=1,
                            sound='default',
                            category='XABAR_KATEGORIYASI'
                        )
                    )
                ),
                token=token
            )
            
            javob = messaging.send(xabar)
            print(f"\n✓ iOS bildirishnomasi yuborildi!")
            print(f"  Nishon: 1")
            print(f"  Ovoz: default")
            print(f"  Xabar ID: {javob}")
            
            return javob
            
        except Exception as e:
            print(f"\n✗ Xato: {str(e)}")
            return None
    
    def yuqori_muhimlik_yuborish(self, token):
        """
        Yuqori muhimlikdagi bildirishnoma yuborish
        
        Args:
            token (str): Qurilma FCM tokeni
        """
        try:
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title='🚨 MUHIM: Kitob Muddati O\'tgan',
                    body='Kitobingiz 7 kun kechikdi! Kechikish to\'lovi: $7.00'
                ),
                android=messaging.AndroidConfig(
                    priority='high',
                    ttl=3600,  # 1 soat
                    notification=messaging.AndroidNotification(
                        priority='max',
                        default_sound=True,
                        default_vibrate_timings=True
                    )
                ),
                apns=messaging.APNSConfig(
                    headers={'apns-priority': '10'},
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            alert='Kitobingiz muddati o\'tgan!',
                            sound='default'
                        )
                    )
                ),
                data={
                    'tur': 'muddati_otgan',
                    'muhimlik': 'yuqori',
                    'kitob_id': '789'
                },
                token=token
            )
            
            javob = messaging.send(xabar)
            print(f"\n✓ Yuqori muhimlikdagi bildirishnoma yuborildi!")
            print(f"  Muhimlik: Yuqori")
            print(f"  TTL: 1 soat")
            print(f"  Xabar ID: {javob}")
            
            return javob
            
        except Exception as e:
            print(f"\n✗ Xato: {str(e)}")
            return None
    
    def jim_bildirishnoma_yuborish(self, token):
        """
        Jim (faqat ma'lumot) bildirishnoma yuborish
        
        Args:
            token (str): Qurilma FCM tokeni
        """
        try:
            xabar = messaging.Message(
                data={
                    'tur': 'sinxronlash',
                    'harakat': 'kutubxonani_yangilash',
                    'vaqt_belgisi': '1640000000'
                },
                android=messaging.AndroidConfig(
                    priority='normal'
                ),
                apns=messaging.APNSConfig(
                    headers={'apns-push-type': 'background'},
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            content_available=True
                        )
                    )
                ),
                token=token
            )
            
            javob = messaging.send(xabar)
            print(f"\n✓ Jim bildirishnoma yuborildi!")
            print(f"  Tur: Faqat ma'lumot")
            print(f"  Xabar ID: {javob}")
            
            return javob
            
        except Exception as e:
            print(f"\n✗ Xato: {str(e)}")
            return None
    
    def shartli_yuborish(self, shart):
        """
        Shartga asoslanib bildirishnoma yuborish
        
        Args:
            shart (str): Shart qatori (mavzuga asoslangan)
        """
        try:
            xabar = messaging.Message(
                notification=messaging.Notification(
                    title='📚 Dam Olish Kunlari Aksiyasi',
                    body='Barcha kitoblar bu dam olish kunlarida 20% chegirma!'
                ),
                condition=shart
            )
            
            javob = messaging.send(xabar)
            print(f"\n✓ Shartli bildirishnoma yuborildi!")
            print(f"  Shart: {shart}")
            print(f"  Xabar ID: {javob}")
            
            return javob
            
        except Exception as e:
            print(f"\n✗ Xato: {str(e)}")
            return None


def main():
    """Asosiy misol funksiyasi"""
    
    print("=" * 60)
    print("Firebase Push Bildirishnomalar - Qo'shimcha Xususiyatlar")
    print("=" * 60)
    
    # Ishga tushirish
    fcm = FirebasePushQoshimcha()
    
    # Qurilma tokeni bilan almashtiring
    qurilma_tokeni = "SIZNING_QURILMA_TOKENI_BU_YERDA"
    
    # Misol 1: Rasm bilan boy bildirishnoma
    print("\n--- Misol 1: Boy Bildirishnoma ---")
    fcm.boy_bildirishnoma_yuborish(qurilma_tokeni)
    
    # Misol 2: Harakat tugmalari bilan bildirishnoma
    print("\n--- Misol 2: Harakat Tugmalari ---")
    fcm.harakatlar_bilan_yuborish(qurilma_tokeni)
    
    # Misol 3: iOS bildirishnomasi
    print("\n--- Misol 3: iOS Bildirishnomasi ---")
    fcm.ios_bildirishnoma_yuborish(qurilma_tokeni)
    
    # Misol 4: Yuqori muhimlikdagi bildirishnoma
    print("\n--- Misol 4: Yuqori Muhimlik ---")
    fcm.yuqori_muhimlik_yuborish(qurilma_tokeni)
    
    # Misol 5: Jim bildirishnoma
    print("\n--- Misol 5: Jim Bildirishnoma ---")
    fcm.jim_bildirishnoma_yuborish(qurilma_tokeni)
    
    # Misol 6: Shartli yuborish
    print("\n--- Misol 6: Shartli Yuborish ---")
    # 'premium' YOKI 'vip' mavzulariga obuna bo'lgan foydalanuvchilarga yuborish
    shart = "'premium' in topics || 'vip' in topics"
    fcm.shartli_yuborish(shart)
    
    print("\n" + "=" * 60)
    print("Qo'shimcha misollar tugadi!")
    print("=" * 60)


if __name__ == "__main__":
    main()


"""
Qo'shimcha Xususiyatlar Tushuntirildi:
=======================================

1. Boy Bildirishnomalar
   - Bildirishnomalarga rasmlar qo'shing
   - Android va iOS'da qo'llab-quvvatlanadi
   - Rasm URL ochiq bo'lishi kerak
   - Tavsiya etilgan o'lcham: 1024x512 piksel

2. Harakat Tugmalari (Android)
   - Bosiladigan harakatlarni qo'shing
   - Har bir bildirishnomada 3 tagacha harakat
   - Maxsus ikonkalar va belgilar
   - Ilova kodida boshqarish

3. iOS Xususiyatlari
   - Nishon hisobi
   - Maxsus ovozlar
   - Kategoriyalar
   - Muhim ogohlantirishlar
   - Kontent mavjud

4. Muhimlik Darajalari
   - Yuqori: Darhol yetkaziladi
   - Oddiy: Batareya optimallashtiruvchi yetkazish
   - Yetkazish vaqtiga ta'sir qiladi
   - Shoshilinch xabarlar uchun yuqoridan foydalaning

5. Yashash Vaqti (TTL)
   - FCM xabarni qancha vaqt saqlaydi
   - 0-4 hafta (2,419,200 soniya)
   - Sukut: 4 hafta
   - Vaqtga bog'liq kontent uchun foydali

6. Jim Bildirishnomalar
   - UI bildirishnomasi ko'rsatilmaydi
   - Fonda ma'lumot yetkazish
   - Ilova ishlaydi va qayta ishlaydi
   - Sinxronlash operatsiyalari uchun foydali

7. Shartli Yuborish
   - Mavzuga asoslangan shartlar
   - Boolean operatorlar: &&, ||
   - Misol: "'sport' in topics && 'yangiliklar' in topics"


Platformaga Xos Konfiguratsiya:
================================

Android:
```python
android=messaging.AndroidConfig(
    priority='high',
    ttl=3600,
    collapse_key='key1',
    notification=messaging.AndroidNotification(
        title='Sarlavha',
        body='Matn',
        icon='ikon_nomi',
        color='#FF0000',
        sound='ovoz_nomi',
        click_action='HARAKAT_OCHISH',
        channel_id='kanal_id'
    )
)
```

iOS (APNS):
```python
apns=messaging.APNSConfig(
    headers={
        'apns-priority': '10',
        'apns-expiration': '1640000000'
    },
    payload=messaging.APNSPayload(
        aps=messaging.Aps(
            alert='Ogohlantirish matni',
            badge=1,
            sound='default',
            content_available=True,
            category='KATEGORIYA_NOMI',
            thread_id='thread1'
        )
    )
)
```


Bildirishnoma Ko'rinishi:
==========================

Android:
- Katta ikon (kvadrat)
- Kichik ikon (monoxrom)
- Bildirishnoma ovozi
- LED rangi
- Vibratsiya naqshi

iOS:
- Ilova ikon nishoni
- Bildirishnoma ovozi
- Ogohlantirish uslubi
- Banner yoki modal


Eng Yaxshi Amaliyotlar:
========================

1. Tegishli muhimlikdan foydalaning
2. Oqilona TTL belgilang
3. Rasm o'lchamlarini optimallashtiring
4. Ko'p qurilmalarda test qiling
5. Bildirishnoma ruxsatlarini boshqaring
6. Yetkazilish holatini kuzatib boring
7. Bildirishnoma kontentini A/B test qiling
8. Sokin soatlarni hurmat qiling
9. Foydalanuvchi sozlamalariga ruxsat bering
10. Jalb qilish ko'rsatkichlarini monitoring qiling


Test Maslahatlari:
==================

1. Haqiqiy qurilmalarda test qiling (emulatorlarda emas)
2. Ilova oldingi va orqa fonda bo'lganda test qiling
3. Turli Android versiyalarida test qiling
4. iOS va Android'da test qiling
5. Internet bor/yo'q holatda test qiling
6. Bildirishnoma ruxsatlarini tekshiring
7. Ma'lumot yuklashni boshqarishni tasdiqlang
"""