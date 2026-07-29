"""Tests for authentication infrastructure."""

import time

import jwt
import pytest

from backend.infrastructure.auth import JWTService
from backend.infrastructure.password_hasher import BcryptHasher


LONG_SECRET = "test-secret-key-that-is-at-least-32-bytes-long!!"


class TestJWTService:
    def setup_method(self):
        self.service = JWTService(secret=LONG_SECRET)

    def test_create_access_token(self):
        token = self.service.create_access_token("user123")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self):
        token = self.service.create_access_token("user123")
        payload = self.service.decode_token(token)
        assert payload["sub"] == "user123"
        assert payload["type"] == "access"

    def test_get_user_id_from_token(self):
        token = self.service.create_access_token("user123")
        user_id = self.service.get_user_id_from_token(token)
        assert user_id == "user123"

    def test_decode_expired_token(self):
        expired = jwt.encode(
            {"sub": "user1", "exp": 0, "type": "access"},
            LONG_SECRET,
            algorithm="HS256",
        )
        with pytest.raises(ValueError, match="Token has expired"):
            self.service.decode_token(expired)

    def test_decode_invalid_token(self):
        with pytest.raises(ValueError):
            self.service.decode_token("invalid-token")

    def test_refresh_token_structure(self):
        token = self.service.create_refresh_token("user123")
        payload = self.service.decode_token(token)
        assert payload["type"] == "refresh"


class TestBcryptHasher:
    def setup_method(self):
        self.hasher = BcryptHasher()

    def test_hash_returns_string(self):
        hashed = self.hasher.hash("password123")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_correct_password(self):
        hashed = self.hasher.hash("password123")
        assert self.hasher.verify("password123", hashed) is True

    def test_verify_incorrect_password(self):
        hashed = self.hasher.hash("password123")
        assert self.hasher.verify("wrongpassword", hashed) is False

    def test_same_password_hashes_differently(self):
        h1 = self.hasher.hash("password")
        h2 = self.hasher.hash("password")
        assert h1 != h2
