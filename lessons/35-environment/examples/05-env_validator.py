"""
Lesson 35: Environment Setup - Example 05
Environment Variables Validator

Bu misolda:
- Environment validation
- Required variables checking
- Type validation
- Custom validators
- Security checks
- Management command
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Callable
from decouple import config


# =====================================
# 1. BASIC VALIDATOR
# =====================================

class BasicEnvironmentValidator:
    """Oddiy environment validator"""
    
    REQUIRED_VARS = [
        'SECRET_KEY',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
    
    @classmethod
    def validate(cls):
        """Barcha required variablelarni tekshirish"""
        print("=" * 50)
        print("1. BASIC VALIDATION")
        print("=" * 50)
        
        missing = []
        
        for var in cls.REQUIRED_VARS:
            value = os.getenv(var)
            
            if value:
                print(f"✓ {var}: OK")
            else:
                print(f"✗ {var}: MISSING")
                missing.append(var)
        
        if missing:
            print(f"\n❌ Missing variables: {', '.join(missing)}")
            return False
        else:
            print(f"\n✅ All required variables are set!")
            return True


def basic_validator_example():
    """Basic validator example"""
    # Set test environment
    os.environ['SECRET_KEY'] = 'test-key'
    os.environ['DB_NAME'] = 'test_db'
    os.environ['DB_USER'] = 'test_user'
    os.environ['DB_PASSWORD'] = 'test_pass'
    
    BasicEnvironmentValidator.validate()
    print()


# =====================================
# 2. TYPED VALIDATOR
# =====================================

class TypedEnvironmentValidator:
    """Type checking bilan validator"""
    
    REQUIRED_VARS = {
        'SECRET_KEY': str,
        'DEBUG': bool,
        'DB_PORT': int,
        'TAX_RATE': float,
        'ALLOWED_HOSTS': list,
    }
    
    @classmethod
    def validate(cls):
        """Type checking bilan validation"""
        print("=" * 50)
        print("2. TYPE VALIDATION")
        print("=" * 50)
        
        errors = []
        
        for var_name, var_type in cls.REQUIRED_VARS.items():
            try:
                value = os.getenv(var_name)
                
                if not value:
                    errors.append(f"{var_name} is not set")
                    print(f"✗ {var_name}: NOT SET")
                    continue
                
                # Type conversion
                if var_type == bool:
                    converted = value.lower() in ('true', '1', 'yes')
                elif var_type == int:
                    converted = int(value)
                elif var_type == float:
                    converted = float(value)
                elif var_type == list:
                    converted = [v.strip() for v in value.split(',')]
                else:
                    converted = value
                
                # Check type
                if not isinstance(converted, var_type):
                    errors.append(f"{var_name} must be {var_type.__name__}")
                    print(f"✗ {var_name}: WRONG TYPE")
                else:
                    print(f"✓ {var_name}: OK ({var_type.__name__})")
                    
            except Exception as e:
                errors.append(f"{var_name}: {str(e)}")
                print(f"✗ {var_name}: ERROR - {str(e)}")
        
        if errors:
            print(f"\n❌ Validation failed:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print(f"\n✅ All validations passed!")
            return True


def typed_validator_example():
    """Type validator example"""
    # Set test environment
    os.environ['SECRET_KEY'] = 'test-key'
    os.environ['DEBUG'] = 'True'
    os.environ['DB_PORT'] = '5432'
    os.environ['TAX_RATE'] = '0.18'
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
    
    TypedEnvironmentValidator.validate()
    print()


# =====================================
# 3. ADVANCED VALIDATOR
# =====================================

class ValidationRule:
    """Validation rule class"""
    
    def __init__(self, name: str, var_type: type = str, 
                 required: bool = True, default: Any = None,
                 validator: Callable = None, message: str = None):
        self.name = name
        self.var_type = var_type
        self.required = required
        self.default = default
        self.validator = validator
        self.message = message or f"{name} validation failed"
    
    def validate(self, value: Any) -> tuple:
        """Validate value"""
        # Required check
        if self.required and not value:
            return False, f"{self.name} is required"
        
        # Use default if not set
        if not value:
            return True, self.default
        
        # Type conversion
        try:
            if self.var_type == bool:
                converted = value.lower() in ('true', '1', 'yes', 'on')
            elif self.var_type == int:
                converted = int(value)
            elif self.var_type == float:
                converted = float(value)
            elif self.var_type == list:
                converted = [v.strip() for v in value.split(',')]
            else:
                converted = value
        except Exception as e:
            return False, f"{self.name}: Type conversion failed - {str(e)}"
        
        # Custom validator
        if self.validator:
            try:
                if not self.validator(converted):
                    return False, self.message
            except Exception as e:
                return False, f"{self.name}: Validation error - {str(e)}"
        
        return True, converted


class AdvancedEnvironmentValidator:
    """Advanced environment validator with rules"""
    
    RULES = [
        ValidationRule(
            'SECRET_KEY',
            required=True,
            validator=lambda x: len(x) >= 50,
            message="SECRET_KEY must be at least 50 characters"
        ),
        ValidationRule(
            'DEBUG',
            var_type=bool,
            default=False
        ),
        ValidationRule(
            'ALLOWED_HOSTS',
            var_type=list,
            required=True,
            validator=lambda x: len(x) > 0,
            message="ALLOWED_HOSTS must not be empty"
        ),
        ValidationRule(
            'DB_NAME',
            required=True,
            validator=lambda x: len(x) > 0,
            message="DB_NAME must not be empty"
        ),
        ValidationRule(
            'DB_PORT',
            var_type=int,
            default=5432,
            validator=lambda x: 1 <= x <= 65535,
            message="DB_PORT must be between 1 and 65535"
        ),
        ValidationRule(
            'EMAIL_PORT',
            var_type=int,
            default=587,
            validator=lambda x: x in (25, 465, 587),
            message="EMAIL_PORT must be 25, 465, or 587"
        ),
    ]
    
    @classmethod
    def validate_all(cls):
        """Validate all rules"""
        print("=" * 50)
        print("3. ADVANCED VALIDATION")
        print("=" * 50)
        
        results = {}
        errors = []
        
        for rule in cls.RULES:
            value = os.getenv(rule.name)
            success, result = rule.validate(value)
            
            if success:
                results[rule.name] = result
                print(f"✓ {rule.name}: OK")
            else:
                errors.append(result)
                print(f"✗ {rule.name}: FAILED - {result}")
        
        if errors:
            print(f"\n❌ Validation failed ({len(errors)} errors):")
            for error in errors:
                print(f"  - {error}")
            return False, None
        else:
            print(f"\n✅ All validations passed!")
            return True, results


def advanced_validator_example():
    """Advanced validator example"""
    # Set test environment
    os.environ['SECRET_KEY'] = 'django-insecure-' + 'a' * 50
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = 'example.com'
    os.environ['DB_NAME'] = 'library_db'
    os.environ['DB_PORT'] = '5432'
    os.environ['EMAIL_PORT'] = '587'
    
    AdvancedEnvironmentValidator.validate_all()
    print()


# =====================================
# 4. SECURITY VALIDATOR
# =====================================

class SecurityValidator:
    """Security-focused validator"""
    
    @staticmethod
    def validate_secret_key(secret_key: str) -> tuple:
        """Validate SECRET_KEY"""
        if not secret_key:
            return False, "SECRET_KEY is required"
        
        if len(secret_key) < 50:
            return False, "SECRET_KEY must be at least 50 characters"
        
        if 'django-insecure' in secret_key.lower():
            return False, "SECRET_KEY contains 'django-insecure'"
        
        # Check complexity
        has_upper = any(c.isupper() for c in secret_key)
        has_lower = any(c.islower() for c in secret_key)
        has_digit = any(c.isdigit() for c in secret_key)
        has_special = any(c in '!@#$%^&*()_+-=' for c in secret_key)
        
        if not all([has_upper, has_lower, has_digit, has_special]):
            return False, "SECRET_KEY must contain uppercase, lowercase, digits, and special characters"
        
        return True, "SECRET_KEY is secure"
    
    @staticmethod
    def validate_debug_mode(debug: bool, environment: str) -> tuple:
        """Validate DEBUG mode"""
        if environment == 'production' and debug:
            return False, "DEBUG must be False in production"
        
        return True, "DEBUG mode is correct"
    
    @staticmethod
    def validate_allowed_hosts(hosts: list, environment: str) -> tuple:
        """Validate ALLOWED_HOSTS"""
        if not hosts:
            return False, "ALLOWED_HOSTS is empty"
        
        if environment == 'production':
            if 'localhost' in hosts or '127.0.0.1' in hosts:
                return False, "localhost/127.0.0.1 in ALLOWED_HOSTS (production)"
            
            if '*' in hosts:
                return False, "Wildcard '*' in ALLOWED_HOSTS (production)"
        
        return True, "ALLOWED_HOSTS is correct"
    
    @staticmethod
    def validate_database_password(password: str) -> tuple:
        """Validate database password"""
        if not password:
            return False, "Database password is required"
        
        if len(password) < 12:
            return False, "Database password must be at least 12 characters"
        
        if password in ['password', '123456', 'admin']:
            return False, "Database password is too common"
        
        return True, "Database password is secure"
    
    @classmethod
    def validate_all(cls, environment: str = 'production'):
        """Validate all security aspects"""
        print("=" * 50)
        print(f"4. SECURITY VALIDATION ({environment.upper()})")
        print("=" * 50)
        
        errors = []
        
        # SECRET_KEY
        secret_key = os.getenv('SECRET_KEY', '')
        success, message = cls.validate_secret_key(secret_key)
        if success:
            print(f"✓ SECRET_KEY: {message}")
        else:
            print(f"✗ SECRET_KEY: {message}")
            errors.append(message)
        
        # DEBUG
        debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
        success, message = cls.validate_debug_mode(debug, environment)
        if success:
            print(f"✓ DEBUG: {message}")
        else:
            print(f"✗ DEBUG: {message}")
            errors.append(message)
        
        # ALLOWED_HOSTS
        hosts_str = os.getenv('ALLOWED_HOSTS', '')
        hosts = [h.strip() for h in hosts_str.split(',') if h.strip()]
        success, message = cls.validate_allowed_hosts(hosts, environment)
        if success:
            print(f"✓ ALLOWED_HOSTS: {message}")
        else:
            print(f"✗ ALLOWED_HOSTS: {message}")
            errors.append(message)
        
        # Database password
        db_password = os.getenv('DB_PASSWORD', '')
        success, message = cls.validate_database_password(db_password)
        if success:
            print(f"✓ DB_PASSWORD: {message}")
        else:
            print(f"✗ DB_PASSWORD: {message}")
            errors.append(message)
        
        if errors:
            print(f"\n❌ Security validation failed ({len(errors)} issues)")
            return False
        else:
            print(f"\n✅ All security checks passed!")
            return True


def security_validator_example():
    """Security validator example"""
    # Set test environment
    os.environ['SECRET_KEY'] = 'Secure!Key123@' + 'x' * 50
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = 'example.com,www.example.com'
    os.environ['DB_PASSWORD'] = 'SecurePassword123!@#'
    
    SecurityValidator.validate_all('production')
    print()


# =====================================
# 5. ENVIRONMENT-SPECIFIC VALIDATOR
# =====================================

class EnvironmentValidator:
    """Environment-specific validator"""
    
    DEVELOPMENT_REQUIRED = [
        'SECRET_KEY',
        'DEBUG',
    ]
    
    STAGING_REQUIRED = [
        'SECRET_KEY',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'REDIS_URL',
    ]
    
    PRODUCTION_REQUIRED = [
        'SECRET_KEY',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'EMAIL_HOST',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'REDIS_URL',
        'ALLOWED_HOSTS',
    ]
    
    @classmethod
    def validate(cls, environment: str = 'development'):
        """Validate based on environment"""
        print("=" * 50)
        print(f"5. ENVIRONMENT-SPECIFIC VALIDATION ({environment.upper()})")
        print("=" * 50)
        
        # Get required vars for environment
        if environment == 'production':
            required_vars = cls.PRODUCTION_REQUIRED
        elif environment == 'staging':
            required_vars = cls.STAGING_REQUIRED
        else:
            required_vars = cls.DEVELOPMENT_REQUIRED
        
        missing = []
        
        for var in required_vars:
            value = os.getenv(var)
            
            if value:
                print(f"✓ {var}: OK")
            else:
                print(f"✗ {var}: MISSING")
                missing.append(var)
        
        if missing:
            print(f"\n❌ Missing {environment} variables:")
            for var in missing:
                print(f"  - {var}")
            return False
        else:
            print(f"\n✅ All {environment} variables are set!")
            return True


def environment_validator_example():
    """Environment validator example"""
    # Set test environment
    os.environ['SECRET_KEY'] = 'test-key'
    os.environ['DEBUG'] = 'True'
    os.environ['DB_NAME'] = 'library_db'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = 'password'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
    os.environ['EMAIL_HOST_USER'] = 'test@example.com'
    os.environ['EMAIL_HOST_PASSWORD'] = 'email_pass'
    os.environ['REDIS_URL'] = 'redis://localhost:6379/0'
    os.environ['ALLOWED_HOSTS'] = 'example.com'
    
    # Validate production
    EnvironmentValidator.validate('production')
    print()


# =====================================
# 6. COMPREHENSIVE VALIDATOR
# =====================================

class ComprehensiveValidator:
    """All-in-one comprehensive validator"""
    
    def __init__(self, environment: str = 'development'):
        self.environment = environment
        self.errors = []
        self.warnings = []
    
    def validate_required_vars(self):
        """Required variables check"""
        print("Checking required variables...")
        
        required = {
            'development': ['SECRET_KEY', 'DEBUG'],
            'staging': ['SECRET_KEY', 'DB_NAME', 'DB_PASSWORD', 'REDIS_URL'],
            'production': ['SECRET_KEY', 'DB_NAME', 'DB_PASSWORD', 'ALLOWED_HOSTS'],
        }
        
        for var in required.get(self.environment, []):
            if not os.getenv(var):
                self.errors.append(f"Missing required variable: {var}")
                print(f"  ✗ {var}: MISSING")
            else:
                print(f"  ✓ {var}: OK")
    
    def validate_security(self):
        """Security checks"""
        print("\nChecking security...")
        
        # SECRET_KEY
        secret_key = os.getenv('SECRET_KEY', '')
        if len(secret_key) < 50:
            self.errors.append("SECRET_KEY too short (< 50 chars)")
            print(f"  ✗ SECRET_KEY: TOO SHORT")
        else:
            print(f"  ✓ SECRET_KEY: OK")
        
        # DEBUG in production
        if self.environment == 'production':
            debug = os.getenv('DEBUG', 'False').lower() in ('true', '1')
            if debug:
                self.errors.append("DEBUG is True in production")
                print(f"  ✗ DEBUG: TRUE IN PRODUCTION")
            else:
                print(f"  ✓ DEBUG: FALSE")
    
    def validate_database(self):
        """Database configuration check"""
        print("\nChecking database...")
        
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        
        if db_name:
            print(f"  ✓ DB_NAME: {db_name}")
        
        if db_user:
            print(f"  ✓ DB_USER: {db_user}")
        
        if db_password and len(db_password) < 12:
            self.warnings.append("Database password is short (< 12 chars)")
            print(f"  ⚠ DB_PASSWORD: SHORT")
        elif db_password:
            print(f"  ✓ DB_PASSWORD: OK")
    
    def validate_email(self):
        """Email configuration check"""
        print("\nChecking email...")
        
        if self.environment in ['staging', 'production']:
            email_host = os.getenv('EMAIL_HOST')
            email_user = os.getenv('EMAIL_HOST_USER')
            email_password = os.getenv('EMAIL_HOST_PASSWORD')
            
            if not email_host:
                self.warnings.append("EMAIL_HOST not set")
                print(f"  ⚠ EMAIL_HOST: NOT SET")
            else:
                print(f"  ✓ EMAIL_HOST: {email_host}")
            
            if email_user:
                print(f"  ✓ EMAIL_HOST_USER: OK")
            if email_password:
                print(f"  ✓ EMAIL_HOST_PASSWORD: OK")
    
    def validate(self):
        """Run all validations"""
        print("=" * 50)
        print(f"6. COMPREHENSIVE VALIDATION ({self.environment.upper()})")
        print("=" * 50)
        print()
        
        self.validate_required_vars()
        self.validate_security()
        self.validate_database()
        self.validate_email()
        
        # Summary
        print("\n" + "=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print(f"\n✅ ALL CHECKS PASSED!")
            return True
        elif not self.errors:
            print(f"\n✅ No errors (but {len(self.warnings)} warnings)")
            return True
        else:
            print(f"\n❌ VALIDATION FAILED")
            return False


def comprehensive_validator_example():
    """Comprehensive validator example"""
    # Set test environment
    os.environ['SECRET_KEY'] = 'Secure!Key123@' + 'x' * 50
    os.environ['DEBUG'] = 'False'
    os.environ['DB_NAME'] = 'library_db'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = 'SecurePassword123!'
    os.environ['ALLOWED_HOSTS'] = 'example.com'
    os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
    os.environ['EMAIL_HOST_USER'] = 'test@example.com'
    os.environ['EMAIL_HOST_PASSWORD'] = 'email_pass'
    os.environ['REDIS_URL'] = 'redis://localhost:6379/0'
    
    validator = ComprehensiveValidator('production')
    validator.validate()
    print()


# =====================================
# 7. DJANGO MANAGEMENT COMMAND
# =====================================

def management_command_example():
    """Django management command example"""
    print("=" * 50)
    print("7. DJANGO MANAGEMENT COMMAND")
    print("=" * 50)
    
    print("""
# management/commands/validate_env.py
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.validators import ComprehensiveValidator


class Command(BaseCommand):
    help = 'Validate environment variables'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--environment',
            type=str,
            default='development',
            help='Environment to validate'
        )
    
    def handle(self, *args, **options):
        environment = options['environment']
        
        self.stdout.write(
            self.style.WARNING(
                f'Validating {environment} environment...'
            )
        )
        
        validator = ComprehensiveValidator(environment)
        success = validator.validate()
        
        if success:
            self.stdout.write(
                self.style.SUCCESS('✅ Validation successful!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Validation failed!')
            )
            exit(1)

# Usage:
# python manage.py validate_env --environment=production
    """)
    print()


# =====================================
# MAIN EXECUTION
# =====================================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "=" * 50)
    print("LESSON 35: ENVIRONMENT VALIDATOR")
    print("=" * 50 + "\n")
    
    # Examples
    basic_validator_example()
    typed_validator_example()
    advanced_validator_example()
    security_validator_example()
    environment_validator_example()
    comprehensive_validator_example()
    management_command_example()
    
    print("=" * 50)
    print("✅ All examples completed!")
    print("=" * 50)


if __name__ == '__main__':
    main()