#!/usr/bin/env python
"""
Script to check if deployment settings are correct
Run this before deploying to production
"""
import os
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_vault.settings')

import django
django.setup()

from django.conf import settings
from django.core.management import execute_from_command_line

def check_settings():
    """Check if all required settings are configured"""
    errors = []
    warnings = []
    
    # Check SECRET_KEY
    if not settings.SECRET_KEY or settings.SECRET_KEY == 'django-insecure-change-this-in-production':
        errors.append("❌ SECRET_KEY is not set or is using default value!")
    else:
        print("✅ SECRET_KEY is set")
    
    # Check DEBUG
    if settings.DEBUG:
        warnings.append("⚠️  DEBUG is True - should be False in production")
    else:
        print("✅ DEBUG is False")
    
    # Check ALLOWED_HOSTS
    if '*' in settings.ALLOWED_HOSTS:
        warnings.append("⚠️  ALLOWED_HOSTS contains '*' - consider restricting for security")
    elif not settings.ALLOWED_HOSTS:
        errors.append("❌ ALLOWED_HOSTS is empty!")
    else:
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Check Database
    db = settings.DATABASES['default']
    if db['ENGINE'] == 'django.db.backends.sqlite3':
        warnings.append("⚠️  Using SQLite - PostgreSQL recommended for production")
    else:
        print(f"✅ Database: {db['ENGINE']}")
        if not db.get('NAME'):
            errors.append("❌ Database NAME is not set!")
        if not db.get('USER'):
            errors.append("❌ Database USER is not set!")
        if not db.get('HOST'):
            errors.append("❌ Database HOST is not set!")
    
    # Check Static Files
    if not settings.STATIC_ROOT:
        errors.append("❌ STATIC_ROOT is not set!")
    else:
        print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
    
    # Check if whitenoise is installed
    try:
        import whitenoise
        print("✅ WhiteNoise is installed")
    except ImportError:
        warnings.append("⚠️  WhiteNoise is not installed - static files may not work on Render")
    
    # Print results
    print("\n" + "="*50)
    if errors:
        print("\n❌ ERRORS FOUND:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n✅ No critical errors found!")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    return True

def check_database():
    """Check database connection"""
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    print("🔍 Checking deployment configuration...\n")
    
    settings_ok = check_settings()
    db_ok = check_database()
    
    print("\n" + "="*50)
    if settings_ok and db_ok:
        print("✅ All checks passed! Ready for deployment.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

