# inspire_scrape/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quote/', views.daily_quote, name='daily_quote'),
    path('news/', views.news_list, name='news_list'),
    path('scrape/', views.scrape_news, name='scrape_news'),
]