"""
Lesson 35: Environment Setup - Example 03
python-dotenv usage and patterns

Bu misolda:
- python-dotenv kutubxonasi
- load_dotenv() usullari
- Multiple .env files
- Environment priorities
- dotenv_values()
"""

import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values, find_dotenv, set_key, unset_key


# =====================================
# 1. BASIC DOTENV USAGE
# =====================================

def basic_dotenv():
    """load_dotenv() asosiy foydalanish"""
    print("=" * 50)
    print("1. BASIC DOTENV USAGE")
    print("=" * 50)
    
    # Create test .env file
    env_content = """SECRET_KEY=django-insecure-test-key
DEBUG=True
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=testpassword
"""
    
    env_file = Path('.env')
    env_file.write_text(env_content)
    
    # Load .env file
    load_dotenv()
    
    # Access variables
    secret_key = os.getenv('SECRET_KEY')
    debug = os.getenv('DEBUG')
    db_name = os.getenv('DB_NAME')
    
    print(f"SECRET_KEY: {secret_key}")
    print(f"DEBUG: {debug}")
    print(f"DB_NAME: {db_name}")
    
    # Cleanup
    env_file.unlink()
    print("\n✓ Test completed")
    print()


# =====================================
# 2. LOAD FROM SPECIFIC FILE
# =====================================

