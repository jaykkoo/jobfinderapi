            
            
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .serializers import OfferSerializer
from .models import Offer
from jobfinderapi.permissions import IsOwner


class OfferView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def post(self, request, *args, **kwargs):
        serializer = OfferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'offer created successfully.'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            offer = get_object_or_404(Offer, pk=kwargs.get("pk"))
            self.check_object_permissions(request, offer)
            serializer = OfferSerializer(offer)
            return JsonResponse(serializer.data)
        else:
            professional = get_object_or_404(User, pk=request.user.id)
            offers = professional.offer_set.all()
            serializer = OfferSerializer(offers, many=True)
            return JsonResponse(serializer.data, safe=False)
    
    def put(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        offer = get_object_or_404(Offer, pk=id)
        self.check_object_permissions(request, offer)
        serializer = OfferSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        try:
            id = kwargs.get("pk")
            offer = get_object_or_404(Offer, pk=id)
            self.check_object_permissions(request, offer)
            offer.delete()
            return Response({
                    'message': 'Offer deleted successfully.'
                }, status=status.HTTP_200_OK)
        except NotFound:
            return Response({
            'error': 'Offer not found.'
        }, status=status.HTTP_404_NOT_FOUND)



