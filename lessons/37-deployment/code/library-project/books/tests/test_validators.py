"""
Books Validators Tests - REAL PROJECT
======================================

Custom validator testlari
"""

from django.test import TestCase
from rest_framework import serializers
from books.validators import (
    validate_isbn_format,
    validate_not_digits_only,
    validate_no_special_chars,
    validate_capitalized,
    PriceRangeValidator,
    MinWordsValidator,
    YearRangeValidator
)
from datetime import date


class ISBNValidatorTest(TestCase):
    """ISBN validator testlari"""
    
    def test_valid_isbn_10(self):
        """Valid 10 raqamli ISBN"""
        try:
            validate_isbn_format('1234567890')
        except serializers.ValidationError:
            self.fail("Valid ISBN raised ValidationError")
    
    def test_valid_isbn_13(self):
        """Valid 13 raqamli ISBN"""
        try:
            validate_isbn_format('9781234567897')
        except serializers.ValidationError:
            self.fail("Valid ISBN raised ValidationError")
    
    def test_isbn_too_short(self):
        """ISBN juda qisqa"""
        with self.assertRaises(serializers.ValidationError):
            validate_isbn_format('123456')
    
    def test_isbn_too_long(self):
        """ISBN juda uzun"""
        with self.assertRaises(serializers.ValidationError):
            validate_isbn_format('12345678901234')
    
    def test_isbn_with_letters(self):
        """ISBN'da harflar"""
        with self.assertRaises(serializers.ValidationError):
            validate_isbn_format('ABC1234567890')
    
    def test_empty_isbn(self):
        """Bo'sh ISBN"""
        with self.assertRaises(serializers.ValidationError):
            validate_isbn_format('')


class NotDigitsOnlyValidatorTest(TestCase):
    """Not digits only validator testlari"""
    
    def test_text_with_numbers_valid(self):
        """Text va raqamlar - valid"""
        try:
            validate_not_digits_only('Book 123')
        except serializers.ValidationError:
            self.fail("Valid text raised ValidationError")
    
    def test_only_digits_invalid(self):
        """Faqat raqamlar - invalid"""
        with self.assertRaises(serializers.ValidationError):
            validate_not_digits_only('12345')
    
    def test_only_text_valid(self):
        """Faqat text - valid"""
        try:
            validate_not_digits_only('Book Title')
        except serializers.ValidationError:
            self.fail("Valid text raised ValidationError")


class NoSpecialCharsValidatorTest(TestCase):
    """No special chars validator testlari"""
    
    def test_text_no_special_chars(self):
        """Maxsus belgilarsiz text"""
        try:
            validate_no_special_chars('Book Title')
            validate_no_special_chars('Book 123')
            validate_no_special_chars('Book-Title')
            validate_no_special_chars('Book: Title')
        except serializers.ValidationError:
            self.fail("Valid text raised ValidationError")
    
    def test_text_with_special_chars(self):
        """Maxsus belgilar bilan"""
        with self.assertRaises(serializers.ValidationError):
            validate_no_special_chars('Book@Title')
        
        with self.assertRaises(serializers.ValidationError):
            validate_no_special_chars('Book#Title')
        
        with self.assertRaises(serializers.ValidationError):
            validate_no_special_chars('Book$Title')


class CapitalizedValidatorTest(TestCase):
    """Capitalized validator testlari"""
    
    def test_all_words_capitalized(self):
        """Barcha so'zlar bosh harf bilan"""
        try:
            validate_capitalized('John Doe')
            validate_capitalized('John Smith Anderson')
        except serializers.ValidationError:
            self.fail("Valid text raised ValidationError")
    
    def test_not_capitalized(self):
        """Bosh harf bilan boshlanmagan"""
        with self.assertRaises(serializers.ValidationError):
            validate_capitalized('john doe')
        
        with self.assertRaises(serializers.ValidationError):
            validate_capitalized('John doe')


class PriceRangeValidatorTest(TestCase):
    """Price range validator testlari"""
    
    def test_price_in_range(self):
        """Narx oralig'ida"""
        validator = PriceRangeValidator(5, 1000)
        
        try:
            validator(10)
            validator(500)
            validator(999)
        except serializers.ValidationError:
            self.fail("Valid price raised ValidationError")
    
    def test_price_below_min(self):
        """Minimal narxdan past"""
        validator = PriceRangeValidator(5, 1000)
        
        with self.assertRaises(serializers.ValidationError):
            validator(3)
    
    def test_price_above_max(self):
        """Maksimal narxdan yuqori"""
        validator = PriceRangeValidator(5, 1000)
        
        with self.assertRaises(serializers.ValidationError):
            validator(1500)
    
    def test_price_at_boundaries(self):
        """Chegaradagi qiymatlar"""
        validator = PriceRangeValidator(5, 1000)
        
        try:
            validator(5)  # Minimal
            validator(1000)  # Maksimal
        except serializers.ValidationError:
            self.fail("Boundary values raised ValidationError")


