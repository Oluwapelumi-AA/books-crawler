import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/"
books = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_rating(star_tag):
    """Convert class to readable rating"""
    classes = star_tag.get("class", [])
    for cls in classes:
        if cls != "star-rating":
            return cls
    return "Not Rated"

def scrape_page(url):
    """Scrape a single page"""
    print(f"Scraping: {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text
        availability = article.find("p", class_="instock availability").text.strip()
        rating = get_rating(article.find("p", class_="star-rating"))

        # SAFELY get category
        breadcrumb = soup.find("ul", class_="breadcrumb")
        if breadcrumb:
            items = breadcrumb.find_all("li")
            category = items[2].text.strip() if len(items) > 2 else "Home"
        else:
            category = "Home"

        product_url = urljoin(BASE_URL, article.h3.a["href"])

        books.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating,
            "Category": category,
            "Product URL": product_url
        })

    # Delay to avoid hammering server
    time.sleep(1)

    # Crawl next page if exists
    next_button = soup.find("li", class_="next")
    if next_button:
        next_page = urljoin(url, next_button.a["href"])
        scrape_page(next_page)

def main():
    scrape_page(BASE_URL)
    df = pd.DataFrame(books)
    df.to_csv("books_data_full.csv", index=False)
    print("\n✅ Scraping complete!")
    print(f"📚 Total books scraped: {len(books)}")
    print("📁 Saved as books_data_full.csv")

if __name__ == "__main__":
    main()