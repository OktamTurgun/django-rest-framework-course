"""
Parol validatsiyasi misollari
"""
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re


class CustomPasswordValidator:
    """
    Custom parol validator
    
    Talablar:
    - Kamida 8 ta belgi
    - Kamida 1 ta katta harf
    - Kamida 1 ta kichik harf
    - Kamida 1 ta raqam
    - Kamida 1 ta maxsus belgi
    """
    
    def validate(self, password, user=None):
        """Parolni validatsiya qilish"""
        
        # Minimum uzunlik
        if len(password) < 8:
            raise ValidationError(
                "Parol kamida 8 ta belgidan iborat bo'lishi kerak.",
                code='password_too_short'
            )
        
        # Katta harf
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "Parolda kamida 1 ta katta harf bo'lishi kerak.",
                code='password_no_upper'
            )
        
        # Kichik harf
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                "Parolda kamida 1 ta kichik harf bo'lishi kerak.",
                code='password_no_lower'
            )
        
        # Raqam
        if not re.search(r'\d', password):
            raise ValidationError(
                "Parolda kamida 1 ta raqam bo'lishi kerak.",
                code='password_no_digit'
            )
        
        # Maxsus belgi
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "Parolda kamida 1 ta maxsus belgi bo'lishi kerak (!@#$%^&*).",
                code='password_no_special'
            )
        
        # Username bilan o'xshamaslik
        if user and user.username.lower() in password.lower():
            raise ValidationError(
                "Parol username bilan o'xshab ketmasligi kerak.",
                code='password_too_similar'
            )
    
    def get_help_text(self):
        """Yordam matni"""
        return (
            "Parolingiz quyidagi talablarga javob berishi kerak:\n"
            "- Kamida 8 ta belgi\n"
            "- Kamida 1 ta katta harf (A-Z)\n"
            "- Kamida 1 ta kichik harf (a-z)\n"
            "- Kamida 1 ta raqam (0-9)\n"
            "- Kamida 1 ta maxsus belgi (!@#$%^&*)\n"
            "- Username bilan o'xshamamasligi kerak"
        )


def test_passwords():
    """Turli parollarni test qilish"""
    
    test_cases = [
        ("abc", False, "Juda qisqa"),
        ("abcdefgh", False, "Katta harf yo'q"),
        ("Abcdefgh", False, "Raqam yo'q"),
        ("Abcdefg1", False, "Maxsus belgi yo'q"),
        ("Abcdef1!", True, "To'g'ri parol"),
        ("SecurePass123!", True, "To'g'ri parol"),
        ("MyP@ssw0rd", True, "To'g'ri parol"),
    ]
    
    validator = CustomPasswordValidator()
    
    print("\n" + "="*60)
    print("PAROL VALIDATSIYA TESTLARI".center(60))
    print("="*60 + "\n")
    
    for password, should_pass, description in test_cases:
        print(f"Test: {description}")
        print(f"Parol: '{password}'")
        
        try:
            validator.validate(password)
            if should_pass:
                print("✅ To'g'ri - Parol validatsiyadan o'tdi\n")
            else:
                print("❌ Xato - Parol validatsiyadan o'tmasligi kerak edi\n")
        except ValidationError as e:
            if not should_pass:
                print(f"✅ To'g'ri - Xato: {e.message}\n")
            else:
                print(f"❌ Xato - Parol validatsiyadan o'tishi kerak edi: {e.message}\n")
    
    print("="*60)


def check_password_strength(password):
    """
    Parol kuchliligini baholash
    
    Returns:
        str: 'Zaif', 'O'rtacha', 'Kuchli'
    """
    score = 0
    
    # Uzunlik
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1
    
    # Turli xil belgilar
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    
    # Natija
    if score <= 3:
        return "Zaif", score
    elif score <= 5:
        return "O'rtacha", score
    else:
        return "Kuchli", score


def demo_password_strength():
    """Parol kuchliligi demo"""
    
    passwords = [
        "123456",
        "password",
        "Password1",
        "MyP@ssw0rd",
        "V3ry$tr0ng!P@ssw0rd123",
    ]
    
    print("\n" + "="*60)
    print("PAROL KUCHLILIGI BAHOSI".center(60))
    print("="*60 + "\n")
    
    for password in passwords:
        strength, score = check_password_strength(password)
        print(f"Parol: {password:30} | Ball: {score}/7 | {strength}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    test_passwords()
    demo_password_strength()
    
    print("\nValidator yordam matni:")
    print("-" * 60)
    validator = CustomPasswordValidator()
    print(validator.get_help_text())