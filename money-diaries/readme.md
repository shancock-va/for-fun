# Money Diaries Project
This project is used to scrape and analyze Refinery29's Money Diary posts. These posts are a weekly diary of an individual's spending habits. There is also meta data on employment, income, and monthly expenses.

## Scraping
### How to run the Scraper
A simple example on how to run the scraper can be found in `demo/demp.py`. A more complex, threaded example can be found in `demo/run_scraper.py`.

### Data
Data from the scraped pages is stored as a JSON array of scrape pages in `data/json/money_diaries-results.json`.

### Methodology
Scraping is a challenge. The content seems to be at best semi-structured. Beautiful Soup with regex and if statements build the scraping rules. When a page fails to be properly parsed, new tests are created for it and code is refactored until the tests pass. See `test/test_money_diaries_page_scrape_real_pages.py`

