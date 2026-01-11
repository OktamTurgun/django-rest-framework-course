"""
Settings loader - Automatically loads correct environment settings
"""
from decouple import config

# Get environment from .env file
environment = config('ENVIRONMENT', default='development')

# Load appropriate settings based on environment
if environment == 'production':
    print("Loading PRODUCTION settings...")
    from .production import *
elif environment == 'staging':
    print("Loading STAGING settings...")
    from .staging import *
else:
    print("Loading DEVELOPMENT settings...")
    from .development import *

print(f"Running in {environment.upper()} mode")