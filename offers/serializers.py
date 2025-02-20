from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Offer, ContractType


class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    contract = ContractTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Offer
        exclude = ['professional']

class OfferActionSerializer(serializers.ModelSerializer):
    contract = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ContractType.objects.all()
    )
    class Meta:
        model = Offer
        exclude = ['professional']

    def create(self, validated_data):
        contract_data = validated_data.pop('contract', [])
        if not contract_data:
            raise serializers.ValidationError({'contract': 'This field cant be null.'})
        validated_data['professional'] = self.context['request'].user
        offer = Offer.objects.create(**validated_data)
        offer.contract.set(contract_data)
        return offer


    def update(self, instance, validated_data):
        contract_data = validated_data.pop('contract', None)
        if not contract_data:
            raise serializers.ValidationError({'contract': 'This field cant be null.'})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if contract_data is not None:
            instance.contract.set(contract_data)
        return instance