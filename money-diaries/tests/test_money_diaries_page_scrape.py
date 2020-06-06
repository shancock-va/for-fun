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
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2018, 12, 15, 18, 35))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Baker')
        self.assertEqual(self.scrape.occupation_data.industry, 'Food Service')
        self.assertEqual(self.scrape.occupation_data.location, 'Minneapolis, MN')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '27', None), ('salary', '$20,000', None), ('paycheck amount (2x/month)', '$630-$670', None)
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
            ('rent', '$525', None),
            ('gym', '$54', None),
            ('electricity bill', '$24', None),
            ('gas bill', '$26', None),
            ('internet', '$20', None)
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


class MoneyDiariesGbAnaesthetistScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-anaesthetist-coronavirus.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'Money Diary: An ICU Doctor In Bristol On 60k')
        self.assertEqual(self.scrape.page_meta_data.author, 'Anonymous')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 5, 20, 6, 0, 47))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, None)
        self.assertEqual(self.scrape.occupation_data.industry, 'Healthcare')
        self.assertEqual(self.scrape.occupation_data.location, 'Bristol')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '31', None), 
            ('salary', '£60,000', 'ish, changes every three months depending on the amount of out-of-hours work. Contracts are like unicorns in the NHS so I’m never sure how much I should earn.'),
            ('paycheque amount', '£3,175', '(after tax and student loan).'),
            ('housemates', None, 'None.')
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
            ('housing costs', '£600', '(£400 mortgage, £200 rent for 50% property and service charge), this is the least I’ve ever paid. I’m hoping to buy the whole property soon or increase mortgage payments.'),
            ('credit cards', '£2,400.', 'I paid off £2,200 at the start of the month from study budget reimbursements and holiday refunds. I pay £250 a month and hope to pay it all off by September. This credit card debt was up to £7,000 and has been hanging over me for years. Lockdown has actually helped me save enough to pay a chunk off.'),
            ('utilities', '£350', ': council tax, water, electricity (this is £120/month, I only have electricity and a dodgy old boiler and heaters, which I plan on changing to more energy-efficient ones when lockdown is over), window cleaner, house, life and appliance insurance, Sky TV and broadband.'),
            ('transportation', '£30', 'roughly on petrol, more if I visit people. I cycle, run and walk as much as possible.'),
            ('phone bill', '£60', 'including insurance.'),
            ('savings?', '£2,265.', '£1,000 is earmarked for paying off my credit card but I like to have enough available in case of an emergency. There was more but I bought my flat this time last year. My parents paid for the deposit and new flooring (I’m eternally grateful and will pay them back one day), I paid the legal fees, furniture and new white goods.'),
            ('monzo', None, 'I put about £400-500/month in this account. I take my card to work so it pays for lunches, supermarket trips and drinks out. I round up my spending to the nearest pound, also I put £5/day into a separate account. So far it has £550 in, I’m saving up for a Gucci handbag – it was meant to be a treat when I got my training job but I bought a flat and new sofa instead, so I’m going to get it once I pass all my exams.'),
            ('other', None, 'Spotify £14.99, Netflix £5.99, Apple storage £0.79, PayPal credit for Dyson Airwrap £37.50.'),
            ('annual', '£550', "car insurance, £200 tax, service, MOT. I got given my mum's old car as a graduation present, he’s 12 years old and luckily never had any major problems."),
            ('professional subscriptions', '£700', 'ish, this year I’ll also spend over £2,000 on exams and courses. I took the first exam the week before lockdown – we were meant to get results early April but this has been delayed until the world restarts. I know it’s not a big deal but it adds an extra anxiety to life and I don’t know if I should start studying for a resit or my last ever exam.')
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '£146.91')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 18)

        day_0_time_entries = self.scrape.days_data[0].time_entries
        self.assertEqual(day_0_time_entries[17].description, "Shower, have a sleeping tablet, make a hot water bottle (even in the heatwave my flat is freezing), put on some night cream – I use Drunk Elephant LaLa and it's the most amazing thing ever, like a little treat for my face. Finally go to bed.")
        self.assertEqual(day_0_time_entries[17].money_spent, None)
        self.assertEqual(day_0_time_entries[17].time_of_day, datetime(year=1900, month=1, day=1, hour=9, minute=15))

        self.assertEqual(self.scrape.days_data[5].title, 'Day Six')
        self.assertEqual(self.scrape.days_data[5].total, '£76')
        self.assertEqual(len(self.scrape.days_data[5].time_entries), 10)

        day_5_time_entries = self.scrape.days_data[5].time_entries
        self.assertEqual(day_5_time_entries[4].description, 'Find a colouring book I got for my 30th birthday and spend some time doing that.')
        self.assertEqual(day_5_time_entries[4].money_spent, None)
        self.assertEqual(day_5_time_entries[4].time_of_day, datetime(year=1900, month=1, day=1, hour=15, minute=30))


