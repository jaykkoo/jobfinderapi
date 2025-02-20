from offers.models import Offer

def create_offer(user, title, zip, city, salary, contracts=[]):
    offer = Offer.objects.create(
        title=title, 
        zip=zip, 
        city=city,
        salary=salary,
        professional=user
    )
    offer.contract.set(contracts)
    return offer

def force_authenticate(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

def create_offers(user, get_cdi, get_cdd, get_freelance):
    offers_data = [
        (1, 4, 'Paris', 75000, [get_cdi.id]),
        (4, 7, 'Marseille', 13000, [get_cdd.id]),
        (7, 10, 'Lyon', 69000, [get_freelance.id]),
        (10, 13, 'Toulouse', 31000, [get_cdi.id, get_cdd.id]),
        (13, 16, 'Serris', 77700, [get_cdi.id, get_freelance.id]),
        (16, 19, 'Lille', 59000, [get_freelance.id, get_cdd.id]),
    ]

    for start, end, city, zip_code, contracts in offers_data:
        for i in range(start, end):
            create_offer(user, f'Offer {i}', zip_code, city, 30000, contracts)