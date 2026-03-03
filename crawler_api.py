import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# ------------------- Database Setup -------------------
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_HOST = "localhost"
DB_NAME = "books_db"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    price = Column(String(20))
    availability = Column(String(50))
    rating = Column(String(20))
    category = Column(String(100))
    product_url = Column(String(255))

Base.metadata.create_all(engine)

# ------------------- Scraper -------------------
BASE_URL = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0"}
books = []

def get_rating(star_tag):
    classes = star_tag.get("class", [])
    for cls in classes:
        if cls != "star-rating":
            return cls
    return "Not Rated"

def scrape_page(url):
    print(f"Scraping: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text
        availability = article.find("p", class_="instock availability").text.strip()
        rating = get_rating(article.find("p", class_="star-rating"))

        breadcrumb = soup.find("ul", class_="breadcrumb")
        if breadcrumb:
            items = breadcrumb.find_all("li")
            category = items[2].text.strip() if len(items) > 2 else "Home"
        else:
            category = "Home"

        product_url = urljoin(BASE_URL, article.h3.a["href"])

        # Save to DB
        book = Book(
            title=title,
            price=price,
            availability=availability,
            rating=rating,
            category=category,
            product_url=product_url
        )
        session.add(book)
        session.commit()

    time.sleep(1)

    # Crawl next page
    next_button = soup.find("li", class_="next")
    if next_button:
        next_page = urljoin(url, next_button.a["href"])
        scrape_page(next_page)

# ------------------- FastAPI Setup -------------------
app = FastAPI(title="Books Crawler API")

@app.on_event("startup")
def startup_event():
    # Scrape books when API starts
    print("Starting scraping...")
    scrape_page(BASE_URL)
    print("Scraping finished!")

@app.get("/books")
def get_books(category: str = None):
    query = session.query(Book)
    if category:
        query = query.filter(Book.category == category)
    data = [
        {
            "title": b.title,
            "price": b.price,
            "availability": b.availability,
            "rating": b.rating,
            "category": b.category,
            "product_url": b.product_url
        }
        for b in query.all()
    ]
    return JSONResponse(content=data)