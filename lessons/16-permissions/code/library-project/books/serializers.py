from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Book
from .validators import (
    validate_isbn_format,
    validate_not_digits_only,
    validate_no_special_chars,
    validate_capitalized,
    PriceRangeValidator,
    MinWordsValidator,
    YearRangeValidator
)
from datetime import date

class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = "__all__"

# ============================================
# 1. FIELD-LEVEL VALIDATION
# ============================================

class BookFieldValidationSerializer(serializers.ModelSerializer):
    """
    Field-level validation misollari
    Har bir field uchun alohida validate_ metodi
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_title(self, value):
        """
        Title validation:
        - Kamida 2 ta so'zdan iborat
        - Bosh harf bilan boshlanadi
        """
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Kitob nomi kamida 2 ta so'zdan iborat bo'lishi kerak"
            )
        
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Kitob nomi bosh harf bilan boshlanishi kerak"
            )
        
        if value.isdigit():
            raise serializers.ValidationError(
                "Sarlavha faqat raqamlardan iborat bo'lishi mumkin emas!"
            )
        
        return value.title()  # Har bir so'zni bosh harf bilan qaytarish
    
    def validate_author(self, value):
        """
        Author validation:
        - Kamida 2 ta so'z (ism va familiya)
        - Har bir so'z bosh harf bilan
        """
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Muallif ismi kamida 2 ta so'zdan (ism va familiya) iborat bo'lishi kerak"
            )
        
        for word in words:
            if not word[0].isupper():
                raise serializers.ValidationError(
                    "Har bir so'z bosh harf bilan boshlanishi kerak"
                )
        
        return value
    
    def validate_isbn(self, value):
        """
        ISBN validation:
        - 10 yoki 13 ta belgi
        - Unique bo'lishi kerak
        """
        clean_value = value.replace('-', '').replace(' ', '')
        
        if len(clean_value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
            )
        
        if not clean_value.isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        
        # Uniqueness check
        if not self.instance:  # Yangi obyekt
            if Book.objects.filter(isbn_number=value).exists():
                raise serializers.ValidationError(
                    "Bu ISBN allaqachon mavjud"
                )
        else:  # Mavjud obyektni yangilash
            if Book.objects.filter(isbn_number=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    "Bu ISBN allaqachon mavjud"
                )
        
        return value
    
    def validate_price(self, value):
        """
        Price validation:
        - Musbat son
        - 15000 so'm dan kam emas
        - 1000000 so'm dan ko'p emas
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Narx musbat son bo'lishi kerak"
            )
        
        if value < 15000:
            raise serializers.ValidationError(
                "Kitob narxi kamida 15000 so'm bo'lishi kerak"
            )
        
        if value > 1000000:
            raise serializers.ValidationError(
                "Narx 1000000 so'mdan oshmasligi kerak"
            )
        
        return value
    
    def validate_published_date(self, value):
        """
        Published date validation:
        - Kelajakda emas
        - 1450-yildan keyin (Gutenberg bosmaxonasi)
        """
        if value > date.today():
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        if value.year < 1450:
            raise serializers.ValidationError(
                "Nashr sanasi 1450-yildan keyin bo'lishi kerak"
            )
        
        return value


# ============================================
# 2. OBJECT-LEVEL VALIDATION
# ============================================

