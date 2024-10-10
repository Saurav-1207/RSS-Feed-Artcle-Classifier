import feedparser
from models import NewsArticle, engine
from sqlalchemy.orm import sessionmaker
from tasks import process_article
from dateutil import parser
from datetime import datetime

feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

Session = sessionmaker(bind=engine)
session = Session()

def parse_feed(url):
    return feedparser.parse(url)

def save_article_to_db(title, content, published, source_url):
    if not session.query(NewsArticle).filter_by(title=title).first():  # Avoid duplicates
        # Validate and parse the published date
        if published == "Unknown":
            published = None  # or set to datetime.utcnow() for the current time
        else:
            try:
                published = parser.parse(published)
            except (ValueError, TypeError):
                published = None  # or set to datetime.utcnow() for the current time

        article = NewsArticle(
            title=title,
            content=content,
            publication_date=published,
            source_url=source_url
        )
        
        session.add(article)
        session.commit()
        # Send article to Celery for further processing (e.g., classification)
        process_article.delay(article.id)

# Loop through RSS feeds and store articles
for feed_url in feeds:
    feed = parse_feed(feed_url)
    for entry in feed.entries:
        title = entry.title
        content = getattr(entry, 'summary', 'No content available')
        published = getattr(entry, 'published', 'Unknown')
        link = entry.link
        save_article_to_db(title, content, published, link)
