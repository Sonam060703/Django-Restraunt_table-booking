# conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from table_management.models import Table, Reservation
from datetime import date, time, timedelta

User = get_user_model()

@pytest.fixture
def api_client():
    """Return an API client for testing"""
    return APIClient()

@pytest.fixture
def admin_user():
    """Create and return an admin user"""
    admin = User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='testpassword',
        is_admin=True
    )
    return admin

@pytest.fixture
def regular_user():
    """Create and return a regular user"""
    user = User.objects.create_user(
        username='user_test',
        email='user@test.com',
        password='testpassword'
    )
    return user

@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    """Return an API client authenticated as admin"""
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def authenticated_user_client(api_client, regular_user):
    """Return an API client authenticated as regular user"""
    api_client.force_authenticate(user=regular_user)
    return api_client

@pytest.fixture
def sample_table():
    """Create and return a sample table"""
    table = Table.objects.create(
        name='Table 1',
        capacity=4,
        is_available=True,
        location='Main Hall'
    )
    return table

@pytest.fixture
def future_date():
    """Return a date in the future for reservations"""
    return date.today() + timedelta(days=5)

@pytest.fixture
def sample_reservation(regular_user, sample_table, future_date):
    """Create and return a sample reservation"""
    reservation = Reservation.objects.create(
        user=regular_user,
        table=sample_table,
        reservation_date=future_date,
        start_time=time(18, 0),
        end_time=time(20, 0),
        party_size=2,
        status='confirmed'
    )
    return reservation