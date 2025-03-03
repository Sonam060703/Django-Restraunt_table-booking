# authentication/tests/test_auth.py
import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.auth

@pytest.mark.user
def test_user_signup(api_client):
    """Test user registration"""
    url = reverse('signup')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'StrongPass123!'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'refresh' in response.data
    assert 'access' in response.data
    assert response.data['user']['username'] == 'newuser'
    assert response.data['user']['is_admin'] is False

@pytest.mark.user
def test_user_login(api_client, regular_user):
    """Test user login with JWT"""
    url = reverse('login')
    data = {
        'username': 'user_test',
        'password': 'testpassword'
    }