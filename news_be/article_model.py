from datetime import datetime

def is_same_day_as_today(date_to_check):
    # Get today's date
    today = datetime.now().date()

    # Compare only the date part of the datetime object
    return date_to_check.date() == today

class ArticleModel:
    def __init__(self, client) -> None:
        self.client = client
        self.db = self.client.news_db
        self.articles = self.db.articles

    def get_article(self, articleId):
        article = self.articles.find_one({'articleId': articleId})
        if not article:
            print(f"Article {article} not found")
            return None
        return article
        
    def save_article(self, articleId, title, body, summary, url, cateogry, articleDate):
        new_article = self.articles.update_one({
            'articleId': articleId
        }, {
            '$set': { 'title': title, 'body': body, 'summary': summary, 'url': url, 'category': cateogry, 'articleDate': articleDate }
        }, upsert=True)

        return new_article

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

   


if __name__ == '__main__':
    pass
