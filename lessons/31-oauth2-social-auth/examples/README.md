# OAuth2 & Social Authentication - Examples

Bu faylda Lesson 31 uchun amaliy misollar keltirilgan.

## Examples ro'yxati

1. **01-oauth2-flow-example.py** - OAuth2 flow va asosiy tushunchalar
2. **02-google-oauth-example.py** - Google OAuth2 integration
3. **03-github-oauth-example.py** - GitHub OAuth integration
4. **04-custom-adapter-example.py** - Custom social adapter implementation

## Har bir example nima o'rgatadi?

### 01-oauth2-flow-example.py
- OAuth2 protokolining qadamma-qadamlik ishlashi
- Authorization code flow
- State parameter va CSRF protection
- Access token va Refresh token

### 02-google-oauth-example.py
- Google Cloud Console sozlash
- django-allauth bilan Google OAuth2
- Callback URL handling
- User ma'lumotlarini olish

### 03-github-oauth-example.py
- GitHub OAuth App yaratish
- Scope management
- User va repository ma'lumotlarini olish
- Token bilan API requests

### 04-custom-adapter-example.py
- CustomSocialAccountAdapter yaratish
- pre_social_login hook
- save_user customization
- Email matching va duplicate prevention

## Ishlatish

Har bir faylni alohida o'rganish mumkin. Kodlar izohli va step-by-step tushuntirilgan.

```bash
# Fayllarni o'qish
cat 01-oauth2-flow-example.py
cat 02-google-oauth-example.py
cat 03-github-oauth-example.py
cat 04-custom-adapter-example.py
```

## Eslatma

Bu fayllar educational maqsadda yozilgan. Production kodda qo'shimcha xavfsizlik va error handling kerak.