
import unittest
import requests

from books.spiders.book import BookSpider
from scrapy.http import HtmlResponse, Request
from books.items import BooksItem

class BookSpiderTest(unittest.TestCase):
    """ Uses unittest to test the book spider
    """
    def setUp(self):
        self.spider = BookSpider()
        # Request html of sequential art page
        request = requests.get("https://books.toscrape.com")
        request.encoding = request.apparent_encoding
        
        self.example_html = request.text
        self.response = HtmlResponse(
            url = "https://books.toscrape.com",
            body = self.example_html,
            encoding="utf-8",
        )
    
    def test_parse_scrapes_all_items(self):
        """ Test if spider scrapes all books and pagination links 
        """
        book_items = []
        pagination_requests = []
        
        results = list(self.spider.parse(self.response))
        
        for item in results:
            if isinstance(item, BooksItem):
                book_items.append(item)
            elif isinstance(item, Request):
                pagination_requests.append(item)
        
        self.assertEqual(len(book_items), 20)
        self.assertEqual(len(pagination_requests), 1)
        
    def test_parse_scrapes_correct_book_info(self):
        """ Test for correct book information
        """
        results = self.spider.parse(self.response)
        
        book_1 = next(results)
        self.assertIsInstance(book_1, BooksItem)
        self.assertEqual(
            book_1["url"], 
            "catalogue/a-light-in-the-attic_1000/index.html"
            )
        self.assertEqual(book_1["title"], "A Light in the Attic")
        
        self.assertEqual(book_1["price"], "£51.77")
    
    def test_parse_creates_pagination_request(self):
        """ Test for correct pagination request creation
        """
        results = list(self.spider.parse(self.response))
        
        next_page_request = results[-1]
        self.assertIsInstance(next_page_request, Request)
        self.assertEqual(
            next_page_request.url,"https://books.toscrape.com/catalogue/page-2.html"
        )
        

if __name__ == "__main__":
    unittest.main()