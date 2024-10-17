from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ['professional']

    def create(self, validated_data):
        validated_data['professional'] = self.context['request'].user
        return Offer.objects.create(**validated_data)

    