class BookObjectValidationSerializer(serializers.ModelSerializer):
    """
    Object-level validation misollari
    Bir nechta fieldlarni birgalikda tekshirish
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate(self, data):
        """
        Object-level validation:
        - Title va author kombinatsiyasi unique
        - Subtitle title'dan qisqa bo'lmasligi kerak
        """
        # 1. Title va author unique kombinatsiyasi
        title = data.get('title')
        author = data.get('author')
        
        if title and author:
            queryset = Book.objects.filter(title=title, author=author)
            
            if not self.instance:  # Yangi obyekt
                if queryset.exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
            else:  # Mavjud obyektni yangilash
                if queryset.exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
        
        # 2. Subtitle validation
        subtitle = data.get('subtitle', '')
        if subtitle and title:
            if len(subtitle) > len(title):
                raise serializers.ValidationError({
                    'subtitle': 'Subtitle asosiy nomdan uzun bo\'lmasligi kerak'
                })
        
        return data


# ============================================
# 3. CUSTOM VALIDATORS
# ============================================

class BookCustomValidatorsSerializer(serializers.ModelSerializer):
    """
    Custom validators bilan serializer
    Qayta ishlatish mumkin bo'lgan validator'lar
    """
    
    title = serializers.CharField(
        max_length=200,
        validators=[
            validate_no_special_chars,
            MinWordsValidator(2)
        ]
    )
    
    author = serializers.CharField(
        max_length=100,
        validators=[validate_capitalized]
    )
    
    isbn_number = serializers.CharField(
        max_length=17,
        validators=[
            validate_isbn_format,
            UniqueValidator(
                queryset=Book.objects.all(),
                message='Bu ISBN allaqachon mavjud'
            )
        ]
    )
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[PriceRangeValidator(5, 1000)]
    )
    
    published_date = serializers.DateField(
        validators=[YearRangeValidator(1450, date.today().year)]
    )
    
    class Meta:
        model = Book
        fields = '__all__'


# ============================================
# 4. BUILT-IN VALIDATORS
# ============================================

class BookBuiltInValidatorsSerializer(serializers.ModelSerializer):
    """
    Django built-in validators bilan serializer
    """
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(15000, message="Narx kamida 15000 so'm bo'lishi kerak"),
            MaxValueValidator(1000000, message="Narx 1000000 so'm dan oshmasligi kerak")
        ]
    )
    
    class Meta:
        model = Book
        fields = '__all__'


# ============================================
# 5. COMBINED VALIDATION (HAMMASINI BIRLASHTIRISH)
# ============================================

class BookCompleteValidationSerializer(serializers.ModelSerializer):
    """
    Barcha validation turlarini birlashtirgan to'liq serializer
    """
    
    # Custom validators
    title = serializers.CharField(
        max_length=200,
        validators=[
            validate_no_special_chars,
            validate_not_digits_only,
            MinWordsValidator(2)
        ]
    )
    
    isbn_number = serializers.CharField(
        max_length=17,
        validators=[
            validate_isbn_format,
            UniqueValidator(
                queryset=Book.objects.all(),
                message='Bu ISBN allaqachon mavjud'
            )
        ]
    )
    
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(15000, message="Narx kamida 15000 so'm bo'lishi kerak"),
            MaxValueValidator(1000000, message="Narx 1000000 so'm dan oshmasligi kerak")
        ]
    )
    
    published_date = serializers.DateField(
        validators=[YearRangeValidator(1450, date.today().year)]
    )
    
    class Meta:
        model = Book
        fields = '__all__'

    # Field-level validation
    def validate_author(self, value):
        """Author har bir so'z bosh harf bilan"""
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Muallif ismi kamida 2 ta so'zdan iborat bo'lishi kerak"
            )
        
        for word in words:
            if not word[0].isupper():
                raise serializers.ValidationError(
                    "Har bir so'z bosh harf bilan boshlanishi kerak"
                )
        
        return value
    
    # Object-level validation
    def validate(self, data):
        """Barcha fieldlarni tekshirish"""
        
        # Title va author unique kombinatsiyasi
        title = data.get('title')
        author = data.get('author')
        cover_image = data.get('cover_image')
        
        if title and author:
            queryset = Book.objects.filter(title=title, author=author)
            
            if not self.instance:
                if queryset.exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
            else:
                if queryset.exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
                
        if cover_image:
            same_cover_books = Book.objects.filter(cover_image=cover_image)
            if same_cover_books.exists():
                raise serializers.ValidationError(
                    "Bu rasm boshqa kitob uchun allaqachon ishlatilgan"
                )
        
        return data


