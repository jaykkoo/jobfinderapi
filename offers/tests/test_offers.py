import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_post_offer(auth_client, create_user):
    url = reverse('offer-create')
    data = {
        'title': 'New Offer',
        'zip': '75000',
        'city': 'Paris',
        'salary': 30000,
        'contract': 'CDI',
        'professional': create_user.id
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'offer created successfully.'

@pytest.mark.django_db
def test_get_offer(auth_client, offer):
    print(offer.id)
    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = auth_client.get(url)
    print(response)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == offer.title

@pytest.mark.django_db
def test_get_all_offers(auth_client, offer):
    url = reverse('offers')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

@pytest.mark.django_db
def test_put_offer(auth_client, offer, create_user):
    url = reverse('offer-detail', kwargs={'pk': offer.id})
    updated_data = {
        'title': 'New Offer2',
        'zip': '75000',
        'city': 'Paris',
        'salary': 30000,
        'contract': 'CDI',
        'professional': create_user.id
    }
    response = auth_client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'New Offer2'

@pytest.mark.django_db
def test_delete_offer(auth_client, offer):
    url = reverse('offer-detail', kwargs={'pk': offer.id})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Offer deleted successfully.'
