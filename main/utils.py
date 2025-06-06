import feedparser
from dateutil import parser
import logging
from django.utils import timezone
from bs4 import BeautifulSoup
import bleach
from .models import DataScienceNews

logger = logging.getLogger(__name__)

def clean_html_content(text, max_length=1000):
    """Clean HTML content and return plain text"""
    if not text:
        return ""
    
    # First remove unwanted HTML tags and attributes
    cleaned = bleach.clean(text, tags=[], strip=True)
    
    # Then use BeautifulSoup for additional cleaning
    soup = BeautifulSoup(cleaned, "html.parser")
    text = soup.get_text().strip()
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text[:max_length]

def scrape_datascience_news():
    """Scrape data science news from RSS feeds with improved HTML cleaning"""
    new_count = 0
    rss_feeds = [
        {
            'url': 'https://towardsdatascience.com/feed',
            'source': 'Towards Data Science'
        },
        {
            'url': 'https://www.kdnuggets.com/feed',
            'source': 'KDnuggets'
        },
        {
            'url': 'https://feeds.feedburner.com/DataScienceCentral',
            'source': 'Data Science Central'
        }
    ]

    for feed_info in rss_feeds:
        try:
            logger.info(f"Scraping RSS feed: {feed_info['source']}")
            feed = feedparser.parse(feed_info['url'])
            
            if feed.bozo:
                logger.warning(f"Feed parsing error for {feed_info['source']}: {feed.bozo_exception}")
                continue
                
            for entry in feed.entries[:5]:
                try:
                    if DataScienceNews.objects.filter(url=entry.link).exists():
                        continue
                        
                    # Clean the title and summary
                    title = clean_html_content(entry.get('title', 'No title available'))[:300]
                    summary = clean_html_content(entry.get('description', ''))
                    
                    # Parse publish date
                    publish_date = None
                    if hasattr(entry, 'published'):
                        try:
                            publish_date = parser.parse(entry.published).date()
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Couldn't parse date for {entry.link}: {e}")
                            publish_date = timezone.now().date()
                    
                    DataScienceNews.objects.create(
                        title=title,
                        url=entry.link,
                        source=feed_info['source'],
                        summary=summary,
                        publish_date=publish_date
                    )
                    new_count += 1
                    
                except Exception as entry_error:
                    logger.error(f"Error processing entry: {entry_error}", exc_info=True)
                    continue
                    
        except Exception as feed_error:
            logger.error(f"Error scraping feed: {feed_error}", exc_info=True)
            continue
            
    logger.info(f"Added {new_count} new articles")
    return new_count