import pytest
from src.infrastructure.security.password_service import PasswordService

def test_password_hashing():
    svc = PasswordService()
    raw_password = "mySecretPassword123!"
    
    hashed = svc.get_password_hash(raw_password)
    
    assert hashed != raw_password
    assert len(hashed) > 10

def test_password_verification():
    svc = PasswordService()
    raw_password = "securePassword123!"
    
    hashed = svc.get_password_hash(raw_password)
    
    # Correct
    assert svc.verify_password(raw_password, hashed) is True
    # Incorrect
    assert svc.verify_password("wrongPassword123!", hashed) is False
