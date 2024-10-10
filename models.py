from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = 'news_articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)  # Unique title to avoid duplicates
    content = Column(Text)
    publication_date = Column(DateTime, default=datetime.utcnow)
    source_url = Column(String)
    category = Column(String)

# Initialize the PostgreSQL connection
engine = create_engine('postgresql://postgres:admin@localhost:3030/newsdb')
Base.metadata.create_all(engine)  # Creates the table
