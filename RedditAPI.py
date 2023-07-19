import requests
import pickle
from tqdm import tqdm
import time
import json

TOTAL_COUNT = 2000

# Set up the Reddit API endpoint and parameters
baseUrl = 'https://www.reddit.com/r/'
tailUrl = "/top.json?t=year"
params = {
    'limit': 100,  # Number of posts per request (maximum is 100)
    'after': None,  # Pagination parameter for fetching the next set of posts
}
subreddits = ['AskScience', 'explainlikeimfive', 'AskHistorians', 'AskEngineers', 'AskComputerScience', 
              'AskReddit', 'NoStupidQuestions', 'AskCulinary', 'AskScienceFiction', 'Ask', 'AskMen', 
              'AskWomen', 'TooAfraidToAsk', 'AskAnAmerican', 'AskEurope', 'TrueAskReddit', 'AskOldPeople', 
              'AskAnthropology', 'AskPhysics', 'AskHistory']

for subreddit in subreddits:
    total_questions = 0
    questions_and_answers = []

    print('Extracting from subreddit ', subreddit)
    progress_bar = tqdm(total=TOTAL_COUNT)
    
    while total_questions < TOTAL_COUNT:
        # Make a GET request to the Reddit API
        response = requests.get(baseUrl+subreddit+tailUrl, params=params, headers={'User-agent': 'Mozilla/5.0'})

        remaining_requests = int(response.headers.get('x-ratelimit-remaining', 0))
        reset_timestamp = int(response.headers.get('x-ratelimit-reset', 0))

        # If remaining requests is zero, wait until the reset time before making the next request
        if remaining_requests == 0:
            wait_time = reset_timestamp - time.time()
            if wait_time > 0:
                time.sleep(wait_time)

        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']

            for post in posts:
                question = post['data']['title'] + post['data']['selftext']
                answers = []

                # Extract comments if available
                if post['data']['num_comments'] > 0:
                    post_id = post['data']['id']
                    comments_url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"

                    comments_response = requests.get(comments_url, headers={'User-agent': 'Mozilla/5.0'})

                    if comments_response.status_code == 200:
                        comments_data = comments_response.json()
                        comments = comments_data[1]['data']['children']
                        comments = [c for c in comments if 'score' in c['data']]
                        sorted_comments = sorted(comments, key=lambda com: com['data']['score'], reverse=True)

                        for comment in sorted_comments[:5]:
                            if 'body' in comment['data']:
                                answers.append(comment['data']['body'])

                if(len(answers) > 0):
                    questions_and_answers.append({'question': question, 'answers': answers})
                    total_questions += 1
                    progress_bar.update(1)

                if total_questions >= TOTAL_COUNT:
                    print("Breaking because total_count posts extracted")
                    break

            # Update the 'after' parameter for pagination
            params['after'] = data['data']['after']

            if params['after'] is None:
                #print("Breaking because next page is none")
                break
        else:
            print(f"Request failed with status code {response.status_code}")
            break

    progress_bar.close()
    print(f"Total questions extracted: {total_questions}")

    # Do further processing with the extracted questions and answers
    # For example, you can save them to a file or perform analysis
    # Path to the file where the list will be stored
    file_path = subreddit+'_data.pkl'
    json_path = subreddit+'_data.json'

    # Store the list in the file using pickle
    with open(file_path, 'wb') as file:
        pickle.dump(questions_and_answers, file)

    with open(json_path, 'w') as file:
        json.dump(questions_and_answers, file, indent=4)