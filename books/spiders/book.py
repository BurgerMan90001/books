from collections.abc import Iterable
from typing import Any
import scrapy

from books.items import BooksItem

# Run spider command: scrapy crawl book
class BookSpider(scrapy.Spider):
    """_summary_

    Args:
        scrapy (_type_): _description_

    Yields:
        _type_: _description_
    """
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    # "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.log_error,
            )

    def parse(self, response):
        """
        @url https://books.toscrape.com
        @returns items 20 20
        @returns request 1 50
        @scrapes url title price
        """
        for book in response.css("article.product_pod"):
            item = BooksItem()

            item["url"] = book.css("h3 > a::attr(href)").get()
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()

            yield item

        next_page = response.css("li.next > a::attr(href)").get()

        # if there is a next page
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Navigating to next page with URL {next_page_url}.")
            yield scrapy.Request(
                url=next_page_url, 
                callback=self.parse,
                errback=self.log_error,
            )

    def log_error(self, error_message):
        self.logger.error(repr(error_message))