class MoneyDiariesUsMarketingCoordinatorScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diaries-marketing-coordinator-phoenix-az-salary.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'A Week In Phoenix, AZ, On A $50,000 Salary')
        self.assertEqual(self.scrape.page_meta_data.author, 'Refinery29')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 4, 17, 15, 30, 47))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Marketing Coordinator')
        self.assertEqual(self.scrape.occupation_data.industry, 'Construction')
        self.assertEqual(self.scrape.occupation_data.location, 'Phoenix, AZ')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '20', None), 
            ('salary', '$50,000', '+ $2,000 sign-on bonus'),
            ('net worth', '$10,000', '(Savings, HSA, 401(k))'),
            ('debt', '$6,000', '(I bought a 1973 VW Bug, because fun car?)'),
            ('paycheck amount (1x/week)', '$800', '(post-tax)'),
            ('pronouns', None, 'She/her')
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
                ('rent', '$550', 'for my half of a two bedroom two bathroom apartment I share with my fiancé)'), 
                ('car loan', '$145', None), 
                ('car insurance', '$50', None), 
                ('horse boarding', '$715', '(I have two horses)'), 
                ('internet', '$60', None), 
                ('gym', '$25', None), 
                ('electricity', None, 'Fiancé pays'), 
                ('savings', '$600', '(Sometimes more depending on the month. I am slowly trying to save to buy a home and/or land within the next few years. My fiancé makes $35,000. We split finances right now, but I recently got a raise so we are looking to split costs according to our income %. We have about $8,000 in combined savings right now. I just started an HSA and 401(k) plan in March, so there is very little in those accounts.)')
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '$0')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 7)

        day_0_time_entries = self.scrape.days_data[0].time_entries
        self.assertEqual(day_0_time_entries[3].description, "I find out I have a project due tomorrow and have a small panic attack. I calm down and am thankful for something to work on, especially because I've been having issues focusing during the pandemic. I coordinate with my manager to go over tasks for this project and hop on a conference call to ensure all my boxes are checked.")
        self.assertEqual(day_0_time_entries[3].money_spent, None)
        self.assertEqual(day_0_time_entries[3].time_of_day, datetime(year=1900, month=1, day=1, hour=12, minute=0))

        self.assertEqual(self.scrape.days_data[3].title, 'Day Four')
        self.assertEqual(self.scrape.days_data[3].total, '$320')
        self.assertEqual(len(self.scrape.days_data[3].time_entries), 4)

        day_3_time_entries = self.scrape.days_data[3].time_entries
        self.assertEqual(day_3_time_entries[1].description, 'I get a much-anticipated call! I purchased a 1973 VW Beetle in September as a "fun car" to enjoy the sunny Arizona weather in. It\'s been in the shop for the last two weeks due to some clutch and pressure plate issues, and I just got a call that it\'s ready for pickup. The payment came in two parts, the first part already paid for was $1,200 and then the final cost for completion was $305. I pay over the phone with my credit card which earns cashback and will pay it off as soon as the bill processes. ')
        self.assertEqual(day_3_time_entries[1].money_spent, '$305')
        self.assertEqual(day_3_time_entries[1].time_of_day, datetime(year=1900, month=1, day=1, hour=11, minute=0))


