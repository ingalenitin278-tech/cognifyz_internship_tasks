"""Task 6: Interactive web scraper (requests + BeautifulSoup).

Practice sites built for scraping: books.toscrape.com and quotes.toscrape.com.
Install first:  pip install requests beautifulsoup4
"""
import csv

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit("Missing libraries. Run: pip install requests beautifulsoup4")

HEADERS = {"User-Agent": "Mozilla/5.0 (Cognifyz internship learning project)"}
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.MissingSchema:
        print("Invalid URL. Include http:// or https://")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError:
        print("Could not connect. Check your internet connection or the URL.")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return None


def scrape_books(page):
    soup = fetch(f"https://books.toscrape.com/catalogue/page-{page}.html")
    if not soup:
        return []
    books = []
    for item in soup.select("article.product_pod"):
        books.append({
            "Title": item.h3.a["title"],
            "Price": item.select_one(".price_color").get_text(strip=True),
            "Rating": RATINGS.get(item.select_one("p.star-rating")["class"][1], 0),
            "Stock": item.select_one(".availability").get_text(strip=True),
        })
    return books


def scrape_quotes(page):
    soup = fetch(f"https://quotes.toscrape.com/page/{page}/")
    if not soup:
        return []
    quotes = []
    for q in soup.select("div.quote"):
        quotes.append({
            "Quote": q.select_one("span.text").get_text(strip=True),
            "Author": q.select_one("small.author").get_text(strip=True),
            "Tags": ", ".join(t.get_text() for t in q.select("a.tag")),
        })
    return quotes


def scrape_any(url):
    soup = fetch(url)
    if not soup:
        return []
    rows = [{"Type": "Title", "Text": soup.title.get_text(strip=True) if soup.title else "(none)", "Link": url}]
    for h in soup.find_all(["h1", "h2", "h3"], limit=15):
        text = h.get_text(strip=True)
        if text:
            rows.append({"Type": h.name.upper(), "Text": text[:60], "Link": ""})
    for a in soup.find_all("a", href=True, limit=10):
        rows.append({"Type": "Link", "Text": a.get_text(strip=True)[:60] or "(no text)", "Link": a["href"][:60]})
    return rows


def show_table(rows, limit=None):
    if not rows:
        print("No data found.")
        return
    rows = rows[:limit] if limit else rows
    cols = list(rows[0].keys())
    widths = {c: min(60, max(len(c), *(len(str(r[c])) for r in rows))) for c in cols}
    print("\n" + " | ".join(c.ljust(widths[c]) for c in cols))
    print("-+-".join("-" * widths[c] for c in cols))
    for r in rows:
        print(" | ".join(str(r[c])[:widths[c]].ljust(widths[c]) for c in cols))
    print(f"\n{len(rows)} row(s) shown.")


def save_csv(rows, name):
    try:
        with open(name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved to {name}")
    except OSError as e:
        print(f"Could not save file: {e}")


def ask_page():
    text = input("Page number (default 1): ").strip()
    return int(text) if text.isdigit() and int(text) > 0 else 1


def main():
    while True:
        print("\n=== INTERACTIVE WEB SCRAPER ===")
        print("1. Books (books.toscrape.com)\n2. Quotes (quotes.toscrape.com)\n3. Any website URL\n4. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            rows = scrape_books(ask_page())
            filename = "books.csv"
        elif choice == "2":
            rows = scrape_quotes(ask_page())
            filename = "quotes.csv"
        elif choice == "3":
            rows = scrape_any(input("Enter URL: ").strip())
            filename = "page_data.csv"
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
            continue
        show_table(rows)
        if rows and input("Save to CSV? (y/n): ").strip().lower() == "y":
            save_csv(rows, filename)


if __name__ == "__main__":
    main()
