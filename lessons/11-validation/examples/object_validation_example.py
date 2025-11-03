"""
Object-level Validation misollari
==================================

Bu faylda bir nechta fieldlarni birgalikda tekshirish
va murakkab biznes logikasini amalga oshirish ko'rsatilgan.
"""

from rest_framework import serializers
from datetime import date, timedelta

# ============================================
# 1. ODDIY OBJECT VALIDATION
# ============================================

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False
    )
    published_date = serializers.DateField()
    is_bestseller = serializers.BooleanField(default=False)
    
    def validate(self, data):
        """
        Object-level validation:
        - Discount price < price
        - Bestseller faqat yangi kitoblar uchun
        """
        # 1. Discount price tekshirish
        if 'discount_price' in data:
            if data['discount_price'] >= data['price']:
                raise serializers.ValidationError({
                    'discount_price': 'Chegirma narxi asl narxdan kam bo\'lishi kerak'
                })
        
        # 2. Bestseller qoidalari
        if data['is_bestseller']:
            two_years_ago = date.today() - timedelta(days=730)
            if data['published_date'] < two_years_ago:
                raise serializers.ValidationError({
                    'is_bestseller': 'Faqat oxirgi 2 yil ichida chiqgan kitoblar bestseller bo\'lishi mumkin'
                })
        
        return data


# ============================================
# 2. MURAKKAB BIZNES LOGIKASI
# ============================================

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    is_available = serializers.BooleanField(default=True)
    min_order_quantity = serializers.IntegerField(default=1)
    max_order_quantity = serializers.IntegerField(required=False)
    
    def validate(self, data):
        """
        Murakkab biznes qoidalari:
        1. Stock va availability
        2. Min va max order quantity
        3. Price range'ga qarab rules
        """
        # 1. Stock va availability
        if data['is_available'] and data['stock'] == 0:
            raise serializers.ValidationError({
                'is_available': 'Omborda yo\'q mahsulot mavjud deb belgilanishi mumkin emas'
            })
        
        # 2. Min va max order quantity
        min_qty = data['min_order_quantity']
        max_qty = data.get('max_order_quantity')
        
        if max_qty and min_qty > max_qty:
            raise serializers.ValidationError({
                'min_order_quantity': 'Minimal buyurtma miqdori maksimaldan katta bo\'lishi mumkin emas'
            })
        
        # 3. Stock va max order quantity
        if max_qty and max_qty > data['stock']:
            raise serializers.ValidationError({
                'max_order_quantity': 'Maksimal buyurtma miqdori ombordagi mahsulotdan ko\'p bo\'lishi mumkin emas'
            })
        
        # 4. Price range rules
        if data['price'] > 1000:
            if data['stock'] < 5:
                raise serializers.ValidationError({
                    'stock': 'Qimmat mahsulotlar uchun minimal stock 5 ta bo\'lishi kerak'
                })
        
        return data


# ============================================
# 3. CONDITIONAL VALIDATION
# ============================================

class EventSerializer(serializers.Serializer):
    EVENT_TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    
    title = serializers.CharField(max_length=200)
    event_type = serializers.ChoiceField(choices=EVENT_TYPE_CHOICES)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    location = serializers.CharField(max_length=200, required=False)
    online_link = serializers.URLField(required=False)
    max_participants = serializers.IntegerField()
    
    def validate(self, data):
        """
        Conditional validation:
        - Online event uchun link kerak
        - Offline event uchun location kerak
        - End date > start date
        """
        # 1. Date validation
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError({
                'end_date': 'Tugash sanasi boshlanish sanasidan keyin bo\'lishi kerak'
            })
        
        # 2. Event type bo'yicha validation
        if data['event_type'] == 'online':
            if not data.get('online_link'):
                raise serializers.ValidationError({
                    'online_link': 'Online tadbir uchun link kiritilishi shart'
                })
        else:  # offline
            if not data.get('location'):
                raise serializers.ValidationError({
                    'location': 'Offline tadbir uchun manzil kiritilishi shart'
                })
        
        # 3. Max participants
        if data['event_type'] == 'offline' and data['max_participants'] > 1000:
            raise serializers.ValidationError({
                'max_participants': 'Offline tadbir uchun maksimal ishtirokchilar soni 1000 ta'
            })
        
        return data


# ============================================
# 4. MULTIPLE FIELD DEPENDENCIES
# ============================================

