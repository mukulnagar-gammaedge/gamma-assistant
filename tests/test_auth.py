import pytest


class TestAuthentication:
    """Test authentication endpoints"""

    def test_signup_creates_user(self, client, test_user_credentials):
        """Test user signup creates a new user"""
        response = client.post(
            "/signup",
            params={
                "username": test_user_credentials["username"],
                "password": test_user_credentials["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "message" in data

    def test_signup_duplicate_user(self, client, test_user, test_user_credentials):
        """Test that duplicate username signup fails"""
        response = client.post(
            "/signup",
            params={
                "username": test_user_credentials["username"],
                "password": "differentpassword"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_login_valid_credentials(self, client, test_user, test_user_credentials):
        """Test login with valid credentials"""
        response = client.post(
            "/login",
            params={
                "username": test_user_credentials["username"],
                "password": test_user_credentials["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "role" in data
        assert data["role"] == "user"

    def test_login_invalid_password(self, client, test_user_credentials):
        """Test login with invalid password"""
        response = client.post(
            "/login",
            params={
                "username": test_user_credentials["username"],
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/login",
            params={
                "username": "nonexistentuser",
                "password": "anypassword"
            }
        )
        assert response.status_code == 401

  


class TestTokenGeneration:
    """Test token generation and verification"""

    def test_token_creation_succeeds(self, test_token):
        """Test that token can be created"""
        assert test_token is not None
        assert isinstance(test_token, str)
        assert len(test_token) > 0