class MoneyDiariesGbDoctorRedeployedCoronaVirusScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-doctor-redeployed-coronavirus.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'Money Diary: A 27-Year-Old Doctor On 47k Redeployed For COVID-19')
        self.assertEqual(self.scrape.page_meta_data.author, 'Anonymous')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 4, 22, 6, 0, 42))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, None)
        self.assertEqual(self.scrape.occupation_data.industry, 'Medical')
        self.assertEqual(self.scrape.occupation_data.location, 'London')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '27', None), 
            ('salary', '£47,000', None),
            ('paycheque amount', '£3,200', "this month – it depends on how much 'out of hours' work I do."),
            ('number of housemates', None, 'Two')
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
                ('housing costs', '£750', None), 
                ('loan payments', None, 'No student loan. University is pretty much free where I’m from and my parents/ very part-time job helped with living costs. I have just paid off my bike via the cycle to work scheme, which cost about £50 per month. I have an American Express credit card which I pay off by standing order (in full) every month.'), 
                ('utilities', '£10', 'for internet, £30ish council tax, £20 electricity, £10 water (approx).'), 
                ('transportation', '£200', 'per month on the Tube and buses. We rotate from hospital to hospital during our training – I cycle to the nearby ones but this one is reeeeally far away. I’m not completely sold on living in a city and this doesn’t help. Also, my partner lives overseas so I pay for flights to see him every few months, probably averaging about £1,200 per year. Long distance is expensive! We have no upcoming trips due to the current pandemic so I won’t include flights this week.'), 
                ('phone bill', '£20', 'per month, which includes Spotify premium. I haggled it down from £24!'), 
                ('savings?', None, 'From putting away money every month (£550 per month atm), taking on extra shifts and selling my car, I have just over £20,000 in a stocks and shares ISA (which was worth a good bit more a few weeks ago). I’m hoping to buy a house in the near future so fingers crossed it picks up a bit! I plan to swap this money to a less risky option once the pandemic is over.'), 
                ('medical training expenses', None, 'We pay for a number of our training costs out of pocket, which we can claim tax back on. These include: medical council fees (£153 this year), medical association (a few £10s per month), royal college fees (£280 this year), exams (£340 this year) etc.'), 
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '£4.68')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 7)

        day_0_time_entries = self.scrape.days_data[0].time_entries
        self.assertEqual(day_0_time_entries[3].description, 'All hospital coffee shops are closed. I head to the local corner shop and buy instant coffee/milk/biscuits. £4.68. It’s going to be a tough few weeks and we won’t get through them without coffee!')
        self.assertEqual(day_0_time_entries[3].money_spent, None)
        self.assertEqual(day_0_time_entries[3].time_of_day, datetime(year=1900, month=1, day=1, hour=11, minute=30))

        self.assertEqual(self.scrape.days_data[3].title, 'Day Four')
        self.assertEqual(self.scrape.days_data[3].total, '£142.13 (oops)')
        self.assertEqual(len(self.scrape.days_data[3].time_entries), 5)

        day_3_time_entries = self.scrape.days_data[3].time_entries
        self.assertEqual(day_3_time_entries[1].description, 'Still queueing to get in – it’s insanely well organised. Someone comes along the queue telling us that key workers can skip to the front. I guiltily walk to the top of the queue and manage to get eggs from the NHS stash. Thank you Waitrose! Get flour (for our sourdough starter, I’m a basic bitch), bananas, oranges, Dettol, beers, chicken, bagels, dark chocolate and some other ingredients. £35.21. I’m sharing food with my flatmate during the lockdown but she’s doing 90% of the cooking while I’m at work so I feel I should definitely pay more. I pop into a pharmacy on the way home to buy paracetamol and hand cream. My hands are chapped and peeling at the knuckles. I need to make sure they don’t crack or bleed as it’s an infection risk. I’ve read that this cream (O’Keeffe’s) is really effective so I give it a go. We get chatting at the till and they give me an NHS discount! Amazing.')
        self.assertEqual(day_3_time_entries[1].money_spent, '£7.57')
        self.assertEqual(day_3_time_entries[1].time_of_day, datetime(year=1900, month=1, day=1, hour=9, minute=0))



if __name__ == '__main__':
    unittest.main()