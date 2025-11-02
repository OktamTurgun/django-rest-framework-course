"""
ModelSerializer misoli
======================

Bu faylda ModelSerializer class'idan foydalanib,
Django modellari bilan qanday ishlash ko'rsatilgan.
"""

from rest_framework import serializers
from datetime import date

# Bu yerda real modellarni import qilish kerak bo'ladi:
# from books.models import Book, Author, Category


# ============================================
# 1. Oddiy ModelSerializer
# ============================================

class BookModelSerializer(serializers.ModelSerializer):
    """
    Eng oddiy ModelSerializer
    Barcha fieldlar avtomatik olinadi
    """
    class Meta:
        model = None  # Real loyihada: Book
        fields = '__all__'  # Barcha fieldlar


# ============================================
# 2. Muayyan fieldlar bilan ModelSerializer
# ============================================

class BookListSerializer(serializers.ModelSerializer):
    """
    Faqat kerakli fieldlarni ko'rsatish
    List view uchun yengil serializer
    """
    class Meta:
        model = None  # Real loyihada: Book
        fields = ['id', 'title', 'author', 'price']
        # yoki exclude ishlatish mumkin:
        # exclude = ['description', 'isbn']


# ============================================
# 3. Read-only fieldlar bilan
# ============================================

class BookCreateSerializer(serializers.ModelSerializer):
    """
    Read-only fieldlar ko'rsatish
    """
    class Meta:
        model = None  # Real loyihada: Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================
# 4. Extra kwargs bilan
# ============================================

class BookWithExtraKwargsSerializer(serializers.ModelSerializer):
    """
    Extra kwargs orqali field sozlamalari
    """
    class Meta:
        model = None  # Real loyihada: Book
        fields = '__all__'
        extra_kwargs = {
            'isbn': {
                'required': True,
                'error_messages': {
                    'required': 'ISBN kiritilishi shart!',
                    'blank': 'ISBN bo\'sh bo\'lishi mumkin emas'
                }
            },
            'price': {
                'min_value': 10,
                'max_value': 1000,
            },
            'description': {
                'required': False,
                'allow_blank': True
            }
        }


# ============================================
# 5. SerializerMethodField bilan
# ============================================

class BookDetailSerializer(serializers.ModelSerializer):
    """
    Qo'shimcha computed fieldlar
    """
    # Qo'shimcha fieldlar
    days_since_published = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    
    class Meta:
        model = None  # Real loyihada: Book
        fields = '__all__'
    
    def get_days_since_published(self, obj):
        """Nashr qilinganiga necha kun bo'ldi"""
        # Real loyihada obj.published_date ishlatiladi
        # delta = date.today() - obj.published_date
        # return delta.days
        return 1500  # Demo uchun
    
    def get_is_new(self, obj):
        """Yangi kitobmi? (30 kun ichida)"""
        # days = self.get_days_since_published(obj)
        # return days <= 30
        return False  # Demo uchun
    
    def get_discount_price(self, obj):
        """10% chegirma narxi"""
        # Real loyihada obj.price ishlatiladi
        # return float(obj.price) * 0.9
        return 40.50  # Demo uchun


# ============================================
# 6. Custom validation bilan
# ============================================

class BookWithValidationSerializer(serializers.ModelSerializer):
    """
    Custom validation qo'shish
    """
    class Meta:
        model = None  # Real loyihada: Book
        fields = '__all__'
    
    def validate_isbn(self, value):
        """ISBN formatini tekshirish"""
        if len(value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
            )
        return value
    
    def validate_price(self, value):
        """Narxni tekshirish"""
        if value < 10:
            raise serializers.ValidationError(
                "Kitob narxi kamida 10$ bo'lishi kerak"
            )
        return value
    
    def validate(self, data):
        """Object-level validation"""
        if data.get('published_date') and data['published_date'] > date.today():
            raise serializers.ValidationError({
                "published_date": "Nashr sanasi kelajakda bo'lishi mumkin emas"
            })
        return data


# ============================================
# 7. Nested Serializers
# ============================================

class AuthorSerializer(serializers.ModelSerializer):
    """Author uchun serializer"""
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = None  # Real loyihada: Author
        fields = ['id', 'first_name', 'last_name', 'email', 'books_count']
    
    def get_books_count(self, obj):
        """Bu muallifning kitoblari soni"""
        # return obj.books.count()
        return 5  # Demo uchun


class CategorySerializer(serializers.ModelSerializer):
    """Category uchun serializer"""
    class Meta:
        model = None  # Real loyihada: Category
        fields = ['id', 'name', 'description']


class BookWithRelationsSerializer(serializers.ModelSerializer):
    """
    ForeignKey va ManyToMany bilan ishlash
    """
    # Read uchun to'liq ma'lumot
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    # Write uchun faqat ID
    author_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = None  # Real loyihada: Book
        fields = [
            'id', 'title', 'subtitle', 'isbn', 'price',
            'published_date', 'description',
            'author', 'author_id',
            'category', 'category_id'
        ]


# ============================================
# 8. Create va Update metodlarini override qilish
# ============================================

class BookCustomCreateSerializer(serializers.ModelSerializer):
    """
    Custom create va update logikasi
    """
    class Meta:
        model = None  # Real loyihada: Book
        fields = '__all__'
    
    def create(self, validated_data):
        """
        Custom create logic
        Masalan, yaratishdan oldin biror narsa qilish
        """
        print(f"📚 Yangi kitob yaratilmoqda: {validated_data.get('title')}")
        
        # Real loyihada:
        # book = Book.objects.create(**validated_data)
        # 
        # # Qo'shimcha amallar
        # send_notification(f"Yangi kitob qo'shildi: {book.title}")
        # 
        # return book
        
        return validated_data  # Demo uchun
    
    def update(self, instance, validated_data):
        """
        Custom update logic
        """
        print(f"✏️ Kitob yangilanmoqda: {validated_data.get('title', 'N/A')}")
        
        # Real loyihada:
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        # instance.save()
        # 
        # return instance
        
        return instance  # Demo uchun


# ============================================
# 9. Multiple serializers bitta model uchun
# ============================================

class BookMinimalSerializer(serializers.ModelSerializer):
    """Eng minimal ma'lumot - list uchun"""
    class Meta:
        model = None  # Real loyihada: Book
        fields = ['id', 'title', 'price']


class BookStandardSerializer(serializers.ModelSerializer):
    """Standart ma'lumot"""
    class Meta:
        model = None  # Real loyihada: Book
        fields = ['id', 'title', 'author', 'price', 'published_date']


class BookFullSerializer(serializers.ModelSerializer):
    """To'liq ma'lumot - detail uchun"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    days_since_published = serializers.SerializerMethodField()
    
    class Meta:
        model = None  # Real loyihada: Book
        fields = '__all__'
    
    def get_days_since_published(self, obj):
        return 1500  # Demo


# ============================================
# ISHLATISH MISOLLARI
# ============================================

def demo_examples():
    """ModelSerializer misollari"""
    print("=" * 50)
    print("MODELSERIALIZER MISOLLARI")
    print("=" * 50)
    
    print("\n1. ODDIY MODELSERIALIZER")
    print("-" * 50)
    print("class BookModelSerializer(serializers.ModelSerializer):")
    print("    class Meta:")
    print("        model = Book")
    print("        fields = '__all__'")
    print("\n✅ Eng sodda variant - barcha fieldlar avtomatik")
    
    print("\n2. MUAYYAN FIELDLAR")
    print("-" * 50)
    print("fields = ['id', 'title', 'author', 'price']")
    print("\n✅ Faqat kerakli fieldlarni ko'rsatish")
    
    print("\n3. SERIALIZERMETHODFIELD")
    print("-" * 50)
    print("days_since_published = serializers.SerializerMethodField()")
    print("\n✅ Qo'shimcha computed fieldlar qo'shish")
    
    print("\n4. NESTED SERIALIZERS")
    print("-" * 50)
    print("author = AuthorSerializer(read_only=True)")
    print("author_id = serializers.IntegerField(write_only=True)")
    print("\n✅ Related obyektlar bilan ishlash")
    
    print("\n5. VALIDATION")
    print("-" * 50)
    print("def validate_price(self, value):")
    print("    if value < 10:")
    print("        raise ValidationError('...')")
    print("\n✅ Custom validation qo'shish")
    
    print("\n" + "=" * 50)
    print("AFZALLIKLAR:")
    print("=" * 50)
    print("✅ Kamroq kod")
    print("✅ Avtomatik create() va update()")
    print("✅ Model bilan yaxshi integratsiya")
    print("✅ Tezkor development")
    
    print("\n" + "=" * 50)
    print("QACHON ISHLATILADI:")
    print("=" * 50)
    print("✅ Model bilan ishlashda")
    print("✅ CRUD operatsiyalar uchun")
    print("✅ Standart validation yetarli bo'lganda")
    print("✅ Kod miqdorini kamaytirish kerak bo'lganda")
    

if __name__ == "__main__":
    demo_examples()