import os
import sys

from selenium import webdriver

from scraper.scraper import MoneyDiariesPageScrape

def main():
    """ demo off scraping """
    chrome_driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    demo_scrape = MoneyDiariesPageScrape(
        'https://www.refinery29.com/en-us/baker-minneapolis-mn-income-money-diary', 
        selenium_driver=chrome_driver
    )
    demo_scrape.scrape_page()

    author = demo_scrape.soup.find('span', class_='contributor').get_text()

    with open("example.html", "w") as text_file:
        text_file.write(demo_scrape.content)





if __name__ == '__main__':
    main()