def load_specific_file():
    """Ma'lum .env fayldan yuklash"""
    print("=" * 50)
    print("2. LOAD FROM SPECIFIC FILE")
    print("=" * 50)
    
    # Create multiple .env files
    dev_env = Path('.env.development')
    prod_env = Path('.env.production')
    
    dev_env.write_text("""ENVIRONMENT=development
DEBUG=True
DB_HOST=localhost
DB_PORT=5432
""")
    
    prod_env.write_text("""ENVIRONMENT=production
DEBUG=False
DB_HOST=prod-db.example.com
DB_PORT=5432
""")
    
    # Load development
    print("Loading development environment:")
    load_dotenv(dotenv_path=dev_env)
    print(f"  ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
    print(f"  DEBUG: {os.getenv('DEBUG')}")
    print(f"  DB_HOST: {os.getenv('DB_HOST')}")
    
    # Clear and load production
    print("\nLoading production environment:")
    load_dotenv(dotenv_path=prod_env, override=True)
    print(f"  ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
    print(f"  DEBUG: {os.getenv('DEBUG')}")
    print(f"  DB_HOST: {os.getenv('DB_HOST')}")
    
    # Cleanup
    dev_env.unlink()
    prod_env.unlink()
    print("\n✓ Test completed")
    print()


# =====================================
# 3. FIND_DOTENV
# =====================================

def find_dotenv_example():
    """find_dotenv() - .env faylni avtomatik topish"""
    print("=" * 50)
    print("3. FIND_DOTENV")
    print("=" * 50)
    
    # Create nested structure
    project_dir = Path('test_project')
    project_dir.mkdir(exist_ok=True)
    
    env_file = project_dir / '.env'
    env_file.write_text("""PROJECT_NAME=TestProject
VERSION=1.0.0
""")
    
    # Save current directory
    original_dir = Path.cwd()
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Find .env file
    dotenv_path = find_dotenv()
    print(f"Found .env at: {dotenv_path}")
    
    # Load it
    load_dotenv(dotenv_path)
    print(f"PROJECT_NAME: {os.getenv('PROJECT_NAME')}")
    print(f"VERSION: {os.getenv('VERSION')}")
    
    # Go back
    os.chdir(original_dir)
    
    # Cleanup
    env_file.unlink()
    project_dir.rmdir()
    print("\n✓ Test completed")
    print()


# =====================================
# 4. DOTENV_VALUES
# =====================================

def dotenv_values_example():
    """dotenv_values() - Dict'ga yuklash"""
    print("=" * 50)
    print("4. DOTENV_VALUES")
    print("=" * 50)
    
    # Create .env file
    env_content = """APP_NAME=LibraryAPI
APP_VERSION=2.0.0
APP_DEBUG=True
APP_PORT=8000
DATABASE_URL=postgresql://user:pass@localhost/db
"""
    
    env_file = Path('.env.config')
    env_file.write_text(env_content)
    
    # Load as dictionary
    config = dotenv_values(env_file)
    
    print("Configuration dictionary:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print(f"\nAccess specific value:")
    print(f"  APP_NAME: {config['APP_NAME']}")
    print(f"  APP_VERSION: {config['APP_VERSION']}")
    
    # Type conversion needed
    print(f"\nWith type conversion:")
    app_debug = config['APP_DEBUG'] == 'True'
    app_port = int(config['APP_PORT'])
    print(f"  APP_DEBUG: {app_debug} (bool)")
    print(f"  APP_PORT: {app_port} (int)")
    
    # Cleanup
    env_file.unlink()
    print("\n✓ Test completed")
    print()


# =====================================
# 5. OVERRIDE BEHAVIOR
# =====================================

def override_behavior():
    """Override va priority testing"""
    print("=" * 50)
    print("5. OVERRIDE BEHAVIOR")
    print("=" * 50)
    
    # Set system environment variable
    os.environ['TEST_VAR'] = 'system_value'
    print(f"System env: TEST_VAR={os.getenv('TEST_VAR')}")
    
    # Create .env with same variable
    env_file = Path('.env')
    env_file.write_text('TEST_VAR=dotenv_value\n')
    
    # Load without override (default)
    print("\nLoad without override:")
    load_dotenv()
    print(f"  TEST_VAR={os.getenv('TEST_VAR')}")  # Still system_value
    
    # Load with override
    print("\nLoad with override=True:")
    load_dotenv(override=True)
    print(f"  TEST_VAR={os.getenv('TEST_VAR')}")  # Now dotenv_value
    
    # Cleanup
    env_file.unlink()
    del os.environ['TEST_VAR']
    print("\n✓ Test completed")
    print()


# =====================================
# 6. MULTIPLE ENV FILES
# =====================================

def multiple_env_files():
    """Multiple .env fayllar bilan ishlash"""
    print("=" * 50)
    print("6. MULTIPLE ENV FILES")
    print("=" * 50)
    
    # Base configuration
    base_env = Path('.env.base')
    base_env.write_text("""APP_NAME=LibraryAPI
APP_VERSION=1.0.0
DB_PORT=5432
REDIS_PORT=6379
""")
    
    # Development overrides
    dev_env = Path('.env.development')
    dev_env.write_text("""DEBUG=True
DB_HOST=localhost
DB_NAME=library_dev
LOG_LEVEL=DEBUG
""")
    
    # Production overrides
    prod_env = Path('.env.production')
    prod_env.write_text("""DEBUG=False
DB_HOST=prod-db.example.com
DB_NAME=library_prod
LOG_LEVEL=ERROR
""")
    
    # Load base first
    print("Loading configuration:")
    print("\n1. Base configuration:")
    load_dotenv(base_env)
    print(f"   APP_NAME: {os.getenv('APP_NAME')}")
    print(f"   APP_VERSION: {os.getenv('APP_VERSION')}")
    
    # Load development (merge)
    print("\n2. Development overrides:")
    load_dotenv(dev_env, override=True)
    print(f"   DEBUG: {os.getenv('DEBUG')}")
    print(f"   DB_HOST: {os.getenv('DB_HOST')}")
    print(f"   DB_NAME: {os.getenv('DB_NAME')}")
    print(f"   DB_PORT: {os.getenv('DB_PORT')}")  # From base
    
    # Cleanup
    base_env.unlink()
    dev_env.unlink()
    prod_env.unlink()
    print("\n✓ Test completed")
    print()


# =====================================
# 7. SET AND UNSET KEYS
# =====================================

def set_unset_keys():
    """set_key va unset_key funksiyalari"""
    print("=" * 50)
    print("7. SET AND UNSET KEYS")
    print("=" * 50)
    
    # Create .env file
    env_file = Path('.env.test')
    env_file.write_text("""INITIAL_KEY=initial_value
ANOTHER_KEY=another_value
""")
    
    print("Initial .env content:")
    print(env_file.read_text())
    
    # Set new key
    print("\nSetting NEW_KEY:")
    set_key(env_file, 'NEW_KEY', 'new_value')
    print(env_file.read_text())
    
    # Update existing key
    print("Updating INITIAL_KEY:")
    set_key(env_file, 'INITIAL_KEY', 'updated_value')
    print(env_file.read_text())
    
    # Unset key
    print("Unsetting ANOTHER_KEY:")
    unset_key(env_file, 'ANOTHER_KEY')
    print(env_file.read_text())
    
    # Cleanup
    env_file.unlink()
    print("✓ Test completed")
    print()


# =====================================
# 8. DJANGO INTEGRATION
# =====================================

def django_integration():
    """Django loyihasida python-dotenv ishlatish"""
    print("=" * 50)
    print("8. DJANGO INTEGRATION")
    print("=" * 50)
    
    print("""
# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Django settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Allowed hosts
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', 'localhost')
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_str.split(',')]

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Alternative: dj-database-url
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}
    """)


# =====================================
# 9. ENVIRONMENT LOADER CLASS
# =====================================

class EnvironmentLoader:
    """Advanced environment loader"""
    
    def __init__(self, env_file='.env'):
        self.env_file = Path(env_file)
        self.config = {}
        
    def load(self, override=False):
        """Load environment variables"""
        if self.env_file.exists():
            load_dotenv(self.env_file, override=override)
            self.config = dotenv_values(self.env_file)
            return True
        return False
    
    def get(self, key, default=None, cast=str):
        """Get environment variable with type casting"""
        value = os.getenv(key, default)
        
        if value is None:
            return default
        
        if cast == bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        elif cast == int:
            return int(value)
        elif cast == float:
            return float(value)
        elif cast == list:
            return [v.strip() for v in value.split(',')]
        else:
            return value
    
    def get_all(self):
        """Get all configuration"""
        return self.config.copy()
    
    def set(self, key, value):
        """Set environment variable"""
        set_key(self.env_file, key, str(value))
        os.environ[key] = str(value)
        self.config[key] = str(value)
    
    def unset(self, key):
        """Unset environment variable"""
        unset_key(self.env_file, key)
        if key in os.environ:
            del os.environ[key]
        if key in self.config:
            del self.config[key]
    
    def validate(self, required_keys):
        """Validate required keys"""
        missing = []
        for key in required_keys:
            if not os.getenv(key):
                missing.append(key)
        
        if missing:
            raise ValueError(f"Missing required keys: {', '.join(missing)}")
        
        return True


def environment_loader_example():
    """EnvironmentLoader class example"""
    print("=" * 50)
    print("9. ENVIRONMENT LOADER CLASS")
    print("=" * 50)
    
    # Create test .env
    env_file = Path('.env.loader')
    env_file.write_text("""SECRET_KEY=test-key
DEBUG=True
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
""")
    
    # Use loader
    loader = EnvironmentLoader('.env.loader')
    
    # Load
    if loader.load():
        print("✓ Environment loaded")
    
    # Get with type casting
    secret_key = loader.get('SECRET_KEY')
    debug = loader.get('DEBUG', cast=bool)
    db_port = loader.get('DB_PORT', cast=int)
    allowed_hosts = loader.get('ALLOWED_HOSTS', cast=list)
    
    print(f"\nLoaded values:")
    print(f"  SECRET_KEY: {secret_key}")
    print(f"  DEBUG: {debug} (type: {type(debug).__name__})")
    print(f"  DB_PORT: {db_port} (type: {type(db_port).__name__})")
    print(f"  ALLOWED_HOSTS: {allowed_hosts}")
    
    # Set new value
    print(f"\nSetting NEW_KEY:")
    loader.set('NEW_KEY', 'new_value')
    print(f"  NEW_KEY: {loader.get('NEW_KEY')}")
    
    # Get all
    print(f"\nAll configuration:")
    for key, value in loader.get_all().items():
        print(f"  {key}: {value}")
    
    # Validate
    print(f"\nValidating required keys:")
    try:
        loader.validate(['SECRET_KEY', 'DEBUG'])
        print("  ✓ Validation passed")
    except ValueError as e:
        print(f"  ✗ Validation failed: {e}")
    
    # Cleanup
    env_file.unlink()
    print("\n✓ Test completed")
    print()


# =====================================
# 10. BEST PRACTICES
# =====================================

def best_practices():
    """Best practices with python-dotenv"""
    print("=" * 50)
    print("10. BEST PRACTICES")
    print("=" * 50)
    
    print("""
1. Load early in application:
   # manage.py or wsgi.py
   from dotenv import load_dotenv
   load_dotenv()

2. Use specific paths:
   env_path = Path(__file__).parent / '.env'
   load_dotenv(dotenv_path=env_path)

3. Different files for different environments:
   .env.development
   .env.staging
   .env.production

4. Base + environment pattern:
   load_dotenv('.env.base')
   load_dotenv('.env.development', override=True)

5. Use dotenv_values() for config objects:
   config = dotenv_values('.env')
   db_config = {
       'host': config['DB_HOST'],
       'port': int(config['DB_PORT'])
   }

6. Never commit .env files:
   # .gitignore
   .env
   .env.*
   !.env.example

7. Document in .env.example:
   # .env.example
   # Required
   SECRET_KEY=
   DB_PASSWORD=
   
   # Optional (with defaults)
   DEBUG=True
   DB_HOST=localhost

8. Validate on startup:
   required = ['SECRET_KEY', 'DB_PASSWORD']
   for key in required:
       if not os.getenv(key):
           raise ValueError(f'{key} is required')

9. Use override carefully:
   # Usually False (system env takes precedence)
   load_dotenv(override=False)
   
   # True only when you want .env to override system
   load_dotenv(override=True)

10. Combine with decouple for type safety:
    from dotenv import load_dotenv
    from decouple import config
    
    load_dotenv()
    DEBUG = config('DEBUG', cast=bool)
    """)


# =====================================
# MAIN EXECUTION
# =====================================

def main():
    """Barcha misollarni ishga tushirish"""
    print("\n" + "=" * 50)
    print("LESSON 35: PYTHON-DOTENV USAGE")
    print("=" * 50 + "\n")
    
    # Examples
    basic_dotenv()
    load_specific_file()
    find_dotenv_example()
    dotenv_values_example()
    override_behavior()
    multiple_env_files()
    set_unset_keys()
    django_integration()
    environment_loader_example()
    best_practices()
    
    print("=" * 50)
    print("✅ All examples completed!")
    print("=" * 50)


if __name__ == '__main__':
    main()