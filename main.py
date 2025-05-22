import scrapy
from scrapy.crawler import CrawlerProcess
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    quotes = []
    authors_data = {}
    visited_authors = set()

    def parse(self, response):
        for quote in response.css("div.quote"):
            text = quote.css("span.text::text").get().strip("“”")
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            author_link = quote.css("a::attr(href)").get()

            self.quotes.append({
                "quote": text,
                "author": author,
                "tags": tags
            })

            if author_link not in self.visited_authors:
                self.visited_authors.add(author_link)
                yield response.follow(author_link, self.parse_author)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        name = response.css("h3.author-title::text").get().strip()
        born_date = response.css("span.author-born-date::text").get()
        born_location = response.css("span.author-born-location::text").get()
        description = response.css("div.author-description::text").get().strip()

        self.authors_data[name] = {
            "fullname": name,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }

    def closed(self, reason):
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=2)
        with open("authors.json", "w", encoding="utf-8") as f:
            json.dump(list(self.authors_data.values()), f, ensure_ascii=False, indent=2)
        print("✅ Файли quotes.json і authors.json створено.")


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()