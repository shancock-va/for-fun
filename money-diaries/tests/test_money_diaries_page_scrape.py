import os
import sys
import unittest
import unicodedata
from unittest import mock
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'scraper'))

from money_diaries_page_scraper import MoneyDiariesPageScraper


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


if __name__ == '__main__':
    unittest.main()