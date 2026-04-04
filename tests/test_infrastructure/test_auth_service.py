import pytest
from datetime import timedelta
import jwt
from src.infrastructure.security.auth_service import create_access_token, decode_access_token, ALGORITHM, SECRET_KEY
from fastapi import HTTPException

def test_create_access_token():
    token = create_access_token(user_id="123", is_superuser=True, expires_delta=timedelta(minutes=15))
    
    # decode raw to verify
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "123"
    assert payload["is_superuser"] is True
    assert "exp" in payload

def test_decode_access_token_valid():
    token = create_access_token(user_id="user-uuid", is_superuser=False)
    
    decoded = decode_access_token(token)
    assert decoded["sub"] == "user-uuid"
    assert decoded["is_superuser"] is False

def test_decode_access_token_invalid():
    decoded = decode_access_token("fake.jwt.token")
    assert decoded is None

def test_decode_access_token_expired():
    # Pass negative timedelta to simulate expired token
    token = create_access_token(user_id="user", expires_delta=timedelta(seconds=-1))
    
    decoded = decode_access_token(token)
    assert decoded is None
