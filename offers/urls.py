from django.urls import path
from .views import OfferView

urlpatterns = [
    path('list/', OfferView.as_view(), name='offers'),
    path('create/', OfferView.as_view(), name='offer-create'),
    path('<int:pk>/', OfferView.as_view(), name='offer-detail'),
    path('<int:pk>/delete/', OfferView.as_view(), name='offer-delete'),
]