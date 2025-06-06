from django.urls import path
from .views import HomeView, DailyQuoteView, NewsListView, ScrapeNewsView

urlpatterns = [
    path('', HomeView.get, name='home'),
    path('citation-du-jour/', DailyQuoteView.get, name='daily_quote'),
    path('actualites/', NewsListView.as_view(), name='news_list'),
    path('recuperer-actualites/', ScrapeNewsView.get, name='scrape_news'),
    path('recuperer-actualites/confirmer/', ScrapeNewsView.post, name='confirm_scrape'),
] 