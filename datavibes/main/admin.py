# inspire_scrape/admin.py
from django.contrib import admin
from .models import DailyQuote, DataScienceNews

@admin.register(DailyQuote)
class DailyQuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'author', 'date', 'source')
    list_filter = ('date',)
    search_fields = ('quote', 'author')

@admin.register(DataScienceNews)
class DataScienceNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'publish_date', 'date_scraped')
    list_filter = ('source', 'publish_date')
    search_fields = ('title', 'summary')