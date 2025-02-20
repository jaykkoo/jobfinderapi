from django.core.management.base import BaseCommand
from offers.models import Offer
import random
import string

class Command(BaseCommand):
    help = 'Creates 1000 Offer objects in the database'

    def handle(self, *args, **kwargs):
        # Define a function to generate random data for the Offer model
        def generate_random_string(length=10):
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Create 1000 Offer objects
        for i in range(5000):
            offer = Offer.objects.create(
                title=f"Offer {i + 1}",
                zip=77700,  # Random description
                city="Serris",  # Random description
                salary=random.uniform(10.0, 1000.0),     # Random price between 10 and 1000
                professional_id=2
            )
            offer.contract.set([1, 2])
        self.stdout.write(self.style.SUCCESS('Successfully created 1000 Offer objects'))