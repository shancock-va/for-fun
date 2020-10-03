import os
import sys
import unittest
from unittest import mock

from scraper.money_diaries_site_map_scraper import MoneyDiariesSiteMapScaper

class MoneyDiariesSiteMapScaperTest(unittest.TestCase):
    def test__set_site_map_urls_sets_additional_site_map_urls(self):
        scrape = MoneyDiariesSiteMapScaper('local.money-diaries')
        with open('{}/tests/content/money-diaries-main-sitemap.xml'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            scrape.content = f.read()
        scrape._get_page_soup()
        scrape._set_site_map_urls()
        self.assertEqual(len(scrape.additional_site_map_urls), 4784)

    def test__set_page_urls_sets_additional_site_map_urls(self):
        scrape = MoneyDiariesSiteMapScaper('local.money-diaries')
        with open('{}/tests/content/money-diaries-day-sitemap.xml'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            scrape.content = f.read()
        scrape._get_page_soup()
        scrape._set_page_urls()
        self.assertEqual(len(scrape.page_urls), 291)

    def test_get_money_diary_page_urls_returns_money_diary_urls(self):
        scrape = MoneyDiariesSiteMapScaper('local.money-diaries')
        scrape.page_urls = [
            'https://www.refinery29.com/en-gb/money-diary-content-manager-leeds-28k',
            'https://www.refinery29.com/en-us/fashion-brand-money-funding'
            ]
        self.assertEqual(len(scrape.get_money_diary_page_urls()), 1)
        self.assertEqual(scrape.get_money_diary_page_urls(), ['https://www.refinery29.com/en-gb/money-diary-content-manager-leeds-28k'])

    def test_get_money_diary_page_urls_returns_money_diaries_urls(self):
        scrape = MoneyDiariesSiteMapScaper('local.money-diaries')
        scrape.page_urls = [
            'https://www.refinery29.com/en-gb/2020/02/9401834/money-diaries-editor-ask-me-anything',
            'https://www.refinery29.com/en-us/fashion-brand-money-funding',
            'https://www.refinery29.com/en-ca/couples-who-met-on-facebook-twitter-tiktok'
            ]
        self.assertEqual(len(scrape.get_money_diary_page_urls()), 1)
        self.assertListEqual(scrape.get_money_diary_page_urls(), ['https://www.refinery29.com/en-gb/2020/02/9401834/money-diaries-editor-ask-me-anything'])

if __name__ == '__main__':
    unittest.main()