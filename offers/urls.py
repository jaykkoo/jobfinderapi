from django.urls import path
from .views import OfferView, get_all_contract_type

urlpatterns = [
    path('create/', OfferView.as_view(), name='offer-create'),
    path('<int:pk>/', OfferView.as_view(), name='offer-detail'),
    path('<int:pk>/', OfferView.as_view(), name='offer-update'),
    path('', OfferView.as_view(), name='offer-list'),
    path('<int:pk>/delete/', OfferView.as_view(), name='offer-delete'),
    path('get-all-contract-type/', get_all_contract_type, name='get-all-contract-type'),
]