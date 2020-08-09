"""
Classes for scraping money diaries
"""

from datetime import datetime
import json
import re

from bs4 import BeautifulSoup

from scraper import PageScraper
from money_diaries_model import PageMetaData, OccupationData, ExpensesData, TimeEntry, Day


class MoneyDiariesPageScraper(PageScraper):
    """ Scrape a Money Diaries page """
    def __init__(self, url, selenium_driver=None, selenium_wait_until=None):
        """ Initiate the class """
        self.page_meta_data = None
        self.occupation_data = None
        self.expense_data = None
        self.days_data = None
        PageScraper.__init__(self, url, selenium_driver)

    def scrape_page(self):
        """ Scrapes page and sets content and parse it using Beautiful Soup """
        self._get_page_contents()
        self._get_page_soup()
        self._set_meta_data()
        self._set_occupation_data()
        self._set_expenses_data()
        self._set_days_data()

    def _set_meta_data(self):
        """ Get and set title, author, and date published for article """
        title = self.soup.find('h1').get_text()
        author = self.soup.find('span', class_='contributor').get_text()

        self.page_meta_data = PageMetaData(title, author, self._get_modified_date())

    
    def _get_modified_date(self):
        """ get modified date """
        elements = self._get_react_data_groups()

        for el in elements:
            if 'datePublished' in el:
                return datetime.strptime(el['datePublished'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        publish_date_container = self.soup.select('div.byline.modified a')
        publish_date_str = publish_date_container[0].get_text()
        try:
            publish_date = datetime.strptime(publish_date_str.replace('.',''), '%B %d, %Y, %I:%M %p')
        except ValueError:
            publish_date = datetime.strptime(publish_date_str.replace('.',''), '%d %B %Y, %H:%M')
        
        return publish_date

    def _set_occupation_data(self):
        """ Get and set occupation data of the article """
        section_texts = self.soup.findAll('div', class_='section-text')
        pairs = []
        for section in section_texts:
            if section.find('strong', string=re.compile(r'Occupation:\s')) or section.find('strong', string=re.compile(r'(Industry)|(Occuptation):\s')):
                pairs = re.findall(r'\<strong\>(.*?):?\s?\<\/strong\>:?\s?([$€£\d\-]{1,}(?:[\,\.]?\d+)*)?[\.\s]*(.*?)(?:<|\Z)', str(section))
                break

        occupation = None
        industry = None
        location = None
        extras = []

        for pair in pairs:
            if 'monthly expenses' in pair[0].lower() or 'costs' in pair[0].lower():
                break
            elif pair[0] == 'Occupation':
                occupation = pair[2].strip()
            elif pair[0] == 'Industry':
                industry = pair[2].strip()
            elif pair[0] == 'Location':
                location = pair[2].strip()
            else:
                label, value, descr = (None if item == '' or item is None else item.strip() for item in pair)
                extras.append((label.lower(), value, descr))

        self.occupation_data = OccupationData(occupation, industry, location, extras)

    def _set_expenses_data(self):
        """ Get and set expense data of the article """
        section_texts = self.soup.findAll('div', class_='section-text')
        pairs = []
        for section in section_texts:
            monthly_expense_label_section = section.find('strong', string=re.compile(r'(Monthly Expenses\s?)|(\w*\scosts)'))
            if monthly_expense_label_section:
                siblings = monthly_expense_label_section.find_next_siblings()
                is_costs = len(re.findall(r'(\w*\scosts)', monthly_expense_label_section.text)) > 0
                if is_costs:
                    section_str = str(monthly_expense_label_section.parent)
                elif siblings and monthly_expense_label_section.previousSibling is None:
                    monthly_expense_label_section.decompose()
                    section_str = str(section)
                else:
                    parent = monthly_expense_label_section.find_parent('div', class_='section-outer-container')
                    if parent.find('strong', string='Industry:'):
                        # Expenses and Occupation data are not well separated
                        contents = parent.findChildren('div', class_='section-text')[0].contents
                        section_str = re.findall(r'\<strong\>Monthly Expenses\<\/strong\>(.*)', ''.join(map(str, contents)))[0]
                    else:
                        sibling = parent.find_next_siblings('div', class_='section-outer-container')
                        content = sibling[0].findChildren('div', class_='section-text')
                        section_str = str(content[0])

                pairs = re.findall(r'\<strong\>(.*?):?\s?\<\/strong\>:?\s?~?([$€£\d\-]{1,}(?:[\,\.]?\d+)*)?[\.\s]*(.*?)(?:<|\Z)', section_str)
                break
        
        expenses = []
        for pair in pairs:
            label, value, descr = (None if item == '' or item is None else item.strip() for item in pair)
            expenses.append((label.lower(), value, descr))
        
        self.expense_data = ExpensesData(expenses)

    def _set_days_data(self):
        """ Get and set expense data of the article """
        # after-section-content contains ads
        soup = self._remove_content_from_soup(self.soup, 'div.after-section-content')

        day_sections = soup.select('div.section-container.section-text-container h3')
        if day_sections:
            self.days_data = self._get_days_when_days_are_headers(day_sections)
        else:
            # Get days when day is just <strong></strong>
            react_elements = self._get_react_data_groups()
            day_sections = []
            for days_content in react_elements:
                if 'description' in days_content and days_content['description'].startswith("<strong>Day"):
                    day_sections.append(days_content['description'])
            self.days_data = self._get_days_when_days_are_strongs(day_sections)

        return

    def _remove_content_from_soup(self, soup, css_selector):
        """ Removes some elements from soup """
        for element in self.soup.select(css_selector):
            element.decompose()
        return soup

    def _get_react_data_groups(self):
        """ Gets react data from script tags returns an array of dicts """
        return [json.loads(element.contents[0]) for element in self.soup.select('script[data-react-helmet="true"]')]

    def _get_days_when_days_are_strongs(self, day_sections):
        """ Get days data when we have days as strong elements """
        days = []
        for section in day_sections:
            time_entries = []
            strong_matches = re.findall(r'<strong>(.*?)<\/strong>', str(section))

            matches = re.findall(r'<br>([\d\.\:]{1,5}[ap]m):\s?(.*?)([$€£\d\-]{1,}[\,\.]?\d+)?\s?<br>', str(section))

            for match in matches:
                time_str = match[0]
                descr = match[1] if match[1] else None
                money_spent = match[2] if match[2] else None
                if "." in time_str:
                    time_of_day = datetime.strptime(time_str, "%I.%M%p")
                else:
                    time_of_day = datetime.strptime(time_str, "%I%p")

                time_entries.append(TimeEntry(
                        time_of_day=time_of_day, 
                        description=descr.strip() if descr else None, 
                        money_spent=money_spent.strip() if money_spent else None
                    ))
            
            days.append(
                Day(
                    title=strong_matches[0].strip() if len(strong_matches) > 1 else None,
                    total=strong_matches[-1].replace('Total: ', '').strip() if len(strong_matches) > 1 else None,
                    time_entries=time_entries
                )
            )
        return days
           

    def _get_days_when_days_are_headers(self, day_sections):
        """ Get days data when we have days as h3s """
        days = []
        for section in day_sections:
            time_entries = []
            daily_total = ''
            parent = section.find_parent('div', class_='section-outer-container')
            for sibling in parent.find_next_siblings('div', class_='section-outer-container'):
                if sibling.select('.section-text-container h3'):
                    break # start a new day

                time_section = sibling.find('div', class_='section-text')
                if not time_section:
                    continue

                daily_total_section = time_section.find('strong', string=re.compile(r'Daily Total.*'))
                if daily_total_section:
                    daily_total = re.findall(r'([$€£\d\-]{1,}[\,\.]?\d+)', str(daily_total_section))[0]

                # Section, not always a single time entry at this point
                time_sections_found = re.split(r'([\d\:\.]+\s(?:[ap]\.?m\.?)?)\s*—\s*', time_section.decode_contents())
                if len(time_sections_found) < 3:
                    continue

                time_section_iterator = iter(time_sections_found[1:])

                prev_am_pm = 'am'
                for time_section in time_section_iterator:
                    time_entry, prev_am_pm = self._create_time_entry(time_section, next(time_section_iterator), prev_am_pm)
                    if time_entry:
                        time_entries.append(time_entry)

            days.append(Day(title=str(section.contents[0]), total=daily_total, time_entries=time_entries))
        return days

    def _create_time_entry(self, time_raw_str: str, body_str: str, default_am_pm: str):
        """ Create a time entry based on some text """
        money_spent = None
        if not time_raw_str or not body_str:
            return None

        body = BeautifulSoup(body_str, 'html.parser')
        money_spent_section = body.find('strong')

        if money_spent_section:
            money_spent = money_spent_section.contents[0]
            money_spent_section.decompose()

        time_raw_str = time_raw_str.replace('.', '')
        default_am_pm = 'am' if not default_am_pm else default_am_pm

        if not time_raw_str.endswith('m'):
            time_raw_str += f" {default_am_pm}"
        else:
            default_am_pm = time_raw_str[-2:]

        if ":" in time_raw_str:
            time_of_day = datetime.strptime(time_raw_str, "%I:%M %p")
        else:
            try:
                time_of_day = datetime.strptime(time_raw_str, "%I %p")
            except ValueError:
                time_of_day = datetime.strptime(time_raw_str, "%I%M %p")

        return (TimeEntry(
                        time_of_day=time_of_day, 
                        description=body.text.strip(), 
                        money_spent=money_spent
                    ), default_am_pm)
