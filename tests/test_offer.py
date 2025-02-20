import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from offers.models import Offer, ContractType
from .utils import create_offer, force_authenticate, create_offers
from rest_framework.test import APIRequestFactory
from rest_framework.permissions import AllowAny, IsAuthenticated
from offers.views import OfferView
from config.permissions import IsProfessional, IsOwner
from unittest.mock import patch

@pytest.mark.django_db
def test_get_all_contracts_types(api_client, create_contract_types):
    url = reverse('get-all-contract-type')
    response = api_client.get(url)
    assert ContractType.objects.count() == 3
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    assert response.data[0]['name'] == 'CDI'

# Create
@pytest.mark.django_db
def test_create_offer(
    api_client ,
    create_contract_types, 
    get_cdi, 
    create_professional,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    url = reverse('offer-create')
    data = {
        "title": "New Offer",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [get_cdi.id, get_cdd.id],
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'offer created successfully.'
    assert Offer.objects.count() == 1

@pytest.mark.django_db
def test_create_offer_with_error(
    api_client ,
    create_professional,
):
    force_authenticate(api_client, create_professional)
    url = reverse('offer-create')
    data = {
        "title": "",
        "zip": "",
        "city": "",
        "salary": "",
        "contract": [],
    }
    response = api_client.post(url, data, format='json')
    response_data = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data['title'][0] == 'This field may not be blank.'
    assert response_data['zip'][0] == 'This field may not be blank.'
    assert response_data['city'][0] == 'This field may not be blank.'
    assert response_data['salary'][0] == 'A valid integer is required.'

@pytest.mark.django_db
def test_create_offer_without_contract(
    api_client ,
    create_professional,
):
    force_authenticate(api_client, create_professional)
    url = reverse('offer-create')
    data = {
        "title": "New Offer",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [],
    }
    response = api_client.post(url, data, format='json')
    response_data = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response_data['contract'] == 'This field cant be null.'

@pytest.mark.django_db
def test_create_offer_with_user(
    api_client ,
    create_contract_types, 
    get_cdi, 
    create_user,
    get_cdd
):
    force_authenticate(api_client, create_user)
    url = reverse('offer-create')
    data = {
        "title": "New Offer",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [get_cdi.id, get_cdd.id],
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data['detail'] == 'You do not have permission to perform this action.'

@pytest.mark.django_db
def test_permission_on_create_offer_not_login(
    api_client,
    create_contract_types,
    get_cdi, 
):
    url = reverse('offer-create')
    data = {
        "title": "Unauthorized Offer",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [get_cdi.id],
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 

# Pagination and display my offers

@pytest.mark.django_db
@pytest.mark.django_db
def test_pagination_offers(
    create_professional, 
    api_client,
    create_contract_types,
    get_cdi,
):
    """Test that pagination returns 10 offers per page and handles edge cases."""

    # Authenticate as a professional user
    api_client.force_authenticate(create_professional)

    # Create 20 offers (so we expect 2 pages)
    for i in range(1, 21):
        create_offer(create_professional, f'Offer {i}', '75000', 'Paris', 30000, [get_cdi])

    # Get first page
    url = reverse('offer-list')
    response = api_client.get(f"{url}?page=1")
    response_data = response.json()

    # Assertions for page 1
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data['offers']) == 10
    assert response_data['total_pages'] == 2  # Since we created 20 offers (10 per page)

    # Get second page
    response = api_client.get(f"{url}?page=2")
    response_data = response.json()

    # Assertions for page 2
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data['offers']) == 10  # Second 10 offers

    # Test invalid page (PageNotAnInteger -> Should default to page 1)
    response = api_client.get(f"{url}?page=abc")
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data['offers']) == 10  # Should return first page

    # Test out-of-range page (EmptyPage -> Should return last page)
    response = api_client.get(f"{url}?page=99")
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data['offers']) == 10  # Should return page 2 (last page)

@pytest.mark.django_db
def test_display_offers_without_permissions(
    create_professional,
    create_professional2,
    api_client,
    create_contract_types,
    get_cdi
):
    force_authenticate(api_client, create_professional)
    for i in range(1, 21):
        create_offer(create_professional, f'Offer {i}', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-list')
    response = api_client.get(url)
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data['offers']) == 10

    force_authenticate(api_client, create_professional2)
    response = api_client.get(url)
    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data['offers']) == 0

