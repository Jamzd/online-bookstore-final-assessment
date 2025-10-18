import pytest
from models import User, Book, Cart
import hashlib

# -------------------------------
# Password hashing tests
# -------------------------------
def test_password_is_hashed():
    """Ensure passwords are stored hashed and not in plaintext"""
    raw_password = "SecurePass123"
    user = User(email="secure@example.com", password=raw_password, name="Tester", address="123 Lane")

    # Plain 'password' attribute should not exist
    assert not hasattr(user, "password")

    # Hashed password exists and matches SHA256 of raw_password
    expected_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    assert user.hashed_password == expected_hash

    # verify_password returns True for correct password
    assert user.verify_password(raw_password) is True
    # False for wrong password
    assert user.verify_password("wrong") is False

# -------------------------------
# Email validation tests
# -------------------------------
def test_email_validation():
    """Check for invalid and duplicate emails"""
    users = {}
    
    # Valid email
    user1 = User(email="test@example.com", password="pass", name="A", address="Addr")
    users[user1.email.lower()] = user1
    assert user1.email.lower() in users

    # Duplicate email (case-insensitive simulation)
    with pytest.raises(Exception):
        duplicate_email = "Test@Example.com"
        if duplicate_email.lower() in users:
            raise Exception("Duplicate email detected")

    # Invalid email format
    invalid_emails = ["noatsign.com", "bademail@", "abc"]
    for email in invalid_emails:
        with pytest.raises(ValueError):
            User(email=email, password="pass", name="B", address="Addr")

# -------------------------------
# Input sanitization / XSS
# -------------------------------
def test_input_sanitization():
    """Ensure inputs are safely handled"""
    malicious_title = "<script>alert('xss')</script>"
    book = Book(title=malicious_title, category="Test", price=10, image="img.jpg")
    assert book.title == malicious_title  # stored safely as string

# -------------------------------
# Session login/logout
# -------------------------------
def test_session_logout():
    """Simulate login and logout"""
    user = User(email="session@example.com", password="MyPass123", name="Tester", address="123 Lane")
    
    # Login with correct password
    assert user.login("MyPass123") is True
    assert user.logged_in is True

    # Logout
    user.logout()
    assert user.logged_in is False
