import requests
import pickle

# Set up the Reddit API endpoint and parameters
url = 'https://www.reddit.com/r/AskReddit.json'
params = {
    'limit': 100,  # Number of posts per request (maximum is 100)
    'after': None  # Pagination parameter for fetching the next set of posts
}
TOTAL_COUNT = 200
total_questions = 0
questions_and_answers = []

while total_questions < TOTAL_COUNT:
    # Make a GET request to the Reddit API
    response = requests.get(url, params=params, headers={'User-agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']

        for post in posts:
            question = post['data']['title']
            answers = []

            # Extract comments if available
            if post['data']['num_comments'] > 0:
                post_id = post['data']['id']
                comments_url = f"https://www.reddit.com/r/AskReddit/comments/{post_id}.json?sort=top&limit=5"

                comments_response = requests.get(comments_url, headers={'User-agent': 'Mozilla/5.0'})

                if comments_response.status_code == 200:
                    comments_data = comments_response.json()
                    comments = comments_data[1]['data']['children']

                    for comment in comments:
                        if 'body' in comment['data']:
                            answers.append(comment['data']['body'])

            questions_and_answers.append({'question': question, 'answers': answers})
            total_questions += 1

            if total_questions >= TOTAL_COUNT:
                break

        print(f"Questions extracted: {total_questions}")

        # Update the 'after' parameter for pagination
        params['after'] = data['data']['after']

        if params['after'] is None:
            break
    else:
        print(f"Request failed with status code {response.status_code}")
        break

print(f"Total questions extracted: {total_questions}")

# Do further processing with the extracted questions and answers
# For example, you can save them to a file or perform analysis
# Path to the file where the list will be stored
file_path = 'Reddit_data.pkl'

# Store the list in the file using pickle
with open(file_path, 'wb') as file:
    pickle.dump(questions_and_answers, file)