"""
Classes for scraping money diaries
"""

from datetime import datetime
import json
import inspect
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
            if section.find('strong', string=re.compile(r'Occupation:\s?')) or section.find('strong', string=re.compile(r'(Industry)|(Occuptation):\s')):
                self._clear_empty_strongs(section)
                sub_section = re.split(r'\<strong\>Monthly Expenses:?\s?\<\/strong\>', str(section))
                pairs = re.findall(r'((?:\<strong\>.*?:?\s?\<\/strong\>\s?)+):?\s?([$€£\d\-]{1,}(?:[\,\.]?\d+)*)?[\.\s]*(.*?)(?:<|\Z)', sub_section[0])
                break

        occupation = None
        industry = None
        location = None
        extras = []

        for pair in pairs:
            label = re.sub(r'\<\/?strong\>', '', pair[0]).replace(':', '').strip()
            
            if 'monthly expenses' in label.lower() or 'costs' in label.lower():
                break
            elif label == 'Occupation':
                occupation = pair[2].strip()
            elif label == 'Job':
                occupation = pair[2].strip()
            elif label == 'Industry':
                industry = pair[2].strip()
            elif label == 'Location':
                location = pair[2].strip()
            else:
                value, descr = (None if item == '' or item is None else item.strip() for item in pair[1:])
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
                    monthly_expense_label_section.parent.decompose()
                elif siblings and monthly_expense_label_section.previousSibling is None:
                    monthly_expense_label_section.decompose()
                    self._clear_empty_strongs(section)
                    section_str = str(section)
                else:
                    parent = monthly_expense_label_section.find_parent('div', class_='section-outer-container')
                    if parent.find('strong', string=re.compile(r'Industry:?\s?')):
                        # Expenses and Occupation data are not well separated
                        child = parent.findChildren('div', class_='section-text')[0]
                        contents = child.contents
                        section_str = re.findall(r'\<strong\>Monthly Expenses:?\s?\<\/strong\>(.*)', ''.join(map(str, contents)))[0]
                        child.decompose()
                    else:
                        sibling = parent.find_next_siblings('div', class_='section-outer-container')
                        content = sibling[0].findChildren('div', class_='section-text')
                        section_str = str(content[0])
                        content[0].decompose()

                pairs += re.findall(r'\<strong\>(.*?):?\s?\<\/strong\>:?\s?~?([$€£\d\-]{1,}(?:[\,\.]?\d+)*%?)?[\.\s]*(.*?)(?:<|\Z)', section_str)
        
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
            strong_matches = re.findall(r'<strong>(.*?)(?:<br>)?<\/strong>', str(section))

            matches = re.findall(r'<br>([\d\.\:]{1,5}\s?[ap].?m.?)\s?[:\—]\s?(.*?)(?:\<strong\>)?([$€£\d\-]{1,}[\,\.]?\d+)?\s*(?:\<\/strong\>)?\s?<br>', str(section))

            for match in matches:
                time_str = match[0]
                descr = match[1] if match[1] else None
                money_spent = match[2] if match[2] else None
                
                time_of_day = self._get_time_from_string(time_str)

                time_entries.append(TimeEntry(
                        time_of_day=time_of_day, 
                        description=descr.strip() if descr else None, 
                        money_spent=money_spent.strip() if money_spent else None
                    ))
            
            days.append(
                Day(
                    title=strong_matches[0].strip() if len(strong_matches) > 1 else None,
                    total=re.sub(r'(Daily)?\s?[Tt]otal:\s?', '', strong_matches[-1]).strip() if len(strong_matches) > 1 else None,
                    time_entries=time_entries
                )
            )
        return days
           

    def _get_days_when_days_are_headers(self, day_sections):
        """ Get days data when we have days as h3s """
        days = []
        for section in day_sections:
            parent = section.find_parent('div', class_='section-outer-container')
            
            if len(parent.text) > 11: # Looking for something like " Day Three "
                time_entries, daily_total = self._get_time_entries_when_headers_are_in_same_section_as_text(parent)
            else:
                time_entries, daily_total = self._get_time_entries_when_headers_are_not_in_same_section_as_text(parent)

            if section.text and not section.find('strong', string=re.compile(r'Weekly Total.*')):
                days.append(Day(title=section.text.strip(), total=daily_total, time_entries=time_entries))
        return days

    def _get_time_entries_when_headers_are_in_same_section_as_text(self, parent):
        """
            Get time entries when headers are not in the same section as text, 
            returns tuple (time_entries, daily_total) 
        """
        time_entries = []
        daily_total = ''
        daily_total_section = None

        time_section = parent.find('div', class_='section-text')
        strong_sections = time_section.findAll('strong')
        for strong_section in strong_sections:
            daily_total_section = re.findall(r'((?:Daily\s)?[Tt]otal.*)', str(strong_section))
            if len(daily_total_section) > 0:
                break

        if daily_total_section:
            daily_total = re.findall(r'([$€£\d\-]{1,}[\,\.]?\d+)', str(daily_total_section))[0]

        # Section, not always a single time entry at this point
        time_sections_found = re.split(r'([\d\:\.]+\s(?:[ap]\.?m\.?)?)\s*—\s*', time_section.decode_contents())

        time_section_iterator = iter(time_sections_found[1:])
        prev_am_pm = 'am'
        for time_section in time_section_iterator:
            time_entry, prev_am_pm = self._create_time_entry(time_section, next(time_section_iterator), prev_am_pm)
            if time_entry:
                time_entries.append(time_entry)

        return time_entries, daily_total

    def _get_time_entries_when_headers_are_not_in_same_section_as_text(self, parent):
        """
            Get time entries when headers are not in the same section as text, 
            returns tuple (time_entries, daily_total) 
        """
        time_entries = []
        daily_total = ''
        for sibling in parent.find_next_siblings('div', class_='section-outer-container'):
            if sibling.select('.section-text-container h3'):
                break # start a new day

            time_section = sibling.find('div', class_='section-text')
            if not time_section:
                continue

            daily_total_section = time_section.find_all('strong')
            if daily_total_section:
                daily_total_section_str = ' '.join([strong_section.decode_contents() for strong_section in daily_total_section])
                found_daily_totals = re.findall(r'Daily?\s?[Tt]otal:\s?([$€£\d\-]{1,}[\,\.]?\d+)', daily_total_section_str)
                if found_daily_totals:
                    daily_total = found_daily_totals[0]

            time_section.decode_contents()
            # Section, not always a single time entry at this point
            time_sections_found = re.split(r'(?:^|(?:\<br\/?\>))([\d]+[\:\.\d]*\s(?:[ap]\.?m\.?)?)\s*—?\s*', time_section.decode_contents())
            if len(time_sections_found) < 3:
                continue

            time_section_iterator = iter(time_sections_found[1:])

            prev_am_pm = 'am'
            for time_section in time_section_iterator:
                time_entry, prev_am_pm = self._create_time_entry(time_section, next(time_section_iterator), prev_am_pm)
                if time_entry:
                    time_entries.append(time_entry)

        return time_entries, daily_total
            

    def _create_time_entry(self, time_raw_str: str, body_str: str, default_am_pm: str):
        """ Create a time entry based on some text """
        money_spent = None
        currency_str = ''
        if not time_raw_str or not body_str:
            return None

        body = BeautifulSoup(body_str, 'html.parser')
        strong_sections = body.findAll('strong')
        for strong_section in strong_sections:
            matches = re.match(r'(^[$€£]$)', strong_section.text)
            if matches:
                currency_str = strong_section.text
                strong_section.decompose()
            money_spent_section = re.findall(r'([$€£\d\-]{1,}[\,\.]?\d+)', str(strong_section))
            if len(money_spent_section) > 0:
                strong_section.decompose()
                money_spent = currency_str + money_spent_section[0]
                break            

        time_of_day = self._get_time_from_string(time_raw_str, default_am_pm)

        return (TimeEntry(
                        time_of_day=time_of_day, 
                        description=body.text.strip(), 
                        money_spent=money_spent
                    ), default_am_pm)

    
    def _get_time_from_string(self, time_str: str, default_am_pm: str='am'):
        """
        Get's time from string, returns a datetime
        """

        time_str = time_str.replace('.', '').strip().replace(' ', '')
        default_am_pm = 'am' if not default_am_pm else default_am_pm

        if not time_str.endswith('m'):
            time_str += f"{default_am_pm}"
        else:
            default_am_pm = time_str[-2:]

        if ":" in time_str:
            return datetime.strptime(time_str, "%I:%M%p")
        else:
            try:
                return datetime.strptime(time_str, "%I%p")
            except ValueError:
                return datetime.strptime(time_str, "%I%M%p")
        return None


    def _clear_empty_strongs(self, element):
        """ For some reason there are empty <strong></strong> elements.
            This messes with the regex. Find them and clear them """
        empty_strongs = element.findAll('strong', string=re.compile(r'\s?'))
        for empty_strong in empty_strongs:
            if empty_strong.text.strip() in ['', '~']:
                empty_strong.decompose()

    def to_json(self):
        """ Serializes this object to JSON """
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
                    return {key: serialize(value) for key, value in o_dict.items()}


        return json.dumps(
                self, 
                default=serialize
            )