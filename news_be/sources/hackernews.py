
import requests
import random
from datetime import datetime, timedelta

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
    
def get_best_articles(max_articles=5, within_date=None):
    articles = []

    article_ids = requests.get("https://hacker-news.firebaseio.com/v0/beststories.json").json()

    articles_data = []
    for i in range(len(article_ids)):
        article = get_article_by_id(article_ids[i])
        try:
            if not ('url' in article):
                continue
            article_data = get_article_info(article['url'])
            if not article_data or not ('date' in article_data) or not article_data['date']:
                continue
            if within_date:
                date_to_compare = datetime.strptime(article_data['date'], "%Y-%m-%d").date()
                is_before = within_date < date_to_compare
                if (is_before):
                    articles_data.append(article_data)
                else:
                    print(f"Hackernews Article Date not within range {article_data['date']}")
            else:
                articles_data.append(article_data)

        except Exception:
            print(f"Failed, article: {article}")

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
    articles = get_best_articles(max_articles=None, within_date=date_object)

if __name__ == "__main__":
    pass
