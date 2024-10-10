from celery import Celery
from text_classification import classify_article
from models import sessionmaker, engine, NewsArticle

app = Celery('tasks', broker='redis://localhost:6379/0')

Session = sessionmaker(bind=engine)

@app.task
def process_article(article_id):
    session = Session()
    article = session.query(NewsArticle).get(article_id)
    if article:
        category = classify_article(article.title, article.content)  # Use title and content
        article.category = category
        session.commit()