class MinWordsValidatorTest(TestCase):
    """Min words validator testlari"""
    
    def test_enough_words(self):
        """Yetarli so'zlar"""
        validator = MinWordsValidator(2)
        
        try:
            validator('Two Words')
            validator('Three Words Here')
        except serializers.ValidationError:
            self.fail("Valid text raised ValidationError")
    
    def test_not_enough_words(self):
        """Yetarli emas"""
        validator = MinWordsValidator(2)
        
        with self.assertRaises(serializers.ValidationError):
            validator('OneWord')
        
        with self.assertRaises(serializers.ValidationError):
            validator('One')


class YearRangeValidatorTest(TestCase):
    """Year range validator testlari"""
    
    def test_year_in_range(self):
        """Yil oralig'ida"""
        validator = YearRangeValidator(1450, date.today().year)
        
        try:
            validator(date(2000, 1, 1))
            validator(date(1990, 6, 15))
            validator(date.today())
        except serializers.ValidationError:
            self.fail("Valid year raised ValidationError")
    
    def test_year_too_early(self):
        """Juda erta yil"""
        validator = YearRangeValidator(1450, date.today().year)
        
        with self.assertRaises(serializers.ValidationError):
            validator(date(1400, 1, 1))
    
    def test_year_too_late(self):
        """Kelajak yili"""
        validator = YearRangeValidator(1450, date.today().year)
        
        future_date = date(date.today().year + 1, 1, 1)
        
        with self.assertRaises(serializers.ValidationError):
            validator(future_date)
    
    def test_year_at_boundaries(self):
        """Chegaradagi yillar"""
        validator = YearRangeValidator(1450, 2024)
        
        try:
            validator(date(1450, 1, 1))  # Min
            validator(date(2024, 12, 31))  # Max
        except serializers.ValidationError:
            self.fail("Boundary years raised ValidationError")


class IntegratedValidationTest(TestCase):
    """Validatorlarni birgalikda test qilish"""
    
    def test_multiple_validators_pass(self):
        """Bir nechta validator - barcha o'tadi"""
        try:
            # ISBN
            validate_isbn_format('9781234567897')
            
            # Not digits only
            validate_not_digits_only('Book Title')
            
            # Capitalized
            validate_capitalized('John Doe')
            
            # Price range
            price_validator = PriceRangeValidator(5, 1000)
            price_validator(50)
            
            # Min words
            words_validator = MinWordsValidator(2)
            words_validator('Two Words')
            
        except serializers.ValidationError:
            self.fail("Valid values raised ValidationError")
    
    def test_multiple_validators_fail(self):
        """Bir nechta validator - ba'zilari fail"""
        # ISBN - fail
        with self.assertRaises(serializers.ValidationError):
            validate_isbn_format('123')
        
        # Only digits - fail
        with self.assertRaises(serializers.ValidationError):
            validate_not_digits_only('12345')
        
        # Not capitalized - fail
        with self.assertRaises(serializers.ValidationError):
            validate_capitalized('john doe')


class EdgeCaseValidationTest(TestCase):
    """Edge case validation testlari"""
    
    def test_empty_string_validators(self):
        """Bo'sh string"""
        # ISBN - bo'sh string
        with self.assertRaises(serializers.ValidationError):
            validate_isbn_format('')
        
        # Not digits only - bo'sh string (raqam emas)
        try:
            validate_not_digits_only('')
        except serializers.ValidationError:
            pass  # Expected or not depending on implementation
    
    def test_whitespace_validators(self):
        """Bo'sh joylar"""
        # ISBN with spaces
        with self.assertRaises(serializers.ValidationError):
            validate_isbn_format('123 456 789 012 3')
        
        # Capitalized with spaces
        try:
            validate_capitalized('John  Doe')  # Double space
        except serializers.ValidationError:
            pass
    
    def test_unicode_validators(self):
        """Unicode belgilar"""
        # Not digits with unicode
        try:
            validate_not_digits_only('Китоб')  # Cyrillic
        except serializers.ValidationError:
            self.fail("Unicode text raised ValidationError")