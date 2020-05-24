import logging
import os
from queue import Queue, Empty
import sys
import traceback
import time
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'scraper'))

from money_diaries_page_scraper import MoneyDiariesPageScraper
from money_diaries_site_map_scraper import MoneyDiariesSiteMapScaper

def site_map_worker(sitemaps_queue, url_queue, thread_number):
    """ Run forever """
    while True:
        try:
            sitemap_url = sitemaps_queue.get(block=True, timeout=10)
            print(f'{thread_number} - {sitemap_url}')
            sitemap_scrape = MoneyDiariesSiteMapScaper(sitemap_url)
            sitemap_scrape.scrape_page()

            for url in sitemap_scrape.additional_site_map_urls[0:50]:
                sitemaps_queue.put(url)

            for url in sitemap_scrape.get_money_diary_page_urls():
                url_queue.put(url)
            
            sitemaps_queue.task_done()
        except Empty:
            break

def page_worker(url_queue, scraped_sites_queue, thread_number):
    """ Run forever """
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    while True:
        scraper = None
        try:
            url = url_queue.get(block=True, timeout=10)
            print(f'{thread_number} - {url}')
            scraper = MoneyDiariesPageScraper(
                            url,
                            selenium_driver=driver,
                            selenium_wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, "div.byline.modified a"))
                        )
            scraper.scrape_page()
            
            scraped_sites_queue.put(scraper)

            url_queue.task_done()
        except Empty:
            break
        except:
            #handle all other exceptions and write scraping contents to disk
            tb = traceback.format_exc()
            print("Unexpected error:\n{}".format(tb))
            if scraper.content:
                with open("{}.html".format(url.split("/")[-1]), "w") as text_file:
                    text_file.write(scraper.content)

    driver.quit()


def money_diaries_site_map_scrape():
    """ demo off scraping """
    sitemaps_queue = Queue()
    url_queue = Queue()
    scraped_sites_queue = Queue()
    start_time = time.time()

    sitemaps_queue.put('https://www.refinery29.com/sitemap.xml')
    
    # Create a group of parallel workers and start them
    for thread_number in range(10):
        worker = Thread(target=site_map_worker, args=(sitemaps_queue, url_queue, thread_number))
        worker.setDaemon(True)
        worker.start()

    # Block until sitemaps queue is emptied
    sitemaps_queue.join()
    print("--- Sitemaps scraped in %s seconds ---" % (time.time() - start_time))
    print("Urls queued to be scraped %s " % len(list(url_queue.queue)))

    for thread_number in range(1):
        worker = Thread(target=page_worker, args=(url_queue, scraped_sites_queue, thread_number))
        worker.setDaemon(True)
        worker.start()

    url_queue.join()
    print("--- Urls scraped in %s seconds ---" % (time.time() - start_time))
    print("Urls scraped %s " % len(list(scraped_sites_queue.queue)))

if __name__ == '__main__':
    money_diaries_site_map_scrape()