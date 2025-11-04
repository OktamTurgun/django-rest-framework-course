"""
Custom Validators
=================

Bu faylda qayta ishlatish mumkin bo'lgan validator'lar
"""

from rest_framework import serializers
import re


# ============================================
# FUNCTION-BASED VALIDATORS
# ============================================

def validate_positive(value):
    """Faqat musbat sonlar"""
    if value <= 0:
        raise serializers.ValidationError("Qiymat musbat bo'lishi kerak")


def validate_isbn_format(value):
    """
    ISBN formatini tekshirish
    Format: 10 yoki 13 ta raqam (- ruxsat etiladi)
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
    
def validate_not_digits_only(value):
    """
    Faqat raqamlardan iborat bo‘lmasin.
    Masalan: '12345' ❌ | 'Book 123' ✅
    """
    cleaned_value = value.replace(" ", "")
    if cleaned_value.isdigit():
        raise serializers.ValidationError(
            "Qiymat faqat raqamlardan iborat bo‘lishi mumkin emas."
        )


def validate_no_special_chars(value):
    """Maxsus belgilar yo'q (faqat harflar, raqamlar, asosiy belgilar)"""
    pattern = r'^[a-zA-Z0-9\s\-:,\.]+$'
    if not re.match(pattern, value):
        raise serializers.ValidationError(
            "Faqat harflar, raqamlar va asosiy belgilar (:,-.) ruxsat etilgan"
        )


def validate_capitalized(value):
    """Har bir so'z bosh harf bilan"""
    words = value.split()
    for word in words:
        if word and not word[0].isupper():
            raise serializers.ValidationError(
                "Har bir so'z bosh harf bilan boshlanishi kerak"
            )


# ============================================
# CLASS-BASED VALIDATORS
# ============================================

class PriceRangeValidator:
    """Narx oralig'ini tekshirish"""
    
    def __init__(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price
    
    def __call__(self, value):
        if not (self.min_price <= value <= self.max_price):
            raise serializers.ValidationError(
                f"Narx {self.min_price} so'm va {self.max_price} so'm orasida bo'lishi kerak"
            )


class MinWordsValidator:
    """Minimum so'zlar soni"""
    
    def __init__(self, min_words):
        self.min_words = min_words
    
    def __call__(self, value):
        words = value.split()
        if len(words) < self.min_words:
            raise serializers.ValidationError(
                f"Kamida {self.min_words} ta so'zdan iborat bo'lishi kerak"
            )


class YearRangeValidator:
    """Yil oralig'ini tekshirish"""
    
    def __init__(self, min_year, max_year):
        self.min_year = min_year
        self.max_year = max_year
    
    def __call__(self, value):
        year = value.year
        if not (self.min_year <= year <= self.max_year):
            raise serializers.ValidationError(
                f"Yil {self.min_year} va {self.max_year} orasida bo'lishi kerak"
            )