"""
Custom Social Account Adapter
==============================

Bu fayl django-allauth da custom adapter yaratish va
social login jarayonini customize qilishni ko'rsatadi.
"""

# ============================================================================
# 1. Adapter nima va nima uchun kerak?
# ============================================================================

"""
ADAPTER - bu django-allauth ning hook system.

Adapter yordamida quyidagilarni customize qilish mumkin:
1. pre_social_login - Social login dan OLDIN
2. save_user - Yangi user yaratilganda
3. populate_user - User ma'lumotlarini to'ldirganda
4. authentication_error - Xatolik yuz berganda
5. is_open_for_signup - Signup ruxsat berilganmi

Adapter hooks:
- pre_social_login(request, sociallogin)
- save_user(request, sociallogin, form=None)
- populate_user(request, sociallogin, data)
- authentication_error(request, provider_id, error, exception, extra_context)
- is_open_for_signup(request, sociallogin)
- is_auto_signup_allowed(request, sociallogin)
"""


# ============================================================================
# 2. Basic Custom Adapter
# ============================================================================

# api/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class BasicSocialAdapter(DefaultSocialAccountAdapter):
    """
    Oddiy custom adapter
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Social login dan OLDIN chaqiriladi
        
        Bu yerda:
        - Email orqali user topish
        - Duplicate account prevention
        - User validation
        """
        print(f"🔍 Pre-login check for provider: {sociallogin.account.provider}")
        
        # Agar user allaqachon social login qilgan bo'lsa, skip
        if sociallogin.is_existing:
            return
        
        # Email olish
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return
        
        # Email orqali mavjud user ni topish
        try:
            existing_user = User.objects.get(email=email)
            print(f"✅ Found existing user: {existing_user.username}")
            
            # Social account ni mavjud user ga ulash
            sociallogin.connect(request, existing_user)
            print(f"🔗 Connected {sociallogin.account.provider} to existing user")
        except User.DoesNotExist:
            print(f"📝 New user will be created with email: {email}")
    
    def save_user(self, request, sociallogin, form=None):
        """
        Yangi user yaratilganda chaqiriladi
        
        Bu yerda:
        - User ma'lumotlarini customize qilish
        - Qo'shimcha ma'lumotlar saqlash
        """
        print(f"💾 Saving new user from {sociallogin.account.provider}")
        
        # Parent metodini chaqirish (user yaratish)
        user = super().save_user(request, sociallogin, form)
        
        print(f"✅ User created: {user.username} ({user.email})")
        return user


# ============================================================================
# 3. Advanced Custom Adapter
# ============================================================================

