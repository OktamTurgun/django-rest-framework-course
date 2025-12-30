"""
Custom Social Account Adapters
===============================

Bu faylda social authentication jarayonini customize qilish uchun
custom adapterlar yozilgan.
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Social authentication uchun custom adapter
    
    Bu adapter quyidagi vazifalarni bajaradi:
    1. Email orqali existing user ni topish va ulash
    2. Provider-specific ma'lumotlarni qayta ishlash
    3. Profile picture, name va boshqa ma'lumotlarni saqlash
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Social login dan OLDIN chaqiriladi
        
        Bu yerda:
        - Agar user allaqachon social login qilgan bo'lsa, skip
        - Email orqali mavjud user ni topamiz
        - Topilsa - social account ni ulaymiz
        - Duplicate account prevention
        """
        # Agar user allaqachon social login qilgan bo'lsa
        if sociallogin.is_existing:
            return
        
        # Email olish
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return
        
        # Email orqali mavjud user ni topish
        try:
            existing_user = User.objects.get(email=email)
            
            # User active ekanligini tekshirish
            if not existing_user.is_active:
                raise ValidationError(
                    "Your account is inactive. Please contact support."
                )
            
            # Social account ni existing user ga ulash
            sociallogin.connect(request, existing_user)
            
            logger.info(f"✅ Connected {sociallogin.account.provider} account "
                       f"to existing user: {existing_user.username}")
        
        except User.DoesNotExist:
            # Yangi user yaratiladi
            logger.info(f"📝 New user will be created with email: {email}")
    
    def save_user(self, request, sociallogin, form=None):
        """
        Yangi user yaratilganda chaqiriladi
        
        Bu yerda:
        - Default user yaratish
        - Provider-specific ma'lumotlarni qo'shish
        - Profile picture, name, bio va boshqalar
        """
        # Parent metodini chaqirish (user yaratish)
        user = super().save_user(request, sociallogin, form)
        
        # Provider va ma'lumotlar
        provider = sociallogin.account.provider
        data = sociallogin.account.extra_data
        
        # Provider ga qarab ma'lumotlarni qayta ishlash
        if provider == 'google':
            self._process_google_data(user, data)
        elif provider == 'github':
            self._process_github_data(user, data)
        
        # Email verified (social login da email har doim verified)
        if hasattr(user, 'email_verified'):
            user.email_verified = True
        
        # Bio
        if hasattr(user, 'bio') and not user.bio:
            user.bio = f"Registered via {provider.capitalize()}"
        
        user.save()
        
        logger.info(f"✅ User saved: {user.username} (via {provider})")
        return user
    
    def _process_google_data(self, user, data):
        """
        Google dan kelgan ma'lumotlarni qayta ishlash
        
        Google extra_data:
        - email: Email address
        - name: Full name
        - given_name: First name
        - family_name: Last name
        - picture: Profile picture URL
        - locale: Language (en, uz, ru, etc.)
        - verified_email: Email verified boolean
        """
        # Profile picture
        if 'picture' in data and hasattr(user, 'profile_picture'):
            user.profile_picture = data['picture']
        
        # Name
        if 'name' in data and data['name']:
            parts = data['name'].split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        
        # Yoki given_name va family_name
        if not user.first_name and 'given_name' in data:
            user.first_name = data['given_name']
        if not user.last_name and 'family_name' in data:
            user.last_name = data['family_name']
        
        # Locale (language preference)
        if 'locale' in data and hasattr(user, 'language'):
            user.language = data['locale']
        
        logger.info(f"  📸 Google profile picture: {data.get('picture', 'N/A')}")
        logger.info(f"  👤 Name: {user.first_name} {user.last_name}")
    
    def _process_github_data(self, user, data):
        """
        GitHub dan kelgan ma'lumotlarni qayta ishlash
        
        GitHub extra_data:
        - login: GitHub username
        - name: Full name
        - email: Email address
        - avatar_url: Profile picture URL
        - bio: User bio
        - location: Location
        - company: Company name
        - blog: Website URL
        - html_url: GitHub profile URL
        - followers: Followers count
        - following: Following count
        - public_repos: Public repositories count
        """
        # Avatar
        if 'avatar_url' in data and hasattr(user, 'profile_picture'):
            user.profile_picture = data['avatar_url']
        
        # Name
        if 'name' in data and data['name']:
            parts = data['name'].split(' ', 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
        
        # Bio
        if 'bio' in data and data['bio'] and hasattr(user, 'bio'):
            user.bio = data['bio']
        
        # Location
        if 'location' in data and data['location'] and hasattr(user, 'location'):
            user.location = data['location']
        
        # Company
        if 'company' in data and data['company'] and hasattr(user, 'company'):
            user.company = data['company']
        
        # GitHub URL
        if 'html_url' in data and hasattr(user, 'github_url'):
            user.github_url = data['html_url']
        
        # GitHub username
        if 'login' in data and hasattr(user, 'github_username'):
            user.github_username = data['login']
        
        logger.info(f"  📸 GitHub avatar: {data.get('avatar_url', 'N/A')}")
        logger.info(f"  🐙 GitHub: @{data.get('login', 'N/A')}")
        logger.info(f"  🏢 Company: {data.get('company', 'N/A')}")
        logger.info(f"  📍 Location: {data.get('location', 'N/A')}")
    
    def populate_user(self, request, sociallogin, data):
        """
        User obyektini ma'lumotlar bilan to'ldirish
        
        Bu metod save_user dan OLDIN chaqiriladi
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Email
        if 'email' in data and not user.email:
            user.email = data['email']
        
        # Username (agar yo'q bo'lsa, email dan yaratish)
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
        
        Bu yerda:
        - Provider tekshirish
        - Email domain tekshirish
        - Boshqa validation rules
        """
        # Barcha providerlardan signup ruxsat berilgan
        # Agar cheklash kerak bo'lsa, bu yerda qo'shing
        
        # Masalan: Faqat Google va GitHub
        allowed_providers = ['google', 'github']
        if sociallogin.account.provider not in allowed_providers:
            return False
        
        return True
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Avtomatik signup ruxsat berilganmi?
        
        Agar False qaytarilsa, user qo'shimcha ma'lumot
        kiritishi kerak bo'ladi.
        """
        # Email verified bo'lsa, avtomatik signup
        email_verified = sociallogin.account.extra_data.get('verified_email', False)
        
        return email_verified
    
    # ❌ BU METODINI O'CHIRIB TASHLADIK
    # DefaultSocialAccountAdapter da authentication_error metodi yo'q!
    # Agar logging kerak bo'lsa, pre_social_login yoki save_user da qiling


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Oddiy registratsiya (non-social) uchun custom adapter
    """

    def save_user(self, request, user, form, commit=True):
        """
        Oddiy signup vaqtida user yaratish
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Email verification qilmasdan activate qilish (development)
        user.is_active = True
        if hasattr(user, 'email_verified'):
            user.email_verified = False

        if commit:
            user.save()
        
        # PROFILE bilan ishlash
        profile = getattr(user, 'profile', None)
        if profile and hasattr(profile, 'bio') and not profile.bio:
            profile.bio = "Regular registration"
            profile.save()
        
        return user

    def is_open_for_signup(self, request):
        """Oddiy signup ruxsat berilganmi?"""
        return True

    def clean_email(self, email):
        """Email validation va lowercase qilish"""
        email = email.lower()
        email = super().clean_email(email)
        return email