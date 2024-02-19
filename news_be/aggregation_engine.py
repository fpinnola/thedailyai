## Aggregation Engine handles querying for and populating the database with news articles from the web 
from datetime import datetime, time
import uuid

from sources import mediastacksource
from article_model import ArticleModel
from article_extractor import get_article_info
from emebddings import get_embedding


QUERIES = [
    { 
        'categories': 'technology, business',
        'category_label': "technology",
    },
    {
        'categories': 'technology, business',
        'keywords': 'legal law court',
        'category_label': "legal",

    },
    {
        'categories': 'technology, business',
        'keywords': 'healthcare',
    },
    {
        'categories': 'general',
        'keywords': 'politics republican democrat',
        'category_label': "politics",
    }
]

# Filter out articles already in DB
# Extract data on article using scraping tool
def filter_format_articles(articles):
    articleModel = ArticleModel(None)
    res_articles = []
    for a in articles:
        external_id = 'ms' + a['url']
        if articleModel.does_article_with_external_id_exist(external_id):
            print(f"external id already exists {external_id}")
            continue
        article_info = get_article_info(a['url'])
        if not article_info or not ('date' in article_info) or not article_info['date']:
                continue
        date_to_compare = datetime.strptime(article_info['date'], "%Y-%m-%d").date()
        article_info['date'] = datetime.combine(date_to_compare, time.min)
        article_info['url'] = a['url']
        article_info['externalId'] = external_id
        article_info['body'] = article_info['raw_text']
        res_articles.append(article_info)
    
    return res_articles

# Generate vector embedding of each article, and add to article
def add_vector_embeddings(article_list):
    for a in article_list:
        a['embedding'] = get_embedding(a['body'])


# Reformats article to save in db
def format_article_for_db(article_old, category=None):
    article = {}
    article['articleId'] = str(uuid.uuid4())
    article['title'] = article_old['title']
    article['body'] = article_old['body']
    article['url'] = article_old['url']
    article['articleDate'] = article_old['date']
    article['externalId'] = article_old['externalId']
    article['embedding'] = article_old['embedding']
    if category is not None:
        article['category'] = category
    return article


def init_pipeline():
    articleModel = ArticleModel(None)
    for q in QUERIES:
        query_result = mediastacksource.fetch_news(**q, limit=25)
        article_list = query_result['data']
        if len(article_list) == 0:
            print(f"AE, No articles found for query {q}")
            continue
        article_list = filter_format_articles(article_list)
        add_vector_embeddings(article_list)
        article_list = [format_article_for_db(a, q['category_label']) for a in article_list]
        articleModel.save_list_articles(article_list)

def test():
    init_pipeline()


if __name__ == "__main__":
    init_pipeline()