# Edit
@pytest.mark.django_db
def test_edit_offer(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd,

):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-update', args=[offer.id])
    data = {
        "title": "Offer 1 Updated",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [get_cdi.id, get_cdd.id],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    offer.refresh_from_db()
    assert offer.title == 'Offer 1 Updated'
    assert offer.zip == '75001'
    assert offer.salary == 40000
    assert offer.contract.all().count() == 2
    assert offer.contract.all()[0].name == get_cdi.name
    assert offer.contract.all()[1].name == get_cdd.name

@pytest.mark.django_db
def test_edit_offer_with_error(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd,

):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-update', args=[offer.id])
    data = {
        "title": "",
        "zip": "",
        "city": "",
        "salary": "",
        "contract": [],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert response_data['title'][0] == 'This field may not be blank.'
    assert response_data['zip'][0] == 'This field may not be blank.'
    assert response_data['city'][0] == 'This field may not be blank.'
    assert response_data['salary'][0] == 'A valid integer is required.'

@pytest.mark.django_db
def test_edit_offer_without_contract(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd,

):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-update', args=[offer.id])
    data = {
        "title": "Offer 1 Updated",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert response_data['contract'] == 'This field cant be null.'



@pytest.mark.django_db
def test_edit_offer_without_permission(
    create_professional,
    create_professional2,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-update', args=[offer.id])
    data = {
        "title": "Offer 1 Updated",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [get_cdi.id, get_cdd.id],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

    force_authenticate(api_client, create_professional2)
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_edit_offer_with_user(
    create_user,
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-update', args=[offer.id])
    data = {
        "title": "Offer 1 Updated",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [get_cdi.id, get_cdd.id],
    }

    force_authenticate(api_client, create_user)
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_edit_offer_not_connected(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-update', args=[offer.id])
    data = {
        "title": "Offer 1 Updated",
        "zip": "75001",
        "city": "Paris",
        "salary": 40000,
        "contract": [get_cdi.id, get_cdd.id],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Detail
@pytest.mark.django_db
def test_detail_offer(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-detail', args=[offer.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'Offer 1'

# Delete
@pytest.mark.django_db
def test_delete_offer(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-delete', args=[offer.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert Offer.objects.count() == 0

@pytest.mark.django_db
def test_delete_offer_with_bad_id(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    url = reverse('offer-delete', args=[9999999])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_offer_without_permission(
    create_professional,
    create_professional2,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-delete', args=[offer.id])

    force_authenticate(api_client, create_professional2)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_offer_not_connected(
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-delete', args=[offer.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_delete_offer_with_user(
    create_user,
    create_professional,
    api_client,
    create_contract_types,
    get_cdi,
    get_cdd
):
    force_authenticate(api_client, create_professional)
    offer = create_offer(create_professional, 'Offer 1', '75000', 'Paris', 30000, [get_cdi])
    url = reverse('offer-delete', args=[offer.id])
    force_authenticate(api_client, create_user)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

# Search
@pytest.mark.django_db
def test_search_connected_with_professional(
    create_contract_types,
    create_professional,
    api_client,
    get_cdi,
    get_cdd,
    get_freelance,
):
    force_authenticate(api_client, create_professional)
    create_offers(create_professional, get_cdi, get_cdd, get_freelance)
    url = reverse('offer-list')

    # Only CDI
    data = {
        'contract': [get_cdi.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # Only CDD
    data = {
        'contract': [get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 4'

    # Only Freelance
    data = {
        'contract': [get_freelance.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

    # Freelance and CDD
    data = {
        'contract': [get_freelance.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 4'

    # CDI and CDD
    data = {
        'contract': [get_cdi.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # CDI and freelance
    data = {
        'contract': [get_freelance.id, get_cdi.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # all contracts only
    data = {
        'contract': [get_freelance.id, get_cdi.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'
    #search on title and city
    data = {
        'title': 'Offer',
        'city': 'Paris',
        'zip': '75000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on partial title and city
    data = {
        'title': 'Offe',
        'city': 'Paris',
        'zip': '75000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on partial title
    data = {
        'title': 'Offe',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi and city
    data = {
        'contract': [get_cdi.id],
        'city': 'Serris',
        'zip': '77700',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 13'

    # search on contract cdd  and city
    data = {
        'contract': [get_cdd.id],
        'city': 'Serris',
        'zip': '77700',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 0
  
    # search on contract cdi and city
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'city': 'Toulouse',
        'zip': '31000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 10'

    # search on contract cdi and title
    data = {
        'contract': [get_cdi.id],
        'title': 'Offer',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi cdd and title
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'title': 'Offer',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi cdd and title and city
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'title': 'Offer',
        'city': 'Lille',
        'zip': '59000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 16'

    # search on contract freelance and title and city
    data = {
        'contract': [get_freelance.id],
        'title': 'Offer',
        'city': 'Lyon',
        'zip': '69000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

    # search on contract freelance and partial title and city
    data = {
        'contract': [get_freelance.id],
        'title': 'Offe',
        'city': 'Lyon',
        'zip': '69000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

@pytest.mark.django_db
def test_search_connected_with_user(
    create_contract_types,
    create_professional,
    create_user,
    api_client,
    get_cdi,
    get_cdd,
    get_freelance,
):  
    force_authenticate(api_client, create_user)
    create_offers(create_professional, get_cdi, get_cdd, get_freelance)
    url = reverse('offer-list')

    # Only CDI
    data = {
        'contract': [get_cdi.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # Only CDD
    data = {
        'contract': [get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 4'

    # Only Freelance
    data = {
        'contract': [get_freelance.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

    # Freelance and CDD
    data = {
        'contract': [get_freelance.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 4'

    # CDI and CDD
    data = {
        'contract': [get_cdi.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # CDI and freelance
    data = {
        'contract': [get_freelance.id, get_cdi.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # all contracts only
    data = {
        'contract': [get_freelance.id, get_cdi.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on title and city
    data = {
        'title': 'Offer',
        'city': 'Paris',
        'zip': '75000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on partial title and city
    data = {
        'title': 'Offe',
        'city': 'Paris',
        'zip': '75000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on partial title
    data = {
        'title': 'Offe',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi and city
    data = {
        'contract': [get_cdi.id],
        'city': 'Serris',
        'zip': '77700',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 13'

    # search on contract cdd  and city
    data = {
        'contract': [get_cdd.id],
        'city': 'Serris',
        'zip': '77700',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 0
  
    # search on contract cdi and city
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'city': 'Toulouse',
        'zip': '31000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 10'

    # search on contract cdi and title
    data = {
        'contract': [get_cdi.id],
        'title': 'Offer',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi cdd and title
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'title': 'Offer',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi cdd and title and city
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'title': 'Offer',
        'city': 'Lille',
        'zip': '59000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 16'

    # search on contract freelance and title and city
    data = {
        'contract': [get_freelance.id],
        'title': 'Offer',
        'city': 'Lyon',
        'zip': '69000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

    # search on contract freelance and partial title and city
    data = {
        'contract': [get_freelance.id],
        'title': 'Offe',
        'city': 'Lyon',
        'zip': '69000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

@pytest.mark.django_db
def test_search_no_connected(
    create_contract_types,
    create_professional,
    api_client,
    get_cdi,
    get_cdd,
    get_freelance,
):
    create_offers(create_professional, get_cdi, get_cdd, get_freelance)
    url = reverse('offer-list')

    # Only CDI
    data = {
        'contract': [get_cdi.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # Only CDD
    data = {
        'contract': [get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 4'

    # Only Freelance
    data = {
        'contract': [get_freelance.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

    # Freelance and CDD
    data = {
        'contract': [get_freelance.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 4'

    # CDI and CDD
    data = {
        'contract': [get_cdi.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # CDI and freelance
    data = {
        'contract': [get_freelance.id, get_cdi.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # all contracts only
    data = {
        'contract': [get_freelance.id, get_cdi.id, get_cdd.id],
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on title and city
    data = {
        'title': 'Offer',
        'city': 'Paris',
        'zip': '75000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on partial title and city
    data = {
        'title': 'Offe',
        'city': 'Paris',
        'zip': '75000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on partial title
    data = {
        'title': 'Offe',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi and city
    data = {
        'contract': [get_cdi.id],
        'city': 'Serris',
        'zip': '77700',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 13'

    # search on contract cdd  and city
    data = {
        'contract': [get_cdd.id],
        'city': 'Serris',
        'zip': '77700',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 0
  
    # search on contract cdi and city
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'city': 'Toulouse',
        'zip': '31000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 10'

    # search on contract cdi and title
    data = {
        'contract': [get_cdi.id],
        'title': 'Offer',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 9
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi cdd and title
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'title': 'Offer',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 10
    assert response.json()['total_pages'] == 2
    assert response.json()['offers'][0]['title'] == 'Offer 1'

    # search on contract cdi cdd and title and city
    data = {
        'contract': [get_cdi.id, get_cdd.id],
        'title': 'Offer',
        'city': 'Lille',
        'zip': '59000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 16'

    # search on contract freelance and title and city
    data = {
        'contract': [get_freelance.id],
        'title': 'Offer',
        'city': 'Lyon',
        'zip': '69000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'

    # search on contract freelance and partial title and city
    data = {
        'contract': [get_freelance.id],
        'title': 'Offe',
        'city': 'Lyon',
        'zip': '69000',
    }
    response = api_client.get(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['offers']) == 3
    assert response.json()['total_pages'] == 1
    assert response.json()['offers'][0]['title'] == 'Offer 7'


#  Test permissions
@pytest.mark.parametrize(
    "method, expected_permissions",
    [
        ("POST", [IsAuthenticated, IsProfessional]),
        ("PUT", [IsAuthenticated, IsOwner]),
        ("DELETE", [IsAuthenticated, IsOwner]),
        ("GET", [AllowAny]),
    ],
)
def test_offer_view_permissions(method, expected_permissions):
    """Test that OfferView returns the correct permissions for each HTTP method."""
    
    factory = APIRequestFactory()
    request = factory.generic(method, "/api/offers/")
    
    view = OfferView()
    view.request = request  # Manually set the request

    # Get permissions from view
    permissions = view.get_permissions()

    # Assert permission classes match expected
    assert len(permissions) == len(expected_permissions)
    for permission, expected in zip(permissions, expected_permissions):
        assert isinstance(permission, expected)


def test_offer_view_fallback_permissions():
    """Test that unsupported methods call super().get_permissions()."""

    factory = APIRequestFactory()
    request = factory.generic("PATCH", "/api/offers/")  # Unsupported method

    view = OfferView()
    view.request = request  # Manually set the request

    with patch.object(APIView, "get_permissions", return_value=["fallback"]) as mock_super:
        permissions = view.get_permissions()

        # Ensure super().get_permissions() was called
        mock_super.assert_called_once()

        # Ensure it returned the "fallback" value
        assert permissions == ["fallback"]