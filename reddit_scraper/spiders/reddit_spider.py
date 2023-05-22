import scrapy

TOTAL_COUNT = 5000

class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = ['https://www.reddit.com/r/AskReddit/']
    post_count = 0

    def parse(self, response):
        # Extracting question-answer data from Reddit threads
        for thread in response.css('div.Post'):
            question = thread.css('h3._eYtD2XCVieq6emjKBH3m::text').get()
            answers = thread.css('div._1rZYMD_4xY3gRcSS3p8ODO::text').getall()

            yield {
                'question': question,
                'answers': answers
            }
            
            self.post_count += 1  # Increment the post count

            if self.post_count >= TOTAL_COUNT:  # Stop scraping when post count reaches TOTAL_COUNT
                break

        # Follow the 'Next' button recursively
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None and self.post_count < TOTAL_COUNT:
            yield response.follow(next_page, self.parse)
