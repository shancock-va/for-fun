import os
import sys
import unittest
from unittest import mock

from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'scraper'))

from money_diaries_page_scraper import MoneyDiariesPageScraper

class MoneyDiariesPageScraperTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diaries-example.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'A Week In Minneapolis, MN, On A $20,000 Income')
        self.assertEqual(self.scrape.page_meta_data.author, 'You')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2018, 12, 15, 12, 35))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Baker')
        self.assertEqual(self.scrape.occupation_data.industry, 'Food Service')
        self.assertEqual(self.scrape.occupation_data.location, 'Minneapolis, MN')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '27'), ('salary', '$20,000'), ('paycheck amount (2x/month)', '$630-$670')
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
            ('rent', '$525'),
            ('gym', '$54'),
            ('electricity bill', '$24'),
            ('gas bill', '$26'),
            ('internet', '$20')
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '$72.70')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 4)

        day_0_time_entries = self.scrape.days_data[0].time_entries
        self.assertEqual(day_0_time_entries[0].description, "I usually find a breakfast I like and stick to for about a year. Right now it's yogurt, muesli, and a banana. While I don't love the politics of buying bananas (yeah, I'm that kind of annoying foodie), they are cheap, filling, and give me potassium. I vow to switch to adding sweet potatoes instead of bananas next week.")
        self.assertEqual(day_0_time_entries[0].money_spent, None)
        self.assertEqual(day_0_time_entries[0].time_of_day, datetime(year=1900, month=1, day=1, hour=8))

        self.assertEqual(self.scrape.days_data[6].title, 'Day Seven')
        self.assertEqual(self.scrape.days_data[6].total, '$79.60')
        self.assertEqual(len(self.scrape.days_data[6].time_entries), 6)

        day_0_time_entries = self.scrape.days_data[6].time_entries
        self.assertEqual(day_0_time_entries[4].description, "Since Target is near a grocery store, I pop in and put $25 on my transit card and buy a pack of 20 stamps for $10. The stamps are all white Santas, but it's either that or American flags, so I'm going with festive hetero-patriarchy. I get home feeling ready to make cards and stretch my artistic skills to the limit. ")
        self.assertEqual(day_0_time_entries[4].money_spent, "$35")
        self.assertEqual(day_0_time_entries[4].time_of_day, datetime(year=1900, month=1, day=1, hour=16, minute=15))


if __name__ == '__main__':
    unittest.main()