# Books Crawler & API

A full-stack Python project that **scrapes book data from [Books to Scrape](https://books.toscrape.com/)**, stores it in a **MariaDB database**, and exposes a **FastAPI REST API** to access the data.

This project demonstrates **web scraping, database integration, and API development** — perfect for a portfolio or showcasing full-stack Python skills.

---

## 🔹 Features

- Scrapes all books from the site (1000+ books, 50 pages)
- Collects:
  - Title
  - Price
  - Availability
  - Rating
  - Category
  - Product URL
- Saves data to **MariaDB** using SQLAlchemy ORM
- Provides a **FastAPI endpoint** `/books`:
  - Returns all books
  - Optional category filter (`/books?category=Travel`)
- Handles pagination automatically
- Includes delays to avoid overloading the website

---

## 🛠️ Tech Stack

- Python 3.x
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for scraping
- [Requests](https://pypi.org/project/requests/) for HTTP requests
- [SQLAlchemy](https://www.sqlalchemy.org/) for ORM
- MariaDB for data storage
- [FastAPI](https://fastapi.tiangolo.com/) for API
- Uvicorn as ASGI server

---

## 💾 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Oluwapelumi-AA/books-crawler.git
cd books-crawler
```

2. Create and activate a virtual environment
python -m venv venv
# Windows
.\venv\Scripts\Activate
# Mac/Linux
# source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt
4. Setup MariaDB

Create the database:

CREATE DATABASE books_db;
USE books_db;

Ensure your crawler_api.py has the correct DB credentials:

DB_USER = "root"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_NAME = "books_db"
5. Run the API (and automatically crawl the site)
uvicorn crawler_api:app --reload

The API will crawl all books on startup

Access all books: http://127.0.0.1:8000/books

Filter by category: http://127.0.0.1:8000/books?category=Travel
