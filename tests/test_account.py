import pytest
from rest_framework import status
from django.contrib.auth.models import User
from accounts.models import Profile
from .utils import force_authenticate


# Test Registration professional
@pytest.mark.django_db
def test_register_professional(api_client):
    data = {
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com',
        "profile": {
            "is_particular": False,
            "is_professional": True,
        }
    }

    response = api_client.post('/accounts/register/', data, format='json')
    user = User.objects.get(username='newuser')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User registered successfully.'
    assert User.objects.filter(username='newuser').exists()
    assert Profile.objects.filter(
        user=user, 
        is_professional=True,
        is_particular=False,
    ).exists()

# Test Registration professional
@pytest.mark.django_db
def test_register_user(api_client):
    data = {
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com',
        "profile": {
            "is_particular": True,
            "is_professional": False
        }
    }

    response = api_client.post('/accounts/register/', data, format='json')
    user = User.objects.get(username='newuser')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User registered successfully.'
    assert User.objects.filter(username='newuser').exists()
    assert Profile.objects.filter(
        user=user, 
        is_professional=False,
        is_particular=True
    ).exists()

@pytest.mark.django_db
def test_register_user_with_errors(api_client):
    data = {
        'username': '',
        'password': '',
        'email': '',
        "profile": {
            "is_particular": "",
            "is_professional": ""
        }
    }

    response = api_client.post('/accounts/register/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['username'][0] == 'This field may not be blank.'
    assert response.data['profile']['is_particular'][0] == 'Must be a valid boolean.'
    assert response.data['profile']['is_professional'][0] == 'Must be a valid boolean.'
    assert response.data['password'][0] == 'This field may not be blank.'

@pytest.mark.django_db
def test_register_user_with_error_email_only(api_client):
    data = {
        'username': 'lkdfgjlkfdg',
        'password': 'dfgdg99@@gf',
        'email': '',
        "profile": {
            "is_particular": True,
            "is_professional": False
        }
    }

    response = api_client.post('/accounts/register/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'] == 'Email is required.'
    


#Test Login
@pytest.mark.django_db
def test_login(api_client, create_user):
    data = {
        'username': "testuser",
        'password': "testpass"
    }
    
    response = api_client.post('/accounts/login/', data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'refresh_token' in response.cookies
    assert 'access_token' in response.data
    assert response.data['message'] == 'User logged in successfully.'

@pytest.mark.django_db
def test_login_with_empty_field(api_client):
    data = {
        'username': "",
        'password': ""
    }
    
    response = api_client.post('/accounts/login/', data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['password'][0] == 'This field may not be blank.'
    assert response.data['username'][0] == 'This field may not be blank.'

@pytest.mark.django_db
def test_login_with_bad_credentials(api_client):
    data = {
        'username': "toto",
        'password': "dkfgjdlfkg"
    }
    
    response = api_client.post('/accounts/login/', data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Invalid credentials.'

# Test Logout
@pytest.mark.django_db
def test_logout(api_client, create_user):
    # First, log in to get a refresh token

    
    force_authenticate(api_client, create_user)
    # Now log out
    response = api_client.post('/accounts/logout/', format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'User logged out successfully.'
    assert response.cookies['refresh_token'].value == ''


# Test Account Retrieval
@pytest.mark.django_db
def test_get_account(api_client, create_user):
    # Authenticate the user to access this view
    force_authenticate(api_client, create_user)
    
    response = api_client.get('/accounts/user/')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == create_user.username


# Test Account Update
@pytest.mark.django_db
def test_update_account(api_client, create_user):
    # Authenticate the user to access this view
    force_authenticate(api_client, create_user)
    data = {
        'email': 'newemail@example.com'
    }

    response = api_client.put('/accounts/user/', data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'User updated successfully.'
    create_user.refresh_from_db()  # Reload the user from the database
    assert create_user.email == 'newemail@example.com'

@pytest.mark.django_db
def test_update_account_with_error_email(api_client, create_user):
    # Authenticate the user to access this view
    force_authenticate(api_client, create_user)
    data = {
        'email': ''
    }

    response = api_client.put('/accounts/user/', data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'] == 'Email is required.'

@pytest.mark.django_db
def test_update_account_with_error_profile(api_client, create_user):
    # Authenticate the user to access this view
    force_authenticate(api_client, create_user)
    data = {
        'profile': {
            'is_particular': '',
            'is_professional': ''
        }        
    }

    response = api_client.put('/accounts/user/', data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['profile']['is_particular'][0] == 'Must be a valid boolean.'
    assert response.data['profile']['is_professional'][0] == 'Must be a valid boolean.'

def test_permission_denied(api_client):
    # Attempt to access a protected view without authentication
    response = api_client.get('/accounts/user/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Authentication credentials were not provided.'