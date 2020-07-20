import os
import sys
import unittest
import unicodedata
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
        self.assertEqual(day_0_time_entries[4].description, "Since Target is near a grocery store, I pop in and put $25 on my transit card and buy a pack of 20 stamps for $10. The stamps are all white Santas, but it's either that or American flags, so I'm going with festive hetero-patriarchy. I get home feeling ready to make cards and stretch my artistic skills to the limit.")
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
            ('credit cards', '£2,400', 'I paid off £2,200 at the start of the month from study budget reimbursements and holiday refunds. I pay £250 a month and hope to pay it all off by September. This credit card debt was up to £7,000 and has been hanging over me for years. Lockdown has actually helped me save enough to pay a chunk off.'),
            ('utilities', '£350', ': council tax, water, electricity (this is £120/month, I only have electricity and a dodgy old boiler and heaters, which I plan on changing to more energy-efficient ones when lockdown is over), window cleaner, house, life and appliance insurance, Sky TV and broadband.'),
            ('transportation', '£30', 'roughly on petrol, more if I visit people. I cycle, run and walk as much as possible.'),
            ('phone bill', '£60', 'including insurance.'),
            ('savings?', '£2,265', '£1,000 is earmarked for paying off my credit card but I like to have enough available in case of an emergency. There was more but I bought my flat this time last year. My parents paid for the deposit and new flooring (I’m eternally grateful and will pay them back one day), I paid the legal fees, furniture and new white goods.'),
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
        self.assertEqual(day_3_time_entries[1].description, 'I get a much-anticipated call! I purchased a 1973 VW Beetle in September as a "fun car" to enjoy the sunny Arizona weather in. It\'s been in the shop for the last two weeks due to some clutch and pressure plate issues, and I just got a call that it\'s ready for pickup. The payment came in two parts, the first part already paid for was $1,200 and then the final cost for completion was $305. I pay over the phone with my credit card which earns cashback and will pay it off as soon as the bill processes.')
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


class MoneyDiariesGbPrivateNannyScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-private-nanny-on-furlough.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'Money Diary: A Private Nanny On Furlough')
        self.assertEqual(self.scrape.page_meta_data.author, 'Anonymous')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 4, 29, 6, 0, 29))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, None)
        self.assertEqual(self.scrape.occupation_data.industry, 'Nanny')
        self.assertEqual(self.scrape.occupation_data.location, 'Berkshire')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '26', None), 
            ('salary', '£34,000', None),
            ('paycheque amount', None, 'Usually £2,100. Unsure what my next one will be although I anticipate around £1,600 with furlough.'),
            ('number of housemates', None, 'One, my boyfriend E.')
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
                ('housing costs', None, 'Mortgage is £950, split between me and E.'), 
                ('loan payments', None, 'None but £400 sitting on a credit card that shouldn’t be...eek!'), 
                ('utilities', None, 'Water £30, gas £40, electric £30, plus ground rent £240 per annum and service charge £120 per month.'), 
                ('transportation', '£123', 'for the car (split with E), £120 on a normal month in fuel, £2.63 tax (yep, paid monthly ha).'), 
                ('phone bill', '£12', 'SIM only, iPhone paid off last year.'), 
                ('savings?', None, 'Around £8,000 personal, £2,000 split with E for a holiday that clearly isn’t happening now.'), 
                ('other', '£5.99', 'Netflix, £12 pet insurance for the cat that now lives with my sister (betrayal at its finest), £240 put into our joint account for food, despite shopping at Aldi. £12 nanny insurance (kids are mental, insurance is crucial). £7.50 Friction Free Shaving subscription – lifesaver.\xa0£80 internet and phone (split with E).'), 
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '£4.99')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 7)

        day_0_time_entries = self.scrape.days_data[0].time_entries
        self.assertEqual(day_0_time_entries[3].description, 'Embrace my inner Jamie Oliver and decide to whip up a tikka roast chicken and whatever sides look a bit sad in the fridge. This is clearly the definition of frugal. Remind myself to boast about it to E next time he slates our shopping bill.')
        self.assertEqual(day_0_time_entries[3].money_spent, None)
        self.assertEqual(day_0_time_entries[3].time_of_day, datetime(year=1900, month=1, day=1, hour=16, minute=0))

        self.assertEqual(self.scrape.days_data[3].title, 'Day Four')
        self.assertEqual(self.scrape.days_data[3].total, '£36.09')
        self.assertEqual(len(self.scrape.days_data[3].time_entries), 11)

        day_3_time_entries = self.scrape.days_data[3].time_entries
        self.assertEqual(day_3_time_entries[1].description, 'YouTube Pilates to try and remind myself that I need to move at some point this week. Realise my local gym must do a relaxing version because after 25 minutes of a toned blonde woman shouting "JUST BREATHE" at me, I can’t breathe.')
        self.assertEqual(day_3_time_entries[1].money_spent, None)
        self.assertEqual(day_3_time_entries[1].time_of_day, datetime(year=1900, month=1, day=1, hour=9, minute=30))


class MoneyDiariesUsSeniorAccountExecScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-senior-account-executive-charleston-sc-salary-money-diary.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'A Week In Charleston, SC, On A $50,000 Salary')
        self.assertEqual(self.scrape.page_meta_data.author, 'Refinery29')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 5, 1, 15, 30, 22))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Senior Account Executive')
        self.assertEqual(self.scrape.occupation_data.industry, 'Communications')
        self.assertEqual(self.scrape.occupation_data.location, 'Charleston, SC')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '23', None), 
            ('salary', '$50,000', None),
            ('net worth', None, 'About $30,000 across high yield savings, index funds, single stocks, my retirement accounts, and my car'),
            ('debt', '$0', '(I had a merit scholarship for college, I bought my car in cash, and I pay my credit cards in full every month.)'),
            ('paycheck amount (2x/month)', '$1,414.74', '(post-tax and after health insurance of $120/paycheck)'),
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
                ('rent', '$974', '(Room in a three-bed, three-bath duplex with the most amazing high ceilings and a beautiful kitchen)'), 
                ('car insurance', '$105', None), 
                ('utilities', '$75-$100', None), 
                ('internet', '$33.88', None), 
                ('cbs all access', '$6', '(Trade this with family members for Sling, Netflix, and Hulu)'), 
                ('cell phone', '$10', None), 
                ('spotify', '$8', None), 
                ('canva', '$12.95', None), 
                ('classpass', '$29', None), 
                ('ally savings', '$250', None), 
                ('betterment', '$100', None), 
                ('roth ira', '$100', "(my company 401(k) hasn't kicked in yet)"), 
                ('annual expenses', None, None), 
                ('costco', '$60', None), 
                ("renter's insurance", '$180', None), 
                ('credit card', '$150', None), 
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[1].title, 'Day Two')
        self.assertEqual(self.scrape.days_data[1].total, '$20.29')
        self.assertEqual(len(self.scrape.days_data[1].time_entries), 7)

        day_1_time_entries = self.scrape.days_data[0].time_entries
        self.assertEqual(day_1_time_entries[5].description, "I get a lot of last-minute social requests this afternoon so I am just now wrapping up work. I was going to go to Trader Joe's but sadly they close at 7 so I decide to go to Publix instead. I grab the mask that my mom sent me last week and drive over there. The store has made aisles one-way only which is great for social distancing but also makes shopping more confusing. From my list, I get two boxes of Chex, Cheerios, pretzels, two packages of Oreos, two bags of bagel chips, fresh salsa, jarred salsa, tortilla chips, chocolate chips, flour, butter, and cream cheese. I impulse buy Cinnamon Toast Crunch because it's BOGO, Pringles, and a delicious pint of Churro Dough ice cream.")
        self.assertEqual(day_1_time_entries[5].money_spent, '$60.99')
        self.assertEqual(day_1_time_entries[5].time_of_day, datetime(year=1900, month=1, day=1, hour=18, minute=30))

        self.assertEqual(self.scrape.days_data[4].title, 'Day Five')
        self.assertEqual(self.scrape.days_data[4].total, '$0')
        self.assertEqual(len(self.scrape.days_data[4].time_entries), 7)

        day_4_time_entries = self.scrape.days_data[4].time_entries
        self.assertEqual(day_4_time_entries[1].description, "I get about halfway through my book before my roommates make it out to the common area. We chat for a bit and put on Booksmart. I heat up some frozen Trader Joe's Penne Arrabiata for lunch.")
        self.assertEqual(day_4_time_entries[1].money_spent, None)
        self.assertEqual(day_4_time_entries[1].time_of_day, datetime(year=1900, month=1, day=1, hour=11, minute=30))


class MoneyDiariesUsAnalystWashingtonScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-analyst-washington-dc-salary-money-diary.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'A Week In Washington, DC, On A $72,000 Salary')
        self.assertEqual(self.scrape.page_meta_data.author, 'R29 Editors')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 5, 16, 15, 30, 33))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Analyst')
        self.assertEqual(self.scrape.occupation_data.industry, 'Government Consulting')
        self.assertEqual(self.scrape.occupation_data.location, 'Washington, DC')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '24', None), 
            ('salary', '$72,000', None),
            ('net worth', None, "Negative net worth as my student loans are greater than my savings. That said, for savings I have: $6,000 in my high-yield savings account, $3,004 in my 401k (I contribute 6% of every paycheck, which is the maximum that my company matches (25% match)). I plan to up to 7% after this promotion cycle. I wasn't great at saving my first year on the job and am actively trying to save more now."),
            ('debt', '$26,513', None),
            ('paycheck amount (2x/month)', '$1,820', '(exact amount varies based on deductions including 401k, health insurance, and $70 to my Metro Card pre-tax)'),
            ('pronouns', None, 'She/her')
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
                ('rent', '$1,287', '(I live with one roommate in a two-bedroom apartment)'), 
                ('student loans', '$308', "(All of my debt is student loans (all public) to cover what was not paid for by scholarships)"), 
                ('utilities', '$40', '(my share of gas and electric, the building pays for water and WiFi)'), 
                ("renter's insurance", '$14.74', None), 
                ('spotify premium', '$9.99', None), 
                ('netflix', '$12.99', "(my mom pays for Hulu and AT&T TV NOW)"), 
                ('phone', '$75', "(I send my mom $75/month to cover my phone bill, as it is cheaper than having my own plan)"), 
                ('unlimited cyclebar membership', '$52.74', "(my work pays for half, on-pause for now)"), 
                ('apple icloud storage', '$2.99', None), 
                ('high-yield savings contribution', '$500', None), 
                ('donations', None, "I do not have a monthly donation budget but usually end up donating between $200-$300 each month to different organizations/projects."), 
                ('therapy co-pay', '$50', "(I put this aside every month for therapy twice a month)"),
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[2].title, 'Day Three')
        self.assertEqual(self.scrape.days_data[2].total, '$0')
        self.assertEqual(len(self.scrape.days_data[2].time_entries), 7)

        day_2_time_entries = self.scrape.days_data[1].time_entries
        self.assertEqual(day_2_time_entries[5].description, "K. joins her weekly family Zoom call and I decide to grocery shop. I've started exclusively going to the smaller shop by my house. It's a much less overwhelming experience, it's always well-stocked, they require masks to enter the store, and I get to support a local business. I effectively blackout, forget most of what I wanted to get, and end up with English muffins, Tollhouse cookie dough, ground turkey, goat cheese, half-and-half, greek yogurt, black beans, canned tomatoes, oat milk, soy sauce, Bonne Maman blueberry jam (my favorite), onions, garlic, and two absolutely massive limes. Good enough. I try to buy beer and then embarrassingly realize I just brought my credit card and have no ID. K. sends me $20 on Venmo (she's a vegetarian and I still feel like I should pay more for groceries in my own house, even though she insists otherwise).")
        self.assertEqual(day_2_time_entries[5].money_spent, '$29.31')
        self.assertEqual(day_2_time_entries[5].time_of_day, datetime(year=1900, month=1, day=1, hour=18, minute=30))

        self.assertEqual(self.scrape.days_data[6].title, 'Day Seven')
        self.assertEqual(self.scrape.days_data[6].total, '$45.97')
        self.assertEqual(len(self.scrape.days_data[6].time_entries), 5)

        day_4_time_entries = self.scrape.days_data[3].time_entries
        self.assertEqual(day_4_time_entries[2].description, "It's technically Giving Tuesday, which I am not a big fan of for a variety of reasons, but I remember I have some of my stimulus check left to donate. I am so fortunate to still be receiving my usual salary, so I decided to donate half and keep the rest for savings/buying one splurge item (I went with a stupidly expensive, but gorgeous, linen bedding set from Bed Threads -- I am no Mother Theresa). I sent my first donation to a relief fund for local sex workers last week and decide to donate the rest there, too. Over the past year, I've gotten very involved with my local abortion fund and have realized how crucial it is to support smaller, community-based organizations and mutual aid projects whenever possible. Organizations like these typically have no fundraising budget and are not going to benefit from a massive Giving Tuesday campaign, so I'm happy to do my small part.")
        self.assertEqual(day_4_time_entries[2].money_spent, '$200')
        self.assertEqual(day_4_time_entries[2].time_of_day, datetime(year=1900, month=1, day=1, hour=12, minute=0))


