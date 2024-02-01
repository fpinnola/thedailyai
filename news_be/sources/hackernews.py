
import requests
import random

from article_extractor import get_article_info



def sample_indices(N, M):
    # Ensure M is not greater than N
    if M > N:
        raise ValueError("M cannot be greater than N")

    # Generate a list of indices from 0 to N-1
    indices = list(range(N))

    # Randomly sample M indices
    sampled_indices = random.sample(indices, M)

    return sampled_indices


def get_article_by_id(id):
    response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")

    return response.json()
    
def get_best_articles(max_articles=5):
    articles = []

    article_ids = requests.get("https://hacker-news.firebaseio.com/v0/beststories.json").json()

    random_sample = sample_indices(len(article_ids), max_articles)

    for id in random_sample:
        # print(article_id)
        article = get_article_by_id(article_ids[id])
        article_data = get_article_info(article['url'])
        print(article_data)

        # TODO: generate summary and category for article

    return article_ids


def test_source():
    get_best_articles()

if __name__ == "__main__":
    get_best_articles()