
from app.app import app


def test_app_starts():
    """Check that the Flask application starts successfully."""
    assert app is not None


def test_homepage():
    """Check that the CodeVault homepage responds successfully."""
    client = app.test_client()

    response = client.get("/", follow_redirects=True)

    assert response.status_code == 200

