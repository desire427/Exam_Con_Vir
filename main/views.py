from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.utils import timezone
from .models import DailyQuote, DataScienceNews
from .utils import scrape_datascience_news
from datetime import date
import random

class HomeView:
    @staticmethod
    def get(request):
        context = {
            'quote': DailyQuote.get_todays_quote(),
            'news': DataScienceNews.objects.all().order_by('-publish_date')[:5]
        }
        return render(request, 'datavibes/home.html', context)

class DailyQuoteView:
    @staticmethod
    def get(request):
        quote = DailyQuote.get_todays_quote()
        random_quote = None
        
        # Only show random quote if there's no quote for today
        if not quote:
            random_quote = DailyQuote.get_random_quote()
        
        return render(request, 'datavibes/daily_quote.html', {
            'quote': quote,
            'random_quote': random_quote
        })

class NewsListView(ListView):
    model = DataScienceNews
    template_name = 'datavibes/news_list.html'
    context_object_name = 'news'
    ordering = ['-publish_date']
    paginate_by = 10

class ScrapeNewsView:
    @staticmethod
    def get(request):
        return render(request, 'datavibes/scrap_confirm.html')
    
    @staticmethod
    def post(request):
        new_news_count = scrape_datascience_news()
        return redirect('news_list')