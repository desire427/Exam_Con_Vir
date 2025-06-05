# inspire_scrape/views.py
from django.shortcuts import render
from django.utils import timezone
from .models import DailyQuote, DataScienceNews
from .utils import scrape_datascience_news
from datetime import date

def home(request):
    # Try to get today's quote
    today = date.today()
    try:
        quote = DailyQuote.objects.get(date=today)
    except DailyQuote.DoesNotExist:
        quote = None
    
    # Get latest news (last 5)
    news = DataScienceNews.objects.all().order_by('-publish_date')[:5]
    
    return render(request, 'datavibes/home.html', {
        'quote': quote,
        'news': news,
    })

def daily_quote(request):
    # Try to get today's quote
    today = date.today()
    try:
        quote = DailyQuote.objects.get(date=today)
    except DailyQuote.DoesNotExist:
        quote = None
    
    return render(request, 'datavibes/daily_quote.html', {
        'quote': quote,
    })

def news_list(request):
    news = DataScienceNews.objects.all().order_by('-publish_date')
    return render(request, 'datavibes/news_list.html', {
        'news': news,
    })

def scrape_news(request):
    if request.method == 'POST':
        # Scrape news from target sites
        new_news_count = scrape_datascience_news()
        
        return render(request, 'datavibes/news_list.html', {
            'news': DataScienceNews.objects.all().order_by('-publish_date'),
            'scraped_count': new_news_count,
        })
    
    return render(request, 'datavibes/scrap_confirm.html')