class AdvancedSocialAdapter(DefaultSocialAccountAdapter):
    """
    Kengaytirilgan custom adapter
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Advanced pre-login logic
        """
        # Skip agar allaqachon login qilgan bo'lsa
        if sociallogin.is_existing:
            return
        
        # Email validation
        email = sociallogin.account.extra_data.get('email')
        
        if not email:
            from django.core.exceptions import ValidationError
            raise ValidationError(
                "Email address is required for social authentication"
            )
        
        # Email domain restriction (masalan: faqat company email)
        allowed_domains = ['example.com', 'company.com']
        email_domain = email.split('@')[1]
        
        if email_domain not in allowed_domains:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied(
                f"Only {', '.join(allowed_domains)} emails are allowed"
            )
        
        # Existing user ni topish va ulash
        try:
            existing_user = User.objects.get(email=email)
            
            # User status tekshirish
            if not existing_user.is_active:
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied("Your account is inactive")
            
            # Social account ni ulash
            sociallogin.connect(request, existing_user)
            
            # Log qilish
            print(f"🔗 Connected {sociallogin.account.provider} account "
                  f"to existing user {existing_user.username}")
        
        except User.DoesNotExist:
            # Yangi user yaratiladi
            print(f"📝 Creating new user with email: {email}")
    
    def save_user(self, request, sociallogin, form=None):
        """
        Advanced user saving logic
        """
        # Parent metodini chaqirish
        user = super().save_user(request, sociallogin, form)
        
        # Provider aniqlashtirish
        provider = sociallogin.account.provider
        data = sociallogin.account.extra_data
        
        # Provider ga qarab ma'lumotlarni to'ldirish
        if provider == 'google':
            self._process_google_data(user, data)
        elif provider == 'github':
            self._process_github_data(user, data)
        elif provider == 'facebook':
            self._process_facebook_data(user, data)
        
        # User bio
        user.bio = f"Registered via {provider.capitalize()}"
        
        # Email verification (social login da email verified)
        user.email_verified = True
        
        user.save()
        
        print(f"✅ User {user.username} saved with {provider} data")
        return user
    
    def _process_google_data(self, user, data):
        """
        Google dan kelgan ma'lumotlarni qayta ishlash
        """
        # Profile picture
        if 'picture' in data:
            user.profile_picture = data['picture']
        
        # Name
        if 'name' in data:
            parts = data['name'].split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        
        # Locale
        if 'locale' in data:
            user.language = data['locale']
        
        print(f"  📸 Profile picture: {user.profile_picture}")
        print(f"  👤 Name: {user.first_name} {user.last_name}")
    
    def _process_github_data(self, user, data):
        """
        GitHub dan kelgan ma'lumotlarni qayta ishlash
        """
        # Avatar
        if 'avatar_url' in data:
            user.profile_picture = data['avatar_url']
        
        # Name
        if 'name' in data and data['name']:
            parts = data['name'].split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        
        # Bio
        if 'bio' in data and data['bio']:
            user.bio = data['bio']
        
        # Location
        if 'location' in data:
            user.location = data['location']
        
        # Company
        if 'company' in data:
            user.company = data['company']
        
        # GitHub URL
        if 'html_url' in data:
            user.github_url = data['html_url']
        
        print(f"  📸 Avatar: {user.profile_picture}")
        print(f"  🏢 Company: {user.company}")
        print(f"  📍 Location: {user.location}")
    
    def _process_facebook_data(self, user, data):
        """
        Facebook dan kelgan ma'lumotlarni qayta ishlash
        """
        # Profile picture
        if 'picture' in data and 'data' in data['picture']:
            user.profile_picture = data['picture']['data']['url']
        
        # Name
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        # Location
        if 'location' in data and 'name' in data['location']:
            user.location = data['location']['name']
        
        print(f"  📸 Profile picture: {user.profile_picture}")
        print(f"  📍 Location: {user.location}")
    
    def populate_user(self, request, sociallogin, data):
        """
        User obyektini ma'lumotlar bilan to'ldirish
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Email
        if 'email' in data:
            user.email = data['email']
        
        # Username (email dan yaratish)
        if not user.username and user.email:
            username = user.email.split('@')[0]
            # Unique username yaratish
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
        
        return user
    
    def is_open_for_signup(self, request, sociallogin):
        """
        Signup ruxsat berilganmi?
        """
        # Masalan: faqat ma'lum providerlardan signup
        allowed_providers = ['google', 'github']
        
        if sociallogin.account.provider not in allowed_providers:
            return False
        
        # Masalan: faqat ma'lum email domainlardan
        email = sociallogin.account.extra_data.get('email')
        if email:
            domain = email.split('@')[1]
            if domain not in ['example.com', 'company.com']:
                return False
        
        return True
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Avtomatik signup ruxsat berilganmi?
        """
        # Email tasdiqlanganmi?
        email_verified = sociallogin.account.extra_data.get('verified_email', False)
        
        if not email_verified:
            return False
        
        return True
    
    def authentication_error(self, request, provider_id, error=None, 
                           exception=None, extra_context=None):
        """
        Autentifikatsiya xatoligida chaqiriladi
        """
        print(f"❌ Authentication error for {provider_id}: {error}")
        
        # Xatolik logini saqlash
        import logging
        logger = logging.getLogger(__name__)
        logger.error(
            f"Social auth error - Provider: {provider_id}, "
            f"Error: {error}, Exception: {exception}"
        )
        
        # Parent metodini chaqirish
        return super().authentication_error(
            request, provider_id, error, exception, extra_context
        )


# ============================================================================
# 4. Custom Account Adapter (Regular registration uchun)
# ============================================================================

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Oddiy registratsiya uchun custom adapter
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Oddiy registratsiyada user yaratish
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Email verification qilmasdan activate qilish
        user.is_active = True
        
        # Default values
        user.bio = "Regular registration"
        user.email_verified = False
        
        if commit:
            user.save()
        
        return user
    
    def is_open_for_signup(self, request):
        """
        Signup ochiqmi?
        """
        # Masalan: faqat invite code bilan signup
        invite_code = request.POST.get('invite_code')
        valid_codes = ['WELCOME2024', 'BETA_ACCESS']
        
        if invite_code not in valid_codes:
            return False
        
        return True


# ============================================================================
# 5. Settings.py Configuration
# ============================================================================

ADAPTER_SETTINGS = """
# settings.py

# Custom adapters
SOCIALACCOUNT_ADAPTER = 'api.adapters.AdvancedSocialAdapter'
ACCOUNT_ADAPTER = 'api.adapters.CustomAccountAdapter'

# Adapter bilan bog'liq sozlamalar
SOCIALACCOUNT_AUTO_SIGNUP = True  # Avtomatik signup
SOCIALACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # 'mandatory', 'optional', 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
"""

print("Adapter Settings:")
print(ADAPTER_SETTINGS)


# ============================================================================
# 6. Real-world Example: Company Social Auth
# ============================================================================

