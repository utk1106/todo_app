import requests
import os
import json

# Configuration
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")  # Fallback for testing
REGISTRATION_ENDPOINT = "/api/register/"  # From urls.py
LOGIN_ENDPOINT = "/api/token/"  # JWT token endpoint

# Get data from environment variables
registration_data = {
    "phone_number": os.getenv("TEST_PHONE_NUMBER"),
    "email": os.getenv("TEST_EMAIL"),
    "name": os.getenv("TEST_NAME"),
    "password": os.getenv("TEST_PASSWORD")
}

login_data = {
    "email": os.getenv("TEST_EMAIL"),  # Using email for JWT login
    "password": os.getenv("TEST_PASSWORD")
}

def test_registration():
    if not all([registration_data["phone_number"], registration_data["email"], registration_data["name"], registration_data["password"]]):
        raise Exception("Missing required registration data (TEST_PHONE_NUMBER, TEST_EMAIL, TEST_NAME, or TEST_PASSWORD)")
    response = requests.post(BASE_URL + REGISTRATION_ENDPOINT, data=registration_data)
    print(f"Registration Status Code: {response.status_code}")
    print(f"Registration Response: {response.text}")
    if response.status_code == 201:
        print("Registration successful!")
    else:
        print("Registration failed!")
        raise Exception("Registration test failed")

def test_login():
    if not all([login_data["email"], login_data["password"]]):
        raise Exception("Missing required login data (TEST_EMAIL or TEST_PASSWORD)")
    response = requests.post(BASE_URL + LOGIN_ENDPOINT, data=login_data)
    print(f"Login Status Code: {response.status_code}")
    print(f"Login Response: {response.text}")
    if response.status_code == 200:
        print("Login successful!")
        # Optionally verify JWT token in response
        try:
            data = response.json()
            if "access" in data:
                print("JWT access token received!")
        except ValueError:
            print("Response is not JSON, but login might still succeed")
    else:
        print("Login failed!")
        raise Exception("Login test failed")

if __name__ == "__main__":
    try:
        print("Starting authentication validation...")
        test_registration()
        test_login()
        print("All authentication tests passed!")
    except Exception as e:
        print(f"Test failed: {str(e)}")
        exit(1)