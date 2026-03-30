import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import auth
import sqlite3
import tempfile
import os
import uuid




@pytest.fixture
def client():
    """Provides a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def temp_db():
    """Creates a temporary database for testing"""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield db_path
    os.unlink(db_path)


@pytest.fixture(autouse=True)
def reset_auth():
    """Reset auth module state before each test"""
    # Call init_db to ensure tables exist
    try:
        auth.init_db()
    except Exception:
        pass
    yield


@pytest.fixture
def test_user_credentials():
    """Provides unique test user credentials for each test"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "username": f"testuser_{unique_id}",
        "password": "testpass123"
    }


@pytest.fixture
def test_user_admin_credentials():
    """Provides unique test admin credentials for each test"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "username": f"testadmin_{unique_id}",
        "password": "adminpass123"
    }


@pytest.fixture
def test_user(test_user_credentials):
    """Creates and returns a test user, cleans up after test"""
    # Clean up any existing user first
    auth.delete_user(test_user_credentials["username"])
    
    try:
        user_id = auth.create_user(
            test_user_credentials["username"],
            test_user_credentials["password"],
            role="user"
        )
        user_data = {
            "user_id": user_id,
            **test_user_credentials,
            "role": "user"
        }
        yield user_data
        
        # Cleanup after test
        auth.delete_user(test_user_credentials["username"])
    except Exception as e:
        pytest.fail(f"Could not create test user: {e}")


@pytest.fixture
def test_admin_user(test_user_admin_credentials):
    """Creates and returns a test admin user, cleans up after test"""
    # Clean up any existing user first
    auth.delete_user(test_user_admin_credentials["username"])
    
    try:
        user_id = auth.create_user(
            test_user_admin_credentials["username"],
            test_user_admin_credentials["password"],
            role="admin"
        )
        user_data = {
            "user_id": user_id,
            **test_user_admin_credentials,
            "role": "admin"
        }
        yield user_data
        
        # Cleanup after test
        auth.delete_user(test_user_admin_credentials["username"])
    except Exception as e:
        pytest.fail(f"Could not create test admin: {e}")


@pytest.fixture
def test_token(test_user):
    """Generates a test token"""
    try:
        token = auth.create_token(test_user["user_id"], test_user["role"])
        return token
    except Exception as e:
        pytest.fail(f"Could not create test token: {e}")


@pytest.fixture
def test_admin_token(test_admin_user):
    """Generates a test admin token"""
    try:
        token = auth.create_token(test_admin_user["user_id"], test_admin_user["role"])
        return token
    except Exception as e:
        pytest.fail(f"Could not create test admin token: {e}")


