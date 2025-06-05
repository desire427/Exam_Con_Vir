# inspire_scrape/models.py
from django.db import models
from django.utils import timezone

class DailyQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now, unique=True)
    source = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.quote[:50]}... - {self.author} ({self.date})"

class DataScienceNews(models.Model):
    title = models.CharField(max_length=300)
    url = models.URLField()
    source = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-publish_date', '-date_scraped']
        verbose_name_plural = "Data Science News"
    
    def __str__(self):
        return self.title