class MoneyDiariesUsProjectManagerCopenhagenScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-project-manager-copenhagen-denmark-salary-money-diary.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'A Week In Copenhagen, Denmark On A $70,000 Salary')
        self.assertEqual(self.scrape.page_meta_data.author, 'Refinery29')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 5, 15, 15, 30, 4))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Project Manager')
        self.assertEqual(self.scrape.occupation_data.industry, 'Creative')
        self.assertEqual(self.scrape.occupation_data.location, 'Copenhagen, Denmark')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '26', None), 
            ('salary', '$70,000', None),
            ('net worth', '$-1,983', "(I have a 401(k) that I was contributing to at my previous job in NYC and the last time I checked it had about $12,000ish in it) I don't really keep a savings account either, just sort of keep whatever money is left over in my checking account."),
            ('paycheck amount (1x/month)', '$3,788', '(Danish taxes are insane!)'),
            ('pronouns', None, 'She/her')
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
                ('rent', '$1,137', '(for my share in a two-bed, two-bath apartment (total rent is $2,274, split with my boyfriend, S.) the only utility included in water *eye roll*)'), 
                ('loans', '$139', "(started paying this amount when I was making less and have just... never stopped, I try to pay more when I can)"), 
                ('internet', '$41', '(paid for by me in full)'), 
                ("electric", None, "S. pays"), 
                ('spotify', '$14', None), 
                ('netflix', '$9', None), 
                ('gym membership', '$36', "(frozen since March due to COVID (don't know when gyms will open again))"), 
                ('classpass', '$24', "(I like to take classes here and there on the weekend)"), 
                ('phone', '$0', "(paid for by my work)"), 
                ('nytimes subscription', '$4', None), 
                ('lunch at work', "$86", "(taken out of my paycheck for catered lunch every day)"), 
                ('apple care+', '$9.99', "(was suckered into this after purchasing a new phone and had to buy full price cause my old phone had the smallest of small cracks and therefore $0 trade-in value)"),
                ('apple storage', "$0.99", None), 
                ('pillow sleep tracking subscription', "$2.75", None), 
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '$96.16')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 8)

        day_2_time_entries = self.scrape.days_data[1].time_entries
        self.assertEqual(day_2_time_entries[6].description, "Another lazy kale salad from Monday. I promise I eat more exciting than this usually, but I've been trying to be more mindful of my meals during the week instead of just mindlessly eating/snacking all the time — and also I ate about a pound of guacamole and chips.")
        self.assertEqual(day_2_time_entries[6].money_spent, None)
        self.assertEqual(day_2_time_entries[6].time_of_day, datetime(year=1900, month=1, day=1, hour=19, minute=0))

        self.assertEqual(self.scrape.days_data[3].title, 'Day Four')
        self.assertEqual(self.scrape.days_data[3].total, '$226.66')
        self.assertEqual(len(self.scrape.days_data[3].time_entries), 9)

        day_4_time_entries = self.scrape.days_data[3].time_entries
        self.assertEqual(day_4_time_entries[5].description, "Let the long weekend begin! The first thing I do is head to a local running store for a run test. Full disclosure: I'm not a runner. AT ALL. But in January along with my pledge for more mindful eating, I wanted to get back into the rhythm of working out more than once every two weeks (looking at you, fall/winter). Running is something that I hate, until I'm actually doing it. It's also something that S. and I can do together as well so planning to do at least two runs a week. The last run I went on I had horrible foot and ankle pain and realized that my shoes are 1) not running shoes and 2) offer less than zero support. After a quick run test (and not needing any insoles, hooray!!) I land on a pair of Nike Flyknit Infinity Reacts. These things run TIGHT. I'm usually an 8 but I size up to a 9 so I can wear socks with them comfortably. They feel like I'm running on clouds so I can't wait to take these out for a real run this weekend.")
        self.assertEqual(day_4_time_entries[5].money_spent, '$180')
        self.assertEqual(day_4_time_entries[5].time_of_day, datetime(year=1900, month=1, day=1, hour=16, minute=0))


