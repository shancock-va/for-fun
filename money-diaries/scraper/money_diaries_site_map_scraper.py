"""
Classes used for scraping money diaries site map
"""
import re

from scraper import PageScraper

class MoneyDiariesSiteMapScaper(PageScraper):
    """ Scrape a Money Diaries page """
    def __init__(self, url, use_selenium=False):
        """ Initiate the class """
        self.additional_site_map_urls = []
        self.page_urls = []
        PageScraper.__init__(self, url, use_selenium)

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