# Generated by Django 5.1.1 on 2025-02-11 13:50

import django.contrib.postgres.indexes
from django.conf import settings
from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension



class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_offer_search_vector_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        TrigramExtension(),
        migrations.AddIndex(
            model_name='offer',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title'], name='offer_title_trgm', opclasses=['gin_trgm_ops']),
        ),
        
    ]
