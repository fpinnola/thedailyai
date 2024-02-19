## Aggregation Engine handles querying for and populating the database with news articles from the web 
from datetime import datetime, time

from sources import mediastacksource
from article_model import ArticleModel
from article_extractor import get_article_info
from emebddings import get_embedding


QUERIES = [
    { 
        'categories': 'technology, business',
    },
    {
        'categories': 'technology, business',
        'keywords': 'legal law court'
    },
    {
        'categories': 'technology, business',
        'keywords': 'healthcare'
    },
    {
        'categories': 'general',
        'keywords': 'politics republican democrat'
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

def init_pipeline():
    articleModel = ArticleModel(None)
    for q in range(1):
        query_result = mediastacksource.fetch_news(**QUERIES[q], limit=5)
        article_list = query_result['data']
        if len(article_list) == 0:
            print(f"AE, No articles found for query {q}")
            continue
        article_list = filter_format_articles(article_list)
        add_vector_embeddings(article_list)
        articleModel.save_list_articles(article_list)




if __name__ == "__main__":
    init_pipeline()