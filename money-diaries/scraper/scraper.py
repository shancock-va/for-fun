"""
Classes related to scraping a website
"""
import os
import requests
import unicodedata

from bs4 import BeautifulSoup
import lxml
from selenium.webdriver.support.ui import WebDriverWait


from money_diaries_model import PageMetaData, OccupationData, ExpensesData, TimeEntry, Day

class PageScraper:
    """ Scrape a page """
    def __init__(self, url, selenium_driver=None, selenium_wait_until=None, content_location='./data'):
        """ Initiate the class """
        self.url = url
        self.use_selenium = None
        self.content = None
        self.soup = None
        self.html_file_location = None
        self.content_location = content_location
        self.driver = selenium_driver
        self.selenium_wait_until = selenium_wait_until

    def _get_page_contents(self):
        """ Get the page contents """
        if self.driver:
            if self.selenium_wait_until:
                self.driver.get(self.url)
                wait = WebDriverWait(self.driver, 10)
                wait.until(self.selenium_wait_until)
            else:
                self.driver.get(self.url)
            self.content = unicodedata.normalize("NFKD", str(self.driver.page_source))
        else:
            self.content = unicodedata.normalize("NFKD", requests.get(self.url).content.decode("utf-8"))
        return self.content

    def _write_contents_to_file(self):
        """ Write scraped contents to file """
        try:
            os.makedirs(self.content_location)
        except FileExistsError:
            pass
        
        self.html_file_location = "{}/{}.html".format(self.content_location, self.url.split("/")[-1])
        with open(self.html_file_location, "w") as text_file:
            text_file.write(self.content) 

    def _get_page_soup(self, parser='html.parser'):
        """ Returns beautiful soup representation of the page """
        if self.content is None:
            raise ValueError('Missing content, call _get_page_contents first')
        self.soup = BeautifulSoup(self.content, parser)
        return self.soup 

    def scrape_page(self):
        """ Scrapes page and sets content and parse it using Beautiful Soup """
        self._get_page_contents()
        self._get_page_soup()


