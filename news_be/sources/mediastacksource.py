import requests
import os
from datetime import datetime, timedelta, time
from article_extractor import get_article_info
from article_model import ArticleModel


def fetch_news(keywords=None, countries='us', categories=None, limit=100, offset=0, within_days=2):
    base_url = "http://api.mediastack.com/v1/news"
    ACCESS_KEY = os.getenv('MEDIASTACK_API_KEY', '')

    print(f"keywords: {keywords} categories: {categories}")
    # return []

    start_date = datetime.now() - timedelta(days=within_days)
    start_date_str = start_date.strftime('%Y-%m-%d')
    today_str = datetime.now().strftime('%Y-%m-%d')
    print(f"Searching for articles between {start_date_str},{today_str}")

    params = {
        "access_key": ACCESS_KEY,
        "limit": limit,
        "date": f"{start_date_str},{today_str}",
        "sort": "popularity",
        "languages": "en"
    }
    
    # Conditionally add parameters if they are not None
    if keywords is not None:
        params["keywords"] = keywords
    if countries is not None:
        params["countries"] = countries
    if categories is not None:
        params["categories"] = categories
    if offset != 0:
        params["offset"] = offset
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        return response.json()  # Returns the JSON response if successful
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_new_articles():
    response = fetch_news(categories="technology, business", limit=15, countries="us")
    articles = []

    articleModel = ArticleModel(None)

    for article in response['data']:
        external_id = 'ms' + article['url']
        if articleModel.does_article_with_external_id_exist(external_id):
            print(f"external id already exists {external_id}")
            continue
        article_info = get_article_info(article['url'])
        if not article_info or not ('date' in article_info) or not article_info['date']:
                continue
        date_to_compare = datetime.strptime(article_info['date'], "%Y-%m-%d").date()
        article_info['date'] = datetime.combine(date_to_compare, time.min)
        article_info['url'] = article['url']
        article_info['externalId'] = external_id
        articles.append(article_info)
    return articles
