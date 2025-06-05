import feedparser
from dateutil import parser
from datetime import datetime
import logging
from django.utils import timezone
from .models import DataScienceNews

# Set up logging
logger = logging.getLogger(__name__)

def scrape_datascience_news():
    """
    Scrape data science news from RSS feeds
    Returns count of new news items added
    """
    new_count = 0
    
    # List of RSS feeds to scrape
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
        },
        {
            'url': 'https://www.reddit.com/r/datascience/.rss',
            'source': 'Reddit Data Science'
        }
    ]

    for feed_info in rss_feeds:
        try:
            logger.info(f"Scraping RSS feed: {feed_info['source']}")
            
            # Parse the RSS feed with a timeout
            feed = feedparser.parse(feed_info['url'])
            
            if feed.bozo:  # Check for feed parsing errors
                logger.warning(f"Feed parsing error for {feed_info['source']}: {feed.bozo_exception}")
                continue
                
            for entry in feed.entries[:5]:  # Only take the latest 5 entries
                try:
                    # Skip if we already have this URL
                    if DataScienceNews.objects.filter(url=entry.link).exists():
                        continue
                        
                    # Prepare the data
                    news_data = {
                        'title': entry.get('title', 'No title available')[:300],  # Truncate to fit model
                        'url': entry.link,
                        'source': feed_info['source'],
                        'summary': entry.get('description', '')[:1000],  # Truncate summary if needed
                        'publish_date': None
                    }
                    
                    # Parse publish date if available
                    if hasattr(entry, 'published'):
                        try:
                            news_data['publish_date'] = parser.parse(entry.published).date()
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Couldn't parse date for {entry.link}: {e}")
                            news_data['publish_date'] = timezone.now().date()
                    
                    # Create the news item
                    DataScienceNews.objects.create(**news_data)
                    new_count += 1
                    logger.debug(f"Added new article: {news_data['title']}")
                    
                except Exception as entry_error:
                    logger.error(f"Error processing entry from {feed_info['source']}: {entry_error}", exc_info=True)
                    continue
                    
        except Exception as feed_error:
            logger.error(f"Error scraping {feed_info['source']} RSS feed: {feed_error}", exc_info=True)
            continue
            
    logger.info(f"Scraping complete. Added {new_count} new articles.")
    return new_count