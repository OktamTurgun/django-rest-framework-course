"""
Django REST Framework Authentication Turlari Taqqoslash

Bu fayl autentifikatsiya turlarini taqqoslash uchun nazariy misol.
"""


def authentication_comparison():
    """
    DRF'dagi asosiy autentifikatsiya turlarini taqqoslash
    """
    
    auth_types = {
        'SessionAuthentication': {
            'description': 'Django session tizimidan foydalanadi',
            'use_case': 'Browser-based ilovalar uchun',
            'pros': [
                'Django admin bilan bir xil session',
                'CSRF himoyasi mavjud',
                'Browser uchun qulay'
            ],
            'cons': [
                'Mobile ilovalar uchun noqulay',
                'Stateful (server\'da session saqlanadi)',
                'Scaling qiyin'
            ],
            'example': 'Browser orqali login qilish'
        },
        
        'BasicAuthentication': {
            'description': 'HTTP Basic Auth protokoli',
            'use_case': 'Test va oddiy ilovalar uchun',
            'pros': [
                'Oddiy va tez',
                'Hamma HTTP client\'larda ishlaydi',
                'O\'rnatish kerak emas'
            ],
            'cons': [
                'Xavfsiz emas (HTTPS shart)',
                'Har safar username/password yuboriladi',
                'Logout qilish qiyin'
            ],
            'example': 'Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ='
        },
        
        'TokenAuthentication': {
            'description': 'Token asosida autentifikatsiya',
            'use_case': 'Production API\'lar uchun',
            'pros': [
                'Stateless',
                'Mobile ilovalar uchun ideal',
                'Xavfsiz',
                'Logout oson'
            ],
            'cons': [
                'Token\'ni saqlash kerak',
                'Token muddati yo\'q (default)',
                'Har safar database query'
            ],
            'example': 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
        },
        
        'JWT': {
            'description': 'JSON Web Token',
            'use_case': 'Zamonaviy API\'lar uchun',
            'pros': [
                'Stateless',
                'O\'zi-o\'zini tekshiradi',
                'Expire time bor',
                'Refresh token mexanizmi'
            ],
            'cons': [
                'Token hajmi katta',
                'Revoke qilish qiyin',
                'Ko\'proq sozlash kerak'
            ],
            'example': 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        }
    }
    
    return auth_types


def print_comparison():
    """Taqqoslashni chiroyli ko'rinishda chiqarish"""
    
    auth_types = authentication_comparison()
    
    print("=" * 80)
    print("DJANGO REST FRAMEWORK AUTHENTICATION TURLARI TAQQOSLASH")
    print("=" * 80)
    print()
    
    for auth_name, details in auth_types.items():
        print(f"\n{'=' * 80}")
        print(f"{auth_name}")
        print(f"{'=' * 80}")
        print(f"\nTa'rif: {details['description']}")
        print(f"Qo'llanish: {details['use_case']}")
        
        print(f"\n✅ Afzalliklari:")
        for pro in details['pros']:
            print(f"   - {pro}")
        
        print(f"\n❌ Kamchiliklari:")
        for con in details['cons']:
            print(f"   - {con}")
        
        print(f"\n📝 Misol: {details['example']}")
    
    print("\n" + "=" * 80)
    print("XULOSA")
    print("=" * 80)
    print("""
    ✅ Browser ilovalar uchun: SessionAuthentication
    ✅ Test va oddiy ilovalar uchun: BasicAuthentication
    ✅ Production API (Mobile/Web): TokenAuthentication
    ✅ Zamonaviy API: JWT (SimpleJWT)
    """)


if __name__ == "__main__":
    print_comparison()