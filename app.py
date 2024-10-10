import streamlit as st
import feedparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import NewsArticle, Base
from tasks import process_article
from text_classification import classify_article
from datetime import datetime
from dateutil import parser
import pandas as pd
import time
from io import BytesIO
import logging
import matplotlib.pyplot as plt

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

# Initialize the database connection
try:
    engine = create_engine('postgresql://postgres:admin@localhost:3030/newsdb')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    logging.info("Database connected successfully.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
    st.error("Database connection failed. Please check the connection details and try again.")

# Streamlit App
st.title("RSS Feed Article Classifier")

# Input fields for RSS feed URLs
st.write("Enter RSS feed URLs (one per line):")
rss_feed_urls = st.text_area("RSS Feed URLs", height=150)

def fetch_and_classify_articles(feed_url):
    """Fetch and classify articles from an RSS feed."""
    try:
        logging.info(f"Fetching feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        if feed.bozo:
            raise Exception("Feed parsing failed")

        articles = []
        for entry in feed.entries:
            title = entry.title
            content = getattr(entry, 'summary', 'No content available')
            published = getattr(entry, 'published', 'Unknown')
            link = entry.link

            # Check if article already exists
            if not session.query(NewsArticle).filter_by(title=title).first():
                # Parse publication date
                if published == "Unknown":
                    published = None
                else:
                    try:
                        published = parser.parse(published)
                    except (ValueError, TypeError):
                        published = None

                # Create a new NewsArticle object
                article = NewsArticle(
                    title=title,
                    content=content,
                    publication_date=published,
                    source_url=link
                )

                # Add to database
                session.add(article)
                session.commit()

                # Classify the article
                category = classify_article(title, content)
                article.category = category
                session.commit()

                # Append to list
                articles.append({
                    'Title': title,
                    'Content': content,
                    'Publication Date': published,
                    'Source URL': link,
                    'Category': category
                })

        logging.info(f"Successfully processed {len(articles)} articles from {feed_url}")
        return articles

    except Exception as e:
        logging.error(f"Error fetching or processing articles from {feed_url}: {e}")
        st.warning(f"Error processing feed: {feed_url}. Please check the feed URL.")
        return []

if st.button('Fetch and Classify Articles'):
    if rss_feed_urls.strip():
        feeds = rss_feed_urls.splitlines()

        all_articles = []
        num_feeds = len(feeds)
        processed_feeds = 0

        with st.spinner("Processing RSS feeds..."):
            for feed_url in feeds:
                articles = fetch_and_classify_articles(feed_url)
                all_articles.extend(articles)
                processed_feeds += 1
                st.info(f"Processed {processed_feeds} of {num_feeds} feed(s): {feed_url}")

        # Convert articles to a DataFrame and display in Streamlit
        if all_articles:
            df = pd.DataFrame(all_articles)
            st.write("### Classified Articles:")
            st.dataframe(df)

            # Displaying pie chart after classification
            if not df.empty:
                # Count the number of articles per category
                category_counts = df['Category'].value_counts()

                st.write("### Articles Distribution by Category (Pie Chart):")

                # Plot pie chart using matplotlib
                fig, ax = plt.subplots()
                ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                # Display pie chart in Streamlit
                st.pyplot(fig)

            # Button to download the DataFrame as CSV
            csv = df.to_csv(index=False)
            b = BytesIO()
            b.write(csv.encode())
            b.seek(0)

            st.download_button(
                label="Download data as CSV",
                data=b,
                file_name='classified_articles.csv',
                mime='text/csv'
            )
        else:
            st.info("No articles found or classified.")
    else:
        st.error("Please provide at least one RSS feed URL.")
