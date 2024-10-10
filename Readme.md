# RSS Feed News Article Classification with Celery and NLP

This project processes RSS feed articles, stores them in a PostgreSQL database, and classifies each article into categories using Natural Language Processing (NLP). The application uses Celery for asynchronous task management and Redis as a message broker.

## Table of Contents
- Overview
- Features
- How It Works
- Technologies Used
- Setup and Installation
- Docker Setup with Redis
- Usage
- Example Output
- Contributing

---

## Overview

The RSS Feed News Article Classification project automatically reads articles from provided RSS feeds, extracts relevant information such as the title, content, and publication date, and classifies the articles into predefined categories using NLP. The extracted data is stored in a relational database (PostgreSQL) and processed asynchronously using Celery for efficient task handling.

---

## Features
- **Feed Parsing**: Automatically parse multiple RSS feeds.
- **Asynchronous Task Management**: Uses Celery to handle the article processing in the background.
- **Duplicate Detection**: Ensures that duplicate articles from the same feed are not stored in the database.
- **Text Classification**: Uses NLP (Natural Language Toolkit or spaCy) to classify each article.
- **Database Storage**: Stores article metadata and classification in a PostgreSQL database.
- **Logging**: Extensive logging for event tracking and error handling.

---

## How It Works
1. **RSS Feed Parsing**:
   - The application parses RSS feeds using `Feedparser` and extracts titles, content, publication dates, and source URLs.
   - Before storing in the database, the system checks for duplicate articles based on titles.

2. **Celery Task Queue**:
   - New articles are sent to a Celery task queue for asynchronous processing.
   - Redis is used as the message broker to manage task distribution.
   - Articles are classified using an NLP model and stored back in the database with their assigned categories.

3. **Text Classification**:
   - Uses either `NLTK` or `spaCy` to classify articles into predefined categories based on their content.

4. **Database Management**:
   - The system uses SQLAlchemy to interact with a PostgreSQL database. Articles are stored with their titles, content, publication date, source URL, and classification.

---

## Technologies Used
- **Programming Languages**: Python
- **Libraries**:
  - `Feedparser`: For parsing RSS feeds.
  - `SQLAlchemy`: For interacting with PostgreSQL.
  - `Celery`: For asynchronous task management.
  - `NLTK` or `spaCy`: For natural language processing and article classification.
- **Database**: PostgreSQL
- **Message Broker**: Redis (used with Celery)
- **Logging**: Standard Python logging for tracking errors and events.
- **Web Interface**: Streamlit (for visualizing the articles and their classifications)

---

## Setup and Installation

### 1. Prerequisites
- Python 3.7 or newer
- PostgreSQL
- Redis (for task queue)
- Docker (for containerized Redis setup)

### 2. Clone the Repository
```bash
git clone https://github.com/Saurav-1207/RSS-Feed-Article-Classification.git
cd RSS-Feed-Article-Classification
