import json
import logging
import os
from queue import Queue, Empty
import random
import sys
import traceback
import time
from threading import Thread
from urllib3.exceptions import NewConnectionError, MaxRetryError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scraper.money_diaries_page_scraper import MoneyDiariesPageScraper
from scraper.money_diaries_site_map_scraper import MoneyDiariesSiteMapScaper

PAGE_LOCATION = './data/pages'
JSON_LOCATION = './data/json'


def site_map_worker(sitemaps_queue, sitemaps_scraped_queue, thread_number):
    """ Run forever """
    while True:
        try:
            sitemap_url = sitemaps_queue.get(block=True, timeout=10)
            print(f'{thread_number} - {sitemap_url}')
            try:
                sitemap_scrape = MoneyDiariesSiteMapScaper(sitemap_url)
                sitemap_scrape.scrape_page()
            except Exception as e:
                exception_details = repr(e)
                print(f'Error on {thread_number} - {sitemap_url} - {exception_details}')
                print(traceback.format_exc())
                sitemap_scrape.error = exception_details
            else:
                random.shuffle(sitemap_scrape.additional_site_map_urls)
                for url in sitemap_scrape.additional_site_map_urls:
                    sitemaps_queue.put(url)

            sitemaps_scraped_queue.put(sitemap_scrape)
            sitemaps_queue.task_done()
        except Empty:
            break


def page_worker(url_queue, scraped_sites_queue, thread_number):
    """ Run forever """
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    while True:
        scraper = None
        try:
            url = url_queue.get(block=True, timeout=30)
            print(f'{thread_number} - {url}')
            scraper = MoneyDiariesPageScraper(
                            url,
                            selenium_driver=driver,
                            selenium_wait_until=EC.visibility_of_element_located((By.CSS_SELECTOR, "div.byline.modified a")),
                            content_location=PAGE_LOCATION
                        )
            try:
                scraper.scrape_page(write_contents_to_file=True)
            except Exception as e:
                exception_details = repr(e)
                print(f'Error on {thread_number} - {url} - {exception_details}')
                print(traceback.format_exc())
                scraper.error = exception_details
            
            scraped_sites_queue.put(scraper)
            url_queue.task_done()
        except Empty:
            break
        except:
            #handle all other exceptions and write scraping contents to disk
            tb = traceback.format_exc()
            print("Unexpected error on {}:\n{}".format(url, tb))

    driver.quit()


def run_site_map_scraper(number_of_threads, site_maps_queue):
    """ Run the site map scraper """
    site_maps_scraped_queue = Queue()

    for thread_number in range(number_of_threads):
        worker = Thread(
            target=site_map_worker, 
            args=(site_maps_queue, site_maps_scraped_queue, thread_number)
        )
        worker.setDaemon(True)
        worker.start()
    
    # Block until sitemaps queue is emptied -- What happens if one has an exception
    site_maps_queue.join()

    return site_maps_scraped_queue


def run_diaries_scraper(threads, url_queue):
    """ Scrape the diaries """
    scraped_sites_queue = Queue()
    print("Urls queued to be scraped %s " % len(url_queue.queue))

    for thread_number in range(threads):
        worker = Thread(
            target=page_worker,
            args=(url_queue, scraped_sites_queue, thread_number)
        )
        worker.setDaemon(True)
        worker.start()
    url_queue.join()

    print("Urls scraped %s " % len(list(scraped_sites_queue.queue)))
    scraped_sites = list(scraped_sites_queue.queue)
    
    file_location = f"{JSON_LOCATION}/money_diaries-results.json"
    write_data_to_json_file(
        json.dumps([site.to_json_serializable_obj() for site in scraped_sites]),
        file_location
    )


def write_data_to_json_file(data, file_location):
    """
    Write a data to a json file
    """
    with open(file_location, "w") as text_file:
        text_file.write(data)
    print(f"Written json to file {file_location}")


def money_diaries_site_map_scrape(
        scrape_site_maps=True,
        rescrape_site_maps=True,
        scrape_money_diary_pages=True
    ):
    """ Start scraping """
    start_time = time.time()

    try:
        os.makedirs(PAGE_LOCATION)
        os.makedirs(JSON_LOCATION)
    except FileExistsError:
        pass

    url_queue = Queue()
    site_map_location = f"{JSON_LOCATION}/site_map-results.json"

    if scrape_site_maps:
        site_maps_queue = Queue()
        site_maps_queue.put('https://www.refinery29.com/sitemap.xml')

        site_maps_scraped_queue = run_site_map_scraper(20, site_maps_queue)
        write_data_to_json_file(
            json.dumps([obj.to_json_serializable_obj() for obj in list(site_maps_scraped_queue.queue)]), 
            site_map_location
        )

        print("--- Sitemaps scraped in %s seconds ---" % (time.time() - start_time))
    
    if rescrape_site_maps:
        with open(site_map_location, 'r') as json_file:
            site_maps = json.load(json_file)

        for site_map in [site_map for site_map in site_maps if site_map['error']]:
            site_maps_queue = Queue()
            site_maps_queue.put(site_map['url'])
            site_maps_scraped_quey = run_site_map_scraper(1, site_maps_queue)
            site_maps += [obj.to_json_serializable_obj() for obj in list(site_maps_scraped_quey.queue)]

        write_data_to_json_file(json.dumps(site_maps), site_map_location)

    if scrape_money_diary_pages:
        with open(site_map_location, 'r') as json_file:
            site_maps = json.load(json_file)
        
        for site_map in site_maps:
            for url in site_map['money_diary_page_urls']:
                if url.startswith('https://www.refinery29.com/en-'):
                    url_queue.put(url)
                # else it is a non english site
        run_diaries_scraper(3, url_queue)
        print("--- Scraping Process Took: %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    money_diaries_site_map_scrape(False, False, False)