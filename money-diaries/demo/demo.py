import os
import sys

from selenium import webdriver

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'scraper'))

from scraper import MoneyDiariesPageScrape, MoneyDiariesSiteMapScaper

def main():
    money_diaries_site_map_scrape()

def money_diaries_site_map_scrape():
    """ demo off scraping """
    demo_scrape = MoneyDiariesSiteMapScaper(
        'https://www.refinery29.com/sitemap.xml?yyyy=2020&mm=02&dd=10'
    )
    demo_scrape.scrape_page()

    with open("day-sitemap.xml", "w") as text_file:
        text_file.write(demo_scrape.content)


def money_diaries_page_scrape():
    """ demo off scraping """
    chrome_driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    demo_scrape = MoneyDiariesPageScrape(
        'https://www.refinery29.com/en-us/baker-minneapolis-mn-income-money-diary', 
        selenium_driver=chrome_driver
    )
    #demo_scrape.scrape_page()

    author = demo_scrape.soup.find('span', class_='contributor').get_text()

    with open("example.html", "w") as text_file:
        text_file.write(demo_scrape.content)

# To Do Queue for pages to scrape
# Queue for data to write to CSV
# Queue for errors to log



if __name__ == '__main__':
    main()