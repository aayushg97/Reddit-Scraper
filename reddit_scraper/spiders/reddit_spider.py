import scrapy
import json

class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = ['https://www.reddit.com/r/AskReddit/new.json?limit=100']

    def parse(self, response):
        data = json.loads(response.body)
        for post in data['data']['children']:
            title = post['data']['title']
            question = post['data']['selftext']
            post_id = post['data']['id']
            answers_url = f"https://www.reddit.com/r/AskReddit/comments/{post_id}.json"

            yield scrapy.Request(answers_url, callback=self.parse_answers, meta={'title': title, 'question': question})

        after = data['data']['after']
        if after is not None:
            next_url = f'https://www.reddit.com/r/AskReddit/new.json?limit=100&after={after}'
            yield response.follow(next_url, self.parse)

    def parse_answers(self, response):
        data = json.loads(response.body)
        title = response.meta['title']
        question = response.meta['question']
        answers = []

        for comment in data[1]['data']['children']:
            answer = self.extract_answer(comment)
            if answer:
                answers.append(answer)

        yield {
            'title': title,
            'question': question,
            'answers': answers
        }

    def extract_answer(self, comment):
        if 'body' in comment['data']:
            return comment['data']['body']

        # if 'replies' in comment['data']:
        #     replies = comment['data']['replies']['data']['children']
        #     nested_answers = []

        #     for reply in replies:
        #         nested_answer = self.extract_answer(reply)
        #         if nested_answer:
        #             nested_answers.append(nested_answer)

        #     return nested_answers

        return None