class SubscriptionSerializer(serializers.Serializer):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    
    plan = serializers.ChoiceField(choices=PLAN_CHOICES)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    duration_months = serializers.IntegerField()
    features_count = serializers.IntegerField()
    support_level = serializers.CharField(max_length=50)
    
    def validate(self, data):
        """
        Subscription plan qoidalari
        """
        plan = data['plan']
        price = data['price']
        duration = data['duration_months']
        features = data['features_count']
        
        # Free plan qoidalari
        if plan == 'free':
            if price != 0:
                raise serializers.ValidationError({
                    'price': 'Free plan uchun narx 0 bo\'lishi kerak'
                })
            if features > 5:
                raise serializers.ValidationError({
                    'features_count': 'Free plan maksimal 5 ta feature\'ga ega bo\'lishi mumkin'
                })
            if data['support_level'] != 'email':
                raise serializers.ValidationError({
                    'support_level': 'Free plan faqat email support\'ga ega'
                })
        
        # Basic plan qoidalari
        elif plan == 'basic':
            if not (9.99 <= price <= 29.99):
                raise serializers.ValidationError({
                    'price': 'Basic plan narxi 9.99$ va 29.99$ orasida bo\'lishi kerak'
                })
            if features > 15:
                raise serializers.ValidationError({
                    'features_count': 'Basic plan maksimal 15 ta feature\'ga ega bo\'lishi mumkin'
                })
        
        # Premium plan qoidalari
        elif plan == 'premium':
            if price < 30:
                raise serializers.ValidationError({
                    'price': 'Premium plan narxi kamida 30$ bo\'lishi kerak'
                })
            if data['support_level'] != '24/7':
                raise serializers.ValidationError({
                    'support_level': 'Premium plan 24/7 support talab qiladi'
                })
        
        # Duration bo'yicha chegirmalar
        if duration >= 12 and price == data['price']:  # Yillik to'lov
            discount_required = True
            raise serializers.ValidationError({
                'price': 'Yillik to\'lov uchun chegirma berilishi kerak'
            })
        
        return data


# ============================================
# ISHLATISH MISOLLARI
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("OBJECT-LEVEL VALIDATION MISOLLARI")
    print("=" * 60)
    
    # ===== Test 1: Book - to'g'ri ma'lumot =====
    print("\n1. BOOK - TO'G'RI MA'LUMOT")
    print("-" * 60)
    
    book_data = {
        'title': 'Clean Code',
        'author': 'Robert Martin',
        'price': '45.99',
        'discount_price': '35.99',
        'published_date': '2024-01-01',
        'is_bestseller': True
    }
    
    serializer = BookSerializer(data=book_data)
    if serializer.is_valid():
        print("✅ Ma'lumotlar to'g'ri!")
    else:
        print("❌ Xatolar:", serializer.errors)
    
    # ===== Test 2: Book - noto'g'ri discount =====
    print("\n2. BOOK - NOTO'G'RI DISCOUNT")
    print("-" * 60)
    
    invalid_discount = {
        'title': 'Test Book',
        'author': 'Test Author',
        'price': '30.00',
        'discount_price': '35.00',  # Narxdan baland!
        'published_date': '2024-01-01',
        'is_bestseller': False
    }
    
    serializer = BookSerializer(data=invalid_discount)
    if not serializer.is_valid():
        print("❌ Xato topildi:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    # ===== Test 3: Product - stock va availability =====
    print("\n3. PRODUCT - STOCK VA AVAILABILITY")
    print("-" * 60)
    
    invalid_product = {
        'name': 'Laptop',
        'price': '999.99',
        'stock': 0,
        'is_available': True,  # Stock 0 lekin available!
        'min_order_quantity': 1
    }
    
    serializer = ProductSerializer(data=invalid_product)
    if not serializer.is_valid():
        print("❌ Xato topildi:")
        for field, errors in serializer.errors.items():
            print(f"  {field}: {errors[0]}")
    
    # ===== Test 4: Event - online event =====
    print("\n4. EVENT - ONLINE EVENT")
    print("-" * 60)
    
    event_data = {
        'title': 'Python Webinar',
        'event_type': 'online',
        'start_date': '2024-12-01',
        'end_date': '2024-12-01',
        'online_link': 'https://zoom.us/meeting',
        'max_participants': 500
    }
    
    serializer = EventSerializer(data=event_data)
    if serializer.is_valid():
        print("✅ Event ma'lumotlari to'g'ri!")
    else:
        print("❌ Xatolar:", serializer.errors)
    
    # ===== Test 5: Subscription - free plan =====
    print("\n5. SUBSCRIPTION - FREE PLAN")
    print("-" * 60)
    
    subscription_data = {
        'plan': 'free',
        'price': '0.00',
        'duration_months': 1,
        'features_count': 5,
        'support_level': 'email'
    }
    
    serializer = SubscriptionSerializer(data=subscription_data)
    if serializer.is_valid():
        print("✅ Subscription ma'lumotlari to'g'ri!")
    else:
        print("❌ Xatolar:", serializer.errors)
    
    print("\n" + "=" * 60)
    print("OBJECT-LEVEL VALIDATION TEST TUGADI!")
    print("=" * 60)