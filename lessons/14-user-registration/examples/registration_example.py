"""
Foydalanuvchi ro'yxatdan o'tkazish - Test skript
"""
import requests
import json


BASE_URL = "http://127.0.0.1:8000/api/accounts"


def register_user(username, email, password):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish
    """
    url = f"{BASE_URL}/register/"
    
    data = {
        "username": username,
        "email": email,
        "password": password,
        "password2": password
    }
    
    response = requests.post(url, json=data)
    
    print(f"\n{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print(f"{'='*50}\n")
    
    return response


def test_successful_registration():
    """
    Test 1: Muvaffaqiyatli ro'yxatdan o'tish
    """
    print("\n🧪 Test 1: Muvaffaqiyatli ro'yxatdan o'tish")
    response = register_user(
        username="newuser123",
        email="newuser123@example.com",
        password="SecurePass123!"
    )
    assert response.status_code == 201
    print("✅ Test o'tdi!")


def test_duplicate_username():
    """
    Test 2: Takroriy username
    """
    print("\n🧪 Test 2: Takroriy username")
    
    # Birinchi marta
    register_user(
        username="duplicateuser",
        email="user1@example.com",
        password="SecurePass123!"
    )
    
    # Ikkinchi marta (xato bo'lishi kerak)
    response = register_user(
        username="duplicateuser",
        email="user2@example.com",
        password="SecurePass123!"
    )
    assert response.status_code == 400
    print("✅ Test o'tdi!")


def test_duplicate_email():
    """
    Test 3: Takroriy email
    """
    print("\n🧪 Test 3: Takroriy email")
    
    # Birinchi marta
    register_user(
        username="user1",
        email="duplicate@example.com",
        password="SecurePass123!"
    )
    
    # Ikkinchi marta (xato bo'lishi kerak)
    response = register_user(
        username="user2",
        email="duplicate@example.com",
        password="SecurePass123!"
    )
    assert response.status_code == 400
    print("✅ Test o'tdi!")


def test_password_mismatch():
    """
    Test 4: Parollar bir xil emas
    """
    print("\n🧪 Test 4: Parollar bir xil emas")
    
    url = f"{BASE_URL}/register/"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "password2": "DifferentPass123!"  # Boshqa parol
    }
    
    response = requests.post(url, json=data)
    
    print(f"\n{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print(f"{'='*50}\n")
    
    assert response.status_code == 400
    print("✅ Test o'tdi!")


def test_weak_password():
    """
    Test 5: Zaif parol
    """
    print("\n🧪 Test 5: Zaif parol")
    
    response = register_user(
        username="weakpassuser",
        email="weak@example.com",
        password="123"  # Juda qisqa parol
    )
    assert response.status_code == 400
    print("✅ Test o'tdi!")


def test_missing_email():
    """
    Test 6: Email yo'q
    """
    print("\n🧪 Test 6: Email yo'q")
    
    url = f"{BASE_URL}/register/"
    data = {
        "username": "noemail",
        "password": "SecurePass123!",
        "password2": "SecurePass123!"
    }
    
    response = requests.post(url, json=data)
    
    print(f"\n{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print(f"{'='*50}\n")
    
    assert response.status_code == 400
    print("✅ Test o'tdi!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("USER REGISTRATION TEST SCRIPT".center(60))
    print("="*60)
    
    try:
        # Serverning ishlab turganini tekshirish
        response = requests.get(BASE_URL.replace('/accounts', '/'))
        print("✅ Server ishlamoqda!\n")
    except requests.exceptions.ConnectionError:
        print("❌ Xato: Server ishlamayapti!")
        print("Serverni ishga tushiring: python manage.py runserver")
        exit(1)
    
    # Testlarni ishga tushirish
    test_successful_registration()
    test_duplicate_username()
    test_duplicate_email()
    test_password_mismatch()
    test_weak_password()
    test_missing_email()
    
    print("\n" + "="*60)
    print("BARCHA TESTLAR MUVAFFAQIYATLI O'TDI! ✅".center(60))
    print("="*60 + "\n")