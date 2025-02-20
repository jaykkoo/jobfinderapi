import pytest
from accounts.models import Profile
from offers.models import ContractType
from .utils import create_offer

@pytest.mark.django_db
def test_profile_str_method(create_user):
    profile = Profile.objects.get(user=create_user)

    assert str(profile) == profile.user.username

@pytest.mark.django_db
def test_contract_type_creation():
    contract = ContractType.objects.create(name="Full-time")
    assert contract.name == "Full-time"
    assert str(contract) == "Full-time"

@pytest.mark.django_db
def test_contract_type_unique_constraint():
    ContractType.objects.create(name="Part-time")
    
    with pytest.raises(Exception):  # Catch IntegrityError
        ContractType.objects.create(name="Part-time")

@pytest.mark.django_db
def test_offer_str(create_professional, create_contract_types, get_cdi):

    # Create an Offer instance
    offer = create_offer(
        title="Senior Developer",
        zip="12345",
        city="New York",
        salary=100000,
        user=create_professional,
        contracts=[get_cdi.id]
    )

    # Test the __str__ method
    assert str(offer) == "Senior Developer"