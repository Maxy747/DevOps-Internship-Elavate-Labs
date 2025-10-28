import pytest
from app import app as flask_app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with flask_app.test_client() as client:
        yield client

def test_hello_page(client):
    """Test the home page ('/') to ensure it returns the correct message."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, World!" in response.data
