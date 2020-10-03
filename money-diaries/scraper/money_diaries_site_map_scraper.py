"""
Classes used for scraping money diaries site map
"""
import re

from scraper.scraper import PageScraper

class MoneyDiariesSiteMapScaper(PageScraper):
    """ Scrape a Money Diaries page """
    def __init__(self, url, use_selenium=False):
        """ Initiate the class """
        PageScraper.__init__(self, url, use_selenium)
        self.additional_site_map_urls = []
        self.page_urls = []
        self.properties_to_not_encode = [
            'use_selenium', 'content', 'soup', 'driver', 'selenium_driver', 'selenium_wait_until',
            'properties_to_not_encode', 'page_urls', 'additional_site_map_urls', 'content_location'
        ]

    def scrape_page(self):
        """ Scrapes page and sets content and parse it using Beautiful Soup """
        self._get_page_contents()
        self._get_page_soup()
        self._set_site_map_urls()
        self._set_page_urls()

    def _get_page_soup(self, parser='xml'):
        """ Get the page soup for the site map """
        return super()._get_page_soup(parser=parser)

    def _set_site_map_urls(self):
        """ Get and set expense data of the article """
        self.additional_site_map_urls = [
            sitemap.contents[0] for sitemap_section in self.soup.find_all('sitemap')
                for sitemap in sitemap_section.find_all('loc')
        ]

    def _set_page_urls(self):
        """ Get and set expense data of the article """
        self.page_urls = [
            loc.contents[0] for url_section in self.soup.find_all('url')
                for loc in url_section.find_all('loc')
        ]

    def get_money_diary_page_urls(self):
        """ Get and set expense data of the article """
        return [url for url in self.page_urls if re.search(r'money-diar((?:y)|(?:ies))', url)]
    
    def to_json_serializable_obj(self):
        """ Creates a JSON serializable object """
        obj = PageScraper.to_json_serializable_obj(self)
        obj['money_diary_page_urls'] = self.get_money_diary_page_urls()
        return obj
