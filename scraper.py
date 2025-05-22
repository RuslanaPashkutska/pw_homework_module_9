from time import sleep

import requests
from bs4 import BeautifulSoup
import json

base_url = "http://quotes.toscrape.com"
quotes = []
authors_info = {}
visited_authors = set()

def get_page_content(url):
    response = requests.get(url)
    content = BeautifulSoup(response.content, "html.parser")
    return content

def get_author_info(author_url):
    soup = get_page_content(base_url + author_url)
    return {
        "fullname": soup.select_one(".author-title").text,
        "born_date": soup.select_one(".author-born-date").text,
        "born_location": soup.select_one(".author-born-location").text,
        "description": soup.select_one(".author-description").text,
    }


def get_quotes(content):
    for quote in content.select(".quote"):
        text = quote.select_one(".text").text.strip("“”")
        author = quote.select_one(".author").text
        tags = [tag.text for tag in quote.select(".tags .tag")]
        author_link = quote.select_one("a")["href"]

        quotes.append({
            "quote": text,
            "author": author,
            "tags": tags
        })

        if author_link not in visited_authors:
            author_data = get_author_info(author_link)
            authors_info[author_data["fullname"]] = author_data
            visited_authors.add(author_link)
            sleep(0.3)


def run_scraper():
    page_url = "/page/1/"
    while page_url:
        content = get_page_content(base_url + page_url)
        get_quotes(content)

        next_page = content.select_one(".next > a")
        page_url = next_page["href"] if next_page else None


    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(list(authors_info.values()), f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run_scraper()