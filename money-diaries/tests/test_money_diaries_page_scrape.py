from datetime import datetime
import json
import os
import sys
import unittest
from unittest import mock

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'scraper'))

from money_diaries_page_scraper import MoneyDiariesPageScraper
from money_diaries_model import OccupationData, ExpensesData, TimeEntry, Day


class ScrapeGetTimeFromStringTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')

    def test__get_time_from_string_parses_pm(self):
        result = self.scrape._get_time_from_string('930 pm')
        self.assertEqual(result, datetime(1900, 1, 1, 21, 30, 0))

    def test__get_time_from_string_parses_am(self):
        result = self.scrape._get_time_from_string('930 am')
        self.assertEqual(result, datetime(1900, 1, 1, 9, 30, 0))

    def test__get_time_from_string_parses_am_with_periods(self):
        result = self.scrape._get_time_from_string('930 a.m.')
        self.assertEqual(result, datetime(1900, 1, 1, 9, 30, 0))

    def test__get_time_from_string_parses_time_with_colon(self):
        result = self.scrape._get_time_from_string('9:30 a.m.')
        self.assertEqual(result, datetime(1900, 1, 1, 9, 30, 0))

    def test__get_time_from_string_parses_time_with_missing_am_pm(self):
        result = self.scrape._get_time_from_string('9:30', 'am')
        self.assertEqual(result, datetime(1900, 1, 1, 9, 30, 0))

    def test__get_time_from_string_parses_time_without_minutes(self):
        result = self.scrape._get_time_from_string('9 a.m.')
        self.assertEqual(result, datetime(1900, 1, 1, 9, 0, 0))

    def test__get_time_from_string_parses_time_without_spaces(self):
        result = self.scrape._get_time_from_string('9a.m.')
        self.assertEqual(result, datetime(1900, 1, 1, 9, 0, 0))


class MoneyDiariesPageScraperToJsonTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
    
    def test_to_json_encodes_meta_data(self):
        self.scrape.title = 'My title'
        self.scrape.author = 'Author'
        self.scrape.publish_date = datetime(2020, 10, 5, 14, 30, 0)

        result = self.scrape.to_json()
        result_dict = json.loads(result)
        self.assertEqual(result_dict['url'], self.scrape.url)
        self.assertEqual(result_dict['title'], self.scrape.title)
        self.assertEqual(result_dict['author'], self.scrape.author)
        self.assertEqual(result_dict['publish_date'], self.scrape.publish_date.strftime("%Y-%m-%d %H:%M:%S"))
    
    def test_to_json_encodes_occupation_data(self):
        occupation_data = OccupationData(
            'My Occuptation', 
            'An Industry', 
            'Saskatoon Sk', 
            [
                ('label', '123', 'some text'),
                ('more labels', '456', 'some more text'),
            ]
        )
        self.scrape.occupation_data = occupation_data

        result = self.scrape.to_json()
        result_dict = json.loads(result)
        self.assertEqual(result_dict['occupation_data']['occupation'], occupation_data.occupation)
        self.assertEqual(result_dict['occupation_data']['industry'], occupation_data.industry)
        self.assertEqual(result_dict['occupation_data']['location'], occupation_data.location)
        self.assertListEqual(result_dict['occupation_data']['extras'], [list(tup) for tup in occupation_data.extras])

    def test_to_json_encodes_expense_data(self):
        expense_data = ExpensesData(
            [
                ('label', '123', 'some text'),
                ('more labels', '456', 'some more text'),
                ('some more labels', '789', 'lots more text'),
            ]
        )
        self.scrape.expense_data = expense_data

        result = self.scrape.to_json()
        result_dict = json.loads(result)
        self.assertListEqual(result_dict['expense_data']['expenses'], [list(tup) for tup in expense_data.expenses])
    
    def test_to_json_encodes_expense_data(self):
        days = [
            Day(
                'Day 1',
                '$50',
                [
                    TimeEntry(datetime(2020, 1, 1, 7, 30, 0), 'Here is a description', '$10'),
                    TimeEntry(datetime(2020, 1, 1, 12, 30, 0), 'Here is the next description', '$35'),
                    TimeEntry(datetime(2020, 1, 1, 20, 0, 0), 'Here is the last description', '$5'),
                ]
            ),
            Day(
                'Day 2',
                None,
                [
                    TimeEntry(datetime(2020, 1, 1, 11, 0, 0), 'This is a description', None),
                    TimeEntry(datetime(2020, 1, 1, 12, 0, 0), 'This is the next description', None),
                    TimeEntry(datetime(2020, 1, 1, 13, 0, 0), 'This is the last description', None),
                ]
            ),
            Day(
                'Day 3',
                '$100',
                [
                    TimeEntry(datetime(2020, 1, 1, 7, 0, 0), 'Here is a description', '$100'),
                    TimeEntry(datetime(2020, 1, 1, 12, 0, 0), 'Here is the next description', None),
                ]
            ),
        ]
        self.scrape.days_data = days

        result = self.scrape.to_json()
        result_dict = json.loads(result)
        self.assertListEqual(
            result_dict['days_data'], [
                {'title': days[0].title, 'total': days[0].total, 'time_entries': [
                    {
                        'time_of_day': days[0].time_entries[0].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[0].time_entries[0].description,
                        'money_spent': days[0].time_entries[0].money_spent,
                    },
                    {
                        'time_of_day': days[0].time_entries[1].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[0].time_entries[1].description,
                        'money_spent': days[0].time_entries[1].money_spent,
                    },
                    {
                        'time_of_day': days[0].time_entries[2].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[0].time_entries[2].description,
                        'money_spent': days[0].time_entries[2].money_spent,
                    },
                ]},
                {'title': days[1].title, 'total': days[1].total, 'time_entries': [
                    {
                        'time_of_day': days[1].time_entries[0].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[1].time_entries[0].description,
                        'money_spent': days[1].time_entries[0].money_spent,
                    },
                    {
                        'time_of_day': days[1].time_entries[1].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[1].time_entries[1].description,
                        'money_spent': days[1].time_entries[1].money_spent,
                    },
                    {
                        'time_of_day': days[1].time_entries[2].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[1].time_entries[2].description,
                        'money_spent': days[1].time_entries[2].money_spent,
                    },
                ]},
                {'title': days[2].title, 'total': days[2].total, 'time_entries': [
                    {
                        'time_of_day': days[2].time_entries[0].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[2].time_entries[0].description,
                        'money_spent': days[2].time_entries[0].money_spent,
                    },
                    {
                        'time_of_day': days[2].time_entries[1].time_of_day.strftime("%Y-%m-%d %H:%M:%S"),
                        'description': days[2].time_entries[1].description,
                        'money_spent': days[2].time_entries[1].money_spent,
                    }
                ]}
            ]
        )
    

if __name__ == '__main__':
    unittest.main()