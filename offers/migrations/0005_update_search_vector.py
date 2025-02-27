# Generated by Django 5.1.1 on 2025-02-11 14:04

from django.db import migrations, connection


def create_search_trigger(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS pg_trgm;
        """)
        cursor.execute("""
            CREATE FUNCTION update_offer_search_vector() RETURNS trigger AS $$
            BEGIN
                NEW.search_vector := 
                    setweight(to_tsvector('french', NEW.title), 'A') ||
                    setweight(to_tsvector('french', NEW.zip), 'B') ||
                    setweight(to_tsvector('french', NEW.city), 'C');
                RETURN NEW;
            END
            $$ LANGUAGE plpgsql;
        """)

        cursor.execute("""
            CREATE TRIGGER offer_search_vector_update
            BEFORE INSERT OR UPDATE ON offers_offer
            FOR EACH ROW EXECUTE FUNCTION update_offer_search_vector();
        """)

def drop_search_trigger(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("DROP TRIGGER IF EXISTS offer_search_vector_update ON offers_offer;")
        cursor.execute("DROP FUNCTION IF EXISTS update_offer_search_vector();")

class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0004_offer_offer_title_trgm'),
    ]

    operations = [
        migrations.RunPython(create_search_trigger, reverse_code=drop_search_trigger),
    ]