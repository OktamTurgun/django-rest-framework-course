# Error Handling Examples

Bu papkada Django REST Framework'da error handling bilan ishlashning turli usullari ko'rsatilgan.

##  Example Files

### examples_01_custom_exceptions.py
Custom exception'lar yaratish va ulardan foydalanish.

**Topics:**
- Business logic exceptions
- HTTP exceptions
- Exception inheritance
- Error messages

### examples_02_exception_handler.py
Global exception handler yaratish va sozlash.

**Topics:**
- Custom exception handler
- Response formatting
- Logging integration
- Context information

### examples_03_logging.py
Django logging configuration va foydalanish.

**Topics:**
- Logging setup
- Different log levels
- Multiple handlers
- Log rotation
- Custom formatters

### examples_04_sentry.py
Sentry integration va error tracking.

**Topics:**
- Sentry setup
- Error capture
- Performance monitoring
- Custom context
- Breadcrumbs

##  Qanday Ishlatish

Har bir file'ni alohida o'rganish mumkin yoki ketma-ket o'qib chiqish mumkin.
```bash
# Example file'ni ko'rish
cat examples_01_custom_exceptions.py

# Python shell'da sinab ko'rish
python examples_01_custom_exceptions.py
```

##  Learning Path

1. **Start:** examples_01 - Custom exceptions
2. **Then:** examples_02 - Exception handler
3. **Next:** examples_03 - Logging
4. **Finally:** examples_04 - Sentry integration

##  Practice

Har bir example'dan keyin:
1.  Code'ni o'qing
2.  Comment'larni tushunib oling
3.  O'zingiz sinab ko'ring
4.  Qo'shimcha funksiyalar qo'shing

##  Resources

- [DRF Exceptions](https://www.django-rest-framework.org/api-guide/exceptions/)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Sentry Docs](https://docs.sentry.io/)