import os
import sys
import unittest
from unittest import mock

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'scraper'))

from scraper import PageScraper


class PageScraperTest(unittest.TestCase):
    @mock.patch('scraper.requests')
    def test__get_page_contents_returns_content(self, mock_requests):
        mock_requests.get.return_value.content = b'page content'
        scraper = PageScraper('www.google.com')
        self.assertEqual(scraper._get_page_contents(), 'page content')

    @mock.patch('scraper.requests')
    def test__get_page_soup_returns_bs4(self, mock_requests):
        mock_requests.get.return_value.content = b'<h1>Test</h1>'
        scrape = PageScraper('www.google.com')
        scrape._get_page_contents()
        soup = scrape._get_page_soup()
        self.assertEqual(soup.get_text(), 'Test')



if __name__ == '__main__':
    unittest.main()