class CompanySocialAdapter(DefaultSocialAccountAdapter):
    """
    Kompaniya uchun maxsus social auth adapter
    
    Talablar:
    1. Faqat company email bilan signup
    2. Avtomatik department assignment
    3. Avtomatik role assignment
    4. Slack notification yuborish
    """
    
    COMPANY_DOMAINS = ['mycompany.com', 'subsidiary.com']
    
    def pre_social_login(self, request, sociallogin):
        """
        Pre-login validation
        """
        if sociallogin.is_existing:
            return
        
        email = sociallogin.account.extra_data.get('email')
        
        # Company email validation
        if not self._is_company_email(email):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied(
                "Only company email addresses are allowed"
            )
        
        # Existing user ni topish
        try:
            existing_user = User.objects.get(email=email)
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        User yaratish va company ma'lumotlarini qo'shish
        """
        user = super().save_user(request, sociallogin, form)
        
        # Email dan department ni aniqlash
        department = self._get_department_from_email(user.email)
        user.department = department
        
        # Role assignment
        user.role = self._assign_role(department)
        
        # Default permissions
        user.is_staff = True if department == 'IT' else False
        
        user.save()
        
        # Slack notification (async task)
        self._send_slack_notification(user)
        
        return user
    
    def _is_company_email(self, email):
        """
        Company email ekanligini tekshirish
        """
        if not email:
            return False
        
        domain = email.split('@')[1]
        return domain in self.COMPANY_DOMAINS
    
    def _get_department_from_email(self, email):
        """
        Email dan department ni aniqlash
        
        Masalan:
        john.doe.sales@mycompany.com -> Sales
        jane.smith.it@mycompany.com -> IT
        """
        parts = email.split('@')[0].split('.')
        
        department_keywords = {
            'sales': 'Sales',
            'it': 'IT',
            'hr': 'HR',
            'finance': 'Finance',
            'marketing': 'Marketing',
        }
        
        for part in parts:
            if part.lower() in department_keywords:
                return department_keywords[part.lower()]
        
        return 'General'
    
    def _assign_role(self, department):
        """
        Department bo'yicha role berish
        """
        role_mapping = {
            'IT': 'Admin',
            'Sales': 'User',
            'HR': 'Manager',
            'Finance': 'Manager',
            'Marketing': 'User',
            'General': 'User',
        }
        
        return role_mapping.get(department, 'User')
    
    def _send_slack_notification(self, user):
        """
        Slack ga notification yuborish
        """
        # Bu yerda Celery task bo'lishi kerak
        print(f"📨 Sending Slack notification for {user.username}")
        
        # Simulated notification
        message = f"New user joined: {user.get_full_name()} ({user.department})"
        print(f"  Message: {message}")


# ============================================================================
# 7. Testing Custom Adapter
# ============================================================================

def test_custom_adapter():
    """
    Custom adapter ni test qilish
    """
    print("\n" + "="*70)
    print("TESTING CUSTOM ADAPTER")
    print("="*70)
    
    test_scenarios = """
1. Email matching test:
   - Existing user with same email
   - Social account ulanishi kerak
   
2. Profile data test:
   - Google: picture, name, locale
   - GitHub: avatar, bio, location, company
   - Facebook: picture, location
   
3. Validation test:
   - Invalid email domain
   - Inactive user account
   - Missing email
   
4. Department assignment test:
   - Email pattern recognition
   - Correct role assignment
   
5. Error handling test:
   - Authentication errors
   - Network errors
   - Invalid provider
    """
    
    print(test_scenarios)
    
    # Unit test example
    unit_test = """
# api/tests/test_adapters.py
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount, SocialLogin
from api.adapters import AdvancedSocialAdapter

User = get_user_model()

class AdapterTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.adapter = AdvancedSocialAdapter()
    
    def test_email_matching(self):
        # Create existing user
        user = User.objects.create_user(
            username='existing',
            email='test@example.com'
        )
        
        # Simulate social login
        social_account = SocialAccount(
            provider='google',
            uid='123456',
            extra_data={'email': 'test@example.com'}
        )
        
        sociallogin = SocialLogin(account=social_account)
        request = self.factory.get('/')
        
        # Test pre_social_login
        self.adapter.pre_social_login(request, sociallogin)
        
        # Verify connection
        self.assertTrue(sociallogin.is_existing)
    """
    
    print("\n" + "="*70)
    print("UNIT TEST EXAMPLE:")
    print("="*70)
    print(unit_test)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🔧" * 35)
    print("CUSTOM SOCIAL ADAPTER GUIDE")
    print("🔧" * 35)
    
    test_custom_adapter()
    
    print("\n" + "✅" * 35)
    print("ADAPTER READY!")
    print("✅" * 35)
    
    print("\nAdapter Methods:")
    print("1. pre_social_login - Validation va existing user matching")
    print("2. save_user - User ma'lumotlarini customize qilish")
    print("3. populate_user - User obyektini to'ldirish")
    print("4. is_open_for_signup - Signup ruxsati")
    print("5. authentication_error - Xatolik handling")


"""
XULOSA:
=======

Custom Adapter afzalliklari:
1. Email orqali duplicate account prevention
2. Provider-specific ma'lumotlarni qayta ishlash
3. Company-specific logic (department, role)
4. Custom validation rules
5. Integration with other services (Slack, etc.)

Adapter Hooks:
- pre_social_login: Login dan oldin
- save_user: User yaratilganda
- populate_user: User to'ldirilganda
- is_open_for_signup: Signup ruxsati
- authentication_error: Xatolik handling

Best Practices:
1. Har doim parent metodini chaqiring (super())
2. Error handling qo'shing
3. Logging qo'shing
4. Unit tests yozing
5. Async tasks ishlatilsin (Celery)
"""