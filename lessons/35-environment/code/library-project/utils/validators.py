"""
Environment variables validator
"""

from django.core.exceptions import ImproperlyConfigured
from decouple import config


class EnvironmentValidator:
    """Validate required environment variables"""
    
    # Required for all environments
    REQUIRED_VARS = [
        'SECRET_KEY',
    ]
    
    # Required for production
    PRODUCTION_REQUIRED = [
        'ALLOWED_HOSTS',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'EMAIL_HOST',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'REDIS_URL',
        'SENTRY_DSN',
    ]
    
    # Required for staging
    STAGING_REQUIRED = [
        'ALLOWED_HOSTS',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'REDIS_URL',
    ]
    
    @classmethod
    def validate_all(cls):
        """Validate all required environment variables"""
        print("\n" + "="*60)
        print("🔍 VALIDATING ENVIRONMENT VARIABLES")
        print("="*60)
        
        environment = config('ENVIRONMENT', default='development')
        missing = []
        
        # Check basic required vars
        print("\n📋 Checking basic requirements:")
        for var in cls.REQUIRED_VARS:
            if cls._check_var(var):
                print(f"  ✓ {var}: OK")
            else:
                print(f"  ✗ {var}: MISSING")
                missing.append(var)
        
        # Check environment-specific vars
        if environment == 'production':
            print("\n🚀 Checking PRODUCTION requirements:")
            for var in cls.PRODUCTION_REQUIRED:
                if cls._check_var(var):
                    print(f"  ✓ {var}: OK")
                else:
                    print(f"  ✗ {var}: MISSING")
                    missing.append(var)
        
        elif environment == 'staging':
            print("\n🔶 Checking STAGING requirements:")
            for var in cls.STAGING_REQUIRED:
                if cls._check_var(var):
                    print(f"  ✓ {var}: OK")
                else:
                    print(f"  ✗ {var}: MISSING")
                    missing.append(var)
        
        else:
            print("\n🔧 DEVELOPMENT mode - minimal checks")
        
        # Check SECRET_KEY strength
        if not missing or 'SECRET_KEY' not in missing:
            cls._validate_secret_key()
        
        print("\n" + "="*60)
        
        if missing:
            error_msg = f"Missing required environment variables: {', '.join(missing)}"
            print(f"❌ VALIDATION FAILED")
            print(f"   {error_msg}")
            print("="*60 + "\n")
            raise ImproperlyConfigured(error_msg)
        
        print("✅ ALL ENVIRONMENT VARIABLES VALIDATED")
        print("="*60 + "\n")
    
    @staticmethod
    def _check_var(var_name):
        """Check if variable exists and is not empty"""
        try:
            value = config(var_name)
            return bool(value and str(value).strip())
        except Exception:
            return False
    
    @staticmethod
    def _validate_secret_key():
        """Validate SECRET_KEY strength"""
        try:
            secret_key = config('SECRET_KEY')
            
            if len(secret_key) < 50:
                print("  ⚠ WARNING: SECRET_KEY is less than 50 characters")
            
            if 'django-insecure' in secret_key.lower():
                print("  ⚠ WARNING: SECRET_KEY contains 'django-insecure'")
            
            # Check for development key in production
            environment = config('ENVIRONMENT', default='development')
            if environment == 'production' and 'insecure' in secret_key.lower():
                raise ImproperlyConfigured(
                    "Cannot use insecure SECRET_KEY in production!"
                )
        
        except Exception as e:
            if isinstance(e, ImproperlyConfigured):
                raise
            print(f"  ⚠ Could not validate SECRET_KEY: {e}")


def validate_environment():
    """
    Wrapper function for easy import
    
    Usage:
        from utils.validators import validate_environment
        validate_environment()
    """
    EnvironmentValidator.validate_all()