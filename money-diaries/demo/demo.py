import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'scraper'))

from scraper.money_diaries_page_scraper import MoneyDiariesPageScraper
from scraper.money_diaries_site_map_scraper import MoneyDiariesSiteMapScaper

def main():
    money_diaries_page_scrape()

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
    demo_scrape = MoneyDiariesPageScraper(
        'https://www.refinery29.com/en-us/engineer-san-francisco-ca-salary-money-diary', 
        selenium_driver=chrome_driver,
        selenium_wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, "div.byline.modified a"))
    )
    demo_scrape.scrape_page()
    chrome_driver.quit()
    #author = demo_scrape.soup.find('span', class_='contributor').get_text()

    with open("example.html", "w") as text_file:
        text_file.write(demo_scrape.content)



if __name__ == '__main__':
    main()