import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure the settings for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SLID.settings')
import django
django.setup()

# Import test functions
from test_user_auth import (
    test_user_registration,
    test_user_login,
    test_user_registration_duplicate_username,
)
from test_user_profile import test_user_profile_creation
from test_content_creation import test_content_creation
from test_social_media_connection import test_social_media_connection
from test_terms_conditions import test_accept_terms
from test_system_workflow import test_system_workflow

def run_tests():
    all_passed = True

    try:
        print("Running test_user_auth.py...")
        test_user_registration()
        test_user_login()
        test_user_registration_duplicate_username()
        print("test_user_auth.py completed successfully.")
    except Exception as e:
        print(f"test_user_auth.py failed: {e}")
        all_passed = False

    try:
        print("Running test_user_profile.py...")
        test_user_profile_creation()
        print("test_user_profile.py completed successfully.")
    except Exception as e:
        print(f"test_user_profile.py failed: {e}")
        all_passed = False

    try:
        print("Running test_content_creation.py...")
        test_content_creation()
        print("test_content_creation.py completed successfully.")
    except Exception as e:
        print(f"test_content_creation.py failed: {e}")
        all_passed = False

    try:
        print("Running test_social_media_connection.py...")
        test_social_media_connection()
        print("test_social_media_connection.py completed successfully.")
    except Exception as e:
        print(f"test_social_media_connection.py failed: {e}")
        all_passed = False

    try:
        print("Running test_terms_conditions.py...")
        test_accept_terms()
        print("test_terms_conditions.py completed successfully.")
    except Exception as e:
        print(f"test_terms_conditions.py failed: {e}")
        all_passed = False

    try:
        print("Running test_system_workflow.py...")
        test_system_workflow()
        print("test_system_workflow.py completed successfully.")
    except Exception as e:
        print(f"test_system_workflow.py failed: {e}")
        all_passed = False

    return all_passed

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 