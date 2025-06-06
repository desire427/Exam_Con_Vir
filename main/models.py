from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
import bleach
from bs4 import BeautifulSoup

class DailyQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now, unique=True)
    source = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=10, default='fr', choices=[('fr', 'French'), ('en', 'English')])
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Citation du jour"
        verbose_name_plural = "Citations du jour"
    
    def __str__(self):
        return f"{Truncator(self.quote).chars(50)}... - {self.author} ({self.date})"
    
    @classmethod
    def get_todays_quote(cls):
        try:
            return cls.objects.filter(language='fr').get(date=timezone.now().date())
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_random_quote(cls):
        return cls.objects.filter(language='fr').order_by('?').first()

class DataScienceNews(models.Model):
    title = models.CharField(max_length=300)
    url = models.URLField()
    source = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-publish_date', '-date_scraped']
        verbose_name = "Actualité Data Science"
        verbose_name_plural = "Actualités Data Science"
    
    def __str__(self):
        return self.title
    
    def clean_summary(self):
        """Clean HTML tags from summary"""
        if not self.summary:
            return ""
        
        # First bleach to remove unwanted tags/attributes
        cleaned = bleach.clean(self.summary, tags=[], strip=True)
        
        # Then BeautifulSoup for additional cleaning
        soup = BeautifulSoup(cleaned, "html.parser")
        return soup.get_text().strip()
    
    def save(self, *args, **kwargs):
        # Clean summary before saving
        if self.summary:
            self.summary = self.clean_summary()
        super().save(*args, **kwargs)