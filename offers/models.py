
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVectorField
)
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q, Value, FloatField
from django.db.models.functions import Coalesce

class ContractType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Offer(models.Model):
    title = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    salary = models.IntegerField()
    contract = models.ManyToManyField(ContractType)
    professional = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
            GinIndex(
                name="offer_title_trgm", 
                opclasses=["gin_trgm_ops"], 
                fields=["title"]
            ),
        ]

    @classmethod
    def search_offers(cls, title, zip_code, city_str, contract_ids=[]):
        search_query = None
        if title:
            search_query = SearchQuery(title)
        if zip_code:
            search_query = (
                search_query & SearchQuery(zip_code) 
                if search_query else SearchQuery(zip_code)
            )
        if city_str:
            search_query = (
                search_query & SearchQuery(city_str) 
                if search_query else SearchQuery(city_str)
            )

        only_contract_ids = not title and not zip_code and not city_str
    
        # Perform Full-Text Search (FTS) if a query exists
        if search_query:
            fts_offers = (
                Offer.objects
                .annotate(
                    rank=SearchRank('search_vector', search_query)
                )
                .filter(search_vector=search_query)
            )
        else:
            fts_offers = Offer.objects.none()
        # Perform Trigram Search only if `title` is provided
        if title:
            trigram_offers = (
                Offer.objects
                .annotate(similarity=TrigramSimilarity('title', title))
                .filter(similarity__gt=0.3)  # Increase threshold for better accuracy
            )
            if zip_code and trigram_offers.exists() and city_str:
                trigram_offers = trigram_offers.filter(
                    zip=zip_code,
                    city=city_str
                )
        else:
            trigram_offers = Offer.objects.none()


        # Combine both querysets using Q objects
        combined_offers = (
            Offer.objects
            .filter(
                Q(id__in=fts_offers.values('id')) |
                Q(id__in=trigram_offers.values('id'))
            )
            .annotate(
                # Explicitly set output_field for rank and similarity
                rank=Coalesce(
                    SearchRank(
                        'search_vector', search_query), 
                        Value(0.0), output_field=FloatField()) 
                        if search_query else Value(0.0, 
                        output_field=FloatField()
                    ),
                similarity=Coalesce(
                    TrigramSimilarity('title', title), 
                    Value(0.0), output_field=FloatField()) 
                    if title else Value(0.0, 
                    output_field=FloatField()
                )
            )
            .order_by('-rank', '-similarity')
            .distinct()
        )

        # Filter by contract IDs if provided
        if contract_ids and combined_offers.exists():
            combined_offers = combined_offers.filter(
                contract__id__in=contract_ids
            ).distinct()
        elif contract_ids and only_contract_ids:
            combined_offers = cls.objects.filter(
                contract__id__in=contract_ids
            ).distinct()
        return combined_offers
    