# Default serializer (backward compatibility)
BookSerializer = BookCompleteValidationSerializer
BookModelSerializer = BookCompleteValidationSerializer
BookListSerializer = BookCompleteValidationSerializer
BookDetailSerializer = BookCompleteValidationSerializer

# ============================================
# HOMEWORK: VAZIFA 1 - FIELD-LEVEL VALIDATION
# ============================================

class BookHomeworkFieldValidationSerializer(serializers.ModelSerializer):
    """
    Homework: To'liq field-level validation
    Barcha fieldlar uchun validation qo'shilgan
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_title(self, value):
        """
        Title validation:
        ✅ Kamida 2 ta so'zdan iborat
        ✅ Bosh harf bilan boshlanishi
        ✅ Maxsus belgilar yo'q (faqat harflar, raqamlar, :,.)
        ✅ 200 belgidan oshmasligi
        """
        # 1. Kamida 2 ta so'z
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Kitob nomi kamida 2 ta so'zdan iborat bo'lishi kerak"
            )
        
        # 2. Bosh harf bilan boshlanishi
        if not value[0].isupper():
            raise serializers.ValidationError(
                "Kitob nomi bosh harf bilan boshlanishi kerak"
            )
        
        # 3. Maxsus belgilar tekshirish
        import re
        if not re.match(r'^[a-zA-Z0-9\s\-:,\.]+$', value):
            raise serializers.ValidationError(
                "Faqat harflar, raqamlar va asosiy belgilar (:,-.) ruxsat etilgan"
            )
        
        return value.title()
    
    def validate_author(self, value):
        """
        Author validation:
        ✅ Kamida 2 ta so'z (ism va familiya)
        ✅ Har bir so'z bosh harf bilan
        ✅ Faqat harflar va bo'shliq
        ✅ 100 belgidan oshmasligi
        """
        import re
        
        # 1. Faqat harflar va bo'shliq
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError(
                "Muallif ismi faqat harflar va bo'shliqdan iborat bo'lishi kerak"
            )
        
        # 2. Kamida 2 ta so'z
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError(
                "Muallif ismi kamida 2 ta so'zdan (ism va familiya) iborat bo'lishi kerak"
            )
        
        # 3. Har bir so'z bosh harf bilan
        for word in words:
            if not word[0].isupper():
                raise serializers.ValidationError(
                    "Har bir so'z bosh harf bilan boshlanishi kerak"
                )
        
        return value
    
    def validate_isbn_number(self, value):
        """
        ISBN validation:
        ✅ 10 yoki 13 ta belgidan iborat
        ✅ Faqat raqamlar (va '-' ruxsat)
        ✅ Unique bo'lishi kerak
        """
        import re
        
        # 1. Tozalash (- va bo'shliqlarni olib tashlash)
        clean_value = value.replace('-', '').replace(' ', '')
        
        # 2. Uzunlik tekshirish
        if len(clean_value) not in [10, 13]:
            raise serializers.ValidationError(
                "ISBN 10 yoki 13 ta belgidan iborat bo'lishi kerak"
            )
        
        # 3. Faqat raqamlar
        if not clean_value.isdigit():
            raise serializers.ValidationError(
                "ISBN faqat raqamlardan iborat bo'lishi kerak"
            )
        
        # 4. Format tekshirish (agar - bo'lsa)
        if '-' in value:
            if len(clean_value) == 10:
                pattern = r'^\d{1}-\d{3}-\d{5}-\d{1}$'
            else:  # 13
                pattern = r'^\d{3}-\d{1}-\d{3}-\d{5}-\d{1}$'
            
            if not re.match(pattern, value):
                raise serializers.ValidationError(
                    "ISBN formati noto'g'ri. To'g'ri format: XXX-X-XXX-XXXXX-X"
                )
        
        # 5. Unique tekshirish
        queryset = Book.objects.filter(isbn_number=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError(
                "Bu ISBN allaqachon mavjud"
            )
        
        return value
    
    def validate_price(self, value):
        """
        Price validation:
        ✅ Musbat son
        ✅ 5$ dan kam emas
        ✅ 1000$ dan ko'p emas
        ✅ Faqat 2 ta o'nlik xona
        """
        # 1. Musbat son
        if value <= 0:
            raise serializers.ValidationError(
                "Narx musbat son bo'lishi kerak"
            )
        
        # 2. Minimal narx
        if value < 5:
            raise serializers.ValidationError(
                "Kitob narxi kamida 5$ bo'lishi kerak"
            )
        
        # 3. Maksimal narx
        if value > 1000:
            raise serializers.ValidationError(
                "Narx 1000$ dan oshmasligi kerak"
            )
        
        # 4. O'nlik xonalar soni (2 ta)
        decimal_places = str(value).split('.')[-1] if '.' in str(value) else ''
        if len(decimal_places) > 2:
            raise serializers.ValidationError(
                "Narx faqat 2 ta o'nlik xonaga ega bo'lishi mumkin"
            )
        
        return value
    
    def validate_published_date(self, value):
        """
        Published date validation:
        ✅ Kelajakda bo'lmasligi kerak
        ✅ 1450-yildan keyin
        ✅ Bugundan 100 yildan ortiq emas
        """
        from datetime import date, timedelta
        
        today = date.today()
        
        # 1. Kelajakda emas
        if value > today:
            raise serializers.ValidationError(
                "Nashr sanasi kelajakda bo'lishi mumkin emas"
            )
        
        # 2. 1450-yildan keyin (Gutenberg bosmaxonasi)
        if value.year < 1450:
            raise serializers.ValidationError(
                "Nashr sanasi 1450-yildan keyin bo'lishi kerak (bosmaxona ixtirosi)"
            )
        
        # 3. 100 yildan ortiq emas
        hundred_years_ago = today - timedelta(days=36500)  # 100 yil
        if value < hundred_years_ago:
            raise serializers.ValidationError(
                "Nashr sanasi bugundan 100 yildan ortiq emas bo'lishi kerak"
            )
        
        return value
    
# ============================================
# HOMEWORK: VAZIFA 2 - OBJECT-LEVEL VALIDATION
# ============================================

class BookHomeworkObjectValidationSerializer(serializers.ModelSerializer):
    """
    Homework: Object-level validation
    Mavjud Book model fieldlari bilan ishlash
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate(self, data):
        """
        Object-level validation (soddalashtirilgan):
        1. Title va author unique kombinatsiyasi
        2. Subtitle uzunligi
        """
        # 1. Title va author unique bo'lishi kerak
        title = data.get('title')
        author = data.get('author')
        
        if title and author:
            queryset = Book.objects.filter(title=title, author=author)
            
            if not self.instance:  # Yangi obyekt
                if queryset.exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
            else:  # Mavjud obyektni yangilash
                if queryset.exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError(
                        "Bu muallif tomonidan bunday nomli kitob allaqachon mavjud"
                    )
        
        # 2. Subtitle validation
        subtitle = data.get('subtitle', '')
        if subtitle and title:
            if len(subtitle) > len(title):
                raise serializers.ValidationError({
                    'subtitle': 'Subtitle asosiy nomdan uzun bo\'lmasligi kerak'
                })
        
        # 3. Price va published_date bo'yicha qoidalar
        # 3. Price va published_date bo'yicha qoidalar
        price = data.get('price')
        published_date = data.get('published_date')
        
        if price and published_date:
            from datetime import date, timedelta
            
            # Yangi kitoblar qimmatroq bo'lishi kerak
            one_year_ago = date.today() - timedelta(days=365)
            
            # DEBUG: Ko'rish uchun
            print(f"Bugungi sana: {date.today()}")
            print(f"1 yil oldin: {one_year_ago}")
            print(f"Kitob sanasi: {published_date}")
            print(f"Yangi kitobmi: {published_date > one_year_ago}")
            
            if published_date > one_year_ago and price < 20:
                raise serializers.ValidationError({
                    'price': 'Oxirgi 1 yil ichida chiqgan kitoblar narxi kamida 20$ bo\'lishi kerak'
                })
        
        return data