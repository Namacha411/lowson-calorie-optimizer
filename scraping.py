import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


def load_source_urls():
    """Load URLs from dataset/source.json"""
    with open("dataset/source.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["links"]


def scrape_lawson_page(url):
    """Scrape a single Lawson page for food items"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all product items
        products = []

        # Look for links with "detail" in href
        detail_links = soup.find_all("a", href=lambda x: x and "detail" in x)
        
        for link in detail_links:
            li_parent = link.find_parent("li")
            if not li_parent:
                continue
            
            # Extract product name from img alt text
            img = link.find("img")
            if not img:
                continue
                
            name = img.get("alt", "").strip()
            if not name:
                continue
            
            # Look for calories and price in the li text
            li_text = li_parent.get_text()
            calorie_match = re.search(r"(\d+(?:\.\d+)?)kcal", li_text)
            price_match = re.search(r"(\d+)円", li_text)
            
            if calorie_match and price_match:
                product = {
                    "name": name,
                    "calories": int(float(calorie_match.group(1))),  # Handle decimal calories
                    "price": int(price_match.group(1))
                }
                products.append(product)

        return products

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []


def scrape_all_pages():
    """Scrape all pages from source.json"""
    urls = load_source_urls()
    all_products = []

    print(f"Starting to scrape {len(urls)} pages...")

    for i, url in enumerate(urls, 1):
        print(f"Scraping page {i}/{len(urls)}: {url}")
        products = scrape_lawson_page(url)
        all_products.extend(products)

        # Add delay between requests to be respectful
        time.sleep(1)

    print(f"Found {len(all_products)} products total")
    return all_products


def save_to_csv(products, filename="lawson_food_data.csv"):
    """Save products to CSV file"""
    if not products:
        print("No products to save")
        return

    df = pd.DataFrame(products)

    # Remove duplicates based on name
    df = df.drop_duplicates(subset=["name"])

    # Sort by name
    df = df.sort_values("name")

    # Save to CSV
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Saved {len(df)} unique products to {filename}")

    # Display summary
    print("\nDataset summary:")
    print(f"Total products: {len(df)}")
    print(f"Average calories: {df['calories'].mean():.1f}")
    print(f"Average price: {df['price'].mean():.1f}円")
    print(f"Price range: {df['price'].min()}-{df['price'].max()}円")
    print(f"Calorie range: {df['calories'].min()}-{df['calories'].max()}kcal")


def main():
    print("Lawson Food Data Scraper")
    print("========================")

    try:
        # Scrape all pages
        products = scrape_all_pages()

        # Save to CSV
        save_to_csv(products)

        print("\nScraping completed successfully!")

    except Exception as e:
        print(f"Error during scraping: {e}")


if __name__ == "__main__":
    main()
