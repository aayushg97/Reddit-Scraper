# Scraping question-answers from reddit
To extract questions and answers from reddit, run the following. Output will be saved to Reddit_data.pkl

`python RedditAPI.py`

Or use scrapy to scrape reddit posts. To start scraping, go to reddit_scraper/spiders/ and run the following command. Output will be saved to reddit_data.json

`scrapy crawl reddit_spider -o reddit_data.json`
