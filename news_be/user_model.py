import datetime
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.news_db
user_collection = db.user_collection

def get_user(userId):
    user = user_collection.find_one({'userId': userId})
    if not user:
        print(f"User {userId} not found")
    return user

def save_user_preferences(userId, preferences):
    new_user = user_collection.update_one({
        'userId': userId
    }, {
        '$set': { 'preferences': preferences }
    }, upsert=True)

    return new_user

# TODO: implement
def update_user_articles(userId, articles):
    pass

# TODO: implement
def get_user_articles(userId):
    pass

if __name__ == '__main__':
    print(get_user('abc123'))

    preferences = {
        'categories': ['biotech', 'tech']
    }

    save_user_preferences('abc123', preferences)

    print(get_user('abc123'))
