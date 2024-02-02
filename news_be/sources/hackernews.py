
import requests
import random
from datetime import datetime, timedelta, date, time

from article_extractor import get_article_info



def sample_indices(N, M):
    # Adjust M if it's greater than N to ensure we don't sample more indices than available
    M = min(M, N)

    # Generate a list of indices from 0 to N-1
    indices = list(range(N))

    # Randomly sample M indices
    sampled_indices = random.sample(indices, M)

    return sampled_indices


def get_article_by_id(id):
    response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")

    return response.json()

def is_within_n_days(input_date, n_days):
    """
    Check if the given date is within n_days from today.

    :param input_date: The date to check, as a datetime.date object or a string in the format 'YYYY-MM-DD'.
    :param n_days: Number of days to check within, as an integer.
    :return: True if the date is within n_days from today, False otherwise.
    """
    # Ensure input_date is a datetime.date object
    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, "%Y-%m-%d").date()

    # Get today's date
    today = date.today()

    # Calculate the difference in days
    day_difference = abs((input_date - today).days)

    # Check if the difference is within n_days
    return day_difference <= n_days
    
def get_best_articles(max_articles=5, within_days=5):
    articles = []

    article_ids = requests.get("https://hacker-news.firebaseio.com/v0/beststories.json").json()

    articles_data = []
    # for i in range(len(article_ids)):
    for i in range(15):
        article = get_article_by_id(article_ids[i])
        try:
            if not ('url' in article):
                continue
            article_data = get_article_info(article['url'])
            if not article_data or not ('date' in article_data) or not article_data['date']:
                continue
            date_to_compare = datetime.strptime(article_data['date'], "%Y-%m-%d").date()
            article_data['date'] = datetime.combine(date_to_compare, time.min)
            article_data['url'] = article['url']
            if is_within_n_days(date_to_compare, within_days):
                articles_data.append(article_data)
            else:
                print(f"Hackernews Article Date not within range {article_data['date']}")
        except Exception as err:
            print(f"Failed, article: {article}, err: {err}")

    if not max_articles:
        max_articles = len(articles_data)
    

    random_sample = sample_indices(len(articles_data), max_articles)
    for id in random_sample:
        # print(article_id)
        # article = get_article_by_id(article_ids[id])
        # article_data = get_article_info(article['url'])
        # print(article_data)
        articles.append(articles_data[id])


    return articles


def test_source():
    date_object = datetime.now().date() - timedelta(days=5)
    articles = get_best_articles(max_articles=None, within_days=5)

if __name__ == "__main__":
    pass