class MoneyDiarySocialWorkStudentLeedsScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-social-work-student-leeds.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'Money Diary: A Social Work Student In Leeds On 21k')
        self.assertEqual(self.scrape.page_meta_data.author, 'Anonymous')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 5, 13, 6, 0, 9))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Social work student')
        self.assertEqual(self.scrape.occupation_data.industry, 'Local authority')
        self.assertEqual(self.scrape.occupation_data.location, 'Leeds')
        self.assertEqual(self.scrape.occupation_data.extras, [
            ('age', '26', None), 
            ('salary', '£21,166', None),
            ('savings', '£5,500', "in a lifetime ISA"),
            ('take-home pay', '£1,445', 'I also get mileage payments which range from £0-£100+ per month but at present I’m obviously not receiving this.'),
            ])

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(self.scrape.expense_data.expenses, [
                ('housing costs', None, 'My boyfriend and I live in a rented, three-storey townhouse which we love. I pay £397 for my half. Followed by payment into our bills account of £162 per month to cover Sky, phone, gas/electric, council tax, water, Disney+ and Netflix. We’re lucky that my partner works for Sky so we get a good deal on TV and phones.'), 
                ('travel', None, "I moved 30 minutes away from work just before lockdown so I haven’t had the full ‘travel to work’ experience yet. I’ve budgeted about £40 per week for petrol, however this will vary depending on the number of visits I have and if I’m at uni that week, as I travel over 100 miles to get there."), 
                ('debt repayments', '£50', 'per month to a credit card I used for furniture, although I’ve been paying more lately due to not having to pay out for petrol etc.'), 
                ('other expenses', '£4.99', "for Spotify student, £10.56 for prescription certificate (definitely recommend if you're on more than one long-term medication)."), 
                ('savings', None, 'I try to put around £150 into savings each month, split between my LISA and holiday pots.'), 
            ])

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '£138.50')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 8)

        day_2_time_entries = self.scrape.days_data[1].time_entries
        self.assertEqual(day_2_time_entries[1].description, "Myself and S have been looking at some ladder shelves to add some personality to our front room. We don’t have any window ledges so there’s nowhere to put pictures and knick-knacks. Find some on Groupon where I can also get some cash back – £20 for my half.")
        self.assertEqual(day_2_time_entries[1].money_spent, None)
        self.assertEqual(day_2_time_entries[1].time_of_day, datetime(year=1900, month=1, day=1, hour=10, minute=0))

        self.assertEqual(self.scrape.days_data[4].title, 'Day Five')
        self.assertEqual(self.scrape.days_data[4].total, '£18')
        self.assertEqual(len(self.scrape.days_data[4].time_entries), 9)

        day_4_time_entries = self.scrape.days_data[4].time_entries
        self.assertEqual(day_4_time_entries[1].description, "£15 transferred into my 'fuel' pot on Monzo. I’ve realised that when I return to work, I won’t have any mileage payments from the previous month, which usually helps with petrol costs. I’ve decided to move £15 each week into a pot to soften the blow when we re-enter the real world.")
        self.assertEqual(day_4_time_entries[1].money_spent, None)
        self.assertEqual(day_4_time_entries[1].time_of_day, datetime(year=1900, month=1, day=1, hour=9, minute=0))


