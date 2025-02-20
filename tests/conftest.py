import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import connection
from offers.models import Offer, ContractType
from accounts.models import Profile


@pytest.fixture(scope='session')
def enable_pg_trgm_and_migrate(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            # Ensure the pg_trgm extension is installed and available
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
            
            # Run migrations to ensure database schema is up-to-date
            call_command('migrate', interactive=False)
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    Profile.objects.create(user=user, is_particular=True, is_professional=False)
    return user

@pytest.fixture
def create_professional():
    user = User.objects.create_user(username='testuserpro', password='testpass')
    Profile.objects.create(user=user, is_particular=False, is_professional=True)
    return user

@pytest.fixture
def create_user2():
    user = User.objects.create_user(username='testuser2', password='testpass')
    Profile.objects.create(user=user, is_particular=True, is_professional=False)
    return user

@pytest.fixture
def create_professional2():
    user = User.objects.create_user(username='testuserpro2', password='testpass')
    Profile.objects.create(user=user, is_particular=False, is_professional=True)
    return user

@pytest.fixture
def create_contract_types():
    ContractType.objects.get_or_create(name='CDI')
    ContractType.objects.get_or_create(name='CDD')
    ContractType.objects.get_or_create(name='Freelance')

@pytest.fixture
def get_user():
    return User.objects.get(username='testuser')

@pytest.fixture
def get_professional():
    return User.objects.get(username='testuserpro')

@pytest.fixture
def get_user2():
    return User.objects.get(username='testuser2')

@pytest.fixture
def get_professional2():
    return User.objects.get(username='testuserpro2')

@pytest.fixture
def get_cdi():
    return ContractType.objects.get(name='CDI')

@pytest.fixture
def get_cdd():
    return ContractType.objects.get(name='CDD')

@pytest.fixture
def get_freelance():
    return ContractType.objects.get(name='Freelance')
