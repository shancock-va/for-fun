"""
Classes related to scraping a website
"""
from datetime import datetime
import json
import os
import requests
import unicodedata

from bs4 import BeautifulSoup
import lxml
from selenium.webdriver.support.ui import WebDriverWait


from scraper.money_diaries_model import PageMetaData, OccupationData, ExpensesData, TimeEntry, Day

class PageScraper:
    """ Scrape a page """
    def __init__(self, url, selenium_driver=None, selenium_wait_until=None, content_location='./data'):
        """ Initiate the class """
        self.url = url
        self.use_selenium = None
        self.content = None
        self.soup = None
        self.html_file_location = None
        self.error = None
        self.content_location = content_location
        self.driver = selenium_driver
        self.selenium_wait_until = selenium_wait_until
        self.properties_to_not_encode = []

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
        
        extension = 'txt'
        if type(self).__name__ == 'MoneyDiariesPageScraper':
            extension = 'html'
        elif type(self).__name__ == '':
            extension = 'xml'

        self.html_file_location = "{}/{}.{}".format(
            self.content_location, self.url.split("/")[-1], extension)
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

    def to_json_serializable_obj(self):
        """ Creates a JSON serializable object """
        def serialize(o):
            if isinstance(o, dict):
                return {'key': serialize(value) for key, value in o.items()} 
            elif isinstance(o, list):
                return [serialize(value) for value in o]
            elif isinstance(o, datetime):
                return o.strftime("%Y-%m-%d %H:%M:%S")
            elif o is None:
                return None
            elif isinstance(o, (str, int, float, complex)):
                return o
            else:
                try:
                    o_dict = o.__dict__
                except:
                    return o
                else:
                    return {
                        key: serialize(value) for key, value in o_dict.items() 
                            if key not in self.properties_to_not_encode
                    }

        return {
            key: serialize(val) for key, val in vars(self).items()
                if key not in self.properties_to_not_encode
        }