class MoneyDiaryBioMedicalScientistManchesterScrapeTest(unittest.TestCase):
    def setUp(self):
        self.scrape = MoneyDiariesPageScraper('local.money-diaries')
        with open('{}/tests/content/money-diary-biomedical-scientist-manchester.html'.format(os.path.join(os.path.dirname(__file__), os.pardir)), 'r') as f:
            self.scrape.content = f.read()
        self.scrape._get_page_soup()

    def test__set_meta_data_sets_data(self):
        self.scrape._set_meta_data()
        self.assertEqual(self.scrape.page_meta_data.title, 'Money Diary: A Biomedical Scientist In Manchester On 42k')
        self.assertEqual(self.scrape.page_meta_data.author, 'Anonymous')
        self.assertEqual(self.scrape.page_meta_data.publish_date, datetime(2020, 5, 29, 6, 0, 30))

    def test__set_occupation_data_sets_data(self):
        self.scrape._set_occupation_data()
        self.assertEqual(self.scrape.occupation_data.occupation, 'Senior biomedical scientist')
        self.assertEqual(self.scrape.occupation_data.industry, 'NHS')
        self.assertEqual(self.scrape.occupation_data.location, 'Manchester')
        self.assertEqual(self.scrape.occupation_data.extras[:3], [
            ('age', '33', None), 
            ('salary', '£41,723', None),
            ('paycheque amount', None, "Usually around £2,400 after tax, National Insurance, NHS pension (9.3%) and student loan contribution. The exact amount varies depending on how many out-of-hours or extra shifts I have worked the previous month."),
            ])

        self.assertEqual(
            (
                self.scrape.occupation_data.extras[3][0], 
                self.scrape.occupation_data.extras[3][1], 
                unicodedata.normalize('NFD',self.scrape.occupation_data.extras[3][2])
            ),
            (
                'number of housemates', 
                None, 
                unicodedata.normalize('NFD', 'Three: two cats and one fiancé.')
            ),
        )

    def test__set_expense_data_sets_data(self):
        self.scrape._set_expenses_data()
        self.assertEqual(len(self.scrape.expense_data.expenses), 5)
        self.assertEqual(
            (
                self.scrape.expense_data.expenses[0][0], 
                self.scrape.expense_data.expenses[0][1], 
                unicodedata.normalize('NFD', self.scrape.expense_data.expenses[0][2])
            ),
            (
                'housing costs', 
                None, 
                unicodedata.normalize('NFD', 'My fiancé M and I live in a three-bed semi in south Manchester. My half of the mortgage is £378.')
            ),
        )
        self.assertEqual(
            self.scrape.expense_data.expenses[1],
            ('loan payments', '£2,400', "on an interest-free credit card. The balance has gone up and down over the years, starting with funding my master’s degree 10 years ago. Then unexpected large bills arrive so I’ve never quite cleared it (my old and tired car being the main culprit, I just can’t get rid of him yet). I have two cards and always transfer the balance if I’m not able to pay it off in full prior to the interest-free period ending. I pay £200 each month to my credit card and £200 for student loan repayments, which should finally be gone by the end of the year.")
        )
        self.assertEqual(
            self.scrape.expense_data.expenses[2],
            ('utilities', None, 'My half of all the bills works out at £72 for council tax, £16 for water, £40 for gas and electric, £25 for TV/phone/internet, £4 for Netflix and £15 for pet insurance. Along with our mortgage, these all come out of our joint account, which we both pay £1,000 into each month. The rest goes on food, bits for the house and garden and any fun things we want to do, which usually revolve around eating out with friends – something I am really missing at the moment! Any remaining money gets put into our savings or towards our mortgage.'), 
        )
        self.assertEqual(
            (
                self.scrape.expense_data.expenses[3][0], 
                self.scrape.expense_data.expenses[3][1], 
                unicodedata.normalize('NFD', self.scrape.expense_data.expenses[3][2])
            ),
            (
                'savings?', 
                None, 
                unicodedata.normalize('NFD', 'I have approximately £10,000 in a joint savings account with my fiancé which is primarily our wedding fund. A lot of this was meant to be going out to our suppliers over the next month but sadly we have to postpone to next summer due to the pandemic.\xa0We will need to look into what is best to do with this money in the meantime and are continuing to add to the pot for the next year so we can start saving for further house improvements.')
            ),
        )
        self.assertEqual(
            self.scrape.expense_data.expenses[4],
            ('all other monthly expenses', '£250', 'into the wedding fund/savings. £28 car insurance, £14 union membership, £14 Institute of Biomedical Science membership, £7.20 life insurance (why do my cats cost more than me?!), £6 bike insurance,\xa0£40 phone bill (I know I could find a better deal but I’m inherently lazy with this kind of thing, plus I now have unlimited data until October for being NHS so will probably sort it out after that ends) and £25.99 gym membership (currently on hold while the gym is closed). I drive to work and usually have to pay for parking (£32) but this has been suspended for the next three months while we all deal with the pandemic. Petrol/diesel we fund from the joint account but while M is also classed as a key worker, his job can be done at home so we are only spending about £30 a month at present.'), 
        )

    def test__set_days_data(self):
        self.scrape._set_days_data()
        self.assertEqual(len(self.scrape.days_data), 7)

        self.assertEqual(self.scrape.days_data[0].title, 'Day One')
        self.assertEqual(self.scrape.days_data[0].total, '£16')
        self.assertEqual(len(self.scrape.days_data[0].time_entries), 7)

        day_2_time_entries = self.scrape.days_data[1].time_entries
        self.assertEqual(day_2_time_entries[1].description, "Admit defeat and feed cats. M makes us scrambled egg on toast for breakfast which I eat while messaging my friend about her wedding. They have a lovely day planned so I’m glad she is in good spirits.")
        self.assertEqual(day_2_time_entries[1].money_spent, None)
        self.assertEqual(day_2_time_entries[1].time_of_day, datetime(year=1900, month=1, day=1, hour=8, minute=0))

        self.assertEqual(self.scrape.days_data[6].title, 'Day Seven')
        self.assertEqual(self.scrape.days_data[6].total, '£30')
        self.assertEqual(len(self.scrape.days_data[6].time_entries), 9)

        day_6_time_entries = self.scrape.days_data[6].time_entries
        self.assertEqual(day_6_time_entries[8].description, "Head to bed.")
        self.assertEqual(day_6_time_entries[8].money_spent, None)
        self.assertEqual(day_6_time_entries[8].time_of_day, datetime(year=1900, month=1, day=1, hour=22, minute=30))



if __name__ == '__main__':
    unittest.main()