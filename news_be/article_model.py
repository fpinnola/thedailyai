from datetime import datetime

def is_same_day_as_today(date_to_check):
    # Get today's date
    today = datetime.now().date()

    # Compare only the date part of the datetime object
    return date_to_check.date() == today

class ArticleModel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ArticleModel, cls).__new__(cls)
            # Put any initialization here if necessary

        return cls._instance

    def __init__(self, client) -> None:
        if not hasattr(self, 'initialized'):
            self.client = client
            self.db = self.client.news_db
            self.articles = self.db.articles
            self.initialized = True

    def get_article(self, articleId):
        article = self.articles.find_one({'articleId': articleId})
        if not article:
            print(f"Article {article} not found")
            return None
        return article
        
    def save_article(self, articleId, title, body, summary, url, cateogry, articleDate, externalId=None):
        new_article = self.articles.update_one({
            'articleId': articleId
        }, {
            '$set': { 'title': title, 'body': body, 'summary': summary, 'url': url, 'category': cateogry, 'articleDate': articleDate, 'externalId': externalId }
        }, upsert=True)

        return new_article
    
    def save_list_articles(self, article_list):
        result = self.articles.insert_many(article_list)
        return result


    def get_articles_since(self, date):
        query = {"articleDate": {"$gte": date}}

        # Execute the query
        results = self.articles.find(query)
        return list(results)
    
    def get_articles_category_since(self, categories, date):
        query = {
            "articleDate": { "$gte": date },
            "category": { "$in": categories }
                }
        
        return self.articles.find(query)
    
    def does_article_with_external_id_exist(self, external_id):
        query = {'externalId': external_id}

        # Use find_one to search for a matching document
        matching_document = self.articles.find_one(query)

        # Check if a matching document was found
        if matching_document:
            return True
        else:
            return False

   


if __name__ == '__main__':
    pass
