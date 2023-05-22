import scrapy

class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = ['https://www.reddit.com/r/popular/']
    post_count = 0

    def parse(self, response):
        # Extracting data from Reddit posts
        for post in response.css('div.Post'):
            title = post.css('h3._eYtD2XCVieq6emjKBH3m::text').get()
            score = post.css('div._1rZYMD_4xY3gRcSS3p8ODO::text').get()
            comments = post.css('span.FHCV02u6Cp2zYL0fhQPsO::text').get()

            yield {
                'title': title,
                'score': score,
                'comments': comments
            }

            self.post_count += 1  # Increment the post count

            if self.post_count >= 5000:  # Stop scraping when post count reaches 5000
                break

        # Follow the 'Next' button recursively
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None  and self.post_count < 5000:
            yield response.follow(next_page, self.parse)
