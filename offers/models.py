from django.db import models

contract_choices = [
    ('CDI', 'CDI'),
    ('CDD', 'CDD'),
    ('Stage', 'Stage'),
    ('Freelance', 'Freelance')
]

class Offer(models.Model):
    title = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    salary = models.IntegerField()
    contract = models.CharField(choices=contract_choices, max_length=20)
    professional = models.ForeignKey('auth.User', on_delete=models.CASCADE)