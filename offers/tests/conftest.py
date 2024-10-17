import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Offer

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def auth_client(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    return api_client

@pytest.fixture
def offer(create_user):
    return Offer.objects.create(
        title='Test Offer', 
        zip='75000', 
        city='Paris',
        salary=30000,
        contract='CDI',
        professional=create_user
    )
