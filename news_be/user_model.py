import datetime
from pymongo import MongoClient

class UserModel:
    def __init__(self) -> None:
        self.client = MongoClient("localhost", 27017)
        self.db = self.client.news_db
        self.users = self.db.user_collection
        


    def get_user(self, userId):
        user = self.users.find_one({'userId': userId})
        if not user:
            print(f"User {userId} not found")
        return user

    def save_user_preferences(self, userId, preferences):
        new_user = self.users.update_one({
            'userId': userId
        }, {
            '$set': { 'preferences': preferences }
        }, upsert=True)

        return new_user

    # TODO: implement
    def update_user_articles(self, userId, articles):
        pass

    # TODO: implement
    def get_user_articles(self, userId):
        pass

if __name__ == '__main__':
    users = UserModel()

    print(users.get_user('abc123'))

    preferences = {
        'categories': ['biotech', 'tech']
    }

    users.save_user_preferences('abc123', preferences)

    print(users.get_user('abc123'))
