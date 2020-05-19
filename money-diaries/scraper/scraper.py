"""
Classes related to scraping a website
"""
from datetime import datetime
import re
import requests

from bs4 import BeautifulSoup
import lxml

from money_diaries_model import PageMetaData, OccupationData, ExpensesData, TimeEntry, Day


class PageScrape:
    """ Scrape a page """
    def __init__(self, url, selenium_driver=None):
        """ Initiate the class """
        self.url = url
        self.use_selenium = None
        self.content = None
        self.soup = None
        self.driver = None

    def _get_page_contents(self):
        """ Get the page contents """
        if self.driver:
            self.driver.get(self.url)
            self.content = self.driver.page_source
        else:
            self.content = requests.get(self.url).content.decode("utf-8")
        return self.content

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


class MoneyDiariesPageScrape(PageScrape):
    """ Scrape a Money Diaries page """
    def __init__(self, url, use_selenium=False):
        """ Initiate the class """
        self.page_meta_data = None
        self.occupation_data = None
        self.expense_data = None
        self.days_data = None
        PageScrape.__init__(self, url, use_selenium)

    def _set_meta_data(self):
        """ Get and set title, author, and date published for article """
        title = self.soup.find('h1').get_text()
        author = self.soup.find('span', class_='contributor').get_text()
        publish_date_str = self.soup.find('div', class_='byline modified').get_text()
        publish_date = datetime.strptime(publish_date_str.replace('.',''), '%B %d, %Y, %I:%M %p')
        self.page_meta_data = PageMetaData(title, author, publish_date)

    def _set_occupation_data(self):
        """ Get and set occupation data of the article """
        section_texts = self.soup.findAll('div', class_='section-text')
        pairs = None
        for section in section_texts:
            if section.find('strong', string='Occupation:'):
                pairs = re.findall(r'\<strong\>(.*?):\<\/strong\>\W?(.*?)(?:<|\Z)', str(section))
                break

        occupation = None
        industry = None
        location = None
        extras = []
        
        for pair in pairs:
            if pair[0] == 'Occupation':
                occupation = pair[1].strip()
            elif pair[0] == 'Industry':
                industry = pair[1].strip()
            elif pair[0] == 'Location':
                location = pair[1].strip()
            else:
                extras.append((pair[0].lower(), pair[1].strip()))

        self.occupation_data = OccupationData(occupation, industry, location, extras)

    def _set_expenses_data(self):
        """ Get and set expense data of the article """
        section_texts = self.soup.findAll('div', class_='section-text')
        pairs = None
        for section in section_texts:
            monthly_expense_label_section = section.find('strong', string='Monthly Expenses')
            if monthly_expense_label_section:
                monthly_expense_label_section.decompose()
                section_str = str(section)
                pairs = re.findall(r'\<strong\>(.*?):\s?\<\/strong\>\s?(.*?)(?:<|\Z)', section_str)
                break
        
        expenses = [(pair[0].lower(), pair[1].strip()) for pair in pairs]

        self.expense_data = ExpensesData(expenses)

    def _set_days_data(self):
        """ Get and set expense data of the article """
        days = []

        section_h3s = self.soup.select('div.section-container.section-text-container h3')
        for section in section_h3s:
            time_entries = []
            daily_total = ''
            parent = section.find_parent('div', class_='section-outer-container')
            for sibling in parent.find_next_siblings('div', class_='section-outer-container'):
                money_spent = None
                if sibling.select('.section-text-container h3'):
                    break # start a new day

                time_section = sibling.find('div', class_='section-text')
                if not time_section or len(time_section.contents) == 0:
                    continue
                money_spent_section = time_section.find('strong')

                if money_spent_section and 'Daily Total' in str(money_spent_section):
                    daily_total = re.findall(r'([\$\d\.]+)', str(money_spent_section))[0]
                    continue
                elif money_spent_section:
                    money_spent = money_spent_section.contents[0]
                    money_spent_section.decompose()

                if len(time_section.contents) == 0:
                    continue
                    
                matches = re.findall(r'([\d\:]*\s[ap]\.?m\.?)\s*—\s*(.*)', str(time_section.contents[0]))

                if len(matches) == 0:
                    continue

                time_str = matches[0][0]
                descr = matches[0][1]
                if ":" in time_str:
                    time_of_day = datetime.strptime(time_str.replace('.', ''), "%I:%M %p")
                else:
                    time_of_day = datetime.strptime(time_str.replace('.', ''), "%I %p")

                time_entries.append(TimeEntry(
                        time_of_day=time_of_day, 
                        description=descr, 
                        money_spent=money_spent
                    ))
            days.append(Day(title=str(section.contents[0]), total=daily_total, time_entries=time_entries))
        self.days_data = days
        
        return


class MoneyDiariesSiteMapScaper(PageScrape):
    """ Scrape a Money Diaries page """
    def __init__(self, url, use_selenium=False):
        """ Initiate the class """
        self.additional_site_map_urls = []
        self.page_urls = []
        PageScrape.__init__(self, url, use_selenium)

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
