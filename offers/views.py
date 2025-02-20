import json            

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .serializers import OfferSerializer, ContractTypeSerializer, OfferActionSerializer
from .models import Offer, ContractType
from config.permissions import IsOwner, IsProfessional


class OfferView(APIView):
    def get_permissions(self):
        """
        Determine the permissions required for the request method.

        Returns different permission classes based on the HTTP method:
        - POST: Requires the user to be authenticated.
        - PUT, DELETE: Requires the user to be authenticated and the owner of the offer.
        - GET: Allows any user to view offers.

        Returns:
            list: A list of permission instances.
        """
        if self.request.method == "POST":
            return [IsAuthenticated(), IsProfessional()]  # Only authenticated users can create offers
        elif self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated(), IsOwner()]  # Only the owner can modify or delete
        elif self.request.method == "GET":
            return [AllowAny()]  # Everyone can see offers (authenticated users see only their own)
        return super().get_permissions()
     
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a new offer.

        Validates the request data using OfferActionSerializer. If valid,
        saves the new offer and returns a success message with HTTP 201 status.
        If invalid, returns the serializer errors with HTTP 400 status.
        """
        serializer = OfferActionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'offer created successfully.'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve offers.

        If a primary key ('pk') is provided in the URL, retrieve and return
        the specific offer after checking permissions. Otherwise, search for
        offers based on query parameters such as title, zip code, city, and
        contract IDs. If no search parameters are provided and the user is
        authenticated, return all offers associated with the user.

        Paginate the results to limit the number of offers per page and
        serialize the paginated offers for the response.

        Returns:
            JsonResponse: Serialized offer data or paginated offers with
            total pages information.
        """
        if "pk" in kwargs:
            offer = get_object_or_404(Offer, pk=kwargs.get("pk"))
            self.check_object_permissions(request, offer)
            serializer = OfferSerializer(offer)
            return JsonResponse(serializer.data)

        title = request.GET.get("title" ,"")
        zip_code = request.GET.get("zip", "")
        city = request.GET.get("city", "")
        contract_ids = request.GET.getlist('contract')
        page_number = request.GET.get('page')
        if title or zip_code or city or contract_ids:
            offers = Offer.search_offers(
                title, 
                zip_code, 
                city, 
                contract_ids
            )
        else:
            if request.user.is_authenticated:
                
                professional = get_object_or_404(User, pk=request.user.id)
                offers = professional.offer_set.all()
        # Pagination: Limit the number of results per page
        paginator = Paginator(offers, 10)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Serialize the paginated offers
        serializer = OfferSerializer(page_obj, many=True)

        response_data = {
            'offers': serializer.data,
            'total_pages': paginator.num_pages,
        }
        # Create response object
        return JsonResponse(response_data, safe=False)
    
    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to update an existing offer.

        Retrieves the offer by primary key ('pk') from the URL, checks
        permissions, and partially updates the offer with the provided data
        using OfferActionSerializer. If the data is valid, saves the changes
        and returns the updated offer data. If invalid, returns the serializer
        errors with HTTP 400 status.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            JsonResponse: The updated offer data or validation errors.
        """
        id = kwargs.get("pk")
        offer = get_object_or_404(Offer, pk=id)
        self.check_object_permissions(request, offer)
        serializer = OfferActionSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE requests to remove an existing offer.

        Retrieves the offer by primary key ('pk') from the URL, checks
        permissions, and deletes the offer if found. Returns a success
        message with HTTP 200 status if the offer is deleted successfully.
        If the offer is not found, returns an error message with HTTP 404 status.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
           

        Returns:
            Response: Success message or error message with appropriate HTTP status.
        """

        id = kwargs.get("pk")
        offer = get_object_or_404(Offer, pk=id)
        self.check_object_permissions(request, offer)
        offer.delete()
        return Response({
                'message': 'Offer deleted successfully.'
            }, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def get_all_contract_type(request):
    """
    Retrieve all contract types.

    This view handles GET requests to retrieve all contract types from the database.
    It serializes the data using the ContractTypeSerializer and returns it in the response.

    Args:
        request (HttpRequest): The request object.

    Returns:
        Response: A Response object containing serialized contract type data.
    """
    contract_types = ContractType.objects.all()
    serializer = ContractTypeSerializer(contract_types, many=True)
    return Response(